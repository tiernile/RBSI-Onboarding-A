# B7 Field Consolidation Implementation Strategy

## Overview
Detailed technical implementation plan to consolidate B7 "Controlling Parties" from 17 fields to 8 fields while maintaining all business logic and improving user experience.

## Implementation Approach

### **Phase 1: Import Script Modifications**

#### **1.1 Field Consolidation Logic**
Update `import_non_lux_2_2.py` to implement field merging during schema generation.

**New Function: `consolidate_duplicate_fields()`**
```python
def consolidate_duplicate_fields(fields: list, section: str) -> list:
    """
    Consolidate functionally duplicate fields in specified section.
    Combines fields with same label using OR visibility conditions.
    """
    if section != "B7 - Controlling Parties":
        return fields
    
    consolidated = []
    processed_labels = set()
    
    # Group fields by label
    field_groups = {}
    for field in fields:
        label = field.get('label', '').strip()
        if label not in field_groups:
            field_groups[label] = []
        field_groups[label].append(field)
    
    # Process each group
    for label, group in field_groups.items():
        if len(group) == 1:
            # Single field - no consolidation needed
            consolidated.append(group[0])
        else:
            # Multiple fields with same label - consolidate
            consolidated_field = consolidate_field_group(group, label)
            consolidated.append(consolidated_field)
    
    return consolidated
```

#### **1.2 Field Group Consolidation**
```python
def consolidate_field_group(field_group: list, label: str) -> dict:
    """
    Merge multiple fields with same label into single field with OR conditions.
    """
    # Use the unconditional field as base (GEN* without prefixes)
    base_field = None
    conditional_fields = []
    
    for field in field_group:
        key = field.get('key', '')
        if not ('IndicativeAppetite' in key or 'UK' in key):
            base_field = field
        else:
            conditional_fields.append(field)
    
    if not base_field:
        base_field = field_group[0]  # Fallback to first field
    
    # Start with base field
    consolidated = copy.deepcopy(base_field)
    
    # Combine visibility conditions
    if conditional_fields:
        all_conditions = []
        
        # Add existing conditions from base field
        if base_field.get('visibility'):
            all_conditions.extend(base_field['visibility'])
        
        # Add conditions from other fields
        for field in conditional_fields:
            if field.get('visibility'):
                all_conditions.extend(field['visibility'])
        
        # Set combined visibility with OR logic
        if all_conditions:
            consolidated['visibility'] = [{
                'entity': 'entity',
                'targetKeys': [],
                'allConditionsMustMatch': False,  # OR logic
                'conditions': flatten_conditions(all_conditions)
            }]
    
    # Update metadata to reflect consolidation
    consolidated['_metadata']['consolidation_source'] = [f['key'] for f in field_group]
    consolidated['_metadata']['consolidation_count'] = len(field_group)
    
    return consolidated
```

#### **1.3 Field Ordering for Visual Hierarchy**
```python
def reorder_b7_fields_for_hierarchy(fields: list) -> list:
    """
    Reorder B7 fields to group parent-child relationships together.
    """
    b7_field_order = {
        # Secretary group
        'GENSecretary': 143.0,
        'GENSecretaryName': 143.1,
        
        # Fund Manager group  
        'GENFundMngr': 145.0,
        'GENFundMngDom': 145.1,
        'GENFundMngDomUSA': 145.2,
        
        # Investment Adviser group
        'GENOpeningInvestmentAdviser': 148.0,
        'GENOpeningInvestmentAdviserLocation': 148.1,
        'GENOpeningInvestmentAdviserLocationUSA': 148.2,
        
        # Partnership structure
        'GENlimitedpartnershipstructure': 152.0
    }
    
    def get_hierarchy_order(field):
        key = field.get('key', '')
        base_key = get_base_field_key(key)  # Remove IndicativeAppetite/UK prefixes
        return b7_field_order.get(base_key, 999.0)
    
    return sorted(fields, key=get_hierarchy_order)
```

### **Phase 2: Schema Generation Updates**

#### **2.1 Consolidated Field Mapping**
Update the field mapping configuration to specify consolidation targets:

**Add to `non-lux-lp-2-2.json`:**
```json
{
  "field_consolidation_rules": {
    "B7 - Controlling Parties": {
      "fund_manager_group": {
        "target_key": "GENFundMngr",
        "source_keys": [
          "GENFundMngr",
          "GENIndicativeAppetiteFundMng", 
          "GENUKIndicativeAppetiteFundMng"
        ],
        "child_mappings": {
          "domicile": {
            "target_key": "GENFundMngDom",
            "source_keys": [
              "GENFundMngDom",
              "GENIndicativeAppetiteFundMngDom",
              "GENUKIndicativeAppetiteFundMngDom"
            ]
          },
          "delaware": {
            "target_key": "GENFundMngDomUSA", 
            "source_keys": [
              "GENFundMngDomUSA",
              "GENIndicativeAppetiteFundMngDomUSA",
              "GENUKIndicativeAppetiteFundMngDomUSA"
            ]
          }
        }
      },
      "investment_adviser_group": {
        "target_key": "GENOpeningInvestmentAdviser",
        "source_keys": [
          "GENOpeningInvestmentAdviser",
          "GENIndicativeAppetiteOpeningInvestmentAdviser",
          "GENUKIndicativeAppetiteOpeningInvestmentAdviser"
        ],
        "child_mappings": {
          "location": {
            "target_key": "GENOpeningInvestmentAdviserLocation",
            "source_keys": [
              "GENOpeningInvestmentAdviserLocation", 
              "GENIndicativeAppetiteOpeningInvestmentAdviserLocation",
              "GENUKIndicativeAppetiteOpeningInvestmentAdviserLocation"
            ]
          },
          "delaware": {
            "target_key": "GENOpeningInvestmentAdviserLocationUSA",
            "source_keys": [
              "GENOpeningInvestmentAdviserLocationUSA",
              "GENIndicativeAppetiteOpeningInvestmentAdviserLocationUSA", 
              "GENUKIndicativeAppetiteOpeningInvestmentAdviserLocationUSA"
            ]
          }
        }
      }
    }
  }
}
```

#### **2.2 Visibility Condition Logic**
**Consolidated Fund Manager Visibility:**
```yaml
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
  # Field also appears when neither condition is met (default case)
```

**Child Field Dependencies:**
Child fields still reference the consolidated parent:
```yaml
# Fund Manager Domicile field
visibility:
- entity: entity
  targetKeys: []
  allConditionsMustMatch: true
  conditions:
  - sourceKey: GENFundMngr  # References consolidated parent
    operator: eq
    value: 'Yes'
```

### **Phase 3: Visual Grouping Implementation**

#### **3.1 Section Sub-Headers**
Add visual grouping to KYCP components:

**Update `KycpSection.vue`:**
```vue
<template>
  <div class="kycp-section">
    <div v-if="hasSubGroups" class="section-with-subgroups">
      <div v-for="group in fieldGroups" :key="group.title" class="field-group">
        <h4 class="field-group-title">{{ group.title }}</h4>
        <div class="field-group-content">
          <KycpField 
            v-for="field in group.fields" 
            :key="field.key"
            :field="field"
            :class="getFieldHierarchyClass(field)"
          />
        </div>
      </div>
    </div>
    <div v-else class="section-flat">
      <!-- Standard flat field list -->
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    fieldGroups() {
      if (this.section.title !== 'B7 - Controlling Parties') {
        return []
      }
      
      return [
        {
          title: 'Secretary Information',
          fields: this.getFieldsByPattern(['GENSecretary'])
        },
        {
          title: 'Fund Manager Details', 
          fields: this.getFieldsByPattern(['GENFundMngr'])
        },
        {
          title: 'Investment Adviser Details',
          fields: this.getFieldsByPattern(['GENOpeningInvestmentAdviser'])
        },
        {
          title: 'Partnership Structure',
          fields: this.getFieldsByPattern(['GENlimitedpartnershipstructure'])
        }
      ]
    }
  },
  
  methods: {
    getFieldHierarchyClass(field) {
      const key = field.key
      if (key.includes('Name') || key.includes('Dom') || key.includes('Location')) {
        return 'field-level-1'  // Child field
      }
      if (key.includes('USA')) {
        return 'field-level-2'  // Grandchild field
      }
      return 'field-level-0'  // Parent field
    }
  }
}
</script>

<style scoped>
.field-group {
  margin-bottom: 2rem;
}

.field-group-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-text-strong);
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--color-border-subtle);
}

.field-level-1 {
  margin-left: 1.5rem;
}

.field-level-2 {
  margin-left: 3rem;
}
</style>
```

### **Phase 4: Testing Strategy**

#### **4.1 Scenario Testing Matrix**
Test all user journey combinations:

| Scenario | Pre-App Qs | Jurisdiction | Expected Fields |
|----------|-------------|--------------|----------------|
| 1 | YES | UK | All consolidated fields visible |
| 2 | YES | Non-UK | All consolidated fields visible |
| 3 | NO | UK | All consolidated fields visible |
| 4 | NO | Non-UK | All consolidated fields visible |

#### **4.2 Dependency Chain Testing**
For each scenario, verify:
- [ ] Parent questions appear
- [ ] Child questions appear only when parent = Yes
- [ ] Grandchild questions appear only when child = United States
- [ ] No duplicate questions visible
- [ ] All original business logic preserved

#### **4.3 Field Count Validation**
**Before**: 17 fields in B7 section  
**After**: 8 fields in B7 section  
**Reduction**: 53% fewer fields

### **Phase 5: Implementation Steps**

#### **Step 1: Update Import Script**
1. Add consolidation functions to `import_non_lux_2_2.py`
2. Update field processing pipeline to call consolidation
3. Test with copy map to ensure proper merging

#### **Step 2: Update Field Mapping**
1. Add consolidation rules to `non-lux-lp-2-2.json`
2. Define visual grouping configuration
3. Specify hierarchy classes for styling

#### **Step 3: Regenerate Schema**
1. Run updated import script
2. Verify consolidated fields in generated schema
3. Check field count reduction achieved

#### **Step 4: Update Frontend Components**
1. Add visual grouping support to KycpSection
2. Implement hierarchy styling
3. Test rendering with new structure

#### **Step 5: Comprehensive Testing**
1. Test all user journey scenarios
2. Verify field visibility in browser
3. Confirm no functionality lost
4. Validate improved user experience

## Risk Mitigation

### **Data Integrity**
- Preserve all original field keys in metadata
- Maintain audit trail of consolidation
- Document all condition changes

### **Functionality Preservation** 
- Test every visibility condition combination
- Verify all dependency chains work
- Ensure no business logic lost

### **Rollback Plan**
- Keep original field definitions in metadata
- Implement toggle to use original vs consolidated
- Document reversal process

## Success Criteria

### **Quantitative Targets**
- [ ] 50%+ reduction in field count (Target: 17 → 8 fields)
- [ ] No functionality lost (all scenarios work)
- [ ] No duplicate questions visible to users

### **Qualitative Improvements**
- [ ] Clear parent-child visual relationships
- [ ] Logical question grouping
- [ ] Improved user comprehension
- [ ] Reduced cognitive load

## Timeline
- **Phase 1-2**: Import script & schema updates (1-2 hours)
- **Phase 3**: Visual grouping implementation (1-2 hours)  
- **Phase 4-5**: Testing & validation (1 hour)
- **Total**: 3-5 hours implementation time

---

**This strategy transforms B7 from a confusing, duplicate-heavy section into a clear, logical user experience while preserving all business requirements.**