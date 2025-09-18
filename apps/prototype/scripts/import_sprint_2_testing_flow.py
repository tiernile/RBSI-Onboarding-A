#!/usr/bin/env python3
"""
Importer for "Sprint 2 Testing Flow" CSV → KYCP schema YAML

Parses the CSV and outputs:
  apps/prototype/data/schemas/sprint-2-testing-flow/schema-kycp.yaml

"""
from __future__ import annotations
import json, re, sys, yaml, csv
import io
from pathlib import Path

# --- Configuration ---
APP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = APP_DIR / 'data'
JOURNEY_KEY = 'sprint-2-testing-flow'
AS_IS_JOURNEY_KEY = 'non-lux-1-1'
INCOMING_CSV = DATA_DIR / 'incoming' / 'RBSI Onboarding Sprint 2 Testing Flow v3.2.csv'
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
    elif ft in ['date', 'datepicker', 'date picker']:
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
    """Read and process the input CSV file, handling potential formatting errors."""
    rows = []
    if not csv_path.exists():
        warn(f"CSV file not found at {csv_path}")
        return rows

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        # Read raw content and fix known issues before parsing
        content = f.read()
        # This is a brittle fix for a specific known issue in the CSV on line 8.
        # A better long-term solution would be to enforce CSV quality upstream.
        content = content.replace(''',"Before you start:

Think about what your business does and who your main clients/customers are
    Have your annual turnover figure ready
    Know how long you've been trading"''', ''',"Before you start: Think about what your business does and who your main clients/customers are, Have your annual turnover figure ready, Know how long you've been trading"''')
        
        reader = csv.DictReader(io.StringIO(content))
        for row_num, row in enumerate(reader, start=2):
            if not any(row.values()): # Skip completely blank rows
                continue

            # Clean up potential leading/trailing quotes and spaces from keys and values
            cleaned_row = {}
            for k, v in row.items():
                key = k.strip() if isinstance(k, str) else k
                value = v.strip() if isinstance(v, str) else v
                cleaned_row[key] = value

            keyname = (cleaned_row.get('Keyname') or '').strip()
            question = (cleaned_row.get('Question') or '').strip()

            if not keyname and not question: # Skip rows without key identifiers
                continue

            rows.append({
                'source_row': row_num,
                'keyname': keyname,
                'label': question,
                'help': (cleaned_row.get('Helper') or '').strip(),
                'section_title': (cleaned_row.get('Section') or '').strip(),
                'field_type_raw': (cleaned_row.get('FIELD TYPE') or '').strip(),
                'lookup_values_raw': (cleaned_row.get('Lookup Values') or '').strip(),
            })
            
    # After processing, programmatically remove the helper text from the description field
    for row_data in rows:
        if row_data['keyname'] == 'Description-new-application':
            row_data['help'] = ''
            info("Cleaned up duplicated helper text from 'Description-new-application'.")
            break

    info(f"Processed {len(rows)} valid rows from {csv_path.name}")
    return rows

def create_schema_field(row: dict, as_is_data: dict[str, dict]) -> dict | None:
    """Create a single field dictionary for the YAML schema, or None if this should be accordion metadata."""
    style, field_type = normalize_field_type(row['field_type_raw'])
    keyname = row['keyname']
    
    # Override style for specific key patterns
    if keyname.startswith('TITLE-'):
        style = 'divider'
    if keyname.startswith('DESC-'):
        style = 'statement'

    # Skip title fields that are meant to be accordion headers - they'll be handled in accordion generation
    if style == 'divider' and row['field_type_raw'].lower() in ['title']:
        return None
    
    # Infer section for Description fields with empty sections based on keyname patterns
    section_title = row['section_title']
    if not section_title and keyname.startswith('Description-'):
        keyname_suffix = keyname.replace('Description-', '')
        if keyname_suffix == 'intermediary':
            section_title = 'Applying as an intermediary'
        elif keyname_suffix == 'PurposeOfBusiness':
            section_title = 'Purpose of Business'
        elif keyname_suffix == 'Tax':
            section_title = 'Tax'
        elif keyname_suffix == 'fund':
            section_title = 'Purpose of Fund'
    
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
        '_section': section_title,
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
    
    # Create fields, filtering out None returns (title rows)
    all_field_results = [create_schema_field(row, as_is_data) for row in csv_rows]
    fields = [f for f in all_field_results if f is not None]

    info(f"Generated {len(fields)} fields from CSV data.")

    # --- Accordion Generation with Description Text ---
    accordions = []
    accordion_map = {}
    
    # First pass: collect accordion structure and descriptions from title rows
    for row in csv_rows:
        style, _ = normalize_field_type(row['field_type_raw'])
        if style == 'divider' and row['field_type_raw'].lower() in ['title']:
            section_title = row['section_title']
            
            # Infer section for Title fields with empty sections based on keyname patterns
            if not section_title and row['keyname'].startswith('Title-'):
                keyname_suffix = row['keyname'].replace('Title-', '')
                if keyname_suffix == 'intermediary':
                    section_title = 'Applying as an intermediary'
                elif keyname_suffix == 'PurposeOfBusiness':
                    section_title = 'Purpose of Business'
                elif keyname_suffix == 'tax':
                    section_title = 'Tax'
                elif keyname_suffix == 'fund':
                    section_title = 'Purpose of Fund'
                elif keyname_suffix == 'HowYouBank':
                    section_title = 'How you bank with us'
            
            if section_title:  # Only create accordion if we have a valid section title
                accordion_key = slugify(section_title)
                if accordion_key not in accordion_map:
                    # Clean up helper text by normalizing whitespace and line breaks
                    description = None
                    if row['help']:
                        description = ' '.join(row['help'].strip().split())
                    
                    accordion_map[accordion_key] = {
                        'key': accordion_key,
                        'title': section_title,
                        'description': description,  # Use cleaned helper text as description
                    }
    
    # Second pass: ensure all field sections have accordions (even without explicit title rows)
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
