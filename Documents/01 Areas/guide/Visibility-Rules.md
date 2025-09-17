# Visibility Rules (Plain English)

Use simple expressions to control when a field shows. Expressions evaluate against earlier answers. The system includes **Explain Visibility** mode for debugging and **Conditions Report** for comprehensive validation.

**Critical Principle**: Fields should only depend on **earlier** answers, never later ones (backwards dependency elimination).

## Supported Operators
- Equality only: `KEY == "Yes"`, `KEY != "UK"`
- Logic: `&&` (and), `||` (or)
- Parentheses: not supported (keep rules flat)

## Examples
- Show fund size only if closed: `GENFundClosed == "Yes"`
- UK or US region fork:
  - `GENcountryregistration == "United Kingdom"` OR
  - `GENcountryregistration == "United States"`
- Ask for details when "Yes": `GENIndicativeAppetiteRiskadversedetailsother == "Yes"`

## Technical Notes
- **Strings quoted**: Comparisons are case‑insensitive
- **OR logic**: Multiple rules (any may match)
- **AND logic**: Multiple conditions in one rule (all must match)
- **Value canonicalization**: Uses mapping aliases (e.g., `USA` → `United States`)
- **Fail safe**: Unknown keys or invalid expressions default to not visible

## Debugging & Quality Tools

### Explain Visibility Mode
- **Access**: Toggle in KYCP preview or append `?explain=1` to URL
- **Shows**: Field keys, visibility conditions, dependency chains
- **Purpose**: Debug why fields are visible/hidden
- **Essential for**: Understanding complex conditional logic

### Conditions Report API
- **Access**: Admin users - click "Conditions Report" on journey cards
- **URL**: `/api/conditions-report/<journey>?format=html`
- **Validates**: All conditional logic comprehensively
- **Detects**: Unresolved keys, option mismatches, parse errors, dependency cycles
- **Critical for**: Pre-deployment validation

## Flow Design Principles

### Backwards Dependency Elimination
- **Rule**: Questions should only depend on earlier answers
- **Violation**: Later questions affecting earlier field visibility
- **Impact**: Creates confusing user experience with unexpected field appearances
- **Solution**: Move critical branching decisions early in flow

### Quality Guidelines
- **Test thoroughly**: Use both Explain Visibility and Conditions Report
- **Logical flow**: Follow natural business conversation order
- **Simple first**: Unconditional fields before conditional ones within sections
- **User experience**: Predictable journey with clear progression
