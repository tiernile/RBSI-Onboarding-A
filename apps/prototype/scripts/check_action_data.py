#!/usr/bin/env python3
"""
Quick script to check action data in the original spreadsheet
"""

import sys
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import json

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
INCOMING = PROJECT_DIR / "data/incoming/20250911_master_non-lux.xlsx"
MAPPING_FILE = PROJECT_DIR / "data/mappings/non-lux-lp-2-2.json"

# Excel XML namespaces
NS = {
    'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
}

def read_shared_strings(z: ZipFile) -> list[str]:
    """Read shared strings table from Excel file"""
    try:
        xml = z.read('xl/sharedStrings.xml')
        root = ET.fromstring(xml)
        strings = []
        for si in root.findall('a:si', NS):
            text = ""
            for t in si.findall('.//a:t', NS):
                if t.text:
                    text += t.text
            strings.append(text)
        return strings
    except Exception:
        return []

def sheet_index_by_name(z: ZipFile, name: str) -> int:
    """Find sheet index by name"""
    xml = z.read('xl/workbook.xml')
    wb = ET.fromstring(xml)
    sheets = wb.find('a:sheets', NS)
    for i, sh in enumerate(sheets.findall('a:sheet', NS), start=1):
        if (sh.get('name') or '').strip() == name:
            return i
    raise KeyError(f"Sheet not found: {name}")

def read_sheet_rows(z: ZipFile, sheet_idx: int, sst: list[str]):
    """Read all rows from a sheet"""
    xml = z.read(f'xl/worksheets/sheet{sheet_idx}.xml')
    s = ET.fromstring(xml)
    rows = []
    for r in s.findall('.//a:row', NS):
        row_num = int(r.get('r')) if r.get('r') else None
        cells = []
        for c in r.findall('a:c', NS):
            ref = c.get('r')
            t = c.get('t')
            v = c.find('a:v', NS)
            text = ''
            if t == 's' and v is not None and v.text is not None:
                try:
                    idx = int(v.text)
                    text = sst[idx] if idx < len(sst) else ''
                except Exception:
                    text = ''
            elif t == 'inlineStr':
                is_e = c.find('a:is', NS)
                if is_e is not None:
                    text = ''.join((t.text or '') for t in is_e.findall('.//a:t', NS))
            elif v is not None and v.text is not None:
                text = v.text
            cells.append((ref, text))
        rows.append((row_num, cells))
    return rows

def get_column_letter(col_num):
    """Convert column number to letter"""
    result = ""
    while col_num > 0:
        col_num -= 1
        result = chr(ord('A') + col_num % 26) + result
        col_num //= 26
    return result

def main():
    print("Checking action data in original spreadsheet...")
    
    # Load mapping
    with open(MAPPING_FILE) as f:
        mapping = json.load(f)
    
    # Parse Excel
    with ZipFile(INCOMING) as z:
        sst = read_shared_strings(z)
        sheet_idx = sheet_index_by_name(z, mapping['sheet'])
        rows = read_sheet_rows(z, sheet_idx, sst)
    
    # Convert rows to dict by row number
    rows_dict = {}
    for row_num, cells in rows:
        if row_num:
            row_data = {}
            for ref, text in cells:
                # Extract column letter from reference like "A1", "B2"
                col_letter = ''.join(c for c in ref if c.isalpha())
                row_data[col_letter] = text
            rows_dict[row_num] = row_data
    
    # Find header row and action column
    header_row_num = mapping.get('header_row', 2)
    headers = rows_dict.get(header_row_num, {})
    
    # Find Action column
    action_col = None
    for col_letter, header in headers.items():
        if header == "Action":
            action_col = col_letter
            break
    
    if not action_col:
        print("ERROR: Action column not found in headers")
        return 1
    
    print(f"Found Action column at: {action_col}")
    print(f"Header row: {header_row_num}")
    
    # Find KEYNAME column for field identification
    keyname_col = None
    for col_letter, header in headers.items():
        if header == "KEYNAME":
            keyname_col = col_letter
            break
    
    # Look for reworded column
    reworded_col = None
    for col_letter, header in headers.items():
        if "reword" in header.lower():
            reworded_col = col_letter
            print(f"Found reworded column at: {col_letter} ('{header}')")
            break
    
    # Show all column headers for reference
    print(f"\nAll column headers:")
    for col_letter, header in sorted(headers.items()):
        if header.strip():
            print(f"  {col_letter}: {header}")
    
    # Extract action data
    actions_found = []
    pre_app_found = False
    
    for row_num, row_data in rows_dict.items():
        if row_num <= header_row_num:
            continue
            
        keyname = row_data.get(keyname_col, '').strip()
        action = row_data.get(action_col, '').strip()
        
        if keyname and action:
            actions_found.append({
                'row': row_num,
                'keyname': keyname,
                'action': action
            })
            
            # Check for the specific field mentioned
            if keyname == "GENIndicativeAppetiteQuestions":
                pre_app_found = True
                print(f"\n*** FOUND Pre-Application Questions field ***")
                print(f"Row: {row_num}")
                print(f"KEYNAME: {keyname}")
                print(f"Action: '{action}'")
                
                # Also check other columns for context
                field_name_col = None
                for col, header in headers.items():
                    if header == "FIELD NAME":
                        field_name_col = col
                        break
                
                if field_name_col:
                    field_name = row_data.get(field_name_col, '')
                    print(f"Field Name: {field_name}")
    
    print(f"\nTotal actions found: {len(actions_found)}")
    
    # Look for "mandatory wholesale depositor" mentions
    wholesale_actions = []
    for action_data in actions_found:
        if "wholesale depositor" in action_data['action'].lower():
            wholesale_actions.append(action_data)
    
    if wholesale_actions:
        print(f"\nFound {len(wholesale_actions)} wholesale depositor related actions:")
        for action_data in wholesale_actions:
            print(f"  Row {action_data['row']}: {action_data['keyname']} -> {action_data['action']}")
    
    # Search for "replace" actions
    replace_actions = []
    for action_data in actions_found:
        if "replace" in action_data['action'].lower():
            replace_actions.append(action_data)
    
    if replace_actions:
        print(f"\nFound {len(replace_actions)} 'replace' actions:")
        for action_data in replace_actions:
            print(f"  Row {action_data['row']}: {action_data['keyname']} -> {action_data['action']}")
    
    # Search for "mandatory" mentions  
    mandatory_actions = []
    for action_data in actions_found:
        if "mandatory" in action_data['action'].lower():
            mandatory_actions.append(action_data)
    
    if mandatory_actions:
        print(f"\nFound {len(mandatory_actions)} 'mandatory' actions:")
        for action_data in mandatory_actions:
            print(f"  Row {action_data['row']}: {action_data['keyname']} -> {action_data['action']}")
    
    # Check reworded column data
    if reworded_col:
        print(f"\nChecking reworded column data...")
        reworded_data = []
        for row_num, row_data in rows_dict.items():
            if row_num <= header_row_num:
                continue
            keyname = row_data.get(keyname_col, '').strip()
            reworded = row_data.get(reworded_col, '').strip()
            if keyname and reworded:
                reworded_data.append({
                    'row': row_num,
                    'keyname': keyname,
                    'reworded': reworded
                })
        
        print(f"Found {len(reworded_data)} fields with reworded content")
        
        # Look for the specific field
        for data in reworded_data:
            if data['keyname'] == "GENIndicativeAppetiteQuestions":
                print(f"\n*** FOUND GENIndicativeAppetiteQuestions reworded content ***")
                print(f"Row: {data['row']}")
                print(f"KEYNAME: {data['keyname']}")
                print(f"Reworded: '{data['reworded']}'")
                break
        
        # Look for wholesale depositor mentions in reworded
        wholesale_reworded = []
        for data in reworded_data:
            if "wholesale depositor" in data['reworded'].lower():
                wholesale_reworded.append(data)
        
        if wholesale_reworded:
            print(f"\nFound {len(wholesale_reworded)} reworded entries mentioning wholesale depositor:")
            for data in wholesale_reworded:
                print(f"  Row {data['row']}: {data['keyname']} -> {data['reworded']}")
        
        # Look for mandatory mentions in reworded
        mandatory_reworded = []
        for data in reworded_data:
            if "mandatory" in data['reworded'].lower():
                mandatory_reworded.append(data)
        
        if mandatory_reworded:
            print(f"\nFound {len(mandatory_reworded)} reworded entries mentioning mandatory:")
            for data in mandatory_reworded:
                print(f"  Row {data['row']}: {data['keyname']} -> {data['reworded']}")
    
    # Also check if GENIndicativeAppetiteQuestions exists at all (even without action)
    print(f"\nChecking for GENIndicativeAppetiteQuestions in all rows...")
    gen_field_found = False
    for row_num, row_data in rows_dict.items():
        if row_num <= header_row_num:
            continue
        keyname = row_data.get(keyname_col, '').strip()
        if keyname == "GENIndicativeAppetiteQuestions":
            gen_field_found = True
            action = row_data.get(action_col, '').strip()
            reworded = row_data.get(reworded_col, '').strip() if reworded_col else 'N/A'
            print(f"  Row {row_num}: KEYNAME={keyname}")
            print(f"    Action='{action}' (length: {len(action)})")
            print(f"    Reworded='{reworded}' (length: {len(reworded)})")
            break
    
    if not gen_field_found:
        print(f"  GENIndicativeAppetiteQuestions not found in any row")
    
    if not pre_app_found:
        print(f"\nWARNING: GENIndicativeAppetiteQuestions field not found in action data")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())