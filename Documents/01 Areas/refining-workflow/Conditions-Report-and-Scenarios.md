# Conditions Report and Scenario Checks

## Conditions Report

- Endpoint: `/api/conditions-report/:journey` returns JSON; add `?format=html` for a quick HTML table.
- Access: Mission Control → Admin → each card now includes a "Conditions Report" link that opens the HTML table.
- Lints included:
  - Unresolved controller keys in conditions (misspells, missing fields)
  - Option value mismatches (with basic value aliasing for Yes/No and UK variants)
  - Suspicious numeric values in conditions (potential group/index artefacts)
  - Dependency cycles between controllers and dependents

Usage examples:

- JSON: `curl http://localhost:3000/api/conditions-report/non-lux-1-1`
- HTML: `open http://localhost:3000/api/conditions-report/non-lux-1-1?format=html`

## Scenario Checks (CLI)

- Script: `apps/prototype/scripts/scenarios.mjs`
- Script command: `pnpm scenarios` (defaults to `non-lux-1-1`).
- Runs a small set of visibility assertions that exercise key flows without requiring the dev server.

Included scenarios:

1) UK path
   - Asserts Pre-Application question is hidden for UK
   - Asserts UK Fund Manager question is visible
   - Asserts Fund Manager domicile appears only when FM = Yes

2) Non-UK + Pre-Application = Yes
   - Asserts Pre-Application question is visible for non-UK
   - Asserts UK-specific Fund Manager question is hidden for non-UK

Planned additions:

- Add fixtures for non-UK + No path
- Expand assertions to cover option presence for critical lookups
- Promote the conditions linter into a shared util to power both the API and CLI

## Acceptance

- Mission Control shows Conditions Report link for admin users.
- `pnpm scenarios` exits with code 0 and prints `X passed`.
- Docs reference the endpoints and script usage.

