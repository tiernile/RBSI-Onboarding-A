# Visibility Rules (Plain English)

Use simple expressions to control when a field shows. Expressions evaluate against earlier answers.

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

## Notes
- Strings should be quoted. Comparisons are case‑insensitive.
- OR is represented as multiple rules (any may match); AND is multiple conditions in a rule (all must match).
- Values are canonicalized to controller options using a mapping (e.g., `USA` → `United States`). Prefer using the exact option label.
- Unknown keys or invalid expressions default to not visible (fail safe).
- Test rules in `/preview-kycp/<journey>?explain=1` and review `/api/conditions-report/<journey>`.
