# KYCP Design System

## Overview
This design system provides KYCP-faithful components for the RBSI institutional onboarding prototype. All components are built to exactly match KYCP's visual design and interaction patterns.

## Quick Links
- [Component Showcase](/showcase) - Interactive component playground
- [PRD](./PRD.md) - Product requirements for the showcase
- [Architecture Decision](./ADR-0001-component-architecture.md) - Why we built custom components
- [Component Catalog](./component-catalog.md) - Detailed specifications

## Design Principles

### Visual Language
- **Clean & Professional**: Enterprise-appropriate without being sterile
- **Consistent**: Unified spacing, colors, and interactions
- **Accessible**: WCAG 2.2 AA compliant
- **Familiar**: Matches KYCP patterns that users know

### Core Design Tokens
```css
/* Colors */
Primary: #0066CC
Gray: #808080 (headers)
Border: #D0D0D0
Error: #D32F2F

/* Spacing */
Base: 8px grid
Small: 8px
Medium: 16px
Large: 24px

/* Typography */
Base: 14px
Small: 13px
Large: 16px
```

## Component Categories

### Input Components
- **KycpInput** - Single-line text inputs
- **KycpTextarea** - Multi-line text input
- **KycpSelect** - Dropdown selection
- **KycpDatePicker** - Date selection

### Selection Components
- **KycpRadio** - Single choice from options
- **KycpCheckbox** - Multiple choices
- **KycpToggle** - On/off switch

### Layout Components
- **KycpFieldGroup** - Container with gray header
- **KycpFieldWrapper** - Field with label and error
- **KycpFormSection** - Logical grouping

### Feedback Components
- **KycpTag** - Removable selection chips
- **KycpError** - Error messages
- **KycpHelp** - Help text and hints

## Usage Example

```vue
<template>
  <KycpFieldGroup title="Required Group" subtitle="Program: Corporate Services">
    <KycpFieldWrapper 
      label="Name" 
      :required="true"
      :error="errors.name"
    >
      <KycpInput 
        v-model="formData.name"
        placeholder="Enter name"
      />
    </KycpFieldWrapper>
    
    <KycpFieldWrapper label="Entity Type">
      <KycpSelect 
        v-model="formData.entityType"
        :options="entityOptions"
      />
    </KycpFieldWrapper>
  </KycpFieldGroup>
</template>
```

## Development Guidelines

### Component Creation
1. All components use Vue 3 Composition API
2. Props are strongly typed with TypeScript
3. Emit events follow Vue conventions
4. Support v-model where appropriate

### Styling
1. Use CSS custom properties for theming
2. Follow BEM naming convention
3. Scope styles appropriately
4. Support dark mode (future)

### Accessibility
1. Semantic HTML elements
2. ARIA labels and descriptions
3. Keyboard navigation
4. Focus management
5. Screen reader support

## Testing
- Visual testing via showcase page
- Accessibility testing with axe
- Cross-browser testing
- Keyboard navigation testing

## Handover Notes for FinOpz

### Integration
1. Components are self-contained Vue SFCs
2. Styles use standard CSS (no preprocessors)
3. No external dependencies
4. TypeScript types included

### Customization
1. CSS custom properties for colors/spacing
2. Props for component configuration
3. Slots for content flexibility
4. Event handlers for interactions

### Migration Path
1. Components can be copied directly
2. Styles can be extracted to KYCP theme
3. Props map to KYCP component props
4. Minimal refactoring required

## Status
- ✅ Core components defined
- ✅ Design tokens established
- 🚧 Component implementation
- 🚧 Showcase page
- ⏳ Testing and refinement
- ⏳ FinOpz review

## Resources
- [Vue 3 Documentation](https://vuejs.org/)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [WCAG 2.2 Guidelines](https://www.w3.org/WAI/WCAG22/quickref/)

## Contact
For questions about the design system, contact the Nile design team or refer to the RBSI project documentation.