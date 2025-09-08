# RBSI Onboarding Prototype - Comprehensive Handover Document

**Date**: 2025-09-02  
**Session**: 002  
**Status**: POC functional with KYCP component library

## 🎯 Project Overview

### What We're Building
A high-fidelity prototype for RBSI's institutional onboarding journeys that:
- Demonstrates form flows with exact KYCP component styling
- Validates the schema-first approach (spreadsheet → YAML → UI)
- Provides audit trail with diff/export capabilities
- Serves as reference implementation for FinOpz handover

### Current State
- ✅ Mission Control dashboard operational
- ✅ KYCP component library built and documented
- ✅ Component showcase with interactive demos
- ✅ Preview pages rendering with professional styling
- ✅ Schema-driven forms working with conditions
- ⚠️ Select dropdown rendering issue (fixed with v-if approach)

## 🏗️ Architecture

### Tech Stack
```
Frontend:    Vue 3 + Nuxt 3
Styling:     Custom CSS with design tokens
Data:        YAML schemas
Auth:        Bcrypt hashed admin password
Deployment:  Static generation (planned)
```

### Directory Structure
```
/apps/prototype/
├── pages/
│   ├── index.vue           # Mission Control dashboard
│   ├── showcase.vue        # Component library showcase
│   ├── about.vue          # About page
│   └── preview/
│       └── [journey].vue   # Dynamic journey preview
├── components/
│   ├── kycp/
│   │   └── base/          # KYCP-faithful components
│   │       ├── KycpInput.vue
│   │       ├── KycpSelect.vue
│   │       ├── KycpRadio.vue
│   │       ├── KycpTextarea.vue
│   │       ├── KycpFieldWrapper.vue
│   │       ├── KycpFieldGroup.vue
│   │       └── KycpTag.vue
│   └── nile/              # Utility components
├── composables/
│   ├── useManifest.ts     # Journey manifest loader
│   ├── useSchema.ts       # Schema loader
│   ├── useConditions.ts   # Conditional logic engine
│   └── useValidation.ts   # Form validation
├── server/
│   └── api/
│       ├── manifest.get.ts
│       ├── schema/[journey].get.ts
│       ├── diff/[journey].get.ts
│       ├── export/[journey].get.ts
│       └── auth/login.post.ts
└── assets/
    └── kycp-design.css    # Design system tokens

/data/
├── schemas/
│   ├── manifest.yaml      # Journey registry
│   └── non-lux-lp-demo/
│       └── schema.yaml    # Demo journey schema
└── generated/             # Diff/export outputs

/Documents/01 Areas/
├── project-context.md     # Why and what
├── project-structure.md   # How we work
├── mission-control-design.md
├── design-system/         # Component documentation
├── poc-workflow/          # POC plans and status
├── session-context/       # Progress tracking
└── HANDOVER.md           # This file
```

## 🎨 Design Systems

### Two Distinct Design Languages

#### 1. Mission Control (Admin Dashboard)
- **Style**: Flat, clean, journey-agnostic
- **Colors**: Light gray background (#FAFBFC), white cards
- **No branding**: Intentionally neutral
- **Status pills**: Bold colors (red/amber/green)
- **Location**: `/apps/prototype/pages/index.vue`

#### 2. KYCP Forms (Journey Pages)
- **Style**: Matches KYCP exactly
- **Gray headers**: #808080 background with white text
- **Clean inputs**: 1px border (#D0D0D0), 4px radius
- **Professional**: Enterprise-appropriate
- **Location**: `/apps/prototype/components/kycp/`

### Design Tokens (CSS Variables)
```css
/* In app.vue - GLOBAL scope */
--kycp-primary: #0066CC;
--kycp-gray-500: #808080;  /* Header backgrounds */
--kycp-input-border: #D0D0D0;
--kycp-error: #D32F2F;
/* ... see kycp-design.css for full list */
```

## 🚨 Critical Issues & Solutions

### 1. CSS Variable Scoping
**Problem**: CSS variables in `<style scoped>` don't work globally in Vue  
**Solution**: Move all CSS variables to `app.vue` in non-scoped block  
**File**: `/apps/prototype/app.vue`

### 2. Dynamic Component Registration
**Problem**: `<component :is="componentName">` failed with string names  
**Solution**: Use explicit `v-if/v-else-if` for each component type  
**File**: `/apps/prototype/pages/preview/[journey].vue` lines 45-81

### 3. Environment Variables
**Location**: `/apps/prototype/.env`  
**Required**: `NUXT_ADMIN_PASSWORD_HASH`  
**Generate**: `pnpm hash "YourPassword"`  
**Note**: Don't use `.env.local` - Nuxt doesn't read it

## 📍 Current URLs & Routes

```
http://localhost:3000/              # Mission Control
http://localhost:3000/showcase      # Component showcase
http://localhost:3000/about         # About page
http://localhost:3000/preview/non-lux-lp-demo  # Demo journey

# API Endpoints
/api/manifest                       # Journey list
/api/schema/non-lux-lp-demo        # Journey schema
/api/diff/non-lux-lp-demo          # Generate diff
/api/export/non-lux-lp-demo        # Export CSV
/api/auth/login                     # Admin login
```

## 🔧 Common Tasks

### Start Development Server
```bash
cd apps/prototype
pnpm dev
# Visit http://localhost:3000
```

### Add New Component
1. Create in `/components/kycp/base/`
2. Follow existing patterns (v-model support, TypeScript props)
3. Add to showcase page
4. Update preview page v-if conditions

### Add New Journey
1. Create schema in `/data/schemas/[journey-key]/schema.yaml`
2. Add entry to `/data/schemas/manifest.yaml`
3. Preview at `/preview/[journey-key]`

### Update Styling
1. Global variables: `/apps/prototype/app.vue`
2. Design tokens: `/apps/prototype/assets/kycp-design.css`
3. Component styles: In component `<style scoped>` blocks

## 📋 POC Status

### Completed ✅
- [x] Schema-first pipeline working
- [x] KYCP component library (8 components)
- [x] Component showcase with code examples
- [x] Mission Control with admin auth
- [x] Preview pages with proper styling
- [x] Conditional logic engine
- [x] Diff/export functionality
- [x] Design system documentation

### In Progress 🚧
- [ ] Additional KYCP components (date, checkbox)
- [ ] Comprehensive accessibility testing
- [ ] Error summary improvements
- [ ] Performance optimization

### Not Started ⏳
- [ ] Production deployment
- [ ] Visual regression testing
- [ ] Multi-journey testing
- [ ] FinOpz handover package

## 🐛 Known Issues

### 1. Select Component Rendering
**Issue**: Select dropdown may not show options  
**Fix**: Using v-if approach instead of dynamic components  
**Status**: Fixed in latest version

### 2. Route Confusion
**Issue**: Sometimes shows preview page on homepage  
**Fix**: Clear browser cache, restart dev server  
**Prevention**: Always use NuxtLink for navigation

### 3. Component Import Errors
**Issue**: "Cannot find module" errors  
**Fix**: Ensure proper import paths with `~/` prefix  
**Example**: `import KycpInput from '~/components/kycp/base/KycpInput.vue'`

## 🎯 Next Session Priorities

1. **Complete remaining KYCP components**
   - KycpCheckbox
   - KycpDatePicker
   - KycpMultiSelect

2. **Accessibility improvements**
   - Error summary anchoring
   - Focus management
   - ARIA live regions

3. **Testing & validation**
   - Cross-browser testing
   - Mobile responsiveness
   - Journey flow testing

4. **Documentation**
   - API documentation
   - Deployment guide
   - FinOpz integration guide

## 📚 Key Documentation Files

1. **Project Context**: `/Documents/01 Areas/project-context.md`
   - Why the project exists
   - Success metrics (80% RFT)
   - Stakeholder requirements

2. **Project Structure**: `/Documents/01 Areas/project-structure.md`
   - Development workflow
   - Branching strategy
   - PR requirements

3. **POC Workflow**: `/Documents/01 Areas/poc-workflow/README.md`
   - Implementation phases
   - Status tracker
   - Acceptance criteria

4. **Design System**: `/Documents/01 Areas/design-system/`
   - PRD for component showcase
   - ADR for architecture decisions
   - Component specifications

5. **Session Contexts**: `/Documents/01 Areas/session-context/`
   - session-context-001.md: Initial setup
   - session-context-002.md: Component library creation

## 🔑 Key Decisions Made

1. **Vue/Nuxt over React/Next**
   - Aligns with KYCP (client's platform)
   - Better handover compatibility

2. **Custom components over libraries**
   - Exact KYCP match required
   - No unnecessary dependencies
   - Full control over behavior

3. **Schema-first approach**
   - Single source of truth
   - Auditable changes
   - Clean separation of data/UI

4. **Flat design for Mission Control**
   - Journey-agnostic
   - Professional without branding
   - Clear information hierarchy

## 💡 Tips for Next Developer

1. **Always check CSS scoping** - Global variables must be in app.vue
2. **Use v-if for component switching** - More reliable than dynamic components
3. **Test in multiple browsers** - Especially Safari for form controls
4. **Keep schemas clean** - They drive everything
5. **Document decisions** - Future you will thank you
6. **Run pnpm dev from /apps/prototype** - Not from root
7. **Check CLAUDE.md** - Has specific gotchas for this project

## 🚀 Quick Start for New Session

```bash
# 1. Navigate to project
cd /Users/tiernaugh/Documents/PARA/Areas/Nile/01 Projects/RBSI-onboarding/apps/prototype

# 2. Start dev server
pnpm dev

# 3. Open browser
open http://localhost:3000

# 4. Check latest session context
cat ../../../Documents/01\ Areas/session-context/session-context-002.md

# 5. Review this handover
cat ../../../Documents/01\ Areas/HANDOVER.md
```

## 📞 Support & Resources

- **Component Issues**: Check `/apps/prototype/CLAUDE.md`
- **Schema Questions**: See `/data/schemas/README.md`
- **Design Decisions**: Review ADRs in `/Documents/01 Areas/design-system/`
- **Git History**: Detailed commit messages explain changes

---

**Remember**: This is a prototype for demonstration and testing. It's not production code, but it should feel production-ready to users testing it.

**Last Updated**: 2025-09-02 by Assistant in Session 002