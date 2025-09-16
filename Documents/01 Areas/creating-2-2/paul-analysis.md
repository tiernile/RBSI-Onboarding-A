# Paul's Structural Analysis - v2.2

## Overview
Analysis of Paul's section reorganization suggestions for the Non-Lux LP journey, extracted from the PAUL Section Suggestion column.

## Paul's Complete Section Structure

### Main Sections (25 unique sections)
1. **B1 - Pre-App Qs** (Pre-application questions)
2. **B2 - Bank Relationship** (Jurisdiction, banking needs)
3. **B3 - Wholesale Depositor** 
4. **B4 - Introduction of Applicant** (How applying, contact details)
5. **B4.1 - Introduction of Applicant - Introducer / Contact Details**
6. **B4.2 - Introduction of Applicant - Delivery Channel**
7. **B5 - Applicant Details** (Entity details, formation)
8. **B5.1 - Applicant Details - Good Standing Declarations**
9. **B6 - Tax Classification** (FATCA/CRS status)
10. **B7 - Controlling Parties** (Key principals, controllers)
11. **B8 - PEPs** (Politically exposed persons)
12. **B9.1 - Ownership - Bearer Shares**
13. **B9.2 - Ownership - Investor Profile**
14. **B9.3 - Ownership - SWFs** (Sovereign Wealth Funds)
15. **B10 - Key Principal Risk Factors**
16. **B11 - Purpose of Entity** 
17. **B11.1 - Purpose of Entity - Objectives**
18. **B11.2 - Purpose of Entity - Countries**
19. **B11.3 - Purpose of Entity - Cashflow**
20. **B11.4 - Purpose of Entity - Associated Bank Relationships**
21. **B12 - Your Requirements** (Account type, banking needs)
22. **B13 - Use of Product**
23. **B14 - Internal Analysis**
24. **S2 - Applicant Relationship** (Special section)

## Section Hierarchy Analysis

### Paul's Information Architecture
Paul has organized the journey into a logical flow:

1. **Pre-screening** (B1-B3): Basic appetite and relationship setup
2. **Introduction** (B4-B4.2): How customer is being introduced
3. **Entity Details** (B5-B6): Core applicant information and tax status
4. **Ownership & Control** (B7-B9.3): Who owns/controls the entity
5. **Risk Assessment** (B8, B10): PEP and risk factor evaluation
6. **Business Purpose** (B11-B11.4): What the entity does and why
7. **Banking Requirements** (B12-B13): Specific account needs
8. **Internal** (B14): Backend processing

### Key Improvements vs Current v1.1
- **Logical grouping**: Related topics grouped together (ownership, risk, purpose)
- **Progressive disclosure**: Basic details first, complex relationships later
- **Sub-section organization**: B4.1, B5.1, B9.x, B11.x provide detailed breakdowns
- **Clear separation**: Customer-facing vs internal analysis sections

## Question Ordering ✅ DISCOVERED
- **Paul Question Order**: Column Q contains comprehensive ordering data
- **Format**: `"[number] - [section]"` (e.g., "3 - B2", "28 - B4")
- **Coverage**: ~348 fields have specific ordering (vs 258 empty + 92 with "0.0")
- **Range**: Orders from 1 to 262+ indicating detailed sequencing
- **Internal markers**: Some entries marked as "Internal Field"

### Paul's Ordering Analysis
- **Detailed sequencing**: Paul provided specific numbers for field order
- **Section confirmation**: Each order includes the section assignment
- **Progressive numbering**: Lower numbers (1-30) for early sections, higher for later
- **Comprehensive coverage**: Most customer-facing fields have explicit ordering

## Implementation Strategy for v2.2

### Content Approach
- **Keep v1.1 labels/help**: Preserve original AS-IS content
- **No Nile changes**: Focus purely on structural reorganization
- **Show structural changes**: Original sections vs Paul's B-sections in explain mode

### Section Mapping
- **Primary**: Use Paul's section suggestions where provided
- **Fallback**: Use v1.1 section mapping for fields without Paul suggestions
- **Validation**: Ensure all sections have reasonable field counts

### Field Ordering Strategy
- **Parse ordering**: Extract numeric order from `"[number] - [section]"` format
- **Sort within sections**: Order fields by Paul's numbers within each section
- **Handle missing orders**: Place unordered fields (empty/"0.0") at end of sections
- **Respect internal markers**: Filter out fields marked as "Internal Field"

### Accordion Layout
- **Main sections**: B1, B2, B3, B4, B5, B6, B7, B8, B9, B10, B11, B12, B13
- **Sub-sections**: Could be nested or flattened based on testing
- **Progressive**: Earlier sections (B1-B4) likely shorter, later sections (B11) more detailed

## Expected Benefits for Testing
1. **User flow**: Test if Paul's sequence feels more natural
2. **Cognitive load**: Assess if grouping reduces mental effort
3. **Task completion**: Measure if structure improves completion rates
4. **Information findability**: Evaluate if related topics are easier to locate

## Technical Considerations
- **Field count**: Same 306 customer-facing fields as v2.1
- **Conditional logic**: Must preserve all visibility conditions from v1.1
- **Change tracking**: Full audit trail of structural modifications
- **Explain mode**: Show original vs Paul's structure with attribution

## Status
- **Sections identified**: 25 unique Paul sections
- **Coverage**: Need to analyze how many fields have Paul suggestions
- **Next step**: Create mapping configuration and import script