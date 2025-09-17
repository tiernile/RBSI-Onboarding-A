#!/usr/bin/env python3
"""
Importer for CSV wicked problem areas → KYCP schema YAML

Reads mapping from apps/prototype/data/mappings/wicked-problem-areas.json
Parses the CSV and outputs:
  apps/prototype/data/schemas/wicked-problem-areas/schema.yaml

Features:
- CSV-based import with inline lookup values
- Problem area organization (Turnover, Purpose, Source of Funds, etc.)
- Complex field support
- Audit trail with source row references
"""
from __future__ import annotations
import json, re, sys, yaml, csv
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = APP_DIR / 'data'
INCOMING = DATA_DIR / 'incoming' / 'P2140 - RBSI Onboarding wicked-problem-area-questions-sprint-2-testing-flow.csv'
MAPPING = DATA_DIR / 'mappings' / 'wicked-problem-areas.json'
OUT_DIR = DATA_DIR / 'schemas' / 'wicked-problem-areas'
OUT_FILE = OUT_DIR / 'schema.yaml'

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
        else:
            out.append('-')

    result = ''.join(out)
    result = re.sub(r'-+', '-', result).strip('-')
    return result or 'untitled'

def parse_lookup_values(value_str: str) -> list[str]:
    """Parse inline lookup values like 'Yes | No | Don't know yet'"""
    if not value_str or value_str.strip() == '':
        return []

    # Split on | and clean up
    values = [v.strip() for v in value_str.split('|')]
    return [v for v in values if v]

def normalize_field_type(field_type: str, mapping: dict) -> str:
    """Convert field type using normalization rules"""
    if not field_type:
        return 'freeText'

    normalization = mapping.get('normalization', {}).get('data_type', {})
    return normalization.get(field_type, 'freeText')

def process_csv_file(csv_path: Path, mapping: dict) -> list[dict]:
    """Read and process CSV file according to mapping"""
    rows = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row_num, row in enumerate(reader, start=2):  # Start at 2 since header is row 1
            # Skip empty rows
            keyname = row.get(mapping['columns']['id'], '').strip()
            question = row.get(mapping['columns']['label'], '').strip()

            if not keyname or not question:
                continue

            # Extract field data
            field_data = {
                'source_row': row_num,
                'keyname': keyname,
                'question': question,
                'helper': row.get(mapping['columns']['help'], '').strip(),
                'section': row.get(mapping['columns']['section'], '').strip(),
                'field_type': row.get(mapping['columns']['field_type'], '').strip(),
                'lookup_values_inline': row.get(mapping['columns']['lookup_values_inline'], '').strip(),
                'wicked_area': row.get(mapping['columns']['wicked_area'], '').strip(),
                'q_number': row.get(mapping['columns']['q_number'], '').strip()
            }

            rows.append(field_data)

    info(f"Processed {len(rows)} valid rows from CSV")
    return rows

def load_as_is_field_data() -> dict:
    """Load AS-IS field definitions from existing schemas for reference"""
    as_is_fields = {}

    # Key AS-IS field data found from existing schemas
    as_is_fields['GENCashMngtAccPurpose'] = {
        'type': 'freeText',
        'as_is_label': 'Please advise what the account is to be used for. For example, a combination of the following: payments of professional fees, dividend receipts/payments, rental income, expenses, trading income, purchases of wholesale goods, cash elements of an investment portfolio.',
        'required': True,
        'visibility': "GENcashmngtaccount == 'YES'"
    }

    as_is_fields['GENIndicativeAppetiteCountryRegistration'] = {
        'type': 'lookup',
        'as_is_label': 'In relation to the Incorporation of the entity requiring a bank account, can you please specify the Country of registration/formation/Establishment?',
        'options': ['United Kingdom', 'United States', 'Jersey', 'Guernsey', 'Isle of Man', 'Gibraltar', 'France', 'Germany', 'Luxembourg', 'Ireland'],
        'required': True
    }

    as_is_fields['GENFundInvestments'] = {
        'type': 'freeText',
        'as_is_label': 'What are the type of investments including details of asset classes and sectors?',
        'required': True
    }

    as_is_fields['GENFundCurrency'] = {
        'type': 'lookup',
        'as_is_label': 'What is the currency denomination of the fund?',
        'options': ['GBP', 'USD', 'EUR', 'CHF', 'JPY']
    }

    as_is_fields['GENFundClosed'] = {
        'type': 'lookup',
        'as_is_label': 'Has the fund had a final close?',
        'options': ['Yes', 'No'],
        'visibility': 'conditional'
    }

    as_is_fields['GENFundSize'] = {
        'type': 'lookup',
        'as_is_label': 'What is the fund size in the selected currency denomination?',
        'options': ['< 50m', '50m - 250m', '250m - 500m', '500m - 750m', '750m - 1bn', '1bn - 2bn', '2bn - 5bn', '5bn - 10bn', '10bn - 20bn', '20bn +'],
        'visibility': "GENFundClosed == 'Yes'"
    }

    as_is_fields['GENindustrysector'] = {
        'type': 'lookup',
        'as_is_label': 'Industry description incl SIC code',
        'options': ['Agriculture', 'Manufacturing', 'Financial Services', 'Technology', 'Healthcare', 'Real Estate', 'Other']
    }

    as_is_fields['GENInvestorCountryComplex'] = {
        'type': 'complex',
        'as_is_label': 'Please provide details of the typical investors the fund is targeted at, e.g. institutional, private client, retail etc and where the investors are likely to be based. Please also include the percentage of each type of investor, e.g. 50% institutional, 50% private client.',
        'children': ['GENInvestorType', 'GENInvestorTypeOther', 'GENInvestorCountry', 'GENInvestorTypePerc']
    }

    as_is_fields['GENAccountType'] = {
        'type': 'lookup',
        'as_is_label': 'Please specify the type of account you require.',
        'options': ['Business Current Account', 'Business Treasury Cash Management Account']
    }

    as_is_fields['GENCashMngtAccTransCreditMonth'] = {
        'type': 'number',
        'as_is_label': '# of transactions per month',
        'visibility': "GENCashMngtAccTransCreditIdenty == 'Yes'"
    }

    as_is_fields['GENcountryregistration'] = {
        'type': 'lookup',
        'as_is_label': 'Country of registration/formation',
        'options': ['United Kingdom', 'United States', 'Jersey', 'Guernsey', 'Isle of Man', 'Gibraltar', 'France', 'Germany', 'Luxembourg', 'Ireland']
    }

    as_is_fields['GENIndicativeAppetiteRiskadverse'] = {
        'type': 'lookup',
        'as_is_label': 'Are there any Reputational, Environmental, Social and Ethical (ESE) or tax risks associated with the application?',
        'options': ['Yes', 'No']
    }

    as_is_fields['GENtaxcountry'] = {
        'type': 'lookup',
        'as_is_label': 'Country',
        'options': ['United Kingdom', 'United States', 'Jersey', 'Guernsey', 'Isle of Man', 'Gibraltar', 'France', 'Germany', 'Luxembourg', 'Ireland']
    }

    as_is_fields['GENknowtin'] = {
        'type': 'lookup',
        'as_is_label': 'Do you know the Tax identification number?',
        'options': ['Yes', 'No']
    }

    as_is_fields['GENtin'] = {
        'type': 'freeText',
        'as_is_label': 'Provide Tax identification number or an equivalent',
        'visibility': "GENknowtin == 'Yes'"
    }

    as_is_fields['GENincorpUSA'] = {
        'type': 'lookup',
        'as_is_label': 'Is the entity/organisation incorporated/organised in the USA?',
        'options': ['Specified US Person', 'Other US Person', 'No']
    }

    as_is_fields['GENffi'] = {
        'type': 'lookup',
        'as_is_label': 'Is the entity/organisation a Financial Foreign Institution (FFI)?',
        'options': ['Reporting FFI', 'Sponsored FFI', 'Other FFI', 'No', 'Trustee Documented Trust'],
        'visibility': "GENincorpUSA != 'Specified US Person' && GENincorpUSA != 'Other US Person'"
    }

    return as_is_fields

def create_field(field_data: dict, mapping: dict, as_is_data: dict) -> dict:
    """Create a schema field merging CSV data (new Nile) with AS-IS field definitions"""
    keyname = field_data['keyname']
    field_type = normalize_field_type(field_data['field_type'], mapping)

    # Start with CSV data (new Nile enhancements)
    field = {
        'id': keyname,
        'label': field_data['question'],  # New Nile question text
        'type': field_type
    }

    # Add new Nile helper text if present
    if field_data['helper']:
        field['help'] = field_data['helper']

    # Merge with AS-IS data if available
    if keyname in as_is_data:
        as_is = as_is_data[keyname]

        # Use AS-IS type if more specific
        if 'type' in as_is:
            field['type'] = as_is['type']

        # Add AS-IS options for lookup fields
        if field['type'] == 'lookup' and 'options' in as_is:
            field['options'] = as_is['options']
        elif field['type'] == 'lookup' and field_data['lookup_values_inline']:
            # Use CSV inline values as fallback
            lookup_values = parse_lookup_values(field_data['lookup_values_inline'])
            if lookup_values:
                field['options'] = lookup_values

        # Add AS-IS validation and visibility
        if 'required' in as_is:
            field['required'] = as_is['required']
        if 'visibility' in as_is:
            field['visibility'] = as_is['visibility']

        # Handle complex fields
        if field['type'] == 'complex' and 'children' in as_is:
            field['children'] = as_is['children']

    # Handle lookup fallbacks for fields without AS-IS data
    elif field['type'] == 'lookup':
        if field_data['lookup_values_inline']:
            lookup_values = parse_lookup_values(field_data['lookup_values_inline'])
            if lookup_values:
                field['options'] = lookup_values
        else:
            # Use common fallbacks
            if 'Yes' in field_data['question'] or 'Do you' in field_data['question']:
                field['options'] = ['Yes', 'No']

    # Add comprehensive metadata for audit trail
    field['meta'] = {
        'source_row_ref': f"ROW:{field_data['source_row']}|KEY:{keyname}",
        'wicked_area': field_data['wicked_area'],  # Accordion title
        'q_number': field_data['q_number'],
        'as_is_section': field_data['section'],  # Current section for auditability
        'nile_enhanced': True,  # Flag indicating this uses new Nile question/helper
        'has_as_is_data': keyname in as_is_data
    }

    # Add AS-IS label for comparison/audit
    if keyname in as_is_data and 'as_is_label' in as_is_data[keyname]:
        field['meta']['as_is_label'] = as_is_data[keyname]['as_is_label']

    return field

def organize_sections(fields: list[dict], mapping: dict) -> dict:
    """Organize fields into sections based on wicked problem areas"""
    sections = {}
    wicked_area_mapping = mapping.get('wicked_area_sections', {})

    for field in fields:
        wicked_area = field['meta']['wicked_area']
        section_name = wicked_area_mapping.get(wicked_area, wicked_area)

        if section_name not in sections:
            sections[section_name] = {
                'id': slugify(section_name),
                'label': section_name,
                'fields': []
            }

        sections[section_name]['fields'].append(field)

    return sections

def main():
    info("Starting CSV import for wicked problem areas...")

    # Load mapping
    if not MAPPING.exists():
        print(f"[error] Mapping file not found: {MAPPING}", file=sys.stderr)
        sys.exit(1)

    with open(MAPPING, 'r') as f:
        mapping = json.load(f)

    # Check CSV file
    if not INCOMING.exists():
        print(f"[error] CSV file not found: {INCOMING}", file=sys.stderr)
        sys.exit(1)

    # Process CSV
    info(f"Reading CSV: {INCOMING}")
    csv_rows = process_csv_file(INCOMING, mapping)

    if not csv_rows:
        print("[error] No valid rows found in CSV", file=sys.stderr)
        sys.exit(1)

    # Load AS-IS field data for merging
    info("Loading AS-IS field definitions...")
    as_is_data = load_as_is_field_data()

    # Create fields merging CSV with AS-IS data
    fields = []
    for row_data in csv_rows:
        field = create_field(row_data, mapping, as_is_data)
        fields.append(field)

    info(f"Created {len(fields)} fields")

    # Organize into sections
    sections = organize_sections(fields, mapping)
    info(f"Organized into {len(sections)} sections")

    # Convert to working KYCP format with accordions
    kycp_fields = []
    accordions = []

    # Track fields for each accordion
    accordion_fields = {}

    for section_name, section in sections.items():
        wicked_area = None
        accordion_key = None

        for field in section['fields']:
            wicked_area = field['meta']['wicked_area']
            accordion_key = slugify(wicked_area)

            # Sanitize field key (keep original ID where possible)
            field_key = field['id']
            if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', field_key):
                field_key = re.sub(r'[^a-zA-Z0-9_-]', '_', field_key)
                field_key = re.sub(r'^[^a-zA-Z]', 'field_', field_key)
                field_key = re.sub(r'_+', '_', field_key)

            # Convert to working KYCP format
            kycp_field = {
                'key': field_key,
                'entity': 'entity',
                'style': 'field',
                'label': field['label'],
                'original': {
                    'label': field['meta'].get('as_is_label', field['label']),
                    'help': None
                },
                'type': 'lookup' if field['type'] == 'lookup' else 'freeText' if field['type'] == 'freeText' else 'number' if field['type'] == 'number' else 'complex' if field['type'] == 'complex' else 'freeText',
                'validation': {},
                '_section': wicked_area,
                '_metadata': {
                    'source_row_ref': field['meta']['source_row_ref'],
                    'wicked_area': wicked_area,
                    'q_number': field['meta']['q_number'],
                    'as_is_section': field['meta']['as_is_section'],
                    'nile_enhanced': field['meta']['nile_enhanced'],
                    'has_as_is_data': field['meta']['has_as_is_data']
                }
            }

            # Add help text if present
            if field.get('help'):
                kycp_field['help'] = field['help']

            # Convert options to working format
            if field['type'] == 'lookup' and 'options' in field:
                kycp_field['options'] = [
                    {'value': opt, 'label': opt}
                    for opt in field['options']
                ]

            # Add visibility rules
            if 'visibility' in field:
                kycp_field['visibility_rule'] = field['visibility']

            # Add AS-IS metadata for audit
            if field['meta']['has_as_is_data']:
                kycp_field['original']['label'] = field['meta']['as_is_label']

            kycp_fields.append(kycp_field)

            # Track field for accordion
            if accordion_key not in accordion_fields:
                accordion_fields[accordion_key] = {
                    'title': wicked_area,
                    'fields': []
                }
            accordion_fields[accordion_key]['fields'].append(field_key)

    # Create accordions structure
    for accordion_key, accordion_data in accordion_fields.items():
        accordions.append({
            'key': accordion_key,
            'title': accordion_data['title'],
            'fields': accordion_data['fields']
        })

    # Create schema structure in working KYCP format
    schema = {
        'key': 'wicked-problem-areas',
        'name': 'Wicked Problem Areas Sprint 2',
        'version': '0.1.0',
        'entity': 'entity',
        'fields': kycp_fields,
        'accordions': accordions
    }

    # Create output directory
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Write schema file
    with open(OUT_FILE, 'w') as f:
        yaml.dump(schema, f, default_flow_style=False, allow_unicode=True)

    info(f"Schema written to: {OUT_FILE}")

    # Summary
    total_fields = sum(len(section['fields']) for section in sections.values())
    info(f"Summary: {len(sections)} sections, {total_fields} fields")

    for section_name, section in sections.items():
        info(f"  {section_name}: {len(section['fields'])} fields")

if __name__ == '__main__':
    main()