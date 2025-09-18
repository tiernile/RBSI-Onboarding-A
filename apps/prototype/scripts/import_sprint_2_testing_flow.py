#!/usr/bin/env python3
"""
Importer for "Sprint 2 Testing Flow" CSV → KYCP schema YAML

Parses the CSV and outputs:
  apps/prototype/data/schemas/sprint-2-testing-flow/schema-kycp.yaml

"""
from __future__ import annotations
import json, re, sys, yaml, csv
from pathlib import Path

# --- Configuration ---
APP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = APP_DIR / 'data'
JOURNEY_KEY = 'sprint-2-testing-flow'
AS_IS_JOURNEY_KEY = 'non-lux-1-1'
INCOMING_CSV = DATA_DIR / 'incoming' / 'RBSI Onboarding Sprint 2 Testing Flow v3.csv'
AS_IS_SCHEMA_PATH = DATA_DIR / 'schemas' / AS_IS_JOURNEY_KEY / 'schema-kycp.yaml'
OUT_DIR = DATA_DIR / 'schemas' / JOURNEY_KEY
OUT_FILE = OUT_DIR / 'schema-kycp.yaml'

# --- Utility Functions ---

def warn(msg: str):
    print(f"[warn] {msg}", file=sys.stderr)

def info(msg: str):
    print(f"[info] {msg}")

def slugify(s: str) -> str:
    s = (s or '').strip().lower()
    s = s.replace('&', ' and ')
    out = []
    for ch in s:
        if ch.isalnum():
            out.append(ch)
        elif ch in [' ', '-', '_']:
            out.append('-')
    result = ''.join(out).strip('-')
    return re.sub(r'-+', '-', result) or 'untitled'

def parse_lookup_values(value_str: str) -> list[dict[str, str]]:
    """Parse inline lookup values like 'Yes | No' into [{'value': 'Yes', 'label': 'Yes'}]"""
    if not value_str or not value_str.strip():
        return []
    values = [v.strip() for v in value_str.split('|')]
    return [{'value': v, 'label': v} for v in values if v]

def normalize_field_type(field_type_str: str) -> tuple[str, str | None]:
    """Normalize field type from CSV to schema style and type."""
    ft = (field_type_str or '').strip().lower()
    if ft in ['title', 'divider']:
        return ('divider', None)
    if ft in ['description', 'statement']:
        return ('statement', None)
    
    field_type = 'string' # Default
    if ft in ['lookup', 'dropdown', 'select']:
        field_type = 'lookup'
    elif ft in ['textarea', 'freetext']:
        field_type = 'freeText'
    elif ft in ['number', 'integer', 'decimal']:
        field_type = 'integer'
    elif ft in ['date']:
        field_type = 'date'

    return ('field', field_type)

# --- Core Logic ---

def load_as_is_data(path: Path) -> dict[str, dict]:
    """Loads the as-is schema and returns a map of key -> {label, help}."""
    as_is_map = {}
    if not path.exists():
        warn(f"As-is schema not found at {path}, cannot populate original copy.")
        return as_is_map

    with open(path, 'r', encoding='utf-8') as f:
        schema = yaml.safe_load(f)
    
    for field in schema.get('fields', []):
        key = field.get('key')
        if key:
            as_is_map[key] = {
                'label': field.get('label', ''),
                'help': field.get('help') or field.get('description', ''),
            }
            
    info(f"Loaded {len(as_is_map)} fields from as-is journey '{AS_IS_JOURNEY_KEY}'.")
    return as_is_map

def process_csv_file(csv_path: Path) -> list[dict]:
    """Read and process the input CSV file."""
    rows = []
    if not csv_path.exists():
        warn(f"CSV file not found at {csv_path}")
        return rows

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):
            if not any(row.values()): # Skip completely blank rows
                continue
            
            keyname = (row.get('Keyname') or '').strip()
            question = (row.get('Question') or '').strip()
            
            if not keyname or not question:
                continue

            rows.append({
                'source_row': row_num,
                'keyname': keyname,
                'label': question,
                'help': (row.get('Helper') or '').strip(),
                'section_title': (row.get('Section') or '').strip(),
                'field_type_raw': (row.get('FIELD TYPE') or '').strip(),
                'lookup_values_raw': (row.get('Lookup Values') or '').strip(),
            })
    info(f"Processed {len(rows)} valid rows from {csv_path.name}")
    return rows

def create_schema_field(row: dict, as_is_data: dict[str, dict]) -> dict:
    """Create a single field dictionary for the YAML schema."""
    style, field_type = normalize_field_type(row['field_type_raw'])
    keyname = row['keyname']
    
    # Find original copy from as-is data
    original_copy = as_is_data.get(keyname)
    
    field = {
        'key': keyname,
        'entity': 'entity',
        'style': style,
        'label': row['label'],
        'original': {
            'label': original_copy['label'] if original_copy else row['label'],
            'help': original_copy['help'] if original_copy else None,
        },
        'validation': {},
        '_section': row['section_title'],
        '_metadata': {
            'source_row_ref': f"ROW:{row['source_row']}",
            'has_as_is_data': bool(original_copy),
        }
    }

    if field_type:
        field['type'] = field_type

    if row['help']:
        field['help'] = row['help']
    
    if field_type == 'lookup':
        options = parse_lookup_values(row['lookup_values_raw'])
        if options:
            field['options'] = options
        else:
            warn(f"Field '{row['keyname']}' is type 'lookup' but has no lookup values.")

    return field

def main():
    info(f"Starting import for '{JOURNEY_KEY}'...")
    
    csv_rows = process_csv_file(INCOMING_CSV)
    if not csv_rows:
        warn("No data processed from CSV. Exiting.")
        return

    as_is_data = load_as_is_data(AS_IS_SCHEMA_PATH)
    
    fields = [create_schema_field(row, as_is_data) for row in csv_rows]
    info(f"Generated {len(fields)} fields from CSV data.")

    # --- Accordion Generation ---
    accordions = []
    accordion_map = {}
    for field in fields:
        section_title = field.get('_section')
        if not section_title:
            continue
        
        accordion_key = slugify(section_title)
        if accordion_key not in accordion_map:
            accordion_map[accordion_key] = {
                'key': accordion_key,
                'title': section_title,
            }
    
    accordions = list(accordion_map.values())
    info(f"Generated {len(accordions)} accordions.")

    # --- Final Schema Assembly ---
    schema = {
        'key': JOURNEY_KEY,
        'name': 'Sprint 2 Testing Flow',
        'version': '0.1.0',
        'entity': 'entity',
        'fields': fields,
        'accordions': accordions,
    }

    # --- File Output ---
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_FILE, 'w') as f:
        yaml.dump(schema, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    info(f"Schema successfully written to: {OUT_FILE}")
    info("Import complete.")

if __name__ == '__main__':
    main()
