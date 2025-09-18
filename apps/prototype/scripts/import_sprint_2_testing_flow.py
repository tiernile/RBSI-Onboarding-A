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
INCOMING_CSV = DATA_DIR / 'incoming' / 'RBSI Onboarding Sprint 2 Testing Flow v3.csv'
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

def normalize_field_type(field_type_str: str) -> str:
    """Normalize field type from CSV to schema type."""
    ft = (field_type_str or '').strip().lower()
    if ft in ['lookup', 'dropdown', 'select']: return 'lookup'
    if ft in ['string', 'text', 'input']: return 'string'
    if ft in ['textarea', 'freetext']: return 'freeText'
    if ft in ['number', 'integer', 'decimal']: return 'integer'
    if ft in ['date']: return 'date'
    return 'string' # Default to string

# --- Core Logic ---

def process_csv_file(csv_path: Path) -> list[dict]:
    """Read and process the input CSV file."""
    rows = []
    if not csv_path.exists():
        warn(f"CSV file not found at {csv_path}")
        return rows

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):
            keyname = row.get('Keyname', '').strip()
            question = row.get('Question', '').strip()
            
            if not keyname or not question:
                continue

            rows.append({
                'source_row': row_num,
                'keyname': keyname,
                'label': question,
                'help': row.get('Helper', '').strip(),
                'section_title': row.get('Section', '').strip(),
                'field_type_raw': row.get('FIELD TYPE', '').strip(),
                'lookup_values_raw': row.get('Lookup Values', '').strip(),
            })
    info(f"Processed {len(rows)} valid rows from {csv_path.name}")
    return rows

def create_schema_field(row: dict) -> dict:
    """Create a single field dictionary for the YAML schema."""
    field_type = normalize_field_type(row['field_type_raw'])
    
    field = {
        'key': row['keyname'],
        'entity': 'entity',
        'style': 'field',
        'label': row['label'],
        'type': field_type,
        'validation': {},
        '_section': row['section_title'],
        '_metadata': {
            'source_row_ref': f"ROW:{row['source_row']}",
        }
    }

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

    fields = [create_schema_field(row) for row in csv_rows]
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
