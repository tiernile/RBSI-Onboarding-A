# Paul's Question Order Discovery - v2.2

## Critical Discovery ✅
Successfully identified and captured Paul's comprehensive question ordering data from column Q ("PAUL Question Order").

## Issue Resolution
**Problem**: Paul's question order data was missing from the v2.1 copy map
**Root Cause**: Import script wasn't including `paul_question_order` in copy map entries
**Solution**: Added missing field to copy map generation and regenerated data

## Paul's Ordering Data Format
```
"paul_question_order": "[number] - [section]"
```

### Examples
- `"3 - B2"` - 3rd question in Bank Relationship section
- `"28 - B4"` - 28th question in Introduction of Applicant section  
- `"192 - B11.1"` - 192nd question in Purpose of Entity - Objectives subsection
- `"62 - B4.2 (Internal Field)"` - Internal field marked for exclusion

## Data Distribution Analysis
- **Total entries**: 696 (all rows from spreadsheet)
- **Empty orders**: 258 fields (no Paul ordering)
- **Zero orders**: 92 fields ("0.0" - unordered)
- **Valid orders**: ~346 fields with specific numbers
- **Range**: Orders 1-262+ indicating detailed sequencing
- **Internal markers**: Some marked as "Internal Field" for exclusion

## Paul's Structural Approach
### Progressive Numbering
- **B1 (Pre-App)**: Orders 1-30 (early screening)
- **B2 (Bank Relationship)**: Orders 3-5 (jurisdiction selection)
- **B4 (Introduction)**: Orders 28-37 (applicant contact)
- **B5 (Entity Details)**: Orders 65-108 (core information)
- **B7 (Controlling Parties)**: Orders 145-180 (ownership)
- **B11 (Purpose)**: Orders 184-211 (business activity)
- **B13 (Product Use)**: Orders 262+ (final sections)

### Section Confirmation
Each order number includes the section assignment, providing dual validation:
- Confirms Paul's section suggestions
- Provides exact sequencing within sections
- Enables proper accordion organization

## Implementation Impact for v2.2
### Enhanced Structure
- **Both dimensions**: Section grouping AND field ordering
- **User flow**: Optimized sequence based on Paul's logic
- **Progressive disclosure**: Early questions for screening, detailed questions later

### Technical Requirements
- **Parse ordering**: Extract numbers from "[number] - [section]" format
- **Sort fields**: Order by Paul's numbers within each section
- **Handle gaps**: Place unordered fields appropriately
- **Filter internal**: Exclude fields marked as "Internal Field"

## Benefits for Testing
- **Complete evaluation**: Test Paul's full structural vision
- **User flow optimization**: Evaluate question sequence effectiveness
- **Comparison baseline**: Compare against v1.1 current flow
- **Section + order**: Assess both grouping and sequencing improvements

## Next Steps
1. Create v2.2 import script using Paul's ordering logic
2. Generate schema with proper field sequence within sections
3. Test explain visibility showing both section and order changes
4. Validate accordion structure with Paul's complete organization

## Status
**READY**: Paul's complete structural data (sections + ordering) now available for v2.2 implementation.