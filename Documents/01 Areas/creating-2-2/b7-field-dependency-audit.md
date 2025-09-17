# B7 Field Dependency Audit - Comprehensive Analysis

## Overview
B7 "Controlling Parties" section has **critical UX issues** due to field duplication and poor grouping. This audit documents all fields, their relationships, and proposes consolidation strategy.

## Problem Summary
- **17 total fields** in B7 section
- **Massive duplication**: Same questions appear 3x with different field IDs
- **Poor visual hierarchy**: Users can't tell which follow-ups relate to which parent questions
- **Confusing user experience**: Same question appears multiple times in different contexts

## Complete Field Inventory

### **1. Secretary Group** ✅ (Good Structure)
- **GENSecretary** (143) - "Is there a Secretary within the structure?" [NO CONDITIONS]
- **GENSecretaryName** (144) - "Please enter the full name of the Secretary" [IF GENSecretary eq Yes]

### **2. Fund Manager Group** 🚨 (TRIPLE DUPLICATION)

#### **Parent Questions (Order 145)** - "Is there a Fund Manager within the structure?"
- **GENFundMngr** - NO visibility conditions (always shown)
- **GENIndicativeAppetiteFundMng** - IF GENIndicativeAppetiteQuestions eq YES
- **GENUKIndicativeAppetiteFundMng** - IF GENBankAccountJurisdiction eq United Kingdom

#### **Child Questions (Order 147)** - "Where is the Fund Manager domiciled?"
- **GENFundMngDom** - IF GENFundMngr eq Yes
- **GENIndicativeAppetiteFundMngDom** - IF GENIndicativeAppetiteFundMng eq YES
- **GENUKIndicativeAppetiteFundMngDom** - IF GENUKIndicativeAppetiteFundMng eq YES

#### **Grandchild Questions (Order 148)** - "Is it Delaware or Non-Delaware?"
- **GENFundMngDomUSA** - IF GENFundMngDom eq United States
- **GENIndicativeAppetiteFundMngDomUSA** - IF GENIndicativeAppetiteFundMngDom eq United States
- **GENUKIndicativeAppetiteFundMngDomUSA** - IF GENUKIndicativeAppetiteFundMngDom eq United States

### **3. Investment Adviser Group** 🚨 (TRIPLE DUPLICATION)

#### **Parent Questions (Order 149)** - "Is there an Investment Adviser?"
- **GENOpeningInvestmentAdviser** - NO visibility conditions (always shown)
- **GENIndicativeAppetiteOpeningInvestmentAdviser** - IF GENIndicativeAppetiteQuestions eq YES
- **GENUKIndicativeAppetiteOpeningInvestmentAdviser** - IF GENBankAccountJurisdiction eq United Kingdom

#### **Child Questions (Order 150)** - "What is the location of the Investment Adviser?"
- **GENOpeningInvestmentAdviserLocation** - IF GENOpeningInvestmentAdviser eq Yes
- **GENIndicativeAppetiteOpeningInvestmentAdviserLocation** - IF GENIndicativeAppetiteOpeningInvestmentAdviser eq YES
- **GENUKIndicativeAppetiteOpeningInvestmentAdviserLocation** - IF GENUKIndicativeAppetiteOpeningInvestmentAdviser eq YES

#### **Grandchild Questions (Order 151)** - "Is it Delaware or Non-Delaware?"
- **GENOpeningInvestmentAdviserLocationUSA** - IF GENOpeningInvestmentAdviserLocation eq United States
- **GENIndicativeAppetiteOpeningInvestmentAdviserLocationUSA** - IF GENIndicativeAppetiteOpeningInvestmentAdviserLocation eq United States
- **GENUKIndicativeAppetiteOpeningInvestmentAdviserLocationUSA** - IF GENUKIndicativeAppetiteOpeningInvestmentAdviserLocation eq United States

### **4. Limited Partnership Group** ✅ (Good Structure)
- **GENlimitedpartnershipstructure** (152) - "Limited Partnership structure" [NO CONDITIONS]

## User Journey Analysis

### **Scenario 1: UK Jurisdiction + Pre-App Questions = YES**
User sees **BOTH** duplicates for each question:
- "Is there a Fund Manager?" (appears 2x)
- "Where is the Fund Manager domiciled?" (appears 2x if they answer Yes above)
- "Is it Delaware or Non-Delaware?" (appears 2x if they select United States above)
- Same pattern for Investment Adviser questions

### **Scenario 2: Non-UK Jurisdiction + Pre-App Questions = YES**
User sees:
- "Is there a Fund Manager?" (GENFundMngr + GENIndicativeAppetiteFundMng versions)
- "Is there an Investment Adviser?" (GENOpeningInvestmentAdviser + GENIndicativeAppetiteOpeningInvestmentAdviser versions)

### **Scenario 3: UK Jurisdiction + Pre-App Questions = NO**
User sees:
- "Is there a Fund Manager?" (GENFundMngr + GENUKIndicativeAppetiteFundMng versions)
- "Is there an Investment Adviser?" (GENOpeningInvestmentAdviser + GENUKIndicativeAppetiteOpeningInvestmentAdviser versions)

### **Scenario 4: Non-UK Jurisdiction + Pre-App Questions = NO**
User sees only:
- "Is there a Fund Manager?" (GENFundMngr version only)
- "Is there an Investment Adviser?" (GENOpeningInvestmentAdviser version only)

## Critical Issues Identified

### **1. Functional Duplication**
Same questions with identical purpose but different field IDs create confusion and poor UX.

### **2. Broken Visual Hierarchy**
Related questions are scattered throughout the section rather than grouped together.

### **3. Dependency Chain Conflicts**
Multiple versions of same question create complex dependency chains that are hard to follow.

### **4. Field Ordering Issues**
Paul's ordering (143, 144, 145, 147, 148, 149, 150, 151, 152) doesn't group related fields together.

## Consolidation Strategy

### **Phase 1: Merge Duplicate Fields**
Combine functionally identical fields using OR conditions:

#### **Fund Manager Consolidation:**
```yaml
- key: GENFundMngr_CONSOLIDATED
  label: Is there a Fund Manager within the structure?
  visibility:
  - entity: entity
    targetKeys: []
    allConditionsMustMatch: false  # OR logic
    conditions:
    - sourceKey: GENIndicativeAppetiteQuestions
      operator: eq
      value: 'YES'
    - sourceKey: GENBankAccountJurisdiction
      operator: eq
      value: United Kingdom
    # Plus: Always visible when neither condition applies
```

#### **Investment Adviser Consolidation:**
Similar approach - merge three versions into one with OR visibility logic.

### **Phase 2: Reorder for Visual Hierarchy**
Group parent → child → grandchild sequences together:

**Proposed New Order:**
1. Secretary (143) → Secretary Name (144)
2. Fund Manager (145) → Fund Manager Location (146) → Delaware Question (147)
3. Investment Adviser (148) → Investment Adviser Location (149) → Delaware Question (150)
4. Limited Partnership (151)

### **Phase 3: Add Visual Grouping**
Create sub-section headers or indentation to show relationships:
- "Secretary Information"
- "Fund Manager Details" 
- "Investment Adviser Details"
- "Partnership Structure"

## Expected Benefits
✅ **Eliminate duplicate questions** - No more seeing same question 2-3 times
✅ **Clear parent-child relationships** - Logical grouping of related fields
✅ **Maintain all functionality** - All business logic preserved with OR conditions
✅ **Improved user comprehension** - Users understand form structure better
✅ **Reduced form length** - From 17 fields to ~8 fields (significant reduction)

## Implementation Priority
**HIGH PRIORITY** - This directly affects user experience and form completion rates.

## Next Steps
1. Update import script to implement field consolidation logic
2. Create visual grouping components for sub-sections
3. Test all user journey scenarios to ensure no functionality lost
4. Validate consolidated visibility conditions work correctly

---

**Files:** 17 fields → 8 consolidated fields (52% reduction)  
**User Impact:** Eliminates confusing duplicate questions  
**Business Logic:** Fully preserved through OR visibility conditions