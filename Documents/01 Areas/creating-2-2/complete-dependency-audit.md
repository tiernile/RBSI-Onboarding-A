# Complete Dependency Audit - v2.2 Schema

## Executive Summary

**Critical Issue**: The v2.2 schema contains **322 conditional dependencies** with **3 critical backwards dependencies** that violate fundamental UX principles. Immediate restructuring required to eliminate backwards flow dependencies and improve user experience.

## Critical Backwards Dependencies (UX Violations)

### **1. B1 → B2 CRITICAL VIOLATION**
```
Source: GENIndicativeAppetiteQuestions (B1, Order 1) 
Target: GENBankAccountJurisdiction (B2, Order 3)
Issue: FIRST question depends on THIRD question
Impact: Pre-app questions appear/disappear based on later jurisdiction selection
```

### **2. B11 → B5 VIOLATION**  
```
Source: SPEdirectregulatorother (B5, Order 77)
Target: SPEdirectregulator (B11, Order 187) 
Issue: Earlier section depends on much later answer
Impact: Applicant details conditional on entity purpose fields
```

### **3. Internal B8 VIOLATION**
```
Source: GENdetailPEPconnection (B8, Order 154)
Target: GENpepinvestors (B8, Order 155)
Issue: Field depends on immediately following field
Impact: Minor - easily fixed with field reordering
```

## Major Branching Control Points

### **Top 5 Critical Decision Fields**

1. **GENBankAccountJurisdiction** (B2, Order 3)
   - **Controls**: 26 fields across 15 sections
   - **Impact**: UK vs non-UK creates parallel journey paths
   - **Sections Affected**: B1, B3, B4, B5, B6, B7, B8, B9.3, B10, B11, B12, B13, General

2. **GENIndicativeAppetiteQuestions** (B1, Order 1) 
   - **Controls**: 16 fields across 12 sections
   - **Impact**: Pre-app questions gate for appetite assessment
   - **Sections Affected**: B4, B5, B7, B8, B9.3, B10, B11, B13

3. **GENIndicativeAppetiteCustomerApplicationTypeFundsandFundsRelated** (B4, Order 28)
   - **Controls**: 11 fields across 6 sections  
   - **Impact**: Direct vs 3rd party admin branching
   - **Sections Affected**: B4.1, B4.2, B5, B9.1, B11

4. **GENffi** (B6, Order 121)
   - **Controls**: 11 fields within B6
   - **Impact**: Tax classification internal branching
   - **Sections Affected**: B6 (internal only)

5. **GENentitytype** (B11, Order 183)
   - **Controls**: 8 fields in General section
   - **Impact**: Entity type affects final classification
   - **Sections Affected**: General

## Dependency Flow Patterns

### **Section-to-Section Dependencies**

| Source Section | Target Sections | Count | Flow Type |
|---|---|---|---|
| **B1 Pre-App Qs** | B4, B5, B7, B8, B9.3, B10, B11, B13 | 16 | Forward Cascade |
| **B2 Bank Relationship** | **B1** + B3-B13, General | 26 | **BACKWARD + Forward** |
| **B4 Introduction** | B5, B9.1, B11, B4.1, B4.2 | 11 | Forward Cascade |
| **B5 Applicant Details** | B6, B7 | 7 | Forward Cascade |
| **B6 Tax Classification** | Internal B6 only | 11 | Internal Branching |
| **B7 Controlling Parties** | B8 | 6 | Forward Cascade |
| **B11 Purpose of Entity** | **B5** + General | 9 | **BACKWARD + Forward** |

### **Complex Dependency Chains (4+ Levels)**

#### **Chain 1: Geographic → Appetite → Risk Assessment**
```
GENBankAccountJurisdiction (B2) → 
  GENIndicativeAppetiteQuestions (B1) → 
    GENIndicativeAppetiteRiskadversedetailsother (B10) → 
      GENIndicativeAppetiteHighriskadversedetails (B10)
```

#### **Chain 2: Customer Type → Regulation → Entity Details**
```
GENIndicativeAppetiteCustomerApplicationTypeFundsandFundsRelated (B4) → 
  SPEisregulated (B5) → 
    SPEdirectregulator (B11) → 
      SPEdirectregulatorother (B5)
```

### **Cross-Section Field Dependencies**

#### **UK Jurisdiction Impact (26 dependencies)**
```
GENBankAccountJurisdiction == "United Kingdom" affects:
- B1: GENIndicativeAppetiteQuestions (backwards dependency!)
- B3: All wholesale depositor questions (12 fields)
- B4-B13: UK-specific regulatory requirements (13 fields)
```

#### **Customer Application Type Impact (11 dependencies)**
```
Customer Application Type == "3rd party administrator" affects:
- B4.1: Introducer contact details (4 fields)
- B4.2: Delivery channel specifics (3 fields) 
- B5: Regulatory status questions (2 fields)
- B9.1: Bearer share ownership (1 field)
- B11: Entity purpose classification (1 field)
```

## Forward Dependency Complexity Analysis

### **Branching Complexity by Section**

| Section | Internal Conditions | External Dependencies | Complexity Score |
|---|---|---|---|
| **B1** | 0 | **1 backwards** | **HIGH RISK** |
| **B2** | 1 | 26 forward | **CRITICAL CONTROL** |
| **B3** | 8 cascading | 1 from B2 | **HIGH COMPLEXITY** |
| **B4** | 2 | 11 forward + 2 from B1/B2 | **BRANCHING HUB** |
| **B5** | 4 | **1 backwards** + 6 from earlier | **DEPENDENCY HEAVY** |
| **B6** | 11 internal | 1 from B5 | **INTERNAL COMPLEXITY** |
| **B7** | 3 | 2 from B1/B5 | **MODERATE** |
| **B8** | **1 backwards** + 4 | 3 from B1/B7 | **MIXED ISSUES** |
| **B9** | 2 per subsection | 2 from B1/B4 | **MODERATE** |
| **B10** | 3 | 2 from B1/B2 | **MODERATE** |
| **B11** | 2 | **8 backwards** + 1 from B4 | **BACKWARDS HEAVY** |
| **B12** | 5 | 1 from B2 | **MODERATE** |
| **B13** | 1 | 2 from B1/B2 | **LOW** |

## Geographic vs Entity Type Branching

### **UK vs Non-UK Journey Splits**

**UK-Specific Content (26 fields):**
- **B1**: Pre-app questions (conditional appearance)
- **B3**: Wholesale depositor assessment (entire section)
- **B4-B13**: UK regulatory requirements scattered throughout

**Non-UK Journey:**
- **Simplified path**: Fewer regulatory requirements
- **Streamlined sections**: No wholesale depositor complexity
- **Reduced cognitive load**: Fewer conditional branches

### **Entity Type Branching Impact**

**Fund vs Corporate Entity Paths:**
- **B6 Tax**: Different classification requirements
- **B7 Ownership**: Varying complexity levels
- **B11 Purpose**: Fund-specific vs general business purpose

## Platform Constraint Analysis

### **Accordion Interface Limitations**

1. **Cannot Hide Sections**: Must show all accordions, leading to empty/irrelevant sections
2. **Navigation Constraints**: Difficult to jump between dependent sections
3. **Backwards Dependency UX**: Users must scroll up to complete earlier fields
4. **Progress Uncertainty**: Cannot predict journey length or complexity

### **Conditional Logic Constraints**

1. **Field-Level Only**: Conditional logic works at field level, not section level
2. **Visibility Complexity**: Nested conditions create confusing user experience
3. **State Management**: Complex dependencies difficult to debug and maintain

## Restructuring Recommendations

### **Immediate Critical Fixes**

#### **1. Eliminate B1 → B2 Backwards Dependency**
```
CURRENT: B1 Pre-App Qs → B2 Jurisdiction → B3 Wholesale Depositor
PROPOSED: B1 Jurisdiction → B2 Pre-App Qs → B3 Wholesale Depositor
```

#### **2. Fix B11 → B5 Entity Regulator Flow**
```
CURRENT: B5 Applicant Details → ... → B11 Purpose → SPEdirectregulator
PROPOSED: B5 Entity Type → B6 Regulatory Status → B7 Applicant Details
```

#### **3. Resolve B8 Internal Ordering**
```
CURRENT: GENdetailPEPconnection (154) → GENpepinvestors (155)
PROPOSED: GENpepinvestors (154) → GENdetailPEPconnection (155)
```

### **Strategic Section Reordering**

#### **Proposed New Flow Structure**
```
1. B1 - Jurisdiction & Application Type (critical decisions first)
2. B2 - Pre-Application Questions (depends on B1 decisions)  
3. B3 - Entity Classification (enables downstream dependencies)
4. B4 - UK Regulatory Assessment (jurisdiction-specific, depends on B1)
5. B5 - Introduction of Applicant (depends on B1 application type)
6. B6 - Applicant Details (depends on B3 entity type, B5 introduction)
7. B7 - Tax Classification (depends on B3 entity type)
8. B8 - Controlling Parties (depends on B6 details)
9. B9 - PEPs Assessment (depends on B8 parties)
10. B10 - Ownership Structure (depends on B8 parties)
11. B11 - Risk Factors (depends on B10 ownership)
12. B12 - Purpose of Entity (depends on all previous context)
13. B13 - Banking Requirements (depends on B12 purpose)
14. B14 - Product Usage (depends on B13 requirements)
```

### **Success Criteria for Restructure**

#### **Technical Goals**
- ✅ **Zero backwards dependencies** in final flow
- ✅ **Maximum 3-level dependency chains** (currently 4+)
- ✅ **Reduce cross-section dependencies** by 50%
- ✅ **Group related conditional logic** within sections

#### **User Experience Goals**
- ✅ **Predictable section progression** based on early choices
- ✅ **Transparent journey scope** - users understand what's coming
- ✅ **Logical information flow** - natural business conversation order
- ✅ **Minimal cognitive surprises** - no unexpected section appearances

#### **Business Goals**
- ✅ **Maintain regulatory compliance** requirements
- ✅ **Preserve Paul's B-section** organizational intent
- ✅ **Support both UK and non-UK** jurisdiction paths
- ✅ **Enable direct and intermediary** application flows

## Next Steps

1. **Design specific section restructure** based on principles
2. **Update v2.2 schema** with new ordering and fixed dependencies  
3. **Test all conditional logic** to ensure no regressions
4. **Validate user experience** with sequential flow testing
5. **Document all changes** for explain visibility and audit trail

## Status: Critical Issues Identified - Ready for Restructure Design

This audit provides the complete foundation for eliminating UX flow violations and creating a logical, sequential question progression that maintains Paul's organizational intent while fixing fundamental user experience problems.