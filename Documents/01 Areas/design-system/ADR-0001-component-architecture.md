---
title: ADR-0001 - Component Architecture and Library Strategy
date: 2025-09-02
status: Accepted
deciders: [Nile Design Team, FinOpz Representatives]
---

# ADR-0001: Component Architecture and Library Strategy

## Status
Accepted

## Context
We need to build form components that exactly match KYCP's visual design and behavior for the RBSI institutional onboarding prototype. We must decide between:
1. Using an existing Vue component library (PrimeVue, Ant Design Vue, etc.)
2. Building custom components from scratch
3. Using a headless/unstyled library and applying custom styles

### Requirements
- **Visual Fidelity**: Components must exactly match KYCP appearance
- **Behavioral Parity**: Interactions must mirror KYCP patterns
- **Accessibility**: WCAG 2.2 AA compliance required
- **Maintainability**: FinOpz team must be able to understand and modify
- **Performance**: Lightweight, no unnecessary dependencies
- **Type Safety**: TypeScript support preferred

### KYCP Visual Characteristics (from reference image)
- Gray header bars (#808080) with white text
- Clean borders (#D0D0D0) with subtle radius (4px)
- Specific spacing patterns (8px, 12px, 16px, 24px)
- Tag/chip components for field selection
- Professional enterprise aesthetic
- No Material Design or modern gradient trends

## Decision
**Build custom Vue 3 components** with our own design system CSS, rather than using a third-party component library.

### Component Architecture
```
/components/kycp/
  ├── base/           # Atomic components
  │   ├── KycpInput.vue
  │   ├── KycpSelect.vue
  │   ├── KycpRadio.vue
  │   └── KycpCheckbox.vue
  ├── composite/      # Composed components
  │   ├── KycpFieldGroup.vue
  │   ├── KycpFieldWrapper.vue
  │   └── KycpTagInput.vue
  └── index.ts        # Barrel export
```

### Design System Structure
```
/assets/
  ├── kycp-design.css     # Design tokens and base styles
  ├── kycp-components.css # Component-specific styles
  └── kycp-utilities.css  # Utility classes
```

## Rationale

### Why Not Existing Libraries?

#### PrimeVue
- ✅ Comprehensive component set
- ❌ Opinionated styling difficult to override completely
- ❌ Includes many components we don't need (70+ KB extra)
- ❌ Their theme system doesn't match our needs

#### Ant Design Vue
- ✅ Enterprise-focused design
- ❌ Very opinionated, hard to match KYCP exactly
- ❌ Large bundle size (200+ KB)
- ❌ Chinese design patterns differ from UK enterprise

#### Vuetify
- ✅ Well-documented and mature
- ❌ Material Design doesn't match KYCP aesthetic
- ❌ Heavy framework (300+ KB)
- ❌ Difficult to remove Material Design patterns

#### Element Plus
- ✅ Clean design, enterprise-friendly
- ❌ Still requires significant customization
- ❌ Bundle size concerns
- ❌ Some components have fixed behaviors

### Why Custom Components?

1. **Exact Visual Match**
   - Full control over every pixel
   - No fighting with existing styles
   - Can match KYCP precisely

2. **Lightweight**
   - Only include what we need
   - No unused components or styles
   - Estimated 20-30 KB total vs 200-300 KB

3. **Maintainable**
   - Simple, readable code
   - No abstraction layers
   - FinOpz can understand and modify

4. **Progressive Enhancement**
   - Can add headless libraries later if needed
   - Start simple, enhance as required
   - No lock-in to library decisions

5. **Learning & Documentation**
   - Building from scratch ensures deep understanding
   - Better documentation for handover
   - Clear mapping to KYCP patterns

## Consequences

### Positive
- Complete control over component behavior and appearance
- Minimal bundle size and dependencies
- Clear, maintainable codebase
- Direct mapping to KYCP specifications
- No licensing concerns
- Can serve as reference implementation

### Negative
- More initial development time (estimated 2-3 days)
- Need to handle accessibility ourselves
- No community support/updates
- Must maintain component library
- Need to implement features like date pickers from scratch

### Mitigation Strategies
1. **Accessibility**: Use ARIA best practices guides and test with axe
2. **Complex Components**: Can integrate specific headless components if needed
3. **Testing**: Build comprehensive showcase page for testing
4. **Documentation**: Maintain detailed component specifications

## Implementation Plan

### Phase 1: Core Components (Week 1)
- KycpInput (text, number, email)
- KycpSelect (single selection)
- KycpRadio (radio group)
- KycpCheckbox (single and group)
- KycpTextarea (multiline)

### Phase 2: Layout Components (Week 1-2)
- KycpFieldGroup (gray header container)
- KycpFieldWrapper (label, help, error)
- KycpFormSection (logical grouping)

### Phase 3: Advanced Components (Week 2)
- KycpTag (removable chips)
- KycpDatePicker (if needed)
- KycpMultiSelect (if needed)

### Phase 4: Documentation (Week 2-3)
- Component showcase page
- Props documentation
- Usage examples
- Accessibility notes

## Review
This decision will be reviewed after Phase 1 implementation. If custom components prove too time-consuming or complex, we can pivot to a headless library approach.

## References
- KYCP Component Specifications (pending from FinOpz)
- Vue 3 Composition API Documentation
- ARIA Authoring Practices Guide
- Reference screenshot showing target visual style

## Sign-off
- [ ] Design Lead - Agreed with custom approach for exact KYCP match
- [ ] Technical Lead - Confirmed feasibility and timeline
- [ ] FinOpz Representative - Approved for alignment with KYCP
- [ ] Product Owner - Accepted timeline and approach