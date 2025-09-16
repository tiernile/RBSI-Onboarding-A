# Future Prototype – Outstanding Copy Mappings

The following rows from `data/incoming/20250916-rewritten-draft.xlsx` do not yet map to schema fields/options in `schema-kycp.yaml`. They will need new aliases or schema updates before their proposed copy can surface in the prototype.

| Spreadsheet Row | Section                                 | Draft Text (trimmed)                                                      | Notes |
|-----------------|-----------------------------------------|---------------------------------------------------------------------------|-------|
| 5               | Start a New Application                  | You are a 3rd party Captive Insurance Manager…                            | Option not present in current lookup |
| 14              | Business Appetite                        | Is the entity a Money Service Business?                                   | No dedicated field; only option lists |
| 15              | Business Appetite                        | Will the entity invest in Crypto assets?                                  | Same as above |
| 48–55           | Key Principals – Add new principal       | Title / New or existing / Name / Entity type / Controller etc.            | Repeater child fields not yet aliased |
| 56–59           | Key Principals – Address & contact       | Registered address / Telephone / Formation date / Country                 | Repeater child fields |
| 62              | Key Principals – Tax information         | Current Text (placeholder)                                                | Workbook header row |
| 63              | Key Principals – Tax information         | FATCA Tax: Is entity incorporated in USA?                                 | Repeater child field |
| 64              | Key Principals – Tax information         | CRS Tax: Is entity financial institution or investment entity?            | Repeater child field |
| 67              | Key Principals – Tax information         | Provide tax identification number or equivalent?                          | Repeater child field |
| 70              | Key Principals – Risk Profile            | Is the entity a Money Service Business?                                   | Repeater child field |
| 71              | Key Principals – Risk Profile            | Will the entity invest in Crypto assets?                                  | Repeater child field |
| 73              | Key Principals – Risk Profile            | Is the customer connected with a high-risk jurisdiction?                  | Repeater child field |
| 87              | Business Activity & Investment           | Industry description/SIC code                                             | Needs alias to existing field |
| 127             | Banking Requirements                     | How many transactions do you expect to complete in this calendar year?    | Needs alias to existing field |

Remaining unmatched rows are variants of the ones above or workbook headings (e.g. "Current Text"). Update this document as aliases are added.
