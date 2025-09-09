#!/usr/bin/env python3
"""
Interactive Mapping Wizard

Purpose: Help create a mapping JSON for new spreadsheets with changing column headers.
Walks through header detection, column mapping, filters, lookups sheet, and ordering.
Optionally runs the importer afterwards.

Usage:
  python scripts/mapping_wizard.py --input data/incoming/20250901_new.xlsx --journey new-journey
"""

import argparse
from pathlib import Path
import json
import pandas as pd
from difflib import get_close_matches


SYNONYMS = {
  'id': ['KEYNAME','KEY','ID','FIELD KEY','KEY NAME'],
  'label': ['FIELD NAME','LABEL','QUESTION','QUESTION TEXT'],
  'data_type': ['DATA TYPE','TYPE','DATA-TYPE'],
  'field_type': ['FIELD TYPE','INPUT TYPE','CONTROL','WIDGET'],
  'lookup_type': ['LOOKUP','LOOKUP TYPE','CODE LIST','OPTIONS KEY'],
  'mandatory': ['MANDATORY','REQUIRED','IS REQUIRED'],
  'visibility': ['VISIBILITY CONDITION/GROUP NAME','VISIBILITY','CONDITION'],
  'stage': ['STAGE','STEP','PHASE'],
  'section': ['SECTION','GROUP','PAGE'],
  'regex': ['REGEX','VALIDATION','PATTERN'],
  'crm_field': ['CRM Mapping Info','CRM','SYSTEM FIELD'],
  'ref': ['REF','ROW','ROW REF','ROW NUMBER']
}


def pick(prompt: str, options: list[str], default_index: int|None=None) -> str:
    print(f"\n{prompt}")
    for i, opt in enumerate(options):
        print(f"  [{i}] {opt}")
    if default_index is not None:
        resp = input(f"Select index (default {default_index}): ").strip()
        if resp == '':
            return options[default_index]
    else:
        resp = input("Select index: ").strip()
    try:
        return options[int(resp)]
    except Exception:
        print("Invalid selection, using first option")
        return options[0]


def find_candidate(header_names: list[str], synonyms: list[str]) -> str|None:
    # try exact case-insensitive
    lower = {h.lower(): h for h in header_names}
    for s in synonyms:
        if s.lower() in lower:
            return lower[s.lower()]
    # try fuzzy
    best = None
    for s in synonyms:
        matches = get_close_matches(s, header_names, n=1, cutoff=0.6)
        if matches:
            best = matches[0]
            break
    return best


def main():
    ap = argparse.ArgumentParser(description='Interactive mapping wizard for new spreadsheets')
    ap.add_argument('--input', required=True, help='Path to XLSX (data/incoming/*.xlsx)')
    ap.add_argument('--journey', required=True, help='Journey key for mapping filename and defaults')
    args = ap.parse_args()

    xlsx = Path(args.input)
    if not xlsx.exists():
        raise SystemExit(f"File not found: {xlsx}")

    # Select sheet
    xl = pd.ExcelFile(xlsx)
    sheet = pick('Select sheet to import', xl.sheet_names, 0)

    # Decide header row by counting synonyms matched
    header_candidates = [0,1,2]
    best_h = 0
    best_hits = -1
    headers_snapshot = {}
    for h in header_candidates:
        try:
            df = pd.read_excel(xlsx, sheet_name=sheet, header=h)
        except Exception:
            continue
        columns = list(df.columns)
        headers_snapshot[h] = columns
        hits = 0
        for key, syns in SYNONYMS.items():
            if find_candidate(columns, syns):
                hits += 1
        if hits > best_hits:
            best_hits = hits
            best_h = h
    print(f"\nSuggested header row: {best_h} (matched {best_hits} known fields)")
    header_row = input(f"Use header row {best_h}? (Y/n): ").strip().lower()
    if header_row == 'n':
        header_row = int(input('Enter header row index (0-based): ').strip())
    else:
        header_row = best_h

    df = pd.read_excel(xlsx, sheet_name=sheet, header=header_row)
    cols = list(df.columns)
    print("\nDetected columns:")
    print(', '.join(map(str, cols)))

    # Map required fields
    columns_map = {}
    for key, syns in SYNONYMS.items():
        cand = find_candidate(cols, syns)
        if cand:
            ans = input(f"Map '{key}' to '{cand}'? (Y/n/custom): ").strip().lower()
            if ans == 'n':
                manual = input("Enter exact column name (or blank to skip): ").strip()
                if manual:
                    columns_map[key] = manual
            elif ans == 'custom':
                manual = input("Enter exact column name: ").strip()
                if manual:
                    columns_map[key] = manual
            else:
                columns_map[key] = cand
        else:
            manual = input(f"No candidate for '{key}'. Enter column name to use (or blank to skip): ").strip()
            if manual:
                columns_map[key] = manual

    # Filters (optional)
    filters = {}
    add_filters = input("\nAdd filters (e.g., Programme/Entity)? (y/N): ").strip().lower() == 'y'
    while add_filters:
        col = pick('Pick a filter column', [str(c) for c in cols])
        values = sorted(df[col].dropna().astype(str).unique().tolist())[:20]
        print(f"Values (first 20): {values}")
        val = input("Enter value to filter by (exact): ").strip()
        filters[col] = val
        add_filters = input("Add another filter? (y/N): ").strip().lower() == 'y'

    # Lookups sheet (optional)
    lookups_sheet = None
    if input("\nUse a lookups sheet (code lists)? (y/N): ").strip().lower() == 'y':
        lookups_sheet = pick('Select lookups sheet', xl.sheet_names, 0)

    # Ordering
    ordering = pick('Choose field ordering', ['sheet','section','stage_section'], 0)

    # Normalisation defaults
    type_map = {
        'Lookup':'enum', 'Free Text':'string', 'Number':'number', 'Date':'date',
        'Decimal':'number', 'Integer':'number', 'Boolean':'boolean'
    }
    operators = {'=':'==','<>':'!='}

    defaults = {
        'entity_type': input("Default entity_type (default limited_partnership): ").strip() or 'limited_partnership',
        'jurisdiction': input("Default jurisdiction (default non_luxembourg): ").strip() or 'non_luxembourg'
    }

    mapping = {
        'sheet': sheet,
        'header_row': header_row,
        'filters': filters,
        'columns': columns_map,
        'normalization': {
            'data_type': type_map,
            'operators': operators,
            'strip_prefixes': ['If ']
        },
        'lookups_sheet': lookups_sheet,
        'lookups': {},
        'defaults': defaults,
        'ordering': ordering
    }

    # Save mapping
    out = Path(f'data/mappings/{args.journey}.json')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(mapping, indent=2))
    print(f"\nSaved mapping to {out}")

    # Optionally run importer
    if input("Run importer now? (Y/n): ").strip().lower() != 'n':
        from subprocess import run
        cmd = [
            'python', 'scripts/import_xlsx.py',
            '--mapping', str(out),
            '--input', str(xlsx),
            '--sheet', sheet,
            '--out', f'data/schemas/{args.journey}/schema.yaml',
            '--journey-key', args.journey
        ]
        if lookups_sheet:
            cmd += ['--lookups-sheet', lookups_sheet]
        print('>',' '.join(cmd))
        run(cmd, check=False)


if __name__ == '__main__':
    main()

