#!/usr/bin/env python3
"""
Importer for v2.2 Non-Lux LP workbook → KYCP schema YAML with Paul structural suggestions

Reads mapping from apps/prototype/data/mappings/non-lux-lp-2-2.json
Parses the XLSX via zipfile + XML (no external dependencies) and outputs:
  apps/prototype/data/schemas/non-lux-lp-2-2/schema-kycp.yaml
  apps/prototype/data/generated/non-lux-lp-2-2-copy-map.json

Features:
- Focuses on Paul's structural reorganization (sections + ordering)
- Uses original v1.1 content (AS-IS labels/help)
- Implements Paul's B-section hierarchy and question sequencing
- Creates structural change tracking with audit trail
- Handles unordered fields systematically
"""
from __future__ import annotations
import json, re, sys, yaml
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

APP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = APP_DIR / 'data'
INCOMING = DATA_DIR / 'incoming' / '20250916-master-spreadsheet-2.1.xlsx'
MAPPING = DATA_DIR / 'mappings' / 'non-lux-lp-2-2.json'
OUT_DIR = DATA_DIR / 'schemas' / 'non-lux-lp-2-2'
OUT_FILE = OUT_DIR / 'schema-kycp.yaml'
COPY_MAP_FILE = DATA_DIR / 'generated' / 'non-lux-lp-2-2-copy-map.json'

NS = {'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def warn(msg: str):
    print(f"[warn] {msg}", file=sys.stderr)

def info(msg: str):
    print(f"[info] {msg}")

def slugify(s: str) -> str:
    s = (s or '').strip().lower()
    # Replace & with 'and' to match frontend slugify behavior
    s = s.replace('&', ' and ')
    out = []
    for ch in s:
        if ch.isalnum():
            out.append(ch)
        elif ch in [' ', '-', '_']:
            out.append('-')
        else:
            out.append('-')
    slug = ''.join(out)
    while '--' in slug:
        slug = slug.replace('--', '-')
    return slug.strip('-') or 'item'

def parse_visibility(expr: str, op_map: dict[str, str]):
    """Parse a legacy visibility expression into KYCP visibility rules.
    
    Supports AND/OR with tolerance:
    - OR creates multiple rules (any rule can match) by returning multiple entries.
    - AND within a rule becomes multiple conditions with allConditionsMustMatch=True.
    - We avoid replacing AND/OR inside quoted values and only convert single '=' to '=='.
    """
    if not expr or not expr.strip():
        return []
    
    s = (expr or '').replace('\n', ' ')
    
    # Convert operators carefully: <> -> !=, single = -> == (but not == already)
    s = s.replace('<>', '!=')
    s = re.sub(r'(?<![=!])=(?!=)', '==', s)
    
    # Tokenize respecting quotes
    def split_outside_quotes(text: str, seps: list[str]):
        out = []
        i = 0
        buf = []
        in_sq = False
        in_dq = False
        while i < len(text):
            ch = text[i]
            if ch == "'" and not in_dq:
                in_sq = not in_sq
                buf.append(ch)
                i += 1
                continue
            if ch == '"' and not in_sq:
                in_dq = not in_dq
                buf.append(ch)
                i += 1
                continue
            if not in_sq and not in_dq:
                matched = False
                for sep in seps:
                    if text[i:].lower().startswith(sep.lower()):
                        out.append(''.join(buf).strip())
                        buf = []
                        i += len(sep)
                        matched = True
                        break
                if matched:
                    continue
            buf.append(ch)
            i += 1
        out.append(''.join(buf).strip())
        return [p for p in out if p]
    
    # Split on OR tokens first (outside quotes)
    or_groups = split_outside_quotes(s, ['||', ' OR '])
    
    rules = []
    bare_values: list[str] = []
    first_cond: dict | None = None
    for og in or_groups:
        # Split on AND tokens (outside quotes)
        and_parts = split_outside_quotes(og, ['&&', ' AND '])
        conditions = []
        found_op = False
        for p in and_parts:
            # find operator (== or !=)
            op = '==' if '==' in p else ('!=' if '!=' in p else None)
            if not op:
                continue
            found_op = True
            left, right = p.split(op, 1)
            src = (left or '').strip()
            val = (right or '').strip()
            # trim quotes if present
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            if not src:
                continue
            cond = {
                'sourceKey': src,
                'operator': 'eq' if op == '==' else 'neq',
                'value': val
            }
            if first_cond is None:
                first_cond = cond.copy()
            conditions.append(cond)
        if conditions:
            rules.append({
                'entity': 'entity',
                'targetKeys': [],
                'allConditionsMustMatch': True,
                'conditions': conditions
            })
        elif (og or '').strip():
            # Bare value segment (likely from "A == X OR Y OR Z")
            # record after trimming quotes
            val = og.strip()
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            bare_values.append(val)
    # If we have bare OR values and a single-condition base to replicate, expand into additional rules
    if bare_values and first_cond is not None:
        # Only safe if all existing rules are a single condition with the same source/op
        src = first_cond['sourceKey']
        op = first_cond['operator']
        base_rules_ok = all(len(r.get('conditions') or []) == 1 and r['conditions'][0]['sourceKey'] == src and r['conditions'][0]['operator'] == op for r in rules)
        if base_rules_ok:
            for bv in bare_values:
                rules.append({
                    'entity': 'entity',
                    'targetKeys': [],
                    'allConditionsMustMatch': True,
                    'conditions': [{ 'sourceKey': src, 'operator': op, 'value': bv }]
                })
    return rules

def load_mapping():
    with open(MAPPING, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_shared_strings(z: ZipFile):
    strings = []
    try:
        with z.open('xl/sharedStrings.xml') as f:
            root = ET.parse(f).getroot()
            for si in root.findall('.//a:si', NS):
                t = si.find('.//a:t', NS)
                if t is not None and t.text:
                    strings.append(t.text)
    except KeyError:
        pass
    return strings

def get_cell_value(cell_elem, shared_strings):
    v_elem = cell_elem.find('a:v', NS)
    if v_elem is None:
        return None
    
    value = v_elem.text
    cell_type = cell_elem.get('t', '')
    
    if cell_type == 's' and value and value.isdigit():
        idx = int(value)
        if 0 <= idx < len(shared_strings):
            return shared_strings[idx]
    
    return value

def get_column_letter(col_num):
    result = ""
    while col_num > 0:
        col_num -= 1
        result = chr(ord('A') + col_num % 26) + result
        col_num //= 26
    return result

def sheet_index_by_name(z: ZipFile, name: str) -> int:
    xml = z.read('xl/workbook.xml')
    wb = ET.fromstring(xml)
    sheets = wb.find('a:sheets', NS)
    for i, sh in enumerate(sheets.findall('a:sheet', NS), start=1):
        if (sh.get('name') or '').strip() == name:
            return i
    raise KeyError(f"Sheet not found: {name}")

def read_sheet_rows(z: ZipFile, sheet_idx: int, sst: list[str]):
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

def collect_lookup_values(z: ZipFile, mapping):
    """Read the Lookup Values sheet using its own header detection.
    
    Looks for a row that contains both 'LOOKUP TYPE' and 'LOOKUP VALUE' and uses
    their positions as column indices for the rest of the sheet.
    """
    sst = read_shared_strings(z)
    idx = sheet_index_by_name(z, mapping['lookups_sheet'])
    rows = read_sheet_rows(z, idx, sst)  # [(row_num, [(ref, text), ...]), ...]
    
    header_type = (mapping['lookups_columns']['type'] or 'LOOKUP TYPE').strip().upper()
    header_value = (mapping['lookups_columns']['value'] or 'LOOKUP VALUE').strip().upper()
    
    type_i = value_i = None
    header_found = False
    # find header row
    for _, cells in rows[:50]:
        vals = [txt for _, txt in cells]
        ups = [v.strip().upper() for v in vals]
        if header_type in ups and header_value in ups:
            type_i = ups.index(header_type)
            value_i = ups.index(header_value)
            header_found = True
            break
    if not header_found:
        return {}
    
    values: dict[str, list[dict]] = {}
    # iterate all rows after the detected header
    started = False
    for _, cells in rows:
        vals = [txt for _, txt in cells]
        ups = [v.strip().upper() for v in vals]
        if not started:
            if type_i is not None and value_i is not None and type_i < len(ups) and value_i < len(ups):
                if ups[type_i] == header_type and ups[value_i] == header_value:
                    started = True
            continue
        # gather type and value
        if type_i is None or value_i is None:
            continue
        if type_i >= len(vals) or value_i >= len(vals):
            continue
        t = (vals[type_i] or '').strip()
        v = (vals[value_i] or '').strip()
        if not t or not v:
            continue
        # Ignore guidance rows like 'Refer to separate ... list sheet'
        if v.lower().startswith('refer to separate'):
            continue
        bucket = values.setdefault(t, [])
        # dedupe
        if not any(o['value'] == v for o in bucket):
            bucket.append({'value': v, 'label': v})
    return values

def parse_worksheet(z: ZipFile, sheet_name: str, mapping: dict):
    shared_strings = read_shared_strings(z)
    
    # Find sheet index
    with z.open('xl/workbook.xml') as f:
        workbook = ET.parse(f).getroot()
        sheets = {}
        for i, sheet in enumerate(workbook.findall('.//a:sheet', NS), 1):
            name = sheet.get('name', '')
            sheets[name] = i
    
    if sheet_name not in sheets:
        raise ValueError(f"Sheet '{sheet_name}' not found")
    
    sheet_idx = sheets[sheet_name]
    sheet_file = f'xl/worksheets/sheet{sheet_idx}.xml'
    
    with z.open(sheet_file) as f:
        worksheet = ET.parse(f).getroot()
        
        # Parse rows
        rows = {}
        for row in worksheet.findall('.//a:row', NS):
            row_num = int(row.get('r', 0))
            row_data = {}
            
            for cell in row.findall('.//a:c', NS):
                cell_ref = cell.get('r', '')
                if cell_ref:
                    col_letter = ''.join(c for c in cell_ref if c.isalpha())
                    value = get_cell_value(cell, shared_strings)
                    if value:
                        row_data[col_letter] = str(value).strip()
            
            if row_data:
                rows[row_num] = row_data
        
        return rows

def create_copy_mapping(rows: dict, mapping: dict, copy_map: list):
    """Create copy mapping with change tracking"""
    header_row_num = mapping.get('header_row', 2)
    if header_row_num not in rows:
        warn(f"Header row {header_row_num} not found")
        return
    
    headers = rows[header_row_num]
    
    # Get column mappings
    cols = mapping['columns']
    
    # Find column letters for key fields
    col_letters = {}
    for key, col_name in cols.items():
        for letter, header in headers.items():
            if header == col_name:
                col_letters[key] = letter
                break
    
    info(f"Column mappings: {len(col_letters)} found")
    
    # Process data rows
    for row_num, row_data in rows.items():
        if row_num <= header_row_num:
            continue  # Skip header row
            
        # Extract field data
        field_data = {}
        for key, letter in col_letters.items():
            if letter in row_data:
                field_data[key] = row_data[letter]
        
        if not field_data.get('id'):  # Skip rows without KEYNAME
            continue
            
        # Create copy map entry
        original_label = field_data.get('label', '')
        original_help = field_data.get('help', '')
        nile_label = field_data.get('nile_suggested_field_name', '')
        nile_help = field_data.get('nile_suggested_description', '')
        nile_section = field_data.get('nile_suggested_section', '')
        
        entry = {
            "row": row_num,
            "field_key": field_data.get('id'),
            "original_label": original_label,
            "original_help": original_help,
            "nile_suggested_label": nile_label if nile_label else original_label,
            "nile_suggested_help": nile_help if nile_help else original_help,
            "nile_suggested_section": nile_section,
            "paul_section_suggestion": field_data.get('paul_section_suggestion', ''),
            "paul_question_order": field_data.get('paul_question_order', ''),
            "action": field_data.get('action', ''),
            "reworded": field_data.get('reworded', ''),
            "has_label_change": bool(nile_label and nile_label != original_label),
            "has_help_change": bool(nile_help and nile_help != original_help),
            "has_section_suggestion": bool(nile_section),
            "change_source": "Nile team suggestions",
            "change_timestamp": "2025-09-16"
        }
        
        copy_map.append(entry)

def process_field(field_data: dict, mapping: dict, lookups: dict) -> dict:
    """Process a single field into schema format"""
    field = {
        'key': field_data.get('id', ''),
        'entity': 'entity',
        'style': 'field'
    }
    
    # Extract original content and Paul's structural suggestions
    original_label = field_data.get('label', '').strip()
    original_help = field_data.get('help', '').strip()
    paul_section = field_data.get('paul_section_suggestion', '').strip()
    paul_order = field_data.get('paul_question_order', '').strip()
    
    # Always use original as the main label/help (AS-IS approach for v2.2)
    field['label'] = original_label
    if original_help:
        field['help'] = original_help
    
    # Add original field for explain visibility
    field['original'] = {
        'label': original_label,
        'help': original_help if original_help else None
    }
    
    # Parse Paul's ordering and section data
    paul_order_number = None
    paul_order_section = None
    
    if paul_order and paul_order != "0.0":
        # Parse format like "3 - B2" or "192 - B11.1"
        match = re.match(r'^(\d+(?:\.\d+)?)\s*-\s*(.+?)(?:\s*\(.*\))?$', paul_order)
        if match:
            paul_order_number = float(match.group(1))
            paul_order_section = match.group(2).strip()
    
    # Apply ordering fixes for backwards dependencies
    field_key = field_data.get('id', '')
    if field_key == 'GENpepinvestors':
        # Fix B9 internal ordering: GENpepinvestors should come before GENdetailPEPconnection
        paul_order_number = 154.0  # Original was 155
    elif field_key == 'GENdetailPEPconnection':
        # Fix B9 internal ordering: GENdetailPEPconnection should come after GENpepinvestors
        paul_order_number = 155.0  # Original was 154
    
    # Track Paul's structural changes if present
    has_section_change = bool(paul_section)
    has_order_change = bool(paul_order_number is not None)
    
    if has_section_change or has_order_change:
        field['future'] = {
            'proposedSection': paul_section if has_section_change else None,
            'proposedOrder': paul_order_number if has_order_change else None,
            'proposedOrderText': paul_order if paul_order and paul_order != "0.0" else None,
            'changeSource': 'Paul structural suggestions',
            'rationale': 'Optimized information architecture and field sequencing'
        }
    
    # Store Paul's order for schema generation
    if paul_order_number is not None:
        field['_paul_order'] = paul_order_number
    
    # Data type normalization
    data_type = field_data.get('data_type', '').strip()
    norm_data_type = mapping['normalization']['data_type'].get(data_type, 'string')
    
    if norm_data_type == 'lookup':
        field['type'] = 'lookup'
        # Handle lookup options (prioritize dynamic lookups over fallbacks)
        lookup_type = field_data.get('lookup_type', '')
        if lookup_type in lookups:
            # Use dynamic lookups from Lookup Values sheet
            field['options'] = lookups[lookup_type]
        elif lookup_type in mapping.get('fallback_lookups', {}):
            # Use fallback lookups from mapping
            field['options'] = [
                {'value': opt, 'label': opt} 
                for opt in mapping['fallback_lookups'][lookup_type]
            ]
        else:
            # No options found - this will create a broken field
            warn(f"No lookup options found for type: {lookup_type}")
            field['options'] = []
    elif norm_data_type == 'complex':
        field['type'] = 'complex'
        field['children'] = []  # Will be populated later
    else:
        field['type'] = norm_data_type
    
    # Validation
    field['validation'] = {}
    if field_data.get('mandatory', '').lower() in ['y', 'yes', 'true']:
        field['validation']['required'] = True
    
    # Regex
    regex = field_data.get('regex', '').strip()
    if regex:
        field['validation']['regex'] = regex
    
    # Section assignment using restructured flow mappings
    field_key = field_data.get('id', '')
    field_section_mappings = mapping.get('field_section_mappings', {})
    paul_sections = mapping.get('paul_sections', {})
    
    if field_key in field_section_mappings:
        # Use explicit field mapping for restructured flow - expand to full section name
        section_code = field_section_mappings[field_key]
        section_title = paul_sections.get(section_code, section_code)
        field['_section'] = f"{section_code} - {section_title}" if section_title != section_code else section_code
    elif paul_section:
        # Use Paul's section suggestion directly - these are clean B-prefix sections
        field['_section'] = paul_section
    elif paul_order_section:
        # Use section from Paul's order format as fallback - expand to full name if possible
        section_title = paul_sections.get(paul_order_section, paul_order_section)
        field['_section'] = f"{paul_order_section} - {section_title}" if section_title != paul_order_section else paul_order_section
    else:
        # Fallback to v1.1 label-based section mapping for unordered fields
        label_lower = field['label'].lower()
        sections = mapping.get('sections_by_label', {})
        for pattern, section in sections.items():
            if pattern in label_lower:
                field['_section'] = section
                break
        else:
            # Default for fields without Paul guidance
            field['_section'] = mapping['defaults'].get('section', 'General')
    
    # Visibility conditions (using proper parser)
    visibility = field_data.get('visibility', '').strip()
    if visibility:
        field['visibility'] = parse_visibility(visibility, mapping['normalization']['operators'])
    
    # Metadata for change tracking (Paul structural changes)
    field['_metadata'] = {
        'source_row': field_data.get('_row_num'),
        'has_paul_structural_changes': bool(has_section_change or has_order_change),
        'paul_section': paul_section if paul_section else None,
        'paul_order': paul_order if paul_order and paul_order != "0.0" else None
    }
    
    return field

def sort_fields_by_paul_order(fields: list) -> list:
    """Sort fields by Paul's question order within sections, prioritizing unconditional fields"""
    def get_sort_key(field):
        paul_order = field.get('_paul_order')
        section = field.get('_section', 'ZZZ')  # Default to end
        has_visibility = bool(field.get('visibility'))  # True if field has conditional logic
        
        # Within each section, prioritize:
        # 1. Unconditional fields with Paul order
        # 2. Unconditional fields without Paul order  
        # 3. Conditional fields with Paul order
        # 4. Conditional fields without Paul order
        
        if paul_order is not None:
            if not has_visibility:
                # Unconditional fields with Paul order come first
                return (section, 0, paul_order)
            else:
                # Conditional fields with Paul order come after unconditional
                return (section, 2, paul_order)
        else:
            if not has_visibility:
                # Unconditional fields without Paul order 
                return (section, 1, field.get('key', ''))
            else:
                # Conditional fields without Paul order go to end
                return (section, 3, field.get('key', ''))
    
    return sorted(fields, key=get_sort_key)

def generate_schema(rows: dict, mapping: dict, lookups: dict) -> dict:
    """Generate the complete schema"""
    header_row_num = mapping.get('header_row', 2)
    headers = rows[header_row_num]
    
    # Get column mappings
    cols = mapping['columns']
    col_letters = {}
    for key, col_name in cols.items():
        for letter, header in headers.items():
            if header == col_name:
                col_letters[key] = letter
                break
    
    # Process fields
    fields = []
    copy_map = []
    
    for row_num, row_data in rows.items():
        if row_num <= header_row_num:
            continue
            
        # Extract field data
        field_data = {'_row_num': row_num}
        for key, letter in col_letters.items():
            if letter in row_data:
                field_data[key] = row_data[letter]
        
        if not field_data.get('id'):
            continue
            
        # Comprehensive exclusion logic (adapted from v1.1)
        yes_vals = mapping.get('normalization', {}).get('yes_values', ['Y', 'Yes', 'YES', 'a', 'A'])
        label = field_data.get('label', '').strip()
        action = (field_data.get('action', '') or '').lower()
        internal = (field_data.get('internal', '') or '').strip()
        system = (field_data.get('system', '') or '').strip()
        
        # Apply label overrides
        field_id = field_data.get('id', '')
        label_overrides = mapping.get('label_overrides', {})
        if field_id in label_overrides:
            label = label_overrides[field_id]
        
        # 1. Skip fields with internal action patterns
        exclude_config = mapping.get('exclude', {})
        action_patterns = exclude_config.get('action_contains', [])
        if any(p.lower() in action for p in action_patterns):
            continue
            
        # 2. Skip fields marked as internal
        if internal in yes_vals:
            continue
            
        # 3. Skip fields marked as system  
        if system in yes_vals:
            continue
            
        # 4. Skip fields with internal label patterns
        label_patterns = exclude_config.get('label_contains', [])
        if any(p.lower() in label.lower() for p in label_patterns):
            continue
            
        # Process field
        field = process_field(field_data, mapping, lookups)
        fields.append(field)
    
    # Sort fields by Paul's ordering within sections
    fields = sort_fields_by_paul_order(fields)
    
    # Create copy mapping
    create_copy_mapping(rows, mapping, copy_map)
    
    # Canonicalize condition values to match controller options using alias map
    value_aliases = mapping.get('value_aliases', {})
    alias_to_canon = {}
    for canon, syns in value_aliases.items():
        c = (canon or '').strip().lower()
        alias_to_canon[c] = c
        for s in (syns or []):
            alias_to_canon[(s or '').strip().lower()] = c
    
    field_by_key = {f['key']: f for f in fields}
    
    for f in fields:
        vis = f.get('visibility') or []
        changed = False
        for rule in vis:
            for c in (rule.get('conditions') or []):
                # Only canonicalize for eq/neq against lookup/enum controllers
                left_key = c.get('sourceKey')
                ctrl = field_by_key.get(left_key)
                if not ctrl:
                    continue
                if ctrl.get('type') in ['lookup', 'enum']:
                    orig = str(c.get('value') or '')
                    canon = alias_to_canon.get(orig.lower())
                    if canon and canon != orig.lower():
                        # Find matching option value in controller
                        options = ctrl.get('options') or []
                        for opt in options:
                            if (opt.get('value') or '').lower() == canon:
                                c['value'] = opt['value']
                                changed = True
                                break
        if changed:
            f['visibility'] = vis
    
    # Generate schema
    schema = {
        'key': 'non-lux-lp-2-2',
        'name': 'Non-Lux LP — v2.2 (Paul Structure)',
        'version': '0.1.0',
        'entity': 'entity',
        'fields': fields
    }
    
    # Group fields by section for accordion layout (with deduplication)
    sections = {}
    for field in fields:
        section = field.get('_section', 'General')
        # Normalize section name to prevent duplicates
        section_normalized = section.title()  # Consistent Title Case
        if section_normalized not in sections:
            sections[section_normalized] = []
        sections[section_normalized].append(field['key'])
    
    # Add accordion configuration with Paul's section ordering and nested structure
    if len(sections) > 1:
        schema['accordions'] = []
        
        # Get Paul's canonical section order from mapping
        paul_sections = mapping.get('paul_sections', {})
        paul_order = list(paul_sections.keys())  # ['B1', 'B2', 'B3', ...]
        
        # Group sections into hierarchical structure
        def parse_section_hierarchy(sections_dict):
            hierarchical = {}
            processed_subsections = set()
            
            # First pass: handle subsections and create parent containers
            for section_name, field_keys in sections_dict.items():
                section_code = section_name.split(' - ')[0] if ' - ' in section_name else section_name
                
                if '.' in section_code:
                    # This is a subsection (e.g., "B4.1", "B11.2")
                    parent_code = section_code.split('.')[0]  # "B4", "B11"
                    processed_subsections.add(section_name)
                    
                    # Create consistent parent name from restructured sections
                    parent_title = paul_sections.get(parent_code, 'Unknown')
                    
                    parent_name = f"{parent_code} - {parent_title}"
                    
                    # Initialize parent if not exists
                    if parent_name not in hierarchical:
                        hierarchical[parent_name] = {
                            'fields': [],
                            'subsections': []
                        }
                    
                    # Create clean subsection title
                    if ' - ' in section_name:
                        parts = section_name.split(' - ')
                        if len(parts) >= 3:
                            subsection_title = parts[2]
                        else:
                            subsection_title = parts[1] if len(parts) > 1 else section_name
                    else:
                        subsection_title = section_name
                    
                    hierarchical[parent_name]['subsections'].append({
                        'key': slugify(section_name),
                        'title': subsection_title,
                        'fields': field_keys
                    })
            
            # Second pass: handle top-level sections (but avoid duplicates with created parents)
            for section_name, field_keys in sections_dict.items():
                if section_name in processed_subsections:
                    continue
                    
                section_code = section_name.split(' - ')[0] if ' - ' in section_name else section_name
                
                if '.' not in section_code:
                    # Check if this matches a parent we already created
                    parent_match = None
                    for existing_parent in hierarchical.keys():
                        existing_code = existing_parent.split(' - ')[0]
                        if existing_code == section_code:
                            parent_match = existing_parent
                            break
                    
                    if parent_match:
                        # Add fields to existing parent
                        hierarchical[parent_match]['fields'].extend(field_keys)
                    else:
                        # Create new top-level section
                        hierarchical[section_name] = {
                            'fields': field_keys,
                            'subsections': []
                        }
            
            return hierarchical
        
        # Sort sections by Paul's hierarchy
        def get_section_sort_key(section_name):
            # Extract the section code (e.g., "B1" from "B1 - Pre-App Qs")
            section_code = section_name.split(' - ')[0] if ' - ' in section_name else section_name
            parent_code = section_code.split('.')[0] if '.' in section_code else section_code
            
            # Find position in Paul's canonical order
            try:
                return paul_order.index(parent_code)
            except ValueError:
                # Section not in Paul's list - place at end
                return 999
        
        # Parse hierarchical structure
        hierarchical_sections = parse_section_hierarchy(sections)
        
        # Sort and create accordions
        sorted_sections = sorted(hierarchical_sections.items(), key=lambda x: get_section_sort_key(x[0]))
        
        # Get section title priority for restructured sections
        section_title_priority = mapping.get('section_title_priority', {})
        
        for section_name, section_data in sorted_sections:
            # Determine final section title, prioritizing restructured sections
            final_section_name = section_name
            section_code = section_name.split(' - ')[0] if ' - ' in section_name else section_name
            
            # Check if this is a restructured section that should get priority title
            priority_field = section_title_priority.get(section_code)
            if priority_field and priority_field in [f['key'] for f in fields if f.get('_section') == section_name]:
                # Use the restructured section title from paul_sections
                restructured_title = paul_sections.get(section_code)
                if restructured_title:
                    final_section_name = f"{section_code} - {restructured_title}"
            
            accordion_item = {
                'key': slugify(final_section_name),
                'title': final_section_name,
                'fields': section_data['fields']
            }
            
            # Add subsections if they exist
            if section_data['subsections']:
                accordion_item['subsections'] = section_data['subsections']
            
            schema['accordions'].append(accordion_item)
    
    return schema, copy_map

def main():
    info("Starting v2.2 Non-Lux LP import with Paul's structural suggestions")
    
    if not INCOMING.exists():
        print(f"ERROR: Input file not found: {INCOMING}", file=sys.stderr)
        return 1
    
    if not MAPPING.exists():
        print(f"ERROR: Mapping file not found: {MAPPING}", file=sys.stderr)
        return 1
    
    # Load mapping
    mapping = load_mapping()
    info(f"Loaded mapping for sheet: {mapping['sheet']}")
    
    # Parse Excel file
    with ZipFile(INCOMING) as z:
        rows = parse_worksheet(z, mapping['sheet'], mapping)
        info(f"Parsed {len(rows)} rows")
        
        # Collect lookup values from Lookup Values sheet
        lookups = collect_lookup_values(z, mapping)
        info(f"Collected {len(lookups)} lookup types with {sum(len(vals) for vals in lookups.values())} total values")
    
    # Generate schema and copy map
    schema, copy_map = generate_schema(rows, mapping, lookups)
    
    info(f"Generated schema with {len(schema['fields'])} fields")
    info(f"Generated copy map with {len(copy_map)} entries")
    
    # Ensure output directories exist
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    COPY_MAP_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Write schema YAML
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(schema, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    info(f"Schema written to: {OUT_FILE}")
    
    # Write copy map JSON
    with open(COPY_MAP_FILE, 'w', encoding='utf-8') as f:
        json.dump(copy_map, f, indent=2, ensure_ascii=False)
    
    info(f"Copy map written to: {COPY_MAP_FILE}")
    
    # Summary statistics
    paul_structural_changes = sum(1 for entry in copy_map if entry.get('has_paul_structural_changes', False))
    paul_sections = sum(1 for entry in copy_map if entry.get('paul_section'))
    paul_orders = sum(1 for entry in copy_map if entry.get('paul_order'))
    
    info(f"\n=== SUMMARY ===")
    info(f"Total fields: {len(schema['fields'])}")
    info(f"Paul structural changes: {paul_structural_changes}")
    info(f"Paul section assignments: {paul_sections}")
    info(f"Paul ordering assignments: {paul_orders}")
    
    if 'accordions' in schema:
        info(f"Accordion sections: {len(schema['accordions'])}")
        for accordion in schema['accordions']:
            info(f"  - {accordion['title']}: {len(accordion['fields'])} fields")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())