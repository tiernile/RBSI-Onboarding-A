# System Overview (Plain English)

This prototype turns client spreadsheets into clickable journeys using smart defaults and an auditable workflow. It is not production code, but it is structured, repeatable, and explainable.

## What It Does
- Renders journeys from a schema (a readable list of questions, rules, and options).
- Applies visibility and validation rules so screens adapt as you answer.
- Generates review artifacts (HTML diff and CSV export) with references back to the source spreadsheet.
- Provides debugging tools including **Explain Visibility** mode and **Conditions Report** API.
- Supports advanced features like field grouping, complex repeatable fields, and flow optimization.

## How It Works (End‑to‑End)
1) **Master Spreadsheet**: Client provides XLSX with structured field definitions including KEYNAME, FIELD NAME, DATA TYPE, MANDATORY, VISIBILITY columns.
2) **Column Mapping** (Critical User Input): `data/mappings/*.json` defines how spreadsheet columns map to schema fields - **this requires explicit user decisions and cannot be automated**.
3) **Schema Generation**: Import scripts create `data/schemas/<journey>/schema.yaml` with `meta.source_row_ref` for traceability.
4) **Field Organization**: System supports field grouping, complex repeatable components, and flow optimization to eliminate backwards dependencies.
5) **Rendering**: Nuxt app renders KYCP-compliant components with conditional visibility and validation.
6) **Quality Assurance**: Admin tools include Explain Visibility mode, Conditions Report API, and audit artifacts (HTML diff, CSV export).
7) **Review**: Mission Control dashboard manages journey visibility and provides admin access to debugging tools.

## System Capabilities

### Column Mapping (User Input Required)
- **Critical**: Mapping spreadsheet columns to schema fields requires explicit user decisions
- Cannot be automated - requires domain knowledge of field meanings and relationships
- Impacts all downstream functionality including visibility, validation, and user experience
- Common decision points: field types, lookup values, conditional logic, section organization

### Smart Defaults & Fallbacks
- Sheet names, lookups, and operators follow the mapping JSON; missing lookups fall back to simple options (e.g., Yes/No) and are flagged for review.
- Controls are inferred from type/lookup (e.g., enum → select); unknown controls render as text with visible warnings.
- Visibility rules accept expressions like `KEY == "Yes"` and `A && (B != "UK")`; unsupported patterns fail safe (field remains hidden).

### Advanced Features
- **Field Grouping**: Visual organization reduces cognitive load by clustering related fields
- **Complex Fields**: Repeatable field groups with add/remove functionality
- **Flow Optimization**: Backwards dependency elimination for better user experience
- **Debug Tools**: Explain Visibility mode (`?explain=1`) and Conditions Report API

## Workflow Overview

### 1. Preparation
- Place master spreadsheet in `data/incoming/YYYYMMDD_<name>.xlsx`
- Verify spreadsheet has required columns: KEYNAME, FIELD NAME, DATA TYPE, MANDATORY, VISIBILITY
- Review lookup values sheet for completeness

### 2. Column Mapping (Critical)
- Create/update `data/mappings/<journey>.json` - **requires explicit user input**
- Map spreadsheet columns to schema fields based on domain knowledge
- Define field types, lookup values, conditional logic
- Make section organization decisions

### 3. Schema Generation
- Run import scripts to generate schema files
- **Critical**: Use correct schema format and filename:
  - `schema-kycp.yaml` for KYCP accordions format (`fields[]` + `accordions[]`)
  - `schema.yaml` for basic items format (`items[]`)
- Review field organization and grouping
- Implement complex fields if needed
- Ensure `meta.source_row_ref` traceability

### 4. Quality Assurance
- Add journey to `data/schemas/manifest.yaml`
- Test locally: `pnpm dev` → `/preview-kycp/<journey>`
- Use **Explain Visibility** mode for debugging (`?explain=1`)
- Run **Conditions Report** to validate conditional logic
- Generate admin review artifacts (Diff/Export)

### 5. Optimization
- Apply field grouping for better UX
- Eliminate backwards dependencies in flow
- Implement complex fields for repeatable sections
- Validate with stakeholders

## Quality & Debugging Tools

### Schema Format Debugging
- **API Structure Check**: `curl http://localhost:3002/api/schema/<journey> | jq 'keys'`
- **Expected Formats**:
  - KYCP Accordions: `["accordions", "entity", "fields", "key", "name", "version"]`
  - Basic Items: `["items", "key", "name", "version"]`
- **Common Issues**:
  - Wrong filename: `schema-kycp.yaml` vs `schema.yaml`
  - Invalid field keys: Must be alphanumeric with underscores/hyphens
  - Missing accordions: Frontend KYCP components require accordion structure
- **Server Logs**: Check dev server output for "Invalid schema" validation errors

### Explain Visibility Mode
- Toggle in KYCP preview or append `?explain=1` to URL
- Shows which fields are visible/hidden and why
- Displays field keys to eliminate confusion about duplicate questions
- Essential for debugging conditional logic

### Conditions Report API
- Available to admin users from Mission Control
- HTML format: `/api/conditions-report/<journey>?format=html`
- JSON format: `/api/conditions-report/<journey>`
- Flags unresolved keys, option mismatches, parse errors, and dependency cycles

### Audit Artifacts
- Source references: `meta.source_row_ref` (e.g., `ROW:123|KEY:GENFundSize`)
- Diff HTML: `data/generated/diffs/<journey>/<timestamp>.html`
- CSV export: `data/generated/exports/<journey>/<timestamp>.csv`
- Field grouping analysis and dependency chain documentation

## Where Things Live
- App: `apps/prototype/`
- Schemas: `data/schemas/<journey>/schema.yaml`
- Manifest: `data/schemas/manifest.yaml`
- Mappings: `data/mappings/*.json`
- Incoming files: `data/incoming/`
- Generated artifacts: `data/generated/*`

See also: QuickStart, Operations, Visibility Rules, and FAQ in this folder for step‑by‑step usage.
