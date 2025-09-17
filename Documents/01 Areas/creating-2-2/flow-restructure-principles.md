# Flow Restructure Principles - v2.2 UX Enhancement

## Core UX Principles for Question Ordering

### **Principle 1: Dependency Direction Rule** 
**Critical**: Questions should only depend on **earlier** answers, never later ones
- **Upstream questions** must never be conditional on downstream selections
- **Forward dependencies** (early → late) are acceptable
- **Backward dependencies** (late → early) create poor UX and must be eliminated

### **Principle 2: Decision Points First**
- Critical branching decisions should come as early as possible
- Major flow determinants should precede dependent content
- **Jurisdiction selection** is the biggest branching factor - should be very early
- **Entity type** and **Application type** affect multiple downstream sections

### **Principle 3: Natural Information Flow**
- Follow logical business conversation order
- Start with **"What"** and **"Where"** before **"How"** and **"Who"**
- Basic facts before complex assessments
- Regulatory requirements before detailed information gathering

### **Principle 4: Cognitive Load Management**
- Simple decisions before complex ones
- Factual questions before subjective assessments
- Clear progression from general to specific
- Avoid surprising users with unexpected section appearances

### **Principle 5: Platform Constraint Awareness**
- **Accordion limitations**: Cannot conditionally show/hide entire accordions
- Must work within accordion-based section structure
- Consider field-level vs section-level conditional logic
- Progressive disclosure within sections rather than section hiding

## Current Dependency Violations Identified

### **Critical Backwards Dependencies**
1. **B1 Pre-App Questions** → Depends on **UK jurisdiction selection** (from B2)
   - **Problem**: First section depends on later answer
   - **Impact**: B1 questions surprisingly appear/disappear
   - **Solution**: Move jurisdiction selection to very beginning

2. **Other potential violations** need comprehensive audit

### **Forward Dependencies (Acceptable but Need Management)**
1. **B2 Jurisdiction** → **B3 Wholesale Depositor** (UK-specific)
2. **B4 Application Type** → **B4.1/B4.2 Subsections** 
3. **B5 Entity Type** → **B6 Tax Classifications**
4. **B7 Controlling Parties** → **B8 PEPs Assessment**
5. **B9 Ownership Structure** → **B10 Risk Factors**
6. **B11 Business Purpose** → **B12 Banking Requirements**

## Proposed Ordering Principles

### **Tier 1: Fundamental Decisions (New B1-B2)**
**Purpose**: Establish core branching factors early
1. **Jurisdiction selection** - eliminates backwards dependency for current B1
2. **Entity type classification** - affects multiple downstream sections
3. **Application type** (direct vs intermediary) - determines form completion context

### **Tier 2: Regulatory Assessments (New B3-B4)**  
**Purpose**: Handle regulatory requirements early in process
4. **Pre-application appetite** questions (move from current B1)
5. **Jurisdiction-specific requirements** (UK wholesale depositor, etc.)

### **Tier 3: Core Entity Information (B5-B7)**
**Purpose**: Gather fundamental entity details
6. **Entity details and formation**
7. **Tax classification** (depends on entity type from Tier 1)
8. **Controlling parties and ownership** (depends on entity structure)

### **Tier 4: Risk and Purpose Assessment (B8-B11)**
**Purpose**: Evaluate risk and business purpose
9. **PEPs and risk factors** (triggered by controlling parties)
10. **Business purpose and activities**
11. **Countries and cashflow** (depends on business purpose)

### **Tier 5: Banking Requirements (B12-B13)**
**Purpose**: Determine specific banking needs
12. **Account and service requirements** (informed by all previous sections)
13. **Product usage details** (depends on account requirements)

## Platform Considerations

### **Accordion Limitations**
- Cannot conditionally show/hide entire accordions
- Must use field-level conditional logic within visible accordions
- Consider merging related conditional sections
- Use progressive disclosure within accordions

### **User Experience Impact**
- **Transparency**: Users should understand what sections they'll encounter
- **Progress indication**: Clear sense of journey length and complexity
- **Back-navigation**: Changes to early answers should not dramatically alter later sections
- **Cognitive load**: Minimize surprises and unexpected section appearances

## Implementation Strategy

### **Phase 1: Eliminate Backwards Dependencies**
1. **Move jurisdiction selection** to new B1 position
2. **Restructure current B1** as new B3 (after jurisdiction known)
3. **Audit all other backwards dependencies**

### **Phase 2: Optimize Forward Dependencies** 
1. **Group related conditional sections** where possible
2. **Use progressive disclosure** within sections
3. **Add transparency features** (conditional section previews)

### **Phase 3: Test and Validate**
1. **User testing** of new flow sequence
2. **Validate all conditional logic** still works correctly
3. **Ensure no new backwards dependencies** introduced

## Key Decision Points to Resolve

### **Decision A: Jurisdiction Timing**
Should jurisdiction be the **very first question**?
- **Pro**: Eliminates all backwards dependencies for B1
- **Con**: Might feel abrupt to start with regulatory choice
- **Recommendation**: Yes - explain context with intro text

### **Decision B: Entity Type Early Classification**  
Should entity type come very early (new B2)?
- **Pro**: Reduces cascade complexity in B5-B8
- **Con**: User might not know entity type without context
- **Recommendation**: Yes - with help text explaining why it's needed

### **Decision C: Application Type Positioning**
Should "direct vs intermediary" come before entity details?
- **Pro**: Determines who is filling out the form
- **Con**: Might need entity context first
- **Recommendation**: Yes - fundamental to form completion context

### **Decision D: Section Consolidation**
Should highly interdependent sections be merged?
- **B9 Ownership + B10 Risk**: Logical flow from ownership to risk
- **B11 Purpose + B12 Requirements**: Business purpose drives banking needs
- **Recommendation**: Consider for B9+B10, keep B11+B12 separate

## Success Criteria

### **Technical**
- ✅ Zero backwards dependencies in final flow
- ✅ All conditional logic functions correctly
- ✅ Maintains Paul's B-section organizational intent

### **User Experience**
- ✅ Logical, intuitive question progression
- ✅ No surprising section appearances
- ✅ Clear sense of journey scope and progress
- ✅ Reduced cognitive load through better sequencing

### **Business**
- ✅ Maintains regulatory compliance requirements
- ✅ Captures all necessary information effectively
- ✅ Supports both direct and intermediary application flows

## Status: Ready for Implementation
All core principles documented. Next steps:
1. Complete dependency audit
2. Design specific new section structure
3. Update v2.2 schema with new ordering
4. Test flow logic and user experience