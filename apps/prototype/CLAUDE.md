# Claude Development Guide - RBSI Prototype

## Important Context
This is a Nuxt 3 (Vue) prototype for RBSI's institutional onboarding journeys. The app is schema-driven, with all content and validation coming from YAML files in `/data/schemas/`. The system includes advanced features: field grouping, complex fields, flow optimization, and comprehensive debugging tools.

**For Complete System Understanding**: See `/Documents/01 Areas/guide/System-Overview.md`

## Critical Things to Remember

### CSS and Styling
**⚠️ NEVER define CSS variables in scoped styles!**
- CSS custom properties (variables) MUST be defined in `app.vue` in non-scoped `<style>` blocks
- Component-specific styles go in `<style scoped>` blocks in individual components
- Vue's scoped styles transform selectors, so `:root` in scoped styles doesn't work globally

### Design Philosophy
- **Mission Control**: Flat, neutral, journey-agnostic design (no RBSI branding)
- **Form Journeys**: Will use KYCP-faithful components and RBSI branding
- Keep the two design systems separate and distinct

### Project Structure
```
/apps/prototype/
  /components/
    /kycp/        # KYCP-faithful form components
    /nile/        # Utility and layout components
  /composables/   # Vue composables for data/logic
  /pages/         # Route pages
  /server/        # API routes and server logic
  app.vue         # Global styles and root component
  CLAUDE.md       # This file - your guide!
```

### Environment Variables
- Place in `.env` or `.env.development` in THIS directory (`apps/prototype/`)
- Key variable: `NUXT_ADMIN_PASSWORD_HASH` for admin authentication
- Use `pnpm hash "password"` to generate bcrypt hashes

### Common Commands
```bash
# From apps/prototype directory:
pnpm dev          # Start dev server
pnpm build        # Build for production
pnpm hash "pwd"   # Generate password hash
pnpm scenarios    # Run scenario validation
pnpm fields       # Analyze field organization

# Import scripts (from apps/prototype):
python3 scripts/import_non_lux_1_1.py    # Current v1.1 import
python3 scripts/import_non_lux_2_2.py    # v2.2 Paul structure

# Debug URLs:
# http://localhost:3000/preview-kycp/[journey]?explain=1
# http://localhost:3000/api/conditions-report/[journey]?format=html
```

### Schema-First Approach
- All journey content lives in `/data/schemas/[journey]/schema.yaml`
- Components render from schema - never hardcode questions or validation
- Use composables: `useSchema()`, `useManifest()`, `useConditions()`, `useValidation()`

### Key Design Decisions
1. **Vue/Nuxt over React/Next**: Aligns with KYCP (client's platform)
2. **YAML schemas**: Human-readable, diffable, auditable
3. **No production code**: This is a high-fidelity prototype for handover
4. **Accessibility first**: WCAG 2.2 AA compliance is required

### Testing Approach
- Manual testing during development
- Accessibility checks with axe
- No PII or analytics in the prototype
- Admin features for controlling visibility

### Common Pitfalls to Avoid
1. **Don't put CSS variables in scoped styles** (they won't be global)
2. **Don't hardcode content** - always pull from schema
3. **Don't use `.env.local`** - Nuxt doesn't read it
4. **Don't create production-ready code** - this is a prototype
5. **Don't mix design systems** - Mission Control ≠ Form UI

### When Working on Forms
- **Available Journeys**: Check `/data/schemas/manifest.yaml`
- **Current Focus**: `non-lux-1-1` (AS-IS), `non-lux-lp-2-2` (Paul structure)
- **Section Organization**: Stages/sections group questions with field grouping
- **Conditional Logic**: Simple expressions (`field == "value"`) - debug with Explain Visibility
- **Flow Principle**: **Critical** - no backwards dependencies (later questions affecting earlier ones)
- **Validation**: Required, regex, max_length - enhanced error handling
- **Complex Fields**: Look for `type: complex` with `children[]` arrays

### API Endpoints
- `GET /api/manifest` - List of journeys with admin status
- `POST /api/auth/login` - Admin authentication
- `GET /api/schema/[journey]` - Get journey schema
- `GET /api/conditions-report/[journey]` - **NEW** - Comprehensive conditional logic validation
- `GET /api/conditions-report/[journey]?format=html` - **NEW** - HTML format for debugging
- `GET /api/diff/[journey]` - Generate diff report
- `GET /api/export/[journey]` - Export to CSV

### Current System Status (as of Sept 2024)
**✅ Completed Major Features**:
- **Field Grouping System**: Reduces cognitive load by up to 85% in complex sections
- **Complex Fields**: Repeatable components with add/remove functionality
- **Flow Optimization**: Backwards dependency elimination for better UX
- **Debug Tools**: Explain Visibility toggle and Conditions Report API
- **v2.2 Implementation**: Complete with Paul's structural optimizations
- **KYCP Compliance**: All components follow platform standards

**🔄 Current Focus**:
- Complex fields implementation completion
- Enhanced accessibility and error handling
- Stakeholder validation and feedback integration
- Documentation and knowledge transfer

## Quick Start for New Sessions
1. **System Overview**: Read `/Documents/01 Areas/guide/System-Overview.md` for complete context
2. **Current State**: `pnpm dev` and visit localhost:3000
3. **Latest Progress**: Check `/Documents/01 Areas/session-context/session-context-016.md`
4. **Latest Work**: Review `/Documents/01 Areas/creating-2-2/FINAL-HANDOVER.md` for v2.2 status
5. **Test with Debug Tools**: Use Explain Visibility (`?explain=1`) and Conditions Report
6. **CSS Caution**: Always test in browser - scoping can be tricky!

## Advanced Features & Debugging

### Explain Visibility Mode
- **Access**: Toggle in KYCP preview or append `?explain=1` to URL
- **Purpose**: Debug conditional logic, see field keys, understand visibility
- **Essential for**: Troubleshooting complex conditional dependencies

### Conditions Report API
- **Access**: Admin users - click "Conditions Report" on journey cards
- **Purpose**: Comprehensive validation of all conditional logic
- **Detects**: Unresolved keys, option mismatches, parse errors, dependency cycles
- **Critical for**: Pre-deployment validation

### Field Grouping System
- **Purpose**: Visual organization to reduce cognitive load
- **Implementation**: Configured in mapping JSON, applied during import
- **Impact**: Up to 85% reduction in cognitive load for complex sections
- **Usage**: Automatically applied to sections with >10 fields

### Complex Fields
- **Purpose**: Repeatable field groups with add/remove functionality
- **Components**: Uses ComplexGroupRepeater.vue
- **Data Structure**: Stored as array items under parent key
- **Implementation**: Parent field marked as `type: complex` with `children[]` array

## Remember
This prototype demonstrates the journey and gathers feedback. It's not production code, but it should feel production-ready to users testing it.