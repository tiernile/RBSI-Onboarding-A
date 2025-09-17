# Nested Accordion Analysis - v2.2 Structure

## Current Flat Structure Issues

**Problem**: Hierarchical sections are displayed as flat accordion items:
- `B4 - Introduction Of Applicant` (3 fields)
- `B4.1 - Introduction Of Applicant - Introducer / Contact Details` (15 fields)  
- `B4.2 - Introduction Of Applicant - Delivery Channel` (12 fields)

**Should Be**: Nested structure with subsections inside parent accordion.

## Hierarchical Patterns Identified

### B4 - Introduction Of Applicant
- **Parent**: B4 - Introduction Of Applicant (3 fields)
- **Children**:
  - B4.1 - Introducer / Contact Details (15 fields)
  - B4.2 - Delivery Channel (12 fields)

### B5 - Applicant Details  
- **Parent**: B5 - Applicant Details (30 fields)
- **Children**:
  - B5.1 - Good Standing Declarations (12 fields)

### B9 - Ownership
- **Parent**: B9 - Ownership (no direct fields - needs creation)
- **Children**:
  - B9.1 - Bearer Shares (6 fields)
  - B9.2 - Investor Profile (10 fields)
  - B9.3 - SWFs (18 fields)

### B11 - Purpose Of Entity
- **Parent**: B11 - Purpose Of Entity (14 fields)
- **Children**:
  - B11.1 - Objectives (17 fields)
  - B11.2 - Countries (11 fields)
  - B11.3 - Cashflow (7 fields)
  - B11.4 - Associated Bank Relationships (1 field)

## Proposed Nested Structure

### Schema Structure
```yaml
accordions:
- key: b4-introduction-of-applicant
  title: B4 - Introduction Of Applicant
  fields: [direct B4 fields]
  subsections:
    - key: b4-1-introducer-contact
      title: Introducer / Contact Details
      fields: [B4.1 fields]
    - key: b4-2-delivery-channel
      title: Delivery Channel  
      fields: [B4.2 fields]

- key: b9-ownership
  title: B9 - Ownership
  fields: []  # No direct fields
  subsections:
    - key: b9-1-bearer-shares
      title: Bearer Shares
      fields: [B9.1 fields]
    - key: b9-2-investor-profile
      title: Investor Profile
      fields: [B9.2 fields]
    - key: b9-3-swfs
      title: SWFs
      fields: [B9.3 fields]
```

## Component Requirements

### Option 1: Enhance KycpAccordion
- Add `subsections` property to accordion sections
- Render KycpSection components inside accordion content
- Keep single accordion component with nested logic

### Option 2: Create KycpNestedAccordion
- New component specifically for hierarchical sections
- Compose existing KycpAccordion + KycpSection components
- More explicit separation of concerns

## Implementation Strategy

### Phase 1: Update Schema Generation
1. **Group hierarchical sections** in import script
2. **Parse section hierarchy** from Paul's B.x.x format
3. **Generate nested accordion structure** in schema

### Phase 2: Component Updates
1. **Choose component approach** (enhance vs create new)
2. **Implement nested rendering** with proper accessibility
3. **Test accordion behavior** (expand/collapse, focus management)

### Phase 3: Styling & UX
1. **Visual hierarchy** - indent subsections appropriately
2. **Consistent spacing** between parent and child sections
3. **Clear visual separation** of nested content

## Benefits

### User Experience
- **Logical grouping** - related topics organized together
- **Reduced cognitive load** - fewer top-level sections
- **Flexible navigation** - expand only relevant subsections

### Information Architecture  
- **Matches Paul's intent** - proper hierarchical organization
- **Cleaner section list** - fewer accordion items to scan
- **Better content discovery** - related fields grouped contextually

## Technical Considerations

### Accessibility
- **Proper ARIA** for nested structure
- **Keyboard navigation** through hierarchy
- **Screen reader support** for nested relationships

### Performance
- **Conditional rendering** of subsections  
- **Lazy loading** of nested content if needed
- **State management** for expand/collapse across levels

## Status
- **Analysis**: ✅ Complete  
- **Implementation Plan**: ✅ Ready
- **Component Design**: ⏳ Next step