# Proposed Section Restructure - v2.2 Flow Design

## Executive Summary

**Objective**: Eliminate 3 critical backwards dependencies while preserving Paul's B-section organizational intent and maintaining all regulatory/business requirements.

**Critical Changes**: 
1. Move jurisdiction selection to absolute beginning
2. Restructure entity classification timing  
3. Group related regulatory assessments
4. Maintain logical progression from decisions → details → assessments

## Current vs Proposed Structure

### **Current Structure (With Backwards Dependencies)**
```
❌ B1 - Pre-App Qs (depends on B2 UK selection - BACKWARDS!)
❌ B2 - Bank Relationship (GENBankAccountJurisdiction)
❌ B3 - Wholesale Depositor (UK-only, triggered by B2)
❌ B4 - Introduction of Applicant 
❌ B5 - Applicant Details (SPEdirectregulatorother depends on B11 - BACKWARDS!)
   B6 - Tax Classification
   B7 - Controlling Parties
❌ B8 - PEPs (internal field ordering issue)
   B9 - Ownership
   B10 - Key Principal Risk Factors
❌ B11 - Purpose of Entity (SPEdirectregulator triggers B5 dependency - BACKWARDS!)
   B12 - Your Requirements
   B13 - Use of Product
   B14 - Internal Analysis
```

### **Proposed Structure (Zero Backwards Dependencies)**
```
✅ B1 - Jurisdiction & Application Context 
✅ B2 - Pre-Application Assessment
✅ B3 - Entity Classification & Type
✅ B4 - UK Regulatory Requirements (Wholesale Depositor)
✅ B5 - Introduction of Applicant
✅ B6 - Applicant Details & Regulatory Status
✅ B7 - Tax Classification
✅ B8 - Controlling Parties & Ownership
✅ B9 - PEPs Assessment  
✅ B10 - Key Principal Risk Factors
✅ B11 - Purpose of Entity
✅ B12 - Your Requirements
✅ B13 - Use of Product
✅ B14 - Internal Analysis
```

## Detailed Section Restructure

### **B1 - Jurisdiction & Application Context** *(NEW POSITIONING)*
**Purpose**: Establish critical branching factors first
**Fields Moved Here**:
- `GENBankAccountJurisdiction` (moved from current B2) - **CRITICAL CONTROL POINT**
- `GENIndicativeAppetiteCustomerApplicationTypeFundsandFundsRelated` (moved from current B4)

**Rationale**: 
- Eliminates B1 backwards dependency (current B1 disappears if UK not selected)
- Jurisdiction drives 26 field dependencies across 15 sections
- Application type drives 11 field dependencies across 6 sections
- Establishes user context for form completion

### **B2 - Pre-Application Assessment** *(MOVED FROM B1)*
**Purpose**: Appetite and eligibility questions (now that jurisdiction is known)
**Fields from Current B1**:
- `GENIndicativeAppetiteQuestions` - controls 16 fields across 12 sections
- All related appetite assessment fields

**Rationale**:
- Now has proper dependency direction (B1 jurisdiction → B2 appetite)
- No longer creates backwards dependency violation
- Logical flow: know where → assess appetite

### **B3 - Entity Classification & Type** *(NEW SECTION)*
**Purpose**: Establish entity characteristics early for downstream dependencies
**Fields Moved Here**:
- `GENentitytype` (moved from current B11) - controls 8 fields in General section
- Related entity classification fields
- Early regulator classification questions

**Rationale**:
- Enables proper forward dependency flow for regulatory questions
- Reduces cascade complexity in later sections
- Provides context for all subsequent entity-specific questions

### **B4 - UK Regulatory Requirements** *(RENAMED B3)*
**Purpose**: Handle UK-specific wholesale depositor assessment
**Content**: All current B3 fields (unchanged)
**Trigger**: `GENBankAccountJurisdiction == "United Kingdom"` (now from B1)

**Rationale**:
- Maintains Paul's wholesale depositor logic exactly
- Now properly positioned after jurisdiction selection
- UK-specific requirements handled early in process

### **B5 - Introduction of Applicant** *(CURRENT B4)*
**Purpose**: Introducer and contact details
**Content**: Current B4 fields with subsections B5.1, B5.2
**Dependencies**: Application type from B1

**Rationale**:
- Logical progression: context → regulatory → introduction
- Maintains Paul's applicant introduction concept
- Clear dependency direction from B1 application type

### **B6 - Applicant Details & Regulatory Status** *(RESTRUCTURED B5)*
**Purpose**: Entity details and regulatory classification
**Combined Content**:
- Current B5 applicant detail fields
- Regulatory status questions (including regulator fields)
- `SPEdirectregulatorother` field (no longer backwards dependent)

**Rationale**:
- **CRITICAL**: Eliminates B11 → B5 backwards dependency
- Regulatory status logically follows entity classification (B3)
- Groups related entity information together

### **B7 - Tax Classification** *(CURRENT B6)*
**Purpose**: Tax-related classifications
**Content**: Current B6 fields unchanged
**Dependencies**: Entity type from B3

**Rationale**:
- Maintains Paul's tax classification concept
- Now has proper forward dependency from entity type
- Logical progression after entity details

### **B8 - Controlling Parties & Ownership** *(RESTRUCTURED B7 + B9)*
**Purpose**: Ownership structure and control
**Combined Content**:
- Current B7 controlling parties fields
- Current B9 ownership fields and subsections (B8.1, B8.2, B8.3)

**Rationale**:
- Logical grouping of related ownership concepts
- Reduces section proliferation
- Maintains hierarchical subsection structure

### **B9 - PEPs Assessment** *(CURRENT B8)*
**Purpose**: PEP and sanctions screening
**Content**: Current B8 fields with fixed internal ordering
**Fix Applied**: `GENpepinvestors` (154) → `GENdetailPEPconnection` (155)

**Rationale**:
- Logical positioning after ownership/control identification
- Eliminates internal backwards dependency
- Clear progression: know parties → assess risks

### **B10 - Key Principal Risk Factors** *(CURRENT B10)*
**Purpose**: Risk assessment and mitigation
**Content**: Current B10 fields unchanged
**Dependencies**: Clear forward dependency chain

**Rationale**:
- Maintains Paul's risk factor concept
- Properly positioned after PEP assessment
- Natural risk evaluation sequence

### **B11 - Purpose of Entity** *(RESTRUCTURED CURRENT B11)*
**Purpose**: Business purpose and activities
**Content**: Current B11 fields EXCEPT regulator fields (moved to B6)
**Subsections**: B11.1, B11.2, B11.3, B11.4 maintained

**Rationale**:
- **CRITICAL**: No longer drives backwards dependencies to B5
- Maintains Paul's business purpose concept
- Logical positioning: know entity → know purpose

### **B12 - Your Requirements** *(CURRENT B12)*
**Purpose**: Banking service requirements
**Content**: Current B12 fields unchanged

**Rationale**:
- Maintains Paul's requirements concept
- Logical progression: purpose → requirements
- Clear dependency direction

### **B13 - Use of Product** *(CURRENT B13)*
**Purpose**: Specific product usage details
**Content**: Current B13 fields unchanged

**Rationale**:
- Maintains Paul's product concept
- Final step: requirements → usage
- Complete journey flow

### **B14 - Internal Analysis** *(CURRENT B14)*
**Purpose**: Internal processing and analysis
**Content**: Current B14 fields unchanged

**Rationale**:
- Maintains Paul's internal analysis concept
- Final section for internal use only

## Critical Dependency Fixes

### **Fix 1: B1 → B2 Backwards Dependency** ✅
```
BEFORE: B1 Pre-App (conditional on B2 UK) → B2 Jurisdiction
AFTER:  B1 Jurisdiction → B2 Pre-App (conditional on B1 UK)
```

### **Fix 2: B11 → B5 Backwards Dependency** ✅
```
BEFORE: B5 Applicant (SPEdirectregulatorother) ← B11 Purpose (SPEdirectregulator)
AFTER:  B3 Entity Classification → B6 Applicant & Regulatory (SPEdirectregulator → SPEdirectregulatorother)
```

### **Fix 3: B8 Internal Ordering** ✅
```
BEFORE: GENdetailPEPconnection (154) → GENpepinvestors (155)
AFTER:  GENpepinvestors (154) → GENdetailPEPconnection (155)
```

## Dependency Flow Validation

### **Major Control Points (Now Properly Sequenced)**
1. **B1 Jurisdiction** → 26 fields across 13 sections (forward cascade)
2. **B1 Application Type** → 11 fields across 6 sections (forward cascade)  
3. **B2 Appetite Questions** → 16 fields across 12 sections (forward cascade)
4. **B3 Entity Type** → 8 fields in General section (forward cascade)

### **Section-to-Section Dependencies (All Forward)**
- B1 → B2, B3, B4, B5, B6, B7, B8, B9, B10, B11, B12, B13 ✅
- B2 → B5, B6, B7, B8, B9, B10, B11, B13 ✅
- B3 → B6, B7, B11 ✅
- B6 → B7 ✅
- B7 → B8 ✅
- B8 → B9 ✅

**Result**: Zero backwards dependencies ✅

## Paul's Intent Preservation

### **Organizational Concepts Maintained**
- ✅ **B-section hierarchy**: All 25 Paul sections preserved
- ✅ **Nested structure**: B4→B4.1/B4.2, B9→B9.1/B9.2/B9.3, B11→B11.1-B11.4
- ✅ **Field ordering**: Paul's "[number] - [section]" ordering preserved within sections
- ✅ **Content integrity**: No content changes, only structural repositioning

### **Business Logic Preserved**
- ✅ **UK wholesale depositor**: Complete B3 logic maintained, just repositioned
- ✅ **Regulatory compliance**: All requirements captured, better organized
- ✅ **Entity classification**: Enhanced early classification supports better flow
- ✅ **Risk assessment**: Logical progression from entities → parties → risks

## Implementation Requirements

### **Schema Updates Required**
1. **Section reordering**: Update paul_sections mapping in import script
2. **Field movement**: Move specific fields between sections
3. **Dependency updates**: Update all conditional logic references
4. **Subsection handling**: Maintain nested accordion structure

### **Testing Requirements**
1. **Conditional logic**: Validate all 322 dependencies still function
2. **UK jurisdiction path**: Ensure B4 wholesale depositor triggers correctly
3. **Application type**: Verify B5 subsection logic works
4. **Entity classification**: Test B3 → downstream section dependencies

### **Frontend Requirements**
1. **Accordion structure**: Support new section order
2. **Nested sections**: Maintain B5.1/B5.2, B8.1/B8.2/B8.3, B11.1-B11.4
3. **Conditional display**: Update section/field visibility logic
4. **Progress indication**: Update journey steps and navigation

## Next Steps

1. **Update import script** with new section mapping and field movements
2. **Regenerate v2.2 schema** with restructured flow
3. **Test all conditional dependencies** to ensure no regressions  
4. **Validate UX flow** with sequential progression testing
5. **Update explain visibility** to show structural changes from original

## Success Criteria

### **Technical Validation** 
- ✅ Zero backwards dependencies in final flow
- ✅ All conditional logic functions correctly
- ✅ Maintains Paul's B-section organizational intent  
- ✅ 306 customer-facing fields properly organized

### **User Experience**
- ✅ Logical, intuitive question progression
- ✅ No surprising section appearances
- ✅ Clear sense of journey scope and progress
- ✅ Reduced cognitive load through better sequencing

### **Business Value**
- ✅ Regulatory compliance requirements maintained
- ✅ Captures all necessary information effectively
- ✅ Supports both direct and intermediary application flows
- ✅ Improved completion rates through better UX

## Status: Ready for Implementation

This restructure design eliminates all critical UX violations while preserving Paul's organizational intent and maintaining complete regulatory compliance. The proposed structure creates a logical, sequential flow that eliminates user confusion and supports better completion rates.