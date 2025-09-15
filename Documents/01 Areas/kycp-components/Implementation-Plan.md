# KYCP Components – Implementation Plan

Objective: evolve from PoC components to KYCP-faithful components with a portable schema adapter and comprehensive showcase.

## Phases & Tasks

1) Types & Adapters
- Add TypeScript types under `apps/prototype/types/kycp.ts` (FieldStyle, DataType, BaseField, ComplexGroup, etc.)
- Create a schema adapter: map current YAML items to `ComponentNode` runtime model; carry `internal_only` → `internal`
- Helpers: `resolveRight`, `isVisible`, validators per DataType

2) Component Library (Leafs)
- StringField, FreeTextArea, IntegerField, DecimalField, DateField, LookupField
- Respect status rights (disabled/hidden), apply validators, emit primitives (date as `DD/MM/YYYY`, numeric as number, lookup as option `value`)

3) Structure & Non-data
- StatementBlock, DividerLine, ActionButton (with `scriptId` hook)
- ComplexGroupRepeater (add/remove rows; nested rendering)

4) Showcase & Stories
- Expand `/pages/showcase.vue` to demo each component with states: editable, read-only, hidden-by-rule, invalid input, max length, etc.
- Include a mini example mirroring the PEP conditional pattern

5) Journey Integration
- Introduce adapter usage in `/preview/[journey].vue` (behind a flag) to render from `ComponentNode[]`
- Backward compatibility: keep current journey rendering path while adapter stabilises

6) Quality & Docs
- Minimal unit tests for validators and visibility logic
- ADR capturing mapping and trade-offs vs KYCP features
- Update README/CLAUDE with usage and constraints

## Acceptance Criteria
- Components render with correct states (hidden/readOnly/editable) based on provided status and rules
- Validation limits enforced per type; dates `DD/MM/YYYY` only; decimals rounded to 2dp
- Lookup emits stable codes; conditional visibility behaves as AND across conditions
- Complex groups function: add/remove rows and capture values per row
- Showcase demonstrates all components and key states

## Risks & Mitigations
- Divergence from KYCP behaviours → validate early with shared docs; log gaps as ADRs
- Adapter complexity → start with 1:1 mapping for common patterns; extend iteratively
- Schema mismatch → keep adapter isolated; maintain current YAML as data source

## Dependencies / Inputs
- KYCP component documentation (props, events, constraints)
- Example status flows (to validate status rights resolution)

