#!/usr/bin/env python3
"""
KYCP-aligned Importer: Convert client XLSX directly to KYCP component format
Generates schema that matches the KYCP component expectations exactly.

Inputs:
  --mapping: data/mappings/<journey>.json
  --input:   data/incoming/<file>.xlsx
  --sheet:   override mapping.sheet (optional)
  --lookups-sheet: override mapping.lookups_sheet (optional)
  --out:     output schema path (default: data/schemas/<journey>/schema.yaml)
  --journey-key: journey key (default: derived from --out or mapping file name)

Outputs:
  - schema.yaml in KYCP format at --out
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

# Resolve base data directory
def resolve_base_data_dir() -> Path:
    app_local = Path('apps/prototype/data')
    monorepo = Path('data')
    if app_local.exists():
        return app_local
    return monorepo


def norm_key(s: str) -> str:
    """Normalize string for case-insensitive column matching"""
    return re.sub(r"[^a-z0-9]", "", s.strip().lower())


def as_bool(v) -> bool:
    """Convert various representations to boolean"""
    if isinstance(v, bool):
        return v
    s = str(v).strip().lower()
    return s in ("y", "yes", "true", "1", "a", "required", "mandatory")


def sanitize_id(raw: str) -> str:
    """Create valid field ID from raw string"""
    if not raw:
        return ""
    s = re.sub(r"\s+", "_", raw.strip())
    s = re.sub(r"[^A-Za-z0-9_]", "", s)
    return s or ""


def map_to_kycp_type(data_type: str, control: str, has_options: bool) -> str:
    """
    Map legacy data_type/control to KYCP DataType
    KYCP types: 'string' | 'integer' | 'decimal' | 'date' | 'lookup' | 'freeText'
    """
    dt = (data_type or "").lower()
    ctrl = (control or "").lower()
    
    # Lookups/enums become 'lookup'
    if has_options or dt == "enum" or ctrl in ("select", "radio", "dropdown"):
        return "lookup"
    
    # Long text becomes 'freeText'
    if ctrl == "textarea":
        return "freeText"
    
    # Numbers - try to differentiate integer vs decimal
    if dt in ("number", "integer"):
        return "integer"
    if dt in ("decimal", "float"):
        return "decimal"
    
    # Dates
    if dt == "date":
        return "date"
    
    # Default to string
    return "string"


def parse_visibility_condition(expr: str) -> list:
    """
    Parse visibility expression into KYCP VisibilityCondition format
    Example: 'Field1 == "value"' -> [{"sourceKey": "Field1", "operator": "eq", "value": "value"}]
    """
    if not expr or not expr.strip():
        return []
    
    conditions = []
    
    # Split by && for AND conditions
    parts = expr.split('&&')
    
    for part in parts:
        part = part.strip()
        
        # Match patterns like: Field == "value" or Field != "value"
        match = re.match(r'^([A-Za-z0-9_]+)\s*(==|!=)\s*"([^"]*)"', part)
        if match:
            conditions.append({
                "sourceKey": match.group(1),
                "operator": "eq" if match.group(2) == "==" else "neq",
                "value": match.group(3)
            })
            continue
            
        # Handle unquoted values
        match = re.match(r'^([A-Za-z0-9_]+)\s*(==|!=)\s*([A-Za-z0-9_]+)', part)
        if match:
            conditions.append({
                "sourceKey": match.group(1),
                "operator": "eq" if match.group(2) == "==" else "neq", 
                "value": match.group(3)
            })
    
    return conditions


def normalize_visibility_expression(raw: str, operator_map: dict) -> str:
    """Normalize visibility expression with operator mapping"""
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
    
    # Quote bare RHS values
    def quote_rhs(m):
        key, op, rhs = m.group(1), m.group(2), m.group(3)
        rhs_str = rhs.strip()
        if re.match(r'^".*"$', rhs_str) or re.match(r"^[0-9.]+$", rhs_str) or rhs_str.lower() in ("true", "false"):
            return f"{key} {op} {rhs_str}"
        rhs_clean = rhs_str.strip('"\'')
        return f'{key} {op} "{rhs_clean}"'
    
    s = re.sub(r"([A-Za-z0-9_]+)\s*(==|!=)\s*([^&|()]+)", quote_rhs, s)
    return s


def load_lookups_from_sheet(xlsx_path: Path, sheet: str) -> dict:
    """Load lookup values from a dedicated sheet"""
    lookups = {}
    try:
        df = pd.read_excel(xlsx_path, sheet_name=sheet)
    except Exception:
        return lookups
    
    # Try to find lookup type and value columns
    cols = {norm_key(c): c for c in df.columns}
    lk = cols.get("lookup") or cols.get("lookuptype") or cols.get("type")
    lv = cols.get("lookupvalue") or cols.get("value") or cols.get("option")
    
    # Also check for Code/Label columns for proper value/label pairs
    code_col = cols.get("code") or cols.get("value")
    label_col = cols.get("label") or cols.get("display")
    
    if lk and lv:
        for _, row in df.iterrows():
            t = str(row.get(lk)).strip() if pd.notna(row.get(lk)) else None
            v = str(row.get(lv)).strip() if pd.notna(row.get(lv)) else None
            if not t or not v:
                continue
            
            # If we have code/label columns, create proper option objects
            if code_col and label_col and pd.notna(row.get(code_col)) and pd.notna(row.get(label_col)):
                option = {
                    "value": str(row.get(code_col)).strip(),
                    "label": str(row.get(label_col)).strip()
                }
            else:
                # Otherwise use value as both code and label
                option = {"value": v, "label": v}
            
            lookups.setdefault(t, []).append(option)
    
    return lookups


def create_kycp_field(row_data: dict, lookups: dict, defaults: dict) -> dict:
    """
    Create a KYCP-compliant field object from spreadsheet row data
    """
    field_id = row_data.get("id", "")
    label = row_data.get("label", "")
    
    # Determine field type
    data_type = row_data.get("data_type", "string")
    control = row_data.get("control", "text")
    options = row_data.get("options", [])
    kycp_type = map_to_kycp_type(data_type, control, bool(options))
    
    # Build base field
    field = {
        "key": field_id,
        "label": label,
        "style": "field",  # Regular fields use 'field' style
        "type": kycp_type,
        "entity": defaults.get("entity", "entity"),
        "order": row_data.get("order", 0)
    }
    
    # Add description if present
    if row_data.get("help"):
        field["description"] = row_data["help"]
    
    # Build validation object
    validation = {}
    if row_data.get("mandatory"):
        validation["required"] = True
    
    if row_data.get("regex"):
        validation["pattern"] = row_data["regex"]
    
    if row_data.get("max_length"):
        validation["maxLength"] = row_data["max_length"]
    
    # Type-specific validation
    if kycp_type == "date":
        validation["dateFormat"] = "DD/MM/YYYY"
    elif kycp_type == "integer":
        # Could add min/max from column data
        pass
    elif kycp_type == "decimal":
        # Could add precision/scale
        validation["precision"] = 10  # Default
        validation["scale"] = 2  # Default
    
    if validation:
        field["validation"] = validation
    
    # Add options for lookup type
    if kycp_type == "lookup" and options:
        # Ensure options are in {value, label} format
        formatted_options = []
        for opt in options:
            if isinstance(opt, dict):
                formatted_options.append(opt)
            else:
                formatted_options.append({"value": str(opt), "label": str(opt)})
        field["options"] = formatted_options
    
    # Add visibility rules
    if row_data.get("visibility_conditions"):
        visibility_rules = []
        for condition_set in row_data["visibility_conditions"]:
            if condition_set:  # Only add non-empty condition sets
                visibility_rules.append({
                    "entity": defaults.get("entity", "entity"),
                    "targetKeys": [],  # Not used in current implementation
                    "allConditionsMustMatch": True,
                    "conditions": condition_set
                })
        if visibility_rules:
            field["visibility"] = visibility_rules
    
    # Status rights (placeholder - could be enhanced with mapping config)
    field["statusRights"] = [
        {"status": "draft", "right": "write"},
        {"status": "submitted", "right": "read"},
        {"status": "approved", "right": "invisible"}
    ]
    
    # Mark as internal if specified
    if row_data.get("internal_only"):
        field["internal"] = True
    
    # Store source reference in scriptId for traceability
    if row_data.get("source_ref"):
        field["scriptId"] = row_data["source_ref"]
    
    return field


def main():
    ap = argparse.ArgumentParser(description="Import XLSX to KYCP-format schema.yaml")
    ap.add_argument("--mapping", required=True, help="Path to mapping JSON")
    ap.add_argument("--input", required=True, help="Path to input XLSX")
    ap.add_argument("--sheet", help="Override sheet name")
    ap.add_argument("--lookups-sheet", dest="lookups_sheet", help="Override lookups sheet")
    ap.add_argument("--out", help="Output schema path")
    ap.add_argument("--journey-key", help="Journey key")
    args = ap.parse_args()
    
    base_data = resolve_base_data_dir()
    mapping_path = Path(args.mapping)
    xlsx_path = Path(args.input)
    
    if not mapping_path.exists():
        print(f"Mapping not found: {mapping_path}", file=sys.stderr)
        sys.exit(2)
    if not xlsx_path.exists():
        print(f"Input XLSX not found: {xlsx_path}", file=sys.stderr)
        sys.exit(2)
    
    # Load mapping configuration
    with mapping_path.open("r", encoding="utf-8") as f:
        mapping = json.load(f)
    
    sheet = args.sheet or mapping.get("sheet")
    if not sheet:
        print("Sheet name required", file=sys.stderr)
        sys.exit(2)
    
    # Try to load spreadsheet with different header rows
    header_row = mapping.get("header_row")
    df = None
    header_candidates = [header_row] if header_row is not None else [0, 1, 2]
    
    for h in header_candidates:
        try:
            tmp = pd.read_excel(xlsx_path, sheet_name=sheet, header=h)
            # Check if we can find key columns
            hm = {norm_key(c): c for c in tmp.columns}
            probe_cols = [mapping.get("columns", {}).get("label"), mapping.get("columns", {}).get("id")]
            probe_cols = [p for p in probe_cols if p]
            hits = sum(1 for p in probe_cols if hm.get(norm_key(p)))
            if hits:
                df = tmp
                break
        except Exception:
            continue
    
    if df is None:
        print(f"Failed to load sheet {sheet}", file=sys.stderr)
        sys.exit(2)
    
    # Build column mapping
    header_map = {norm_key(c): c for c in df.columns}
    cols = mapping.get("columns") or {}
    
    def col(name):
        col_decl = cols.get(name)
        return header_map.get(norm_key(col_decl)) if col_decl else None
    
    # Map columns
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
    help_col = col("help")
    ref_col = col("ref")
    
    # Check for internal-only column
    internal_col = col("internal") or col("internal_only")
    if not internal_col:
        for cand in ("INTERNAL ONLY", "INTERNAL", "Action"):
            resolved = header_map.get(norm_key(cand))
            if resolved:
                internal_col = resolved
                break
    
    # Apply filters
    filters = mapping.get("filters") or {}
    filtered_df = df.copy()
    for fcol, fval in filters.items():
        resolved = header_map.get(norm_key(fcol))
        if resolved:
            filtered_df = filtered_df[filtered_df[resolved].astype(str) == str(fval)]
    
    # Load lookups
    lookups = {}
    if mapping.get("lookups"):
        # Convert inline lookups to proper format
        for k, vals in mapping["lookups"].items():
            lookups[k] = [{"value": v, "label": v} for v in vals]
    
    lk_sheet = args.lookups_sheet or mapping.get("lookups_sheet")
    if lk_sheet:
        lookups_from_sheet = load_lookups_from_sheet(xlsx_path, lk_sheet)
        lookups.update(lookups_from_sheet)
    
    # Normalize lookups for matching
    lookups_norm = {}
    for k, vals in lookups.items():
        lookups_norm[norm_key(k)] = vals
    
    # Process rows into KYCP fields
    fields = []
    order = 0
    
    norm = mapping.get("normalization") or {}
    op_map = norm.get("operators") or {}
    
    # Track statistics
    summary = {
        "timestamp": datetime.now().isoformat(),
        "journey": args.journey_key or mapping_path.stem,
        "input_file": xlsx_path.name,
        "sheet": sheet,
        "rows_processed": len(filtered_df),
        "fields_created": 0,
        "internal_fields": 0,
        "fields_with_visibility": 0
    }
    
    for idx, row in filtered_df.iterrows():
        # Extract basic field info
        raw_id = str(row.get(id_col)) if id_col and pd.notna(row.get(id_col)) else ""
        label = str(row.get(label_col)) if label_col and pd.notna(row.get(label_col)) else ""
        
        if not raw_id and not label:
            continue
        
        field_id = sanitize_id(raw_id) or sanitize_id(label) or f"field_{order}"
        if not label:
            label = field_id
        
        # Get data type and control
        data_type = str(row.get(dtype_col)) if dtype_col and pd.notna(row.get(dtype_col)) else "string"
        
        # Normalize data type using mapping
        type_map = norm.get("data_type") or {}
        data_type = type_map.get(data_type, data_type).lower()
        
        # Determine control type
        control = "text"
        field_type = str(row.get(ftype_col)) if ftype_col and pd.notna(row.get(ftype_col)) else ""
        
        # Get options from lookup
        options = []
        lookup_key = str(row.get(lookup_col)).strip() if lookup_col and pd.notna(row.get(lookup_col)) else ""
        if lookup_key:
            lk_norm = norm_key(lookup_key)
            if lk_norm in lookups_norm:
                options = lookups_norm[lk_norm]
                control = "select"
            elif lk_norm in {norm_key('Yes/No'), 'yesno'}:
                options = [{"value": "Yes", "label": "Yes"}, {"value": "No", "label": "No"}]
                control = "select"
        
        # Check for textarea
        if any(w in label.lower() for w in ["details", "describe", "explain"]):
            control = "textarea"
        
        # Get other field properties
        mandatory = as_bool(row.get(mandatory_col)) if mandatory_col and pd.notna(row.get(mandatory_col)) else False
        
        # Parse visibility
        visibility_conditions = []
        if visibility_col and pd.notna(row.get(visibility_col)):
            vis_raw = str(row.get(visibility_col))
            vis_expr = normalize_visibility_expression(vis_raw, op_map)
            if vis_expr:
                conditions = parse_visibility_condition(vis_expr)
                if conditions:
                    visibility_conditions.append(conditions)
                    summary["fields_with_visibility"] += 1
        
        # Check if internal
        internal_only = False
        if internal_col and pd.notna(row.get(internal_col)):
            val = str(row.get(internal_col))
            internal_only = as_bool(val) or bool(re.search(r"\binternal\b", val, flags=re.IGNORECASE))
            if internal_only:
                summary["internal_fields"] += 1
        
        # Get help text
        help_text = str(row.get(help_col)) if help_col and pd.notna(row.get(help_col)) else None
        
        # Get reference
        ref = str(row.get(ref_col)) if ref_col and pd.notna(row.get(ref_col)) else None
        source_ref = f"ROW:{ref or idx}|KEY:{field_id}"
        
        # Build row data
        row_data = {
            "id": field_id,
            "label": label,
            "help": help_text,
            "data_type": data_type,
            "control": control,
            "options": options,
            "mandatory": mandatory,
            "visibility_conditions": visibility_conditions,
            "internal_only": internal_only,
            "source_ref": source_ref,
            "order": order
        }
        
        # Get regex validation
        if regex_col and pd.notna(row.get(regex_col)):
            regex = str(row.get(regex_col))
            try:
                re.compile(regex)
                row_data["regex"] = regex
            except re.error:
                pass
        
        # Create KYCP field
        defaults = mapping.get("defaults", {})
        field = create_kycp_field(row_data, lookups, defaults)
        
        # Group fields by section (optional enhancement)
        section = str(row.get(section_col)) if section_col and pd.notna(row.get(section_col)) else "General"
        stage = str(row.get(stage_col)) if stage_col and pd.notna(row.get(stage_col)) else "onboarding"
        
        # Add section/stage metadata (could be used for grouping later)
        field["_section"] = section
        field["_stage"] = stage
        
        fields.append(field)
        order += 1
        summary["fields_created"] += 1
    
    # Build final schema in KYCP format
    journey_key = args.journey_key or mapping_path.stem
    schema = {
        "key": journey_key,
        "name": mapping.get("name") or journey_key.replace("-", " ").title(),
        "version": "1.0.0",
        "entity": mapping.get("defaults", {}).get("entity", "entity"),
        "fields": fields
    }
    
    # Write output
    out_path = Path(args.out) if args.out else (base_data / f"schemas/{journey_key}/schema-kycp.yaml")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    with out_path.open("w", encoding="utf-8") as f:
        yaml.dump(schema, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    # Write summary
    gen_dir = base_data / f"generated/importer-cli/{journey_key}"
    gen_dir.mkdir(parents=True, exist_ok=True)
    
    with (gen_dir / "summary-kycp.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    
    print("KYCP Import complete")
    print(f"- Schema: {out_path}")
    print(f"- Summary: {gen_dir}/summary-kycp.json")
    print(f"- Fields created: {summary['fields_created']}")
    print(f"- Internal fields: {summary['internal_fields']}")
    print(f"- Fields with visibility: {summary['fields_with_visibility']}")


if __name__ == "__main__":
    main()