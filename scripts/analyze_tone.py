#!/usr/bin/env python3
"""
Tone of Voice Analyzer for RBSI Question Sets

Analyzes schema questions against tone of voice guidelines and outputs
a CSV report for human review with suggested improvements.

Usage:
    python3 scripts/analyze_tone.py --schema path/to/schema.yaml --output analysis.csv
"""

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import yaml


class ToneAnalyzer:
    """Analyzes questions for tone of voice compliance"""
    
    # Common banking/legal jargon to flag
    JARGON_TERMS = {
        'entity', 'jurisdiction', 'domiciled', 'incorporated', 'subsidiary',
        'fiduciary', 'regulatory', 'compliance', 'statutory', 'prudential',
        'counterparty', 'custodian', 'beneficial owner', 'nominee',
        'intermediary', 'administrator', 'adviser', 'discretionary',
        'mandate', 'instrument', 'facility', 'covenant', 'indemnity'
    }
    
    # Simple word replacements
    SIMPLE_REPLACEMENTS = {
        'contact us': 'get in touch',
        'submit': 'send',
        'commence': 'start',
        'utilize': 'use',
        'prior to': 'before',
        'in order to': 'to',
        'in relation to': 'about',
        'in respect of': 'for',
        'pursuant to': 'under',
        'notwithstanding': 'despite',
        'mandatory': 'required',
        'supplementary': 'extra'
    }
    
    def __init__(self):
        self.issues = []
        
    def analyze_field(self, field: Dict) -> List[Dict]:
        """Analyze a single field for tone issues"""
        issues = []
        
        # Skip non-question fields
        if field.get('style') in ['statement', 'divider', 'button']:
            return issues
            
        label = field.get('label', '')
        key = field.get('key', '')
        source_ref = field.get('scriptId', '')
        
        if not label:
            return issues
            
        # Check length
        word_count = len(label.split())
        if word_count > 20:
            issues.append({
                'row_ref': source_ref,
                'field_key': key,
                'original': label,
                'issue_type': 'Too Long',
                'severity': 'High' if word_count > 30 else 'Medium',
                'details': f'{word_count} words',
                'suggestion': self._suggest_shorter(label)
            })
        
        # Check for jargon
        jargon_found = []
        label_lower = label.lower()
        for term in self.JARGON_TERMS:
            if term in label_lower:
                jargon_found.append(term)
        
        if jargon_found:
            issues.append({
                'row_ref': source_ref,
                'field_key': key,
                'original': label,
                'issue_type': 'Jargon',
                'severity': 'Medium',
                'details': f"Contains: {', '.join(jargon_found)}",
                'suggestion': self._suggest_simpler(label, jargon_found)
            })
        
        # Check for passive voice
        if self._is_passive(label):
            issues.append({
                'row_ref': source_ref,
                'field_key': key,
                'original': label,
                'issue_type': 'Passive Voice',
                'severity': 'Low',
                'details': 'Could be more direct',
                'suggestion': self._suggest_active(label)
            })
        
        # Check pronoun usage
        pronoun_issue = self._check_pronouns(label)
        if pronoun_issue:
            issues.append({
                'row_ref': source_ref,
                'field_key': key,
                'original': label,
                'issue_type': 'Pronoun Usage',
                'severity': 'Medium',
                'details': pronoun_issue,
                'suggestion': self._fix_pronouns(label)
            })
        
        # Check for complex sentences
        if ',' in label and len(label) > 100:
            issues.append({
                'row_ref': source_ref,
                'field_key': key,
                'original': label,
                'issue_type': 'Complex Sentence',
                'severity': 'Medium',
                'details': 'Multiple clauses',
                'suggestion': self._simplify_sentence(label)
            })
            
        return issues
    
    def _suggest_shorter(self, text: str) -> str:
        """Suggest a shorter version of the text"""
        # Remove unnecessary phrases
        shorter = text
        replacements = [
            ('in order to', 'to'),
            ('please provide', 'enter'),
            ('you are required to', ''),
            ('it is necessary to', ''),
            ('for the purpose of', 'for'),
            ('in the event that', 'if'),
            ('with regard to', 'about'),
            ('at this time', 'now')
        ]
        
        for old, new in replacements:
            shorter = re.sub(old, new, shorter, flags=re.IGNORECASE)
        
        # Trim and clean
        shorter = ' '.join(shorter.split())
        
        # If still too long, truncate smartly
        if len(shorter.split()) > 15:
            # Try to keep the core question
            if '?' in shorter:
                shorter = shorter.split('?')[0] + '?'
        
        return shorter
    
    def _suggest_simpler(self, text: str, jargon: List[str]) -> str:
        """Replace jargon with simpler terms"""
        simpler = text
        
        replacements = {
            'entity': 'company',
            'jurisdiction': 'country or region',
            'domiciled': 'based',
            'incorporated': 'registered',
            'subsidiary': 'owned company',
            'administrator': 'admin company',
            'beneficial owner': 'actual owner',
            'intermediary': 'middle company',
            'discretionary': 'optional',
            'mandatory': 'required'
        }
        
        for term in jargon:
            if term in replacements:
                simpler = re.sub(term, replacements[term], simpler, flags=re.IGNORECASE)
        
        return simpler
    
    def _is_passive(self, text: str) -> bool:
        """Check if text uses passive voice"""
        passive_indicators = [
            'is being', 'are being', 'was being', 'were being',
            'has been', 'have been', 'had been',
            'will be', 'would be', 'should be', 'may be', 'might be',
            'is required', 'are required', 'is needed', 'are needed'
        ]
        
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in passive_indicators)
    
    def _suggest_active(self, text: str) -> str:
        """Convert passive to active voice"""
        active = text
        
        replacements = [
            ('is required', 'you need'),
            ('are required', 'you need'),
            ('is needed', 'we need'),
            ('should be provided', 'please provide'),
            ('must be submitted', 'please send'),
            ('will be reviewed', "we'll review"),
            ('has been approved', 'we approved')
        ]
        
        for passive, active_form in replacements:
            active = re.sub(passive, active_form, active, flags=re.IGNORECASE)
        
        return active
    
    def _check_pronouns(self, text: str) -> str:
        """Check for pronoun consistency issues"""
        # Check for third-person references that should be second-person
        if any(word in text.lower() for word in ['the entity', 'the applicant', 'the customer']):
            return "Uses third-person instead of 'you/your'"
        
        # Check for missing pronouns in questions
        if text.endswith('?') and not any(word in text.lower() for word in ['you', 'your', 'i', 'my', 'we', 'our']):
            return "Question lacks personal pronouns"
        
        return ""
    
    def _fix_pronouns(self, text: str) -> str:
        """Fix pronoun usage"""
        fixed = text
        
        replacements = [
            ('the entity', 'your company'),
            ('the applicant', 'you'),
            ('the customer', 'you'),
            ('the fund', 'your fund'),
            ('the business', 'your business')
        ]
        
        for old, new in replacements:
            fixed = re.sub(old, new, fixed, flags=re.IGNORECASE)
        
        return fixed
    
    def _simplify_sentence(self, text: str) -> str:
        """Break complex sentences into simpler ones"""
        # If it's a question with multiple clauses, keep just the question
        if '?' in text:
            parts = text.split(',')
            if len(parts) > 2:
                # Find the part with the question mark
                for part in parts:
                    if '?' in part:
                        return part.strip()
        
        # Otherwise, take the first clause
        if ',' in text:
            return text.split(',')[0].strip()
        
        return text


def load_schema(path: Path) -> Dict:
    """Load and parse YAML schema"""
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def analyze_schema(schema_path: Path) -> List[Dict]:
    """Analyze all fields in a schema"""
    schema = load_schema(schema_path)
    analyzer = ToneAnalyzer()
    all_issues = []
    
    # Handle both formats (items for legacy, fields for KYCP)
    fields = schema.get('fields', schema.get('items', []))
    
    for field in fields:
        issues = analyzer.analyze_field(field)
        all_issues.extend(issues)
    
    return all_issues


def write_csv_report(issues: List[Dict], output_path: Path):
    """Write analysis results to CSV"""
    
    # Sort by severity
    severity_order = {'High': 0, 'Medium': 1, 'Low': 2}
    issues.sort(key=lambda x: (severity_order.get(x['severity'], 3), x['issue_type']))
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'row_ref', 'field_key', 'issue_type', 'severity', 
            'details', 'original', 'suggestion', 'human_decision', 'notes'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for issue in issues:
            # Add empty fields for human input
            issue['human_decision'] = ''  # Accept/Reject/Modified
            issue['notes'] = ''
            writer.writerow(issue)


def print_summary(issues: List[Dict]):
    """Print analysis summary to console"""
    print("\n=== Tone of Voice Analysis Summary ===\n")
    
    if not issues:
        print("✅ No tone issues found!")
        return
    
    # Count by type and severity
    by_type = {}
    by_severity = {'High': 0, 'Medium': 0, 'Low': 0}
    
    for issue in issues:
        issue_type = issue['issue_type']
        severity = issue['severity']
        
        by_type[issue_type] = by_type.get(issue_type, 0) + 1
        by_severity[severity] += 1
    
    print(f"Total issues found: {len(issues)}\n")
    
    print("By severity:")
    for sev in ['High', 'Medium', 'Low']:
        if by_severity[sev] > 0:
            print(f"  {sev}: {by_severity[sev]}")
    
    print("\nBy type:")
    for issue_type, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
        print(f"  {issue_type}: {count}")
    
    print(f"\n📊 Report saved to CSV for review and decisions")
    
    # Show a few examples
    print("\n=== Top Issues to Address ===\n")
    high_priority = [i for i in issues if i['severity'] == 'High'][:3]
    
    for issue in high_priority:
        print(f"Field: {issue['field_key'][:50]}...")
        print(f"Issue: {issue['issue_type']} ({issue['details']})")
        print(f"Original: {issue['original'][:100]}...")
        print(f"Suggested: {issue['suggestion'][:100]}...")
        print("-" * 50)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze schema questions for tone of voice compliance'
    )
    parser.add_argument(
        '--schema',
        required=True,
        type=Path,
        help='Path to schema YAML file'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('tone_analysis.csv'),
        help='Output CSV file (default: tone_analysis.csv)'
    )
    parser.add_argument(
        '--summary',
        action='store_true',
        help='Print summary to console'
    )
    
    args = parser.parse_args()
    
    if not args.schema.exists():
        print(f"Error: Schema file not found: {args.schema}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Analyzing: {args.schema}")
    
    # Run analysis
    issues = analyze_schema(args.schema)
    
    # Write CSV report
    write_csv_report(issues, args.output)
    print(f"Report written to: {args.output}")
    
    # Print summary if requested
    if args.summary or issues:
        print_summary(issues)


if __name__ == '__main__':
    main()