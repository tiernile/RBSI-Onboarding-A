# Claude Development Guide - RBSI Prototype

## Important Context
This is a Nuxt 3 (Vue) prototype for RBSI's institutional onboarding journeys. The app is schema-driven, with all content and validation coming from YAML files in `/data/schemas/`.

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
- Check `/data/schemas/manifest.yaml` for available journeys
- Each journey has stages/sections that group questions
- Conditional logic uses simple expressions: `field == "value"`
- Validation includes: required, regex, max_length

### API Endpoints
- `GET /api/manifest` - List of journeys with admin status
- `POST /api/auth/login` - Admin authentication
- `GET /api/schema/[journey]` - Get journey schema
- `GET /api/diff/[journey]` - Generate diff report
- `GET /api/export/[journey]` - Export to CSV

### Next Priority Tasks (as of Sept 2024)
- Complete remaining KYCP components (date, number, checkbox)
- Enhance accessibility (error summaries, focus management)
- Implement proper form validation and error handling
- Create evidence pack for stakeholder playback

## Quick Start for New Sessions
1. Check current state: `pnpm dev` and visit localhost:3000
2. Review `/Documents/01 Areas/session-context/` for latest progress
3. Check POC status in `/Documents/01 Areas/poc-workflow/README.md`
4. Always test changes in the browser - CSS scoping can be tricky!

## Remember
This prototype demonstrates the journey and gathers feedback. It's not production code, but it should feel production-ready to users testing it.