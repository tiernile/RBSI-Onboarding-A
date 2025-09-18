#!/usr/bin/env python3
"""
Importer for "Wicked Problem Areas" CSV → KYCP schema YAML

Reads the CSV file and generates a schema for a new prototype journey.
"""
import csv
import re
import sys
from pathlib import Path

import yaml

# Project directories
APP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = APP_DIR / 'data'
INCOMING_CSV = DATA_DIR / 'incoming' / 'P2140 - RBSI Onboarding wicked-problem-area-questions-sprint-2-testing-flow.csv'
OUT_DIR = DATA_DIR / 'schemas' / 'wicked-problem-areas'
OUT_FILE = OUT_DIR / 'schema-kycp.yaml'

# --- Utility Functions ---

def info(msg: str):
    """Prints an informational message."""
    print(f"[INFO] {msg}")

def slugify(s: str) -> str:
    """Converts a string into a URL-friendly slug."""
    s = (s or '').strip().lower()
    s = s.replace('&', ' and ')
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-') or 'untitled'

def map_field_type(raw_type: str) -> str:
    """Maps CSV field types to schema field types."""
    type_map = {
        'free text': 'freeText',
        'lookup': 'lookup',
        'complex': 'complex',
        'decimal': 'decimal',
        'integer': 'integer',
        'string': 'string',
        'date': 'date',
    }
    return type_map.get(raw_type.lower().strip(), 'freeText')

def parse_lookup_options(value_str: str) -> list[dict]:
    """Parses a pipe-separated string into a list of value/label objects."""
    if not value_str or value_str.strip().upper() in ['', 'COUNTRIES']:
        return []
    
    options = []
    for item in value_str.split('|'):
        clean_item = item.strip()
        if clean_item:
            options.append({'value': clean_item, 'label': clean_item})
    return options

# --- Main Logic ---

def create_schema_from_csv(csv_path: Path) -> dict:
    """Reads the CSV and builds the complete schema structure."""
    fields = []
    accordions_map = {}

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):
            keyname = row.get('Keyname', '').strip()
            question = row.get('Question', '').strip()

            # Skip rows without essential data
            if not keyname or not question:
                continue

            # Build the field object
            field = {
                'key': keyname,
                'entity': 'entity',
                'style': 'field',
                'label': question,
                'type': map_field_type(row.get('FIELD TYPE', '')),
                '_section': row.get('Wicked problem area', 'General').strip(),
                '_metadata': {'source_row': i},
            }

            # Add help text if available
            if helper := row.get('Helper', '').strip():
                field['help'] = helper
            
            # Add options for lookup fields
            if field['type'] == 'lookup':
                field['options'] = parse_lookup_options(row.get('Lookup Values', ''))
            
            # Add empty validation block (can be filled in later)
            field['validation'] = {}

            fields.append(field)
            
            # Track accordions
            accordion_title = field['_section']
            accordion_key = slugify(accordion_title)
            if accordion_key not in accordions_map:
                accordions_map[accordion_key] = {'key': accordion_key, 'title': accordion_title}

    # Final schema structure
    schema = {
        'key': 'wicked-problem-areas',
        'name': 'Wicked Problem Areas Sprint 2',
        'version': '0.1.0',
        'entity': 'entity',
        'fields': fields,
        'accordions': list(accordions_map.values()),
    }
    
    return schema

def main():
    """Main execution function."""
    info("Starting CSV import for 'Wicked Problem Areas'...")

    if not INCOMING_CSV.exists():
        print(f"[ERROR] CSV file not found at: {INCOMING_CSV}", file=sys.stderr)
        sys.exit(1)

    # Generate the schema from the CSV
    info(f"Processing {INCOMING_CSV}...")
    schema = create_schema_from_csv(INCOMING_CSV)
    
    # Ensure the output directory exists
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Write the YAML file
    info(f"Writing schema to {OUT_FILE}...")
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(schema, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    info("Import complete.")
    info(f"Generated {len(schema['fields'])} fields across {len(schema['accordions'])} accordions.")

if __name__ == '__main__':
    main()