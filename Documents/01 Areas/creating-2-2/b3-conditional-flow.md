# B3 - Wholesale Depositor Conditional Flow Analysis

## Complete Dependency Chain

### **Root Trigger: UK Jurisdiction Selection**
```
B2 - Bank Relationship (Order 3)
├── Question: "In which jurisdiction would you like to open this account?"
├── Field: GENBankAccountJurisdiction  
├── Options: Jersey | Guernsey | Isle of Man | Gibraltar | United Kingdom
└── **TRIGGER**: User selects "United Kingdom" → Opens B3 section
```

### **Primary Entry Point: Business Type Assessment**
```
B3 - Wholesale Depositor (Order 7)
├── Question: "Does the business involve:"
├── Field: GENBusinessType
├── Visibility: Only when GENBankAccountJurisdiction == "United Kingdom"
├── Options:
│   ├── a) taking deposits or other repayable funds from the public and to grant credits
│   ├── b) taking deposits or other repayable funds from the public or to grant credits  
│   └── c) neither
└── **TRIGGER**: Any selection → Opens wholesale depositor assessment
```

### **Entity Type Classification**
```
S2 - Applicant Relationship (Order 8)  
├── Question: "Is the entity:"
├── Field: GENWholesaleDepositorEntityType
├── Visibility: When GENBusinessType has any value
├── Options:
│   ├── (a) body corporate / incorporated → Opens corporate assessment
│   ├── (b) Supranational Institution 
│   ├── (c) Government or Central Administrative Authority
│   ├── (d) Provincial, Regional, Local or Municipal Authority
│   ├── (e) unincorporated association ≤ £1.4m
│   ├── (f) unincorporated association ≤ £1.4m (expect > £1.4m in 6mo)
│   └── (g) unincorporated association > £1.4m
└── **BRANCHES**: Different paths based on entity type
```

## **Conditional Flow Tree**

### **Branch A: Corporate Entities**
```
GENWholesaleDepositorEntityType == "(a) body corporate"
│
├── GENStructureType (Order 9)
│   ├── Question: "Is the entity part of a consolidated group?"
│   ├── Options:
│   │   ├── (a) Yes, more than 80% → Consolidated Path
│   │   ├── (b) Yes, less than 80% → Standalone Path  
│   │   └── (c) No → Standalone Path
│   │
│   ├── **Consolidated Path** (80%+ ownership)
│   │   ├── GENConsolidated (Order 11)
│   │   │   ├── Question: "Does consolidated group meet financial criteria?"
│   │   │   ├── Yes → GENConsolidatedDetails (Order 12)
│   │   │   └── No → GENHalfyearConsolidated (Order 15)
│   │   │
│   │   └── GENHalfyearConsolidated → GENHalfyearConsolidatedDetails (Order 16)
│   │
│   └── **Standalone Path** (<80% or No)
│       ├── GENStandalone (Order 13)
│       │   ├── Question: "Does entity meet standalone financial criteria?"
│       │   ├── Yes → GENStandaloneDetails (Order 14)
│       │   └── No → Continue to asset assessment
│       │
│       └── **Asset Assessment Branch**
│           ├── GENStandaloneNetAssetsType
│           │   ├── (a) Currently > £1.4m → GENWholesaleDepositorType (Order 24)
│           │   └── (b) Expect > £1.4m in 6mo → GENEntity6monthsAssestValueType (Order 25)
│           │
│           └── **Fund/Group Asset Assessment**
│               ├── GENBankGroupOrFundType1 (Order 19)
│               │   ├── (a) Currently > £1.4m → GENConsolidatedGroupOrFundType (Order 21)
│               │   └── (b) Expect > £1.4m in 6mo → GENConsolidatedFund6monthsAssestValueType (Order 22)
```

## **Key Insights**

### **1. UK-Specific Regulatory Requirement**
- B3 - Wholesale Depositor section is **entirely UK-specific**
- Only appears when UK jurisdiction is selected in B2
- Implements UK regulatory wholesale depositor classification

### **2. Progressive Risk Assessment**
- **Step 1**: Business activity type (deposit-taking, etc.)
- **Step 2**: Entity legal structure 
- **Step 3**: Financial size and sophistication
- **Step 4**: Ownership structure complexity

### **3. Multiple Assessment Paths**
- **Corporate entities**: Complex branching based on group structure
- **Other entity types**: Different assessment criteria
- **Financial thresholds**: £1.4m net assets, £5.6m income, 50+ employees

### **4. Forward-Looking Assessment**
- Questions assess both current status and 6-month projections
- Accounts for entities that will meet criteria soon

## **Field Dependencies Summary**

| Field | Trigger Condition | Purpose |
|-------|------------------|---------|
| `GENBusinessType` | `GENBankAccountJurisdiction == "United Kingdom"` | Initial wholesale depositor assessment entry |
| `GENWholesaleDepositorEntityType` | Any `GENBusinessType` value | Entity classification |
| `GENStructureType` | Entity type "(a) body corporate" | Group vs standalone assessment |
| `GENConsolidated` | Structure type ≥80% group | Consolidated financial criteria |
| `GENStandalone` | Structure type <80% or standalone | Individual entity criteria |
| All other B3 fields | Cascading from above decisions | Detailed classification |

## **Business Logic**
This implements UK regulatory requirements for determining if an entity qualifies as a "wholesale depositor" - a classification that affects:
- Account opening eligibility
- Risk assessment requirements  
- Regulatory capital treatment
- Due diligence depth

The complex branching ensures accurate classification based on:
1. **Legal structure** (corporate, government, unincorporated)
2. **Financial size** (assets, income, employees)
3. **Group relationships** (consolidated vs standalone)
4. **Time horizon** (current vs projected status)