# Spreadsheet Analysis - v2.1

## File: `20250916-master-spreadsheet-2.1.xlsx`

### Basic Structure
- **Worksheets**: LP Proposal, Lookup Values, Documents  
- **Dimensions**: 793 rows x 42 columns
- **Header Row**: Row 2 (not row 1)

### Key Findings

#### New Nile Suggestion Columns (L, M, N)
- **Column L**: "Nile Suggested Field Name" - Alternative field labels
- **Column M**: "Nile Suggested Description" - Enhanced descriptions  
- **Column N**: "Nile Suggested Section" - Proposed section groupings

#### Core Mapping Columns (same as v1.1)
- **Column D**: KEYNAME (ID)
- **Column E**: FIELD NAME (label)
- **Column F**: DESCRIPTION (help text)
- **Column O**: VISIBILITY CONDITION/GROUP NAME (conditional logic)
- **Column S**: DATA TYPE (field types)
- **Column T**: LOOKUP (enum options)
- **Column Y**: INTERNAL (internal fields)
- **Column J**: Action (change suggestions)

#### Additional Important Columns
- **Column P**: Live Question Order (AS-IS ordering)
- **Column Q**: PAUL Question Order (suggested reordering)
- **Column R**: PAUL Section Suggestion (proposed groupings)
- **Column AB**: MANDATORY (required fields)
- **Column AC**: FIELD TYPE (input types)

### Sample Data Insights
From rows 3-5, we can see Nile suggestions in action:
- **Field Name**: "Where would you like to bank?" (more conversational)
- **Field Name**: "How are you applying?" (clearer language)  
- **Section**: "Start a New Application" (proposed grouping)
- **Description**: Enhanced explanatory text for better user understanding

### Mapping Structure Comparison

| v1.1 Column | v2.1 Column | Column Letter | Status |
|-------------|-------------|---------------|---------|
| KEYNAME | KEYNAME | D | ✅ Same |
| FIELD NAME | FIELD NAME | E | ✅ Same |
| DESCRIPTION | DESCRIPTION | F | ✅ Same |
| VISIBILITY CONDITION/GROUP NAME | VISIBILITY CONDITION/GROUP NAME | O | ✅ Same |
| DATA TYPE | DATA TYPE | S | ✅ Same |
| **NEW** | Nile Suggested Field Name | L | 🆕 Added |
| **NEW** | Nile Suggested Description | M | 🆕 Added |
| **NEW** | Nile Suggested Section | N | 🆕 Added |
| **NEW** | PAUL Question Order | Q | 🆕 Added |
| **NEW** | PAUL Section Suggestion | R | 🆕 Added |

### Implications for v2.1 Development

1. **Copy Changes**: The Nile suggestions represent systematic rewording for improved user experience
2. **Grouping Changes**: New section suggestions will drive accordion organization
3. **Ordering Changes**: PAUL ordering may differ from current AS-IS order
4. **Backward Compatibility**: Core structure is preserved, so we can extend the v1.1 mapping

### Next Steps

1. Create v2.1 mapping configuration extending v1.1 with new columns
2. Implement copy mapping system to track AS-IS → Nile changes
3. Configure accordion groupings based on Nile/PAUL section suggestions
4. Set up change provenance tracking for all modifications