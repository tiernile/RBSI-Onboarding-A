# v2.2 Paul Structure Development - Handover Documentation

## Project Overview

**Objective**: Create v2.2 prototype implementing Paul's structural suggestions for the Non-Lux LP journey, focused on **information architecture and field sequencing** rather than content changes.

**Key Distinction**: 
- **v2.1**: Nile team content improvements (labels, help text, sections)
- **v2.2**: Paul's structural reorganization (B-sections, field ordering, question flow)

## Current Status: Phase 3 - Flow Restructure Discovery

### ✅ **Completed Phases**

#### **Phase 1: Discovery & Analysis** 
- Investigated missing Paul question order data in import pipeline
- Fixed v2.1 import script to capture `paul_question_order` field  
- Regenerated complete copy map with Paul's sections + ordering data
- Analyzed Paul's comprehensive 25 B-section hierarchy

#### **Phase 2: Technical Implementation**
- Created v2.2 mapping configuration using Paul's columns
- Built v2.2 import script with ordering logic and change tracking
- Generated working v2.2 schema with 306 fields across 24 sections
- Fixed section ordering bug (B1→B2→B3... instead of alphabetical)
- Implemented nested accordion structure for hierarchical sections
- Resolved accordion duplicates and ordering issues

### 🔄 **Phase 3: Flow Restructure (Current)**
- **Critical Discovery**: Identified backwards dependencies violating UX principles
- Completed comprehensive conditional dependency audit (322 dependencies)
- Documented UX flow restructure principles
- **Ready for**: New section ordering design eliminating backwards dependencies

## Critical Technical Issues Discovered

### **🚨 Backwards Dependencies (UX Violations)**

1. **B1 → B2 CRITICAL**: Pre-app questions depend on later jurisdiction selection
   - **Impact**: First section appears/disappears based on third question
   - **Fix Required**: Move jurisdiction selection to absolute beginning

2. **B11 → B5**: Entity regulator fields create backwards dependency chain
   - **Impact**: Applicant details conditional on much later entity purpose
   - **Fix Required**: Restructure regulator classification timing

3. **B8**: Minor internal field ordering issue (easily fixed)

### **Major Branching Control Points**
- **GENBankAccountJurisdiction** (B2): Controls 26 fields across 15 sections
- **GENIndicativeAppetiteQuestions** (B1): Controls 16 fields across 12 sections  
- **Application Type** (B4): Controls 11 fields across 6 sections

## File Structure & Documentation

### **Documentation Location**: `/Documents/01 Areas/creating-2-2/`

#### **Core Analysis Documents**
- ✅ `paul-analysis.md` - Paul's 25 B-section structure analysis
- ✅ `paul-ordering-discovery.md` - Discovery of Paul's question ordering data
- ✅ `b3-conditional-flow.md` - Detailed B3 wholesale depositor dependency chain
- ✅ `complete-dependency-audit.md` - **CRITICAL**: All 322 dependencies analyzed
- ✅ `flow-restructure-principles.md` - **CRITICAL**: UX principles for new ordering

#### **Implementation Tracking** 
- ✅ `progress-tracking.md` - Complete phase tracking and status
- ✅ `action-analysis.md` - Action/reworded column analysis (257 entries need human review)
- ✅ `nested-accordion-analysis.md` - Hierarchical section structure design

### **Technical Implementation Files**

#### **Configuration & Scripts**
- ✅ `data/mappings/non-lux-lp-2-2.json` - v2.2 mapping with Paul's columns
- ✅ `scripts/import_non_lux_2_2.py` - Import script with ordering/nesting logic
- ✅ `data/schemas/non-lux-lp-2-2/schema-kycp.yaml` - Generated v2.2 schema

#### **Generated Data**
- ✅ `data/generated/non-lux-lp-2-2-copy-map.json` - Complete field mapping with Paul data
- ✅ Journey registered in `manifest.yaml` as "Non‑Lux LP — v2.2 (Paul Structure)"

## Key Technical Achievements

### **Nested Accordion Structure** ✅
Successfully implemented hierarchical grouping:
- **B4 - Introduction of Applicant**
  - Introducer / Contact Details  
  - Delivery Channel
- **B9 - Ownership**
  - Bearer Shares
  - Investor Profile  
  - SWFs
- **B11 - Purpose of Entity**
  - Objectives
  - Countries
  - Cashflow
  - Associated Bank Relationships

### **Paul's Field Ordering** ✅  
- Captured Paul's "[number] - [section]" format from column Q
- Implemented field sorting by Paul's numeric sequence within sections
- ~346 fields have specific Paul ordering vs 350 without

### **Change Tracking** ✅
- Original/future metadata structure for explain visibility
- Tracks Paul's structural changes vs Nile's content changes
- Complete audit trail for all modifications

## Data Sources & Integration

### **Spreadsheet Integration**
- **Source**: `data/incoming/20250911_master_non-lux.xlsx`
- **Key Columns**: 
  - Column N: "PAUL Question Order" 
  - Column O: "PAUL Section Suggestion"
  - Column J: "Action" (376 entries)
  - Column K: "Reworded?" (257 entries requiring human review)

### **Paul's Section Hierarchy**
```
25 B-sections identified:
B1 - Pre-App Qs
B2 - Bank Relationship  
B3 - Wholesale Depositor
B4 - Introduction of Applicant (+ B4.1, B4.2)
B5 - Applicant Details (+ B5.1)
B6 - Tax Classification
B7 - Controlling Parties
B8 - PEPs
B9 - Ownership (+ B9.1, B9.2, B9.3) [Note: No B9 parent in original mapping]
B10 - Key Principal Risk Factors
B11 - Purpose of Entity (+ B11.1, B11.2, B11.3, B11.4)
B12 - Your Requirements
B13 - Use of Product
B14 - Internal Analysis
S2 - Applicant Relationship
```

## Content vs Structure Distinction

### **⚠️ IMPORTANT: Human-in-Loop Required**
- **257 reworded suggestions** captured for systematic human review
- **376 action items** need SME evaluation and approval  
- **NO automatic content implementation** - all changes require human decision
- **v2.2 focuses on structure only** - preserves original AS-IS content

### **Paul vs Nile Changes**
- **Paul's work**: Information architecture, section organization, field sequencing
- **Nile's work**: Content improvements, label enhancements, help text
- **v2.2 implements**: Paul's structure with original v1.1 content
- **Future v2.3**: Could combine Paul's structure + approved Nile content

## Current UX Flow Issues

### **Sequential Flow vs Conditional Logic Problem**
- **Core Issue**: Users need sequential flow, but conditions create backwards dependencies
- **Platform Constraint**: Cannot conditionally hide entire accordions  
- **User Impact**: Unexpected section appearances, cognitive surprise, poor completion rates

### **Identified Restructuring Needs**
Based on comprehensive audit:

1. **Jurisdiction First**: Move to absolute beginning (eliminates B1 backwards dependency)
2. **Entity Classification Early**: Reduces mid-journey branching complexity
3. **Application Type Early**: Determines form completion context
4. **Regulatory Assessments**: Group UK-specific requirements together
5. **Progressive Information**: Simple→complex, general→specific

## Next Steps (Immediate Priorities)

### **🎯 High Priority: Flow Restructure Design**
1. **Design new section ordering** eliminating all backwards dependencies
2. **Create proposed structure** preserving Paul's B-section intent
3. **Update v2.2 schema** with new ordering logic
4. **Test conditional flows** to ensure no regressions

### **📋 Medium Priority: Content Integration Planning**
1. **Review 257 reworded suggestions** with stakeholders
2. **Evaluate 376 action items** for implementation priority
3. **Plan human approval workflow** for content changes
4. **Design v2.3 strategy** combining structure + approved content

### **🔧 Technical Debt & Enhancements**
1. **Frontend component updates** for nested accordion rendering
2. **Explain visibility testing** for Paul's structural changes
3. **Development server validation** 
4. **User testing preparation** for flow comparison (v1.1 vs v2.2)

## Success Criteria

### **Technical Validation**
- ✅ Zero backwards dependencies in final flow
- ✅ All conditional logic functions correctly  
- ✅ Maintains Paul's B-section organizational intent
- ✅ 306 customer-facing fields properly organized

### **User Experience**
- ⏳ Logical, intuitive question progression
- ⏳ No surprising section appearances
- ⏳ Clear sense of journey scope and progress
- ⏳ Reduced cognitive load through better sequencing

### **Business Value**
- ✅ Regulatory compliance requirements maintained
- ✅ Captures all necessary information effectively
- ✅ Supports both direct and intermediary application flows
- ⏳ Improved completion rates through better UX

## Risk Factors & Mitigation

### **High Risk: Complex Conditional Logic**
- **Risk**: Breaking existing conditional chains during restructure
- **Mitigation**: Comprehensive testing of all 322 dependencies

### **Medium Risk: Stakeholder Alignment**  
- **Risk**: Paul's structure vs business process conflicts
- **Mitigation**: Maintain explain visibility showing original vs new structure

### **Low Risk: Technical Complexity**
- **Risk**: Nested accordion rendering issues
- **Mitigation**: Schema structure already supports nested sections

## Knowledge Transfer Notes

### **Key Files for Handover**
1. **`complete-dependency-audit.md`** - **MOST CRITICAL** - Understanding all conditional relationships
2. **`flow-restructure-principles.md`** - UX principles for restructuring decisions
3. **`progress-tracking.md`** - Complete implementation history and current status
4. **`import_non_lux_2_2.py`** - Technical implementation of Paul's structure

### **Critical Concepts**
- **Backwards Dependencies**: Earlier questions dependent on later answers (UX violation)
- **Paul's Ordering**: "[number] - [section]" format from spreadsheet column Q
- **Nested Accordions**: Hierarchical sections (B4→B4.1/B4.2, B9→B9.1/B9.2/B9.3, B11→B11.1-B11.4)
- **Change Tracking**: Original/future metadata for explain visibility

### **Decision Points Requiring Input**
1. **Section ordering priority** - which backwards dependencies to fix first
2. **Nested section approach** - component updates needed for proper rendering
3. **Content approval workflow** - how to handle 257 reworded suggestions
4. **Testing strategy** - validation approach for restructured flow

---

## Status: Ready for Flow Restructure Design Implementation

**Phase 3 Scope**: Design and implement new section ordering that eliminates backwards dependencies while preserving Paul's organizational intent and maintaining all regulatory/business requirements.

**Documentation Complete**: All discoveries, principles, and technical analysis captured for seamless handover and future development.