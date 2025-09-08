#!/usr/bin/env python3
"""
Map spreadsheet questions to extracted HTML fields
Creates bidirectional mapping for audit trail
"""

import json
import pandas as pd
from pathlib import Path
from difflib import SequenceMatcher
import re

def normalize_text(text):
    """Normalize text for comparison"""
    if pd.isna(text) or text is None:
        return ""
    # Remove special chars, lowercase, strip whitespace
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = ' '.join(text.split())
    return text

def calculate_similarity(text1, text2):
    """Calculate similarity score between two texts"""
    norm1 = normalize_text(text1)
    norm2 = normalize_text(text2)
    return SequenceMatcher(None, norm1, norm2).ratio()

def load_spreadsheet_data(excel_path):
    """Load and process spreadsheet data"""
    df = pd.read_excel(excel_path, sheet_name='LP Proposal', header=1)
    
    # Filter to rows with KEYNAME and FIELD NAME
    df_filtered = df[df['KEYNAME'].notna() | df['FIELD NAME'].notna()].copy()
    
    questions = []
    for idx, row in df_filtered.iterrows():
        question = {
            'ref': row.get('REF'),
            'keyname': row.get('KEYNAME'),
            'field_name': row.get('FIELD NAME'),
            'data_type': row.get('DATA TYPE'),
            'field_type': row.get('FIELD TYPE'),
            'mandatory': row.get('MANDATORY'),
            'visibility_condition': row.get('VISIBILITY CONDITION/GROUP NAME'),
            'section': row.get('PAUL Section Suggestion'),
            'lookup': row.get('LOOKUP'),
            'validation': row.get('VALIDATION'),
            'question_text': None
        }
        
        # Try to get question text from various columns
        if pd.notna(row.get('FIELD NAME')):
            question['question_text'] = str(row.get('FIELD NAME'))
        elif pd.notna(row.get('LABEL')):
            question['question_text'] = str(row.get('LABEL'))
        
        questions.append(question)
    
    return questions

def load_html_fields(json_path):
    """Load extracted HTML fields"""
    with open(json_path, 'r') as f:
        return json.load(f)

def find_best_matches(html_fields, spreadsheet_questions):
    """Find best matches between HTML fields and spreadsheet questions"""
    
    mappings = []
    unmatched_html = []
    unmatched_spreadsheet = list(range(len(spreadsheet_questions)))
    
    for html_idx, html_field in enumerate(html_fields):
        if not html_field.get('question_text'):
            continue
        
        best_match = None
        best_score = 0
        best_idx = -1
        
        for sp_idx, sp_question in enumerate(spreadsheet_questions):
            if sp_question.get('question_text'):
                score = calculate_similarity(
                    html_field['question_text'],
                    sp_question['question_text']
                )
                
                if score > best_score:
                    best_score = score
                    best_match = sp_question
                    best_idx = sp_idx
        
        if best_score > 0.7:  # Threshold for match
            mapping = {
                'html_index': html_field['index'],
                'html_question': html_field['question_text'],
                'html_component': html_field['component_type'],
                'html_mandatory': html_field['is_mandatory'],
                'spreadsheet_keyname': best_match.get('keyname'),
                'spreadsheet_ref': best_match.get('ref'),
                'spreadsheet_question': best_match.get('question_text'),
                'spreadsheet_data_type': best_match.get('data_type'),
                'spreadsheet_mandatory': best_match.get('mandatory'),
                'match_score': round(best_score, 3),
                'match_confidence': 'HIGH' if best_score > 0.9 else 'MEDIUM'
            }
            mappings.append(mapping)
            
            if best_idx in unmatched_spreadsheet:
                unmatched_spreadsheet.remove(best_idx)
        else:
            unmatched_html.append({
                'index': html_field['index'],
                'question': html_field['question_text'],
                'component': html_field['component_type']
            })
    
    unmatched_sp_questions = [
        {
            'keyname': spreadsheet_questions[idx].get('keyname'),
            'ref': spreadsheet_questions[idx].get('ref'),
            'question': spreadsheet_questions[idx].get('question_text')
        }
        for idx in unmatched_spreadsheet
        if spreadsheet_questions[idx].get('question_text')
    ]
    
    return mappings, unmatched_html, unmatched_sp_questions

def generate_mapping_report(mappings, unmatched_html, unmatched_sp, output_path):
    """Generate markdown mapping report"""
    
    with open(output_path, 'w') as f:
        f.write("# HTML to Spreadsheet Field Mapping\n\n")
        f.write("## Summary\n\n")
        f.write(f"- **Total Mapped Fields**: {len(mappings)}\n")
        f.write(f"- **Unmatched HTML Fields**: {len(unmatched_html)}\n")
        f.write(f"- **Unmatched Spreadsheet Questions**: {len(unmatched_sp)}\n\n")
        
        # High confidence matches
        high_conf = [m for m in mappings if m['match_confidence'] == 'HIGH']
        f.write(f"### Match Confidence\n\n")
        f.write(f"- **High Confidence (>90% match)**: {len(high_conf)}\n")
        f.write(f"- **Medium Confidence (70-90% match)**: {len(mappings) - len(high_conf)}\n\n")
        
        f.write("## Mapped Fields\n\n")
        f.write("| HTML Field | Spreadsheet KEYNAME | Match Score | Component | Data Type |\n")
        f.write("|------------|-------------------|-------------|-----------|------------|\n")
        
        for mapping in sorted(mappings, key=lambda x: x['match_score'], reverse=True):
            html_q = mapping['html_question'][:50] + '...' if len(mapping['html_question']) > 50 else mapping['html_question']
            f.write(f"| {html_q} | {mapping['spreadsheet_keyname'] or 'N/A'} | {mapping['match_score']} | {mapping['html_component']} | {mapping['spreadsheet_data_type']} |\n")
        
        f.write("\n## Unmatched HTML Fields\n\n")
        if unmatched_html:
            f.write("These fields appear in the HTML but could not be matched to spreadsheet questions:\n\n")
            for field in unmatched_html:
                f.write(f"- **Field {field['index']}** ({field['component']}): {field['question']}\n")
        else:
            f.write("All HTML fields were successfully matched.\n")
        
        f.write("\n## Unmatched Spreadsheet Questions\n\n")
        if unmatched_sp:
            f.write("These questions appear in the spreadsheet but not in the HTML:\n\n")
            for q in unmatched_sp[:20]:  # Limit to first 20
                if q['keyname']:
                    f.write(f"- **{q['keyname']}** (REF: {q['ref']}): {q['question']}\n")
            if len(unmatched_sp) > 20:
                f.write(f"\n... and {len(unmatched_sp) - 20} more\n")
        else:
            f.write("All spreadsheet questions were matched.\n")

def main():
    # Paths
    project_root = Path(__file__).parent.parent
    excel_path = project_root / "data/incoming/20250828_draft-master-spreadsheet.xlsx"
    html_fields_path = project_root / "data/generated/as-is-audit/extracted-fields.json"
    output_md = project_root / "Documents/01 Areas/as-is-analysis/field-mapping.md"
    output_json = project_root / "data/generated/as-is-audit/field-mappings.json"
    
    print("Loading spreadsheet data...")
    spreadsheet_questions = load_spreadsheet_data(excel_path)
    print(f"Loaded {len(spreadsheet_questions)} spreadsheet questions")
    
    print("Loading HTML fields...")
    html_fields = load_html_fields(html_fields_path)
    print(f"Loaded {len(html_fields)} HTML fields")
    
    print("Finding matches...")
    mappings, unmatched_html, unmatched_sp = find_best_matches(html_fields, spreadsheet_questions)
    
    print("Generating mapping report...")
    generate_mapping_report(mappings, unmatched_html, unmatched_sp, output_md)
    
    # Save JSON mappings
    with open(output_json, 'w') as f:
        json.dump({
            'mappings': mappings,
            'unmatched_html': unmatched_html,
            'unmatched_spreadsheet': unmatched_sp
        }, f, indent=2)
    
    print(f"\nMapping complete!")
    print(f"- Mapped fields: {len(mappings)}")
    print(f"- Unmatched HTML: {len(unmatched_html)}")
    print(f"- Unmatched spreadsheet: {len(unmatched_sp)}")
    print(f"- Report: {output_md}")
    print(f"- JSON: {output_json}")

if __name__ == "__main__":
    main()