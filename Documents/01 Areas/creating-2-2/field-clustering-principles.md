# Field Clustering Principles for Question Grouping

## Purpose
Establish clear principles for organizing form fields to create logical, user-friendly question flows that eliminate duplication and improve comprehension.

## Core Principles

### **1. Parent-Child Relationship Principle** 🔗
**Rule**: Related questions must be grouped together with clear hierarchical relationships.

**Implementation**:
- Parent question appears first
- All child questions appear immediately after parent
- Grandchild questions appear immediately after their direct parent
- No unrelated questions between related fields

**Example**:
```
✅ GOOD:
- Is there a Fund Manager? (parent)
  - Where is the Fund Manager domiciled? (child)
    - Is it Delaware or Non-Delaware? (grandchild)

❌ BAD:
- Is there a Fund Manager? (parent)
- Is there an Investment Adviser? (unrelated)
- Where is the Fund Manager domiciled? (child - separated from parent)
```

### **2. Functional Consolidation Principle** 🔀
**Rule**: Fields with identical purpose must be consolidated using OR visibility conditions.

**Implementation**:
- Identify fields with same label and function
- Merge into single field with combined visibility logic
- Use `allConditionsMustMatch: false` for OR logic
- Preserve all original business rules

**Example**:
```yaml
# Instead of 3 separate fields:
# GENFundMngr (no conditions)
# GENIndicativeAppetiteFundMng (if pre-app = YES)  
# GENUKIndicativeAppetiteFundMng (if jurisdiction = UK)

# Consolidate to:
- key: GENFundMngr
  label: Is there a Fund Manager within the structure?
  visibility:
  - entity: entity
    allConditionsMustMatch: false  # OR logic
    conditions:
    - sourceKey: GENIndicativeAppetiteQuestions
      operator: eq
      value: 'YES'
    - sourceKey: GENBankAccountJurisdiction
      operator: eq
      value: United Kingdom
    # Always visible when neither condition applies
```

### **3. Visual Hierarchy Principle** 📋
**Rule**: Related question groups must have clear visual separation and organization.

**Implementation**:
- Use sub-section headers for major topic areas
- Indent or visually group child questions under parents
- Add spacing between unrelated question groups
- Use consistent styling for relationship levels

**Visual Structure**:
```
Section: B7 - Controlling Parties

  📋 Secretary Information
    • Is there a Secretary within the structure?
      ↳ Please enter the full name of the Secretary

  📋 Fund Manager Details  
    • Is there a Fund Manager within the structure?
      ↳ Where is the Fund Manager domiciled?
        ↳ Is it Delaware or Non-Delaware?

  📋 Investment Adviser Details
    • Is there an Investment Adviser?
      ↳ What is the location of the Investment Adviser?
        ↳ Is it Delaware or Non-Delaware?

  📋 Partnership Structure
    • Limited Partnership structure
```

### **4. Dependency Direction Principle** ➡️
**Rule**: All dependencies must flow forward - no backwards references allowed.

**Implementation**:
- Child questions can only depend on parent questions that appear earlier
- No circular dependencies
- Dependencies must be resolvable at time of rendering
- Clear dependency chains: A → B → C (never C → A)

### **5. Conditional Grouping Principle** 🎯
**Rule**: Fields with multiple trigger conditions should be consolidated rather than duplicated.

**Implementation**:
- Map all trigger conditions for each logical question
- Create single field with OR visibility encompassing all triggers
- Document all scenarios where field should appear
- Test all condition combinations

### **6. Progressive Disclosure Principle** 📖
**Rule**: Show information in logical progression from general to specific.

**Implementation**:
- High-level category questions first
- Detail questions only after category selection
- Complex sub-questions only when relevant
- Minimize cognitive load at each step

**Example Progression**:
```
1. "Is there a Fund Manager?" (high-level)
2. "Where is domiciled?" (category detail)
3. "Delaware or Non-Delaware?" (specific detail)
```

### **7. Question Scope Separation** 🎭
**Rule**: Different contexts (pre-app vs main form) should not create duplicate user-facing questions.

**Implementation**:
- Merge questions that serve same business purpose
- Use backend logic to determine which data gets used
- Present single question to user regardless of context
- Handle context differences in data processing, not user interface

## Implementation Guidelines

### **Field Consolidation Algorithm**
1. **Identify duplicate labels** - Find fields with identical or near-identical questions
2. **Map visibility conditions** - Document when each version appears
3. **Create OR logic** - Combine conditions with `allConditionsMustMatch: false`
4. **Test all scenarios** - Verify field appears in all originally intended contexts
5. **Update dependencies** - Ensure child fields reference consolidated parent

### **Visual Grouping Implementation**
1. **Add section dividers** - Clear breaks between major topics
2. **Implement indentation** - Visual hierarchy for parent-child relationships
3. **Use consistent spacing** - Predictable layout patterns
4. **Add contextual headers** - Sub-section titles for topic areas

### **Ordering Algorithm**
1. **Group by topic** - Related fields together
2. **Order by dependency** - Parents before children
3. **Maintain Paul's intent** - Preserve business logic sequence where possible
4. **Optimize for flow** - Logical progression for user comprehension

## Quality Checks

### **Before Implementation**
- [ ] All duplicate fields identified
- [ ] Dependency chains mapped
- [ ] User journey scenarios documented
- [ ] Consolidation strategy defined

### **After Implementation**  
- [ ] No functional duplicates remain
- [ ] All original business logic preserved
- [ ] Clear visual hierarchy established
- [ ] All user scenarios tested
- [ ] Field count significantly reduced

## Success Metrics

### **Quantitative**
- **Field reduction**: Target 50%+ reduction in duplicate fields
- **User completion**: Improved form completion rates
- **Error reduction**: Fewer user errors due to confusion

### **Qualitative**
- **User comprehension**: Clear understanding of question relationships
- **Visual clarity**: Obvious parent-child question structure
- **Cognitive load**: Reduced mental effort to understand form flow

## Application to B7 Specific Issues

### **Current State**: 17 fields with massive duplication
### **Target State**: ~8 consolidated fields with clear grouping

**Consolidation Plan**:
1. **Secretary Group**: 2 fields (already good structure)
2. **Fund Manager Group**: 9 fields → 3 fields (consolidate triplicates)  
3. **Investment Adviser Group**: 9 fields → 3 fields (consolidate triplicates)
4. **Partnership Group**: 1 field (already good structure)

**Total Impact**: 17 fields → 8 fields (53% reduction)

---

**These principles ensure forms are logical, efficient, and user-friendly while maintaining all business requirements and regulatory compliance.**