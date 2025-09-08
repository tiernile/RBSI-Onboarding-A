#!/usr/bin/env python3
"""
Extract and analyze form fields from as-is HTML
Generates structured field inventory for mapping
"""

import re
from bs4 import BeautifulSoup
import json
import yaml
from pathlib import Path

def extract_form_fields(html_path):
    """Extract all form fields from HTML with metadata"""
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    fields = []
    
    # Find all question containers
    question_containers = soup.find_all('li', {'data-v-15d17799': True})
    
    for idx, container in enumerate(question_containers):
        field_data = {
            'index': idx + 1,
            'question_text': None,
            'is_mandatory': False,
            'component_type': None,
            'has_visibility_condition': False,
            'options': [],
            'help_text': None,
            'validation_type': None
        }
        
        # Extract question text
        question_span = container.find('span', class_='col-12 text-break')
        if question_span:
            text = question_span.get_text(strip=True)
            field_data['question_text'] = text.rstrip('*')
            field_data['is_mandatory'] = text.endswith('*')
        
        # Identify component type
        if container.find('div', class_='v-select'):
            field_data['component_type'] = 'dropdown'
        elif container.find('textarea'):
            field_data['component_type'] = 'textarea'
        elif container.find('input', type='text'):
            field_data['component_type'] = 'text_input'
        elif container.find('input', type='radio'):
            field_data['component_type'] = 'radio'
        elif container.find('input', type='checkbox'):
            field_data['component_type'] = 'checkbox'
        elif container.find('ul', class_='fieldContainer effisComplex'):
            field_data['component_type'] = 'complex_field'
        
        # Check for visibility conditions (style="display: none")
        if container.get('style') and 'display: none' in container.get('style'):
            field_data['has_visibility_condition'] = True
        
        # Extract help text or labels
        help_label = container.find('label', class_='col-12 text-break')
        if help_label and help_label != question_span:
            field_data['help_text'] = help_label.get_text(strip=True)
        
        # Extract input attributes for validation hints
        input_elem = container.find('input')
        if input_elem:
            if 'txtDecimalInput' in input_elem.get('id', ''):
                field_data['validation_type'] = 'decimal'
            elif input_elem.get('type') == 'email':
                field_data['validation_type'] = 'email'
        
        if field_data['question_text']:
            fields.append(field_data)
    
    return fields

def match_to_spreadsheet_patterns(fields):
    """Try to match extracted fields to common spreadsheet KEYNAMEs"""
    
    # Common patterns from spreadsheet analysis
    keyname_patterns = {
        'jurisdiction': r'jurisdiction.*account',
        'application_type': r'which option.*describes',
        'pre_app_questions': r'pre-application questions',
        'third_party_admin': r'3rd party administrator',
        'fund_manager': r'fund manager',
        'investment_adviser': r'investment adviser',
        'type_of_fund': r'type of fund',
        'high_risk': r'high risk',
        'sovereign_wealth': r'sovereign wealth',
        'peps': r'pep|politically exposed'
    }
    
    for field in fields:
        if field['question_text']:
            question_lower = field['question_text'].lower()
            
            for key, pattern in keyname_patterns.items():
                if re.search(pattern, question_lower):
                    field['likely_keyname_group'] = key
                    break
    
    return fields

def generate_field_inventory(fields, output_path):
    """Generate markdown documentation of extracted fields"""
    
    with open(output_path, 'w') as f:
        f.write("# As-Is HTML Field Inventory\n\n")
        f.write("Extracted from: `Project Stealth Code Questions (1).html`\n")
        f.write(f"Total fields identified: {len(fields)}\n\n")
        
        f.write("## Field Summary by Component Type\n\n")
        
        # Group by component type
        by_type = {}
        for field in fields:
            comp_type = field['component_type'] or 'unknown'
            if comp_type not in by_type:
                by_type[comp_type] = []
            by_type[comp_type].append(field)
        
        for comp_type, type_fields in by_type.items():
            f.write(f"- **{comp_type}**: {len(type_fields)} fields\n")
        
        f.write("\n## Detailed Field List\n\n")
        
        for field in fields:
            f.write(f"### Field {field['index']}\n\n")
            f.write(f"**Question**: {field['question_text']}\n\n")
            f.write(f"- **Component Type**: {field['component_type']}\n")
            f.write(f"- **Mandatory**: {'Yes' if field['is_mandatory'] else 'No'}\n")
            f.write(f"- **Has Visibility Condition**: {'Yes' if field['has_visibility_condition'] else 'No'}\n")
            
            if field.get('likely_keyname_group'):
                f.write(f"- **Likely KEYNAME Group**: {field['likely_keyname_group']}\n")
            
            if field['help_text']:
                f.write(f"- **Help Text**: {field['help_text']}\n")
            
            if field['validation_type']:
                f.write(f"- **Validation Type**: {field['validation_type']}\n")
            
            f.write("\n---\n\n")

def main():
    # Paths
    project_root = Path(__file__).parent.parent
    html_path = project_root / "Documents/01 Areas/As-is/Project Stealth Code Questions (1).html"
    output_md = project_root / "Documents/01 Areas/as-is-analysis/field-inventory.md"
    output_json = project_root / "data/generated/as-is-audit/extracted-fields.json"
    
    # Extract fields
    print("Extracting fields from HTML...")
    fields = extract_form_fields(html_path)
    
    # Try to match patterns
    print("Matching to spreadsheet patterns...")
    fields = match_to_spreadsheet_patterns(fields)
    
    # Generate outputs
    print(f"Generating field inventory markdown...")
    generate_field_inventory(fields, output_md)
    
    print(f"Saving JSON data...")
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with open(output_json, 'w') as f:
        json.dump(fields, f, indent=2)
    
    print(f"\nExtraction complete!")
    print(f"- Total fields: {len(fields)}")
    print(f"- Markdown report: {output_md}")
    print(f"- JSON data: {output_json}")

if __name__ == "__main__":
    main()