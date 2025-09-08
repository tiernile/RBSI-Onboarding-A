#!/usr/bin/env python3
"""
Generate as-is schema with full metadata from mappings
Creates YAML schema for as-is journey recreation
"""

import json
import yaml
import pandas as pd
from pathlib import Path
from datetime import datetime

def load_mappings(json_path):
    """Load field mappings"""
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data['mappings']

def load_lookup_values(excel_path):
    """Load lookup values from spreadsheet"""
    try:
        df = pd.read_excel(excel_path, sheet_name='Lookup Values', header=0)
        lookups = {}
        
        for _, row in df.iterrows():
            lookup_type = row.get('LOOKUP')
            value = row.get('LOOKUP VALUE')
            
            if pd.notna(lookup_type) and pd.notna(value):
                if lookup_type not in lookups:
                    lookups[lookup_type] = []
                lookups[lookup_type].append(str(value))
        
        return lookups
    except Exception as e:
        print(f"Warning: Could not load lookup values: {e}")
        return {}

def map_component_to_control(component_type):
    """Map HTML component type to schema control type"""
    mapping = {
        'dropdown': 'select',
        'text_input': 'text',
        'textarea': 'textarea',
        'radio': 'radio',
        'checkbox': 'checkbox',
        'complex_field': 'complex'
    }
    return mapping.get(component_type, 'text')

def map_data_type(spreadsheet_type):
    """Map spreadsheet data type to schema data type"""
    if pd.isna(spreadsheet_type):
        return 'string'
    
    type_lower = str(spreadsheet_type).lower()
    
    if 'lookup' in type_lower or 'enum' in type_lower:
        return 'enum'
    elif 'decimal' in type_lower or 'number' in type_lower:
        return 'number'
    elif 'date' in type_lower:
        return 'date'
    elif 'bool' in type_lower:
        return 'boolean'
    elif 'text' in type_lower or 'string' in type_lower:
        return 'string'
    else:
        return 'string'

def generate_field_id(keyname, index):
    """Generate field ID"""
    if keyname and not pd.isna(keyname):
        return str(keyname)
    else:
        return f"field_{index}"

def parse_visibility_condition(condition):
    """Parse visibility condition into structured format"""
    if pd.isna(condition) or not condition:
        return {'all': []}
    
    # Simple parsing - this would need enhancement for complex conditions
    conditions = []
    condition_str = str(condition)
    
    # Look for patterns like "field == value" or "field != value"
    if '==' in condition_str or '!=' in condition_str:
        conditions.append(condition_str.strip())
    
    return {'all': conditions} if conditions else {'all': []}

def create_schema_item(mapping, lookups, index):
    """Create a schema item from mapping data"""
    
    item = {
        'id': generate_field_id(mapping.get('spreadsheet_keyname'), index),
        'label': mapping.get('html_question', ''),
        'help': None,  # Would need to extract from HTML
        'entity_type': 'limited_partnership',  # Default for LP
        'jurisdiction': 'various',  # Would need proper mapping
        'stage': 'onboarding',  # Would need section mapping
        'section': 'General',  # Would need proper section
        'data_type': map_data_type(mapping.get('spreadsheet_data_type')),
        'control': map_component_to_control(mapping.get('html_component')),
        'options': [],
        'mandatory': mapping.get('html_mandatory', False),
        'visibility': {'all': []},  # Would need proper parsing
        'validation': {
            'regex': None,
            'max_length': None
        },
        'mappings': {
            'crm_field': None,
            'system_field': None
        },
        'meta': {
            'html_index': mapping.get('html_index'),
            'spreadsheet_ref': mapping.get('spreadsheet_ref'),
            'match_score': mapping.get('match_score'),
            'match_confidence': mapping.get('match_confidence'),
            'source': 'as-is-extraction',
            'extracted_date': datetime.now().isoformat()
        }
    }
    
    # Add options for dropdowns/radios
    if item['control'] in ['select', 'radio', 'checkbox']:
        # Try to find lookup values
        if mapping.get('spreadsheet_lookup') in lookups:
            item['options'] = lookups[mapping.get('spreadsheet_lookup')]
        else:
            # Default options for common patterns
            if 'yes' in item['label'].lower() or 'no' in item['label'].lower():
                item['options'] = ['Yes', 'No']
    
    return item

def generate_schema(mappings, lookups, output_path):
    """Generate complete schema YAML"""
    
    schema = {
        'key': 'as-is-journey',
        'name': 'As-Is Journey - Extracted from KYCP',
        'version': '0.1.0',
        'description': 'Schema extracted from existing KYCP HTML form for recreation',
        'metadata': {
            'extracted_date': datetime.now().isoformat(),
            'source_html': 'Project Stealth Code Questions (1).html',
            'source_spreadsheet': '20250828_draft-master-spreadsheet.xlsx',
            'total_fields': len(mappings),
            'extraction_method': 'automated'
        },
        'items': []
    }
    
    for index, mapping in enumerate(mappings):
        item = create_schema_item(mapping, lookups, index + 1)
        schema['items'].append(item)
    
    # Write YAML
    with open(output_path, 'w') as f:
        yaml.dump(schema, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    return schema

def generate_summary_report(schema, output_path):
    """Generate summary report of schema"""
    
    with open(output_path, 'w') as f:
        f.write("# As-Is Schema Generation Report\n\n")
        f.write(f"Generated: {schema['metadata']['extracted_date']}\n\n")
        
        f.write("## Schema Summary\n\n")
        f.write(f"- **Schema Key**: {schema['key']}\n")
        f.write(f"- **Name**: {schema['name']}\n")
        f.write(f"- **Version**: {schema['version']}\n")
        f.write(f"- **Total Fields**: {len(schema['items'])}\n\n")
        
        # Field type breakdown
        f.write("## Field Types\n\n")
        control_types = {}
        data_types = {}
        mandatory_count = 0
        
        for item in schema['items']:
            control = item['control']
            data = item['data_type']
            
            control_types[control] = control_types.get(control, 0) + 1
            data_types[data] = data_types.get(data, 0) + 1
            
            if item['mandatory']:
                mandatory_count += 1
        
        f.write("### Control Types\n")
        for control, count in sorted(control_types.items()):
            f.write(f"- {control}: {count}\n")
        
        f.write("\n### Data Types\n")
        for data, count in sorted(data_types.items()):
            f.write(f"- {data}: {count}\n")
        
        f.write(f"\n### Mandatory Fields: {mandatory_count} of {len(schema['items'])}\n\n")
        
        # Sample fields
        f.write("## Sample Fields\n\n")
        for item in schema['items'][:10]:
            f.write(f"### {item['id']}\n")
            f.write(f"- **Label**: {item['label']}\n")
            f.write(f"- **Control**: {item['control']}\n")
            f.write(f"- **Mandatory**: {item['mandatory']}\n")
            f.write(f"- **Match Confidence**: {item['meta'].get('match_confidence', 'N/A')}\n\n")

def main():
    # Paths
    project_root = Path(__file__).parent.parent
    mappings_path = project_root / "data/generated/as-is-audit/field-mappings.json"
    excel_path = project_root / "data/incoming/20250828_draft-master-spreadsheet.xlsx"
    schema_path = project_root / "data/schemas/as-is-journey/schema.yaml"
    report_path = project_root / "Documents/01 Areas/as-is-analysis/schema-generation-report.md"
    
    print("Loading field mappings...")
    mappings = load_mappings(mappings_path)
    
    print("Loading lookup values...")
    lookups = load_lookup_values(excel_path)
    print(f"Loaded {len(lookups)} lookup types")
    
    print("Generating schema...")
    schema_path.parent.mkdir(parents=True, exist_ok=True)
    schema = generate_schema(mappings, lookups, schema_path)
    
    print("Generating summary report...")
    generate_summary_report(schema, report_path)
    
    print(f"\nSchema generation complete!")
    print(f"- Schema: {schema_path}")
    print(f"- Report: {report_path}")
    print(f"- Total fields: {len(schema['items'])}")

if __name__ == "__main__":
    main()