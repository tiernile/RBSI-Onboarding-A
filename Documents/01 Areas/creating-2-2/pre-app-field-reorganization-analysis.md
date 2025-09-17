# Pre-Application Field Reorganization Analysis

## Problem Statement

**Current Issue**: Fields conditional on "YES" to pre-application questions (`GENIndicativeAppetiteQuestions eq YES`) are scattered across multiple sections instead of being logically grouped in **B2 - Pre-Application Assessment**.

**Organizational Principle**: *"Anything marked as 'YES' to pre-application questions should appear in the pre-application assessment section"*

## Current Scattered Distribution

### **Pre-App Conditional Fields Found In:**
- **B4 - Introduction of Applicant**
- **B5 - Applicant Details** 
- **B7 - Controlling Parties**
- **B8 - PEPs**
- **B10 - Key Principal Risk Factors**
- **B11 - Purpose of Entity**
- **B13 - Use of Product**

## Complete Pre-App Field Inventory

### **Fields That Should Move to B2:**

#### **1. Entity & Registration (currently in B4/B5)**
- `GENIndicativeAppetite3rdPartyAdministrator` - "Does the entity have a 3rd party administrator?"
- `GENIndicativeAppetiteFundAdminDomicile` - "Where is the 3rd party administrator domiciled?"
- `GENIndicativeAppetiteCountryRegistration` - Country registration questions

#### **2. Controlling Parties (currently in B7)**
- `GENIndicativeAppetiteFundMng` - "Is there a Fund Manager within the structure?"
- `GENIndicativeAppetiteFundMngDom` - "Where is the Fund Manager domiciled?"
- `GENIndicativeAppetiteFundMngDomUSA` - "Is it Delaware or Non-Delaware?"
- `GENIndicativeAppetiteOpeningInvestmentAdviser` - "Is there an Investment Adviser?"
- `GENIndicativeAppetiteOpeningInvestmentAdviserLocation` - "What is the location of the Investment Adviser?"
- `GENIndicativeAppetiteOpeningInvestmentAdviserLocationUSA` - "Is it Delaware or Non-Delaware?"

#### **3. Investment & Risk Profile (currently in B10/B11)**
- `GENIndicativeAppetiteInvestmentsubsec` - "Type of Fund"
- `GENIndicativeAppetiteInvestmentsubsecOther` - "Other Type of Fund details"
- `GENIndicativeAppetiteInvesthighrisk` - High risk investment questions
- `GENIndicativeAppetiteInvestmentCountryComplex` - Investment countries
- `GENIndicativeAppetiteInvestmentCountry` - Country details
- `GENIndicativeAppetiteRiskadverse` - Risk adverse questions
- `GENIndicativeAppetiteRiskadversedetailsother` - Risk details

#### **4. Product Requirements (currently in B13)**
- `GENIndicativeAppetiteRBSIProductOptionsComplex` - RBSI product options
- `GENIndicativeAppetiteRBSIProductOptions` - Product selection
- `GENIndicativeAppetiteRBSIProductOptionsOther` - Other product details

## Impact Analysis

### **Current Problems:**
1. **Logical Inconsistency**: Pre-app questions scattered across 7+ sections
2. **User Confusion**: Similar questions appear in multiple places
3. **Broken Flow**: Pre-app assessment incomplete in B2
4. **Cognitive Load**: Users must remember pre-app context across many sections

### **Proposed Solution Benefits:**
1. **Logical Organization**: All pre-app questions in dedicated B2 section
2. **Complete Assessment**: B2 becomes comprehensive pre-application evaluation
3. **Clear User Flow**: Users complete all pre-app questions in one place
4. **Reduced Duplication**: Eliminate scattered pre-app variants

## Implementation Strategy

### **Phase 1: Field Section Remapping**
Update field section assignments in import script configuration:

```json
"field_section_mappings": {
  // Move all GENIndicativeAppetite* fields to B2
  "GENIndicativeAppetite3rdPartyAdministrator": "B2",
  "GENIndicativeAppetiteFundAdminDomicile": "B2", 
  "GENIndicativeAppetiteCountryRegistration": "B2",
  "GENIndicativeAppetiteFundMng": "B2",
  "GENIndicativeAppetiteFundMngDom": "B2",
  "GENIndicativeAppetiteFundMngDomUSA": "B2",
  "GENIndicativeAppetiteOpeningInvestmentAdviser": "B2",
  "GENIndicativeAppetiteOpeningInvestmentAdviserLocation": "B2",
  "GENIndicativeAppetiteOpeningInvestmentAdviserLocationUSA": "B2",
  "GENIndicativeAppetiteInvestmentsubsec": "B2",
  "GENIndicativeAppetiteInvestmentsubsecOther": "B2",
  "GENIndicativeAppetiteInvesthighrisk": "B2",
  "GENIndicativeAppetiteInvestmentCountryComplex": "B2",
  "GENIndicativeAppetiteInvestmentCountry": "B2",
  "GENIndicativeAppetiteRiskadverse": "B2",
  "GENIndicativeAppetiteRiskadversedetailsother": "B2",
  "GENIndicativeAppetiteRBSIProductOptionsComplex": "B2",
  "GENIndicativeAppetiteRBSIProductOptions": "B2",
  "GENIndicativeAppetiteRBSIProductOptionsOther": "B2"
}
```

### **Phase 2: B2 Field Grouping Configuration**
Extend field grouping system to organize the expanded B2 section:

```javascript
'b2-pre-application-assessment': {
  groups: [
    { title: 'Entity Structure', pattern: /^GENIndicativeAppetite.*(3rdParty|Admin|Country)/ },
    { title: 'Controlling Parties', pattern: /^GENIndicativeAppetite.*(Fund|Investment)/ },
    { title: 'Investment Profile', pattern: /^GENIndicativeAppetite.*(Investment|Risk)/ },
    { title: 'Product Requirements', pattern: /^GENIndicativeAppetite.*Product/ }
  ]
}
```

### **Phase 3: Dependency Chain Updates**
Ensure all child dependencies follow their parents to B2:
- Fund Manager → Domicile → Delaware chain
- Investment Adviser → Location → Delaware chain  
- Investment Type → Other details chain
- Product Options → Other details chain

## Expected B2 Structure After Reorganization

### **B2 - Pre-Application Assessment (Expanded)**
```
Do you wish to answer Pre-Application Questions? (existing)

[If YES to above, show all grouped pre-app fields:]

Entity Structure:
├── Does the entity have a 3rd party administrator?
├── Where is the 3rd party administrator domiciled?
└── Country registration details

Controlling Parties:
├── Is there a Fund Manager?
│   ├── Where is domiciled?
│   └── Delaware or Non-Delaware?
└── Is there an Investment Adviser?
    ├── What is the location?
    └── Delaware or Non-Delaware?

Investment Profile:
├── Type of Fund
├── Investment countries
├── High risk investments
└── Risk adverse details

Product Requirements:
├── RBSI Product Options
└── Other product details
```

## Risk Assessment

### **Low Risk Changes:**
- ✅ Field section remapping (configuration change only)
- ✅ Field grouping addition (extends existing system)
- ✅ No impact on field logic or dependencies

### **Medium Risk Considerations:**
- ⚠️ B2 will become large section (20+ fields)
- ⚠️ Need to test all dependency chains still work
- ⚠️ Visual organization critical for usability

### **Mitigation Strategies:**
- Use field grouping to organize B2 sub-sections
- Preserve all existing dependency relationships
- Test thoroughly across all user journeys

## Success Criteria

### **Organizational Improvements:**
- ✅ All pre-app fields logically grouped in B2
- ✅ No pre-app fields scattered in other sections
- ✅ Clear separation between pre-app and main assessment

### **User Experience:**
- ✅ Complete pre-app assessment in one location
- ✅ Clear visual organization of pre-app topic areas
- ✅ Logical flow from pre-app to main form sections

### **Technical Quality:**
- ✅ All dependency chains preserved
- ✅ No broken field relationships
- ✅ Maintain all existing business logic

## Implementation Priority

**HIGH PRIORITY** - This addresses a fundamental organizational inconsistency that affects user comprehension and form logic.

## Next Steps

1. **Update import script** with field section mappings
2. **Add B2 field grouping** configuration  
3. **Regenerate v2.2 schema** with reorganized sections
4. **Test all dependency chains** work correctly
5. **Validate user experience** with consolidated B2

---

**Result**: Transform B2 from minimal section to comprehensive pre-application assessment, eliminating organizational inconsistencies and improving user flow.**