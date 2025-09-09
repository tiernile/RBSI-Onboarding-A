# Visibility Rules (Plain English)

Use simple expressions to control when a field shows. Expressions evaluate against earlier answers.

## Supported Operators
- Equality: `KEY == "Yes"`, `KEY != "UK"`
- Sets: `KEY includes "Option"` (for multi-select answers)
- Numbers: `AMOUNT > 100`, `SCORE >= 3`
- Booleans: `IS_ACTIVE == true`
- Logic: `&&` (and), `||` (or), parentheses `(...)` for grouping

## Examples
- Show fund size only if closed: `GENFundClosed == "Yes"`
- Ask for details when "Yes": `GENIndicativeAppetiteRiskadversedetailsother == "Yes"`
- Exact size when extreme: `GENFundSize == "10bn +"`
- Country‑based rule: `(COUNTRY != "United Kingdom") && (RISK_SCORE >= 3)`
- Multi‑select contains: `PERMITS includes "Derivatives"`

## Notes
- Strings must be quoted, numbers don’t need quotes.
- Unknown keys or invalid expressions evaluate to "not visible" (fail safe).
- Keep conditions simple and test them in `/preview/<journey>`.
- Equality on strings is case‑insensitive (e.g., `YES` equals `Yes`).
