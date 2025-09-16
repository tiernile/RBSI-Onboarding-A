#!/usr/bin/env python3
"""
Importer for 20250911 Non-Lux LP workbook → KYCP schema YAML

Reads mapping from apps/prototype/data/mappings/non-lux-1.1.json
Parses the XLSX via zipfile + XML (no external dependencies) and outputs:
  apps/prototype/data/schemas/non-lux-1.1/schema-kycp.yaml

Dry-run summary is printed to stdout.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

APP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = APP_DIR / 'data'
INCOMING = DATA_DIR / 'incoming' / '20250911_master_non-lux.xlsx'
MAPPING = DATA_DIR / 'mappings' / 'non-lux-1.1.json'
OUT_DIR = DATA_DIR / 'schemas' / 'non-lux-1-1'
OUT_FILE = OUT_DIR / 'schema-kycp.yaml'

NS = {'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def warn(msg: str):
    print(f"[warn] {msg}", file=sys.stderr)

def slugify(s: str) -> str:
    s = (s or '').strip().lower()
    out = []
    for ch in s:
        if ch.isalnum():
            out.append(ch)
        elif ch in [' ', '-', '_']:
            out.append('-')
        else:
            # skip other punctuation/symbols
            out.append('-')
    # collapse dashes
    slug = ''.join(out)
    while '--' in slug:
        slug = slug.replace('--', '-')
    return slug.strip('-') or 'item'

def load_mapping():
    with open(MAPPING, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_shared_strings(z: ZipFile):
    try:
        xml = z.read('xl/sharedStrings.xml')
    except KeyError:
        return []
    sst = ET.fromstring(xml)
    texts = []
    for si in sst.findall('a:si', NS):
        parts = [t.text or '' for t in si.findall('.//a:t', NS)]
        texts.append(''.join(parts))
    return texts

def sheet_index_by_name(z: ZipFile, name: str) -> int:
    xml = z.read('xl/workbook.xml')
    wb = ET.fromstring(xml)
    sheets = wb.find('a:sheets', NS)
    idx = 0
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

def build_table(rows):
    # Find header row by presence of KEYNAME and capture column letters
    header_idx = None
    header_cells = []  # list of (colLetter, headerText)
    def col_letter(ref: str) -> str:
        return ''.join(ch for ch in (ref or '') if ch.isalpha())
    for i, (_, cells) in enumerate(rows[:10]):
        vals = [txt.strip() for _, txt in cells]
        if any(v.upper() == 'KEYNAME' for v in vals):
            header_idx = i
            for ref, txt in cells:
                header_cells.append((col_letter(ref), (txt or '').strip()))
            break
    if header_idx is None:
        # fallback to second row using sequential letters
        header_idx = 1
        header_cells = [(chr(ord('A') + i), (txt or '').strip()) for i, (_, txt) in enumerate(rows[1][1])]
    # Build header order and map
    header_cells = [(c, h) for (c, h) in header_cells if h]
    header_order = [c for c, _ in header_cells]
    header_map = {c: h for c, h in header_cells}
    # Build rows using column letters alignment
    table = []
    for (_, cells) in rows[header_idx+1:]:
        by_col = {col_letter(ref): (txt or '').strip() for ref, txt in cells}
        row = {header_map[c]: by_col.get(c, '') for c in header_order}
        if any(v for v in row.values()):
            table.append(row)
    return table

def normalize_bool(v: str, yes_values: list[str]):
    return (v or '').strip() in yes_values

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

def decide_type(row, mapping):
    dt_raw = (row.get(mapping['columns']['data_type']) or '').strip()
    dt = mapping['normalization']['data_type'].get(dt_raw, dt_raw).lower()
    if dt == 'complex':
        return 'complex'
    if dt == 'lookup':
        return 'lookup'
    if dt == 'freetext' or dt == 'freeText'.lower():
        return 'freeText'
    if dt == 'date':
        return 'date'
    if dt == 'number':
        # Decide decimal vs integer
        hint = (row.get(mapping['columns'].get('field_length','FIELD LENGTH')) or '').lower()
        for pat in mapping['normalization']['decimal_hint_patterns']:
            if pat in hint:
                return 'decimal'
        return 'integer'
    # default
    return 'string'

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

def to_yaml(data) -> str:
    # Minimal YAML dumper sufficient for our structure (strings, lists, dicts)
    def dump_scalar(value: str, pad: str) -> str:
        if value is None:
            return ''
        s = str(value)
        # Use block scalar for multi-line strings
        if '\n' in s:
            lines = s.split('\n')
            body = '\n'.join(pad + '  ' + ln for ln in lines)
            return f"|\n{body}"
        # Quote if contains reserved characters or leading/trailing spaces
        if any(ch in s for ch in [':', '#', '{', '}', '[', ']', ',', '&', '*', '!', '|', '>', '"', "'", '%', '@']) or s.strip() != s:
            return '"' + s.replace('"', '\\"') + '"'
        return s
    def dump(obj, indent=0):
        pad = '  ' * indent
        if isinstance(obj, dict):
            lines = []
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    lines.append(f"{pad}{k}:\n" + dump(v, indent + 1))
                else:
                    if v is None:
                        lines.append(f"{pad}{k}: ")
                    elif isinstance(v, bool):
                        lines.append(f"{pad}{k}: {'true' if v else 'false'}")
                    else:
                        lines.append(f"{pad}{k}: {dump_scalar(v, pad)}")
            return '\n'.join(lines)
        elif isinstance(obj, list):
            lines = []
            for it in obj:
                if isinstance(it, (dict, list)):
                    lines.append(f"{pad}-\n" + dump(it, indent + 1))
                else:
                    if it is None:
                        lines.append(f"{pad}- ")
                    elif isinstance(it, bool):
                        lines.append(f"{pad}- {'true' if it else 'false'}")
                    else:
                        scalar = dump_scalar(it, pad)
                        # Block scalars in lists need dash + space then block
                        if scalar.startswith('|'):
                            lines.append(f"{pad}- {scalar}")
                        else:
                            lines.append(f"{pad}- {scalar}")
            return '\n'.join(lines)
        else:
            return pad + dump_scalar(obj, pad)
    return dump(data) + "\n"

def main():
    mapping = load_mapping()
    value_aliases = mapping.get('value_aliases') or {}
    # Build synonym->canonical map (lowercased)
    alias_to_canon: dict[str,str] = {}
    for canon, syns in value_aliases.items():
        c = (canon or '').strip().lower()
        alias_to_canon[c] = c
        for s in (syns or []):
            alias_to_canon[(s or '').strip().lower()] = c
    with ZipFile(INCOMING, 'r') as z:
        sst = read_shared_strings(z)
        idx = sheet_index_by_name(z, mapping['sheet'])
        rows = read_sheet_rows(z, idx, sst)
        table = build_table(rows)
        lookups = collect_lookup_values(z, mapping)
    fallback = {k: [{'value': v, 'label': v} for v in vals] for k, vals in (mapping.get('fallback_lookups') or {}).items()}

    cols = mapping['columns']
    label_overrides = mapping.get('label_overrides') or {}
    vis_overrides = mapping.get('visibility_overrides') or {}
    internal_label_contains = [s.lower() for s in (mapping.get('internal_label_contains') or [])]
    yes_vals = mapping['normalization']['yes_values']
    op_map = mapping['normalization']['operators']
    sec_map = {k.lower(): v for k,v in mapping.get('sections_by_label', {}).items()}

    # Apply filters
    def row_matches_filters(r):
        for fk, fv in mapping['filters'].items():
            if (r.get(fk) or '').strip() != fv:
                return False
        return True

    filtered = [r for r in table if row_matches_filters(r)]

    included = []
    excluded = []
    ids_seen = set()
    groups = {}

    for r in filtered:
        idv = (r.get(cols['id']) or '').strip()
        label = (r.get(cols['label']) or '').strip()
        if idv in label_overrides:
            label = label_overrides[idv]
        # Exclusions: internal/system/action/label patterns
        action = (r.get(cols['action']) or '').lower()
        internal = (r.get(cols['internal']) or '').strip()
        system = (r.get(cols['system']) or '').strip()
        if any(p in action for p in [s.lower() for s in mapping['exclude']['action_contains']]):
            excluded.append((idv, label, 'action internal'))
            continue
        if internal in yes_vals:
            excluded.append((idv, label, 'INTERNAL=Y'))
            continue
        if system in yes_vals:
            excluded.append((idv, label, 'SYSTEM=Y'))
            continue
        if any(p in label.lower() for p in [s.lower() for s in mapping['exclude']['label_contains']]):
            excluded.append((idv, label, 'label contains internal analysis'))
            continue

        # Determine style by field type hints or data type (some sheets put Title in Data Type)
        ft_raw = (r.get(cols.get('field_type', '')) or '').strip().lower()
        dt_raw_for_style = (r.get(cols.get('data_type', '')) or '').strip().lower()
        style = 'field'
        if ft_raw in ['title', 'divider', 'section title', 'heading'] or dt_raw_for_style in ['title', 'divider', 'section title', 'heading']:
            style = 'divider'
        elif ft_raw in ['statement', 'note', 'information', 'info'] or dt_raw_for_style in ['statement', 'note', 'information', 'info']:
            style = 'statement'

        # For non-input items, synthesize an id when KEYNAME is missing
        if not idv and style != 'field':
            ref = (r.get(cols.get('ref', '')) or '').strip()
            prefix = 'title' if style == 'divider' else 'statement'
            # prefer label-based slug to be stable
            if label:
                idv = f"{prefix}_{slugify(label)[:48]}"
            elif ref:
                idv = f"{prefix}_row_{slugify(ref)}"
            else:
                idv = f"{prefix}_row"

        # If still missing id or label for fields, exclude
        if style == 'field' and (not idv or not label):
            excluded.append((idv, label, 'missing id/label'))
            continue

        # Build field
        # Detect misaligned lookup types: if LOOKUP is blank but DATA TYPE matches a known lookup type
        dt_raw = (r.get(cols.get('data_type', '')) or '').strip()
        lookup_type_val = (r.get(cols.get('lookup_type', '')) or '').strip()
        force_lookup = False
        if style == 'field' and not lookup_type_val:
            if dt_raw in lookups or dt_raw in (mapping.get('fallback_lookups') or {}):
                lookup_type_val = dt_raw
                force_lookup = True

        ky_type = 'lookup' if (style == 'field' and force_lookup) else (decide_type(r, mapping) if style == 'field' else None)
        field = {
            'key': idv,
            'label': label,
            'style': style,
            'entity': mapping['defaults']['entity'],
            'visibility': parse_visibility(r.get(cols['visibility']) or '', op_map),
            'scriptId': f"ROW:{(r.get(cols['ref']) or '').strip()}|KEY:{idv}",
            '_section': mapping['defaults']['section'],
            '_stage': (r.get(cols['stage']) or '').strip()
        }
        # Mark internal by label keywords (e.g., OBT TO COMPLETE)
        if any(tok in label.lower() for tok in internal_label_contains):
            field['internal'] = True
        if style == 'field':
            field['type'] = ky_type
            field['validation'] = {}
        help_text = (r.get(cols.get('help','')) or '').strip()
        if help_text:
            field['description'] = help_text
        if style == 'field':
            # required
            if normalize_bool(r.get(cols['mandatory']) or '', yes_vals):
                field['validation'] = {**field['validation'], 'required': True}
            # date format
            if ky_type == 'date':
                field['validation'] = {**field['validation'], 'dateFormat': 'DD/MM/YYYY'}
            # options
            lookup_type = lookup_type_val
            opts = []
            if ky_type == 'lookup':
                lt_raw = (lookup_type or '').strip()
                lt_norm = lt_raw
                if lt_norm and lt_norm in lookups:
                    opts = lookups[lt_norm]
                elif lt_norm in fallback:
                    opts = fallback[lt_norm]
                else:
                    # robust yes/no detection
                    yn = lt_raw.lower().replace(' ', '')
                    yn = yn.replace('-', '/').replace('\\', '/')
                    if yn in ['yes/no','yesno']:
                        opts = [{'value':'Yes','label':'Yes'},{'value':'No','label':'No'}]
            if not opts and ky_type == 'lookup':
                # Final fallback option when no items provided
                opts = [{'value': 'Lookup items not provided', 'label': 'Lookup items not provided'}]
            if opts:
                field['options'] = opts

        # section mapping by label
        lab_key = label.lower().strip('*').strip()
        if lab_key in sec_map:
            field['_section'] = sec_map[lab_key]
        else:
            # try contains matching for partials
            for k,v in sec_map.items():
                if k in lab_key:
                    field['_section'] = v
                    break

        # Apply visibility overrides from mapping (append AND conditions)
        if idv in vis_overrides:
            extra_exprs = vis_overrides[idv]
            for expr in extra_exprs:
                extra_rules = parse_visibility(expr, op_map)
                if extra_rules:
                    # merge conditions into first rule as AND
                    if field.get('visibility'):
                        field['visibility'][0]['conditions'].extend(extra_rules[0]['conditions'])
                    else:
                        field['visibility'] = extra_rules

        # complex group marking
        cx = (r.get(cols['complex']) or '').strip()
        if cx:
            field['_complex'] = cx
            gi = (r.get(cols.get('complex_identifier','')) or '').strip()
            g = groups.setdefault(cx, {'key': cx, 'children': [], 'titleField': gi or None})
            g['children'].append(idv)

        included.append(field)

    # Add explicit complex group parent fields (type: complex) so consumers can rely on schema fields
    included_keys = {f['key'] for f in included}
    for g in groups.values():
        if g['key'] in included_keys:
            # a sheet row may already define this group; ensure it has children/titleField
            for f in included:
                if f['key'] == g['key']:
                    f['type'] = 'complex'
                    f['children'] = g['children']
                    if g.get('titleField'):
                        f['titleField'] = g['titleField']
                    break
            continue
        # infer section from first child
        first_child = next((f for f in included if f['key'] in g['children']), None)
        section = first_child.get('_section') if first_child else mapping['defaults']['section']
        included.append({
            'key': g['key'],
            'label': g['key'],
            'style': 'field',
            'entity': mapping['defaults']['entity'],
            'visibility': [],
            'scriptId': f"GROUP:{g['key']}",
            '_section': section,
            '_stage': '',
            'type': 'complex',
            'children': g['children'],
            **({'titleField': g['titleField']} if g.get('titleField') else {})
        })

    # Canonicalize condition values to match controller options (by value/label) using alias map
    field_by_key = {f['key']: f for f in included}
    def canonize_value(controller_key: str, raw: str) -> str:
        if not raw:
            return raw
        val_lc = raw.strip().lower()
        # alias substitution
        val_norm = alias_to_canon.get(val_lc, val_lc)
        ctrl = field_by_key.get(controller_key)
        if not ctrl:
            return raw
        opts = ctrl.get('options') or []
        # compare to both value and label
        for o in opts:
            ov = str(o.get('value') or '').strip()
            ol = str(o.get('label') or '').strip()
            if val_norm == ov.strip().lower() or val_norm == ol.strip().lower():
                return ov or ol or raw
        # no match
        return raw

    for f in included:
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
                    newv = canonize_value(left_key, orig)
                    if newv != orig:
                        c['value'] = newv
                        changed = True
        if changed:
            f['visibility'] = vis

    # Assemble KYCP schema
    schema = {
        'key': 'non-lux-1-1',
        'name': 'Non-Lux LP — v1.1 (AS-IS)',
        'version': '0.1.0',
        'entity': mapping['defaults']['entity'],
        'fields': included
    }
    if groups:
        # informational metadata; preview-kycp does not consume yet
        schema['groups'] = list(groups.values())

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write(to_yaml(schema))

    # Summary
    print('[import] non-lux-1-1')
    print(f"  included: {len(included)}")
    print(f"  excluded: {len(excluded)}")
    if excluded:
        # show top 10 reasons
        reasons = {}
        for _,_,why in excluded:
            reasons[why] = reasons.get(why,0)+1
        print('  exclusion summary:', reasons)
    unresolved = [f for f in included if f.get('type')=='lookup' and not f.get('options')]
    if unresolved:
        print(f"  unresolved lookups: {len(unresolved)}")
        ex = unresolved[:5]
        print("   e.g.", ', '.join(x['key'] for x in ex))

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        print(f"[error] {e}")
        sys.exit(1)
        # After determining id and style, check for duplicates
        if idv in ids_seen:
            print(f"[error] Duplicate KEYNAME: {idv}")
            sys.exit(1)
        ids_seen.add(idv)
