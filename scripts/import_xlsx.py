#!/usr/bin/env python3
"""
Importer CLI: Convert a client XLSX and a mapping JSON into a schema.yaml
with smart defaults and audit reports.

Inputs:
  --mapping: data/mappings/<journey>.json
  --input:   data/incoming/<file>.xlsx
  --sheet:   override mapping.sheet (optional)
  --lookups-sheet: override mapping.lookups_sheet (optional)
  --out:     output schema path (default: data/schemas/<journey>/schema.yaml)
  --journey-key: journey key (default: derived from --out or mapping file name)

Outputs:
  - schema.yaml at --out
  - data/generated/importer-cli/<journey>/{summary.json, decisions.json}
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
import re
import sys

import pandas as pd
import yaml


def norm_key(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.strip().lower())


def resolve_column(df, name: str):
    target = norm_key(name)
    for col in df.columns:
        if norm_key(str(col)) == target:
            return col
    return None


def load_mapping(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_lookups_from_sheet(xlsx_path: Path, sheet: str) -> dict:
    lookups = {}
    try:
        df = pd.read_excel(xlsx_path, sheet_name=sheet)
    except Exception:
        return lookups
    # Try tall format with columns like LOOKUP, LOOKUP VALUE
    cols = {norm_key(c): c for c in df.columns}
    # Accept multiple naming variants for lookup type and value columns
    lk = cols.get("lookup") or cols.get("lookuptype") or cols.get("lookup_type") or cols.get("type")
    lv = cols.get("lookupvalue") or cols.get("lookup_value") or cols.get("value") or cols.get("option") or cols.get("options")
    if lk and lv:
        for _, row in df.iterrows():
            t = str(row.get(lk)).strip() if pd.notna(row.get(lk)) else None
            v = str(row.get(lv)).strip() if pd.notna(row.get(lv)) else None
            if not t or not v:
                continue
            lookups.setdefault(t, []).append(v)
    return lookups


def as_bool(v) -> bool:
    if isinstance(v, bool):
        return v
    s = str(v).strip().lower()
    # Treat common encodings as truthy, including some client-specific values
    return s in ("y", "yes", "true", "1", "a", "required", "mandatory")


def sanitize_id(raw: str) -> str:
    if not raw:
        return ""
    # Preserve alnum and underscores, collapse spaces to underscores
    s = re.sub(r"\s+", "_", raw.strip())
    s = re.sub(r"[^A-Za-z0-9_]", "", s)
    return s or ""


def infer_control(data_type: str, label: str, options: list, *, force_select: bool=False) -> str:
    dt = (data_type or "").lower()
    lab = (label or "").lower()
    if force_select:
        return "select"
    if options:
        # radio for small sets or Yes/No, else select
        # Adjusted: prefer dropdowns for enum sets; radio only when explicitly not lookup.
        return "select"
        return "select"
    if dt in ("number", "decimal", "integer"):
        return "number"
    if dt in ("date",):
        return "text"  # prototype uses text for dates
    # Heuristic: long/free-form prompts use textarea
    if any(w in lab for w in ("further details", "provide details", "describe", "explain")):
        return "textarea"
    return "text"


def normalize_condition(raw: str, operator_map: dict) -> str:
    if not raw or not str(raw).strip():
        return ""
    s = str(raw).strip()
    # Strip common prefixes
    s = re.sub(r"^\s*if\s+", "", s, flags=re.IGNORECASE)
    # Replace AND/OR
    s = re.sub(r"\bAND\b", "&&", s, flags=re.IGNORECASE)
    s = re.sub(r"\bOR\b", "||", s, flags=re.IGNORECASE)
    # Replace operators
    for k, v in (operator_map or {}).items():
        s = s.replace(k, v)
    # Quote RHS values for ==/!= when bare words
    def _quote_rhs(m):
        key, op, rhs = m.group(1), m.group(2), m.group(3)
        rhs_str = rhs.strip()
        # Already quoted or numeric/boolean
        if re.match(r'^\".*\"$', rhs_str) or re.match(r"^[0-9.]+$", rhs_str) or rhs_str.lower() in ("true", "false"):
            return f"{key} {op} {rhs_str}"
        # Remove stray quotes and wrap
        rhs_clean = rhs_str.strip('"\'')
        return f'{key} {op} "{rhs_clean}"'

    s = re.sub(r"([A-Za-z0-9_]+)\s*(==|!=)\s*([^&|()]+)", _quote_rhs, s)
    return s


def main():
    ap = argparse.ArgumentParser(description="Import XLSX to schema.yaml using mapping JSON (smart defaults)")
    ap.add_argument("--mapping", required=True, help="Path to mapping JSON (data/mappings/*.json)")
    ap.add_argument("--input", required=True, help="Path to input XLSX (data/incoming/*.xlsx)")
    ap.add_argument("--sheet", help="Override sheet name (defaults to mapping.sheet)")
    ap.add_argument("--lookups-sheet", dest="lookups_sheet", help="Override lookups sheet name")
    ap.add_argument("--out", help="Output schema path (default: data/schemas/<journey>/schema.yaml)")
    ap.add_argument("--journey-key", help="Journey key (default: from --out or mapping file name)")
    args = ap.parse_args()

    mapping_path = Path(args.mapping)
    xlsx_path = Path(args.input)
    if not mapping_path.exists():
        print(f"Mapping not found: {mapping_path}", file=sys.stderr)
        sys.exit(2)
    if not xlsx_path.exists():
        print(f"Input XLSX not found: {xlsx_path}", file=sys.stderr)
        sys.exit(2)

    mapping = load_mapping(mapping_path)
    sheet = args.sheet or mapping.get("sheet")
    if not sheet:
        print("Sheet name is required (mapping.sheet or --sheet)", file=sys.stderr)
        sys.exit(2)

    # Load main sheet with smart header detection
    header_row = mapping.get("header_row")
    df = None
    header_candidates = [header_row] if header_row is not None else [0, 1, 2]
    header_used = None
    for h in header_candidates:
        try:
            tmp = pd.read_excel(xlsx_path, sheet_name=sheet, header=h)
        except Exception as e:
            print(f"Failed to read sheet '{sheet}' with header={h}: {e}", file=sys.stderr)
            continue
        hm = {norm_key(c): c for c in tmp.columns}
        # consider it a match if we can resolve at least one of the key columns
        probe_cols = [mapping.get("columns", {}).get("label"), mapping.get("columns", {}).get("id")]
        probe_cols = [p for p in probe_cols if p]
        hits = sum(1 for p in probe_cols if hm.get(norm_key(p)))
        if hits:
            df = tmp
            header_used = h
            break
    if df is None:
        print(f"Failed to resolve header row; tried {header_candidates}", file=sys.stderr)
        sys.exit(2)

    # Tolerant header map
    header_map = {norm_key(c): c for c in df.columns}

    # Apply filters
    filters = mapping.get("filters") or {}
    filtered_df = df.copy()
    for fcol, fval in filters.items():
        resolved = header_map.get(norm_key(fcol))
        if not resolved:
            print(f"Warning: filter column not found: {fcol}")
            continue
        filtered_df = filtered_df[filtered_df[resolved].astype(str) == str(fval)]

    # Load lookups
    lookups = {}
    if mapping.get("lookups"):
        lookups.update(mapping["lookups"])  # inline
    lk_sheet = args.lookups_sheet or mapping.get("lookups_sheet")
    if lk_sheet:
        lookups_from_sheet = load_lookups_from_sheet(xlsx_path, lk_sheet)
        lookups.update(lookups_from_sheet)

    # Build normalized lookup index for resilient matching
    lookups_norm = {}
    for k, vals in lookups.items():
        lookups_norm[norm_key(k)] = vals

    cols = mapping.get("columns") or {}
    norm = mapping.get("normalization") or {}
    type_map = (norm.get("data_type") or {})
    op_map = (norm.get("operators") or {})
    strip_prefixes = norm.get("strip_prefixes") or []

    # Resolve important columns
    def col(name_key):
        col_decl = cols.get(name_key)
        return header_map.get(norm_key(col_decl)) if col_decl else None

    id_col = col("id")
    label_col = col("label")
    dtype_col = col("data_type")
    ftype_col = col("field_type")
    lookup_col = col("lookup_type")
    mandatory_col = col("mandatory")
    visibility_col = col("visibility")
    section_col = col("section")
    stage_col = col("stage")
    regex_col = col("regex") or col("validation")
    crm_col = col("crm_field")
    ref_col = col("ref")
    help_col = col("help")

    # Prepare outputs
    journey_key = args.journey_key or (Path(args.out).parts[-2] if args.out else None) or mapping_path.stem
    out_path = Path(args.out) if args.out else Path(f"data/schemas/{journey_key}/schema.yaml")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    gen_dir = Path(f"data/generated/importer-cli/{journey_key}")
    gen_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "timestamp": datetime.now().isoformat(),
        "journey": journey_key,
        "sheet": sheet,
        "header_row_used": header_used,
        "rows_total": int(df.shape[0]),
        "rows_after_filters": int(filtered_df.shape[0]),
        "items_written": 0,
        "missing_id": 0,
        "lookup_defaults_used": 0,
        "conditions_transformed": 0,
        "notes": []
    }
    decisions = []

    items = []
    for idx, row in filtered_df.iterrows():
        raw_id = str(row.get(id_col)) if id_col and pd.notna(row.get(id_col)) else ""
        label = str(row.get(label_col)) if label_col and pd.notna(row.get(label_col)) else ""
        if not raw_id and not label:
            continue
        # Generate id
        fid = sanitize_id(raw_id) or sanitize_id(label)
        used_fallback_id = False
        if not fid:
            summary["missing_id"] += 1
            fid = f"field_{len(items)+1}"
            used_fallback_id = True
        # Ensure label present (fallback to id)
        if not label or not str(label).strip():
            label = fid

        # Data type normalisation
        raw_dtype = str(row.get(dtype_col)) if dtype_col and pd.notna(row.get(dtype_col)) else ""
        raw_ftype = str(row.get(ftype_col)) if ftype_col and pd.notna(row.get(ftype_col)) else ""
        # Try mapping table first
        mapped = type_map.get(raw_dtype) or type_map.get(raw_dtype.strip()) or type_map.get(raw_dtype.strip().title())
        dtype = str(mapped or raw_dtype or "string").lower()
        # Coerce unknowns to supported set using field_type hints
        supported = {"string","number","boolean","date","enum"}
        if dtype not in supported:
            ft = raw_ftype.lower()
            if any(k in (raw_dtype.lower() + " " + ft) for k in ["lookup","select","dropdown","radio","yes/no","yes / no"]):
                dtype = "enum"
            elif any(k in (raw_dtype.lower() + " " + ft) for k in ["decimal","number","integer"]):
                dtype = "number"
            elif any(k in (raw_dtype.lower() + " " + ft) for k in ["date","time"]):
                dtype = "date"
            else:
                dtype = "string"

        # Lookups/options
        lookup_key = str(row.get(lookup_col)).strip() if lookup_col and pd.notna(row.get(lookup_col)) else ""
        options = []
        lookup_source = None
        if lookup_key:
            lk_norm = norm_key(lookup_key)
            if lk_norm in lookups_norm:
                options = [str(v) for v in lookups_norm[lk_norm]]
                lookup_source = f"lookups:{lookup_key}"
            elif lk_norm in {norm_key('Yes/No'), 'yesno', 'yes_no'}:
                options = ["Yes", "No"]
                lookup_source = "default:yes_no"
                summary["lookup_defaults_used"] += 1
            else:
                # Missing lookup definition → fall back to text input and note
                options = []
                lookup_source = "missing"
                summary.setdefault("missing_lookups", 0)
                summary["missing_lookups"] += 1

        # Mandatory
        mandatory_val = row.get(mandatory_col) if mandatory_col else False
        mandatory = as_bool(mandatory_val)

        # Visibility
        vis_raw = str(row.get(visibility_col)) if visibility_col and pd.notna(row.get(visibility_col)) else ""
        for p in strip_prefixes:
            if vis_raw.lower().startswith(p.lower()):
                vis_raw = vis_raw[len(p):]
        vis_expr = normalize_condition(vis_raw, op_map)
        if vis_expr:
            summary["conditions_transformed"] += 1

        # Validation
        regex = str(row.get(regex_col)) if regex_col and pd.notna(row.get(regex_col)) else None
        try:
            # sanity check regex compiles
            if regex:
                re.compile(regex)
        except re.error:
            summary["notes"].append(f"Invalid regex for {fid}; removed")
            regex = None

        # Control inference
        force_sel = bool(lookup_key and options)
        control = infer_control(dtype, label, options, force_select=force_sel)
        # If enum but no options resolved, prefer text control to avoid invalid select
        if (dtype == 'enum' and not options) and control == 'select':
            control = 'text'

        # Section/Stage
        section = str(row.get(section_col)) if section_col and pd.notna(row.get(section_col)) else None
        stage = str(row.get(stage_col)) if stage_col and pd.notna(row.get(stage_col)) else None

        # CRM/system mapping
        crm_field = str(row.get(crm_col)) if crm_col and pd.notna(row.get(crm_col)) else None

        # Meta/source
        ref = str(row.get(ref_col)) if ref_col and pd.notna(row.get(ref_col)) else None
        src_ref = None
        if ref or fid:
            src_ref = f"ROW:{ref or '?'}|KEY:{fid}"

        help_text = None
        if help_col and pd.notna(row.get(help_col)):
            help_text = str(row.get(help_col))

        item = {
            "id": fid,
            "label": label,
            "help": help_text,
            "entity_type": (mapping.get("defaults", {}).get("entity_type") or "limited_partnership"),
            "jurisdiction": (mapping.get("defaults", {}).get("jurisdiction") or "non_luxembourg"),
            "stage": stage or "onboarding",
            "section": section or "General",
            "data_type": dtype or "string",
            "control": control,
            "options": options,
            "mandatory": mandatory,
            "visibility": {"all": [vis_expr]} if vis_expr else {"all": []},
            "validation": {"regex": regex, "max_length": None},
            "mappings": {"crm_field": crm_field, "system_field": None},
            "meta": {"source_row_ref": src_ref}
        }
        items.append(item)

        decisions.append({
            "id": fid,
            "label": label,
            "control_inferred": control,
            "lookup_source": lookup_source,
            "visibility_original": vis_raw.strip() if vis_raw else None,
            "visibility_expr": vis_expr or None,
            "used_fallback_id": used_fallback_id
        })

    # Optional ordering: sheet (default), section, stage_section
    ordering = (mapping.get("ordering") or "sheet").lower()
    if ordering in ("section", "stage_section"):
        # preserve original index
        for i, it in enumerate(items):
            it["__idx"] = i
        # order of first appearance
        sections = []
        stages = []
        sec_index = {}
        stg_index = {}
        for it in items:
            sec = (it.get("section") or "")
            stg = (it.get("stage") or "")
            if sec not in sec_index:
                sec_index[sec] = len(sections); sections.append(sec)
            if stg not in stg_index:
                stg_index[stg] = len(stages); stages.append(stg)
        if ordering == "section":
            items.sort(key=lambda it: (sec_index.get(it.get("section") or "", 0), it["__idx"]))
        else:  # stage_section
            items.sort(key=lambda it: (stg_index.get(it.get("stage") or "", 0), sec_index.get(it.get("section") or "", 0), it["__idx"]))
        for it in items:
            it.pop("__idx", None)

    schema = {
        "key": journey_key,
        "name": mapping.get("name") or journey_key.replace("-", " ").title(),
        "version": "0.1.0",
        "items": items
    }

    # Write outputs
    with out_path.open("w", encoding="utf-8") as f:
        yaml.dump(schema, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    summary["items_written"] = len(items)
    with (gen_dir / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    with (gen_dir / "decisions.json").open("w", encoding="utf-8") as f:
        json.dump(decisions, f, indent=2)

    print("Import complete")
    print(f"- Schema: {out_path}")
    print(f"- Reports: {gen_dir}/summary.json, decisions.json")


if __name__ == "__main__":
    main()
