# Prototyping System Guide

**Start Here**: This directory contains canonical guides for using the RBSI onboarding prototyping system. The system turns client spreadsheets into clickable journeys with advanced features including field grouping, complex fields, and debugging tools.

## Quick Navigation

**For newcomers**: Start with [System Overview](System-Overview.md) for complete system understanding
**For implementation**: Use [Complete Workflow Guide](Complete-Workflow-Guide.md) for end-to-end process
**For daily operations**: See [Operations Guide](Operations.md) for admin features and debugging
**For technical details**: Check [Spreadsheet to Prototype Workflow](Spreadsheet-to-Prototype-Workflow.md)

---

# Using The Prototype (Plain English Guide)

This section explains what the prototype is, how to use it, and what the screens and admin controls do. Written for non‑technical readers and client teams.

## What This Is

- A realistic, clickable version of the onboarding journey for funds. It’s not production software.
- It uses the same building blocks (components, rules) that the final platform can support.
- Every screen and question is driven by a simple “schema” (a structured list of fields), not hard‑coded pages. That makes it easy to change and trace.

## What You Can Do

**As a User**:
- Open journeys from Mission Control landing page
- Walk through questions with guidance and validation
- Experience how questions appear/hide based on previous answers
- See field grouping that reduces cognitive load
- Use complex fields with add/remove functionality

**As an Admin**:
- Control journey visibility on Mission Control
- **Debug with Explain Visibility**: See exactly which fields are visible/hidden and why
- **Run Conditions Report**: Comprehensive validation of conditional logic
- Generate audit reports (HTML diff, CSV export) with source traceability
- Manage field organization and complex field implementation

## How To Use It

1) Open Mission Control
- You’ll see cards for each journey. Each card shows a name and status (e.g., alpha/beta).
- Click a card to open that journey.

2) Complete a Journey
- Read the prompt on each screen and answer the questions.
- If something is missing or in the wrong format, an error summary appears at the top and errors appear by the fields.
- Use “Next” and “Back” to move through the steps.

3) Admin Controls (optional)
- Click “Admin” on Mission Control and enter the password to see extra controls.
- As an admin, you can:
  - Show/hide journeys on the landing page (the team uses this to manage what testers see).
  - View a “Diff” report (a simple table of questions and rules), export a CSV, and open the Conditions Report.

## What The Labels Mean

- Status (alpha/beta/live): how mature a journey is. Alpha means early.
- Group (e.g., Funds): used to group cards and manage the order on Mission Control.
- Variant (A/B): if we’re testing two versions of a flow, the variant letter tells you which.

## How Changes Are Tracked

- The prototype reads from a structured list of fields (the “schema”).
- Each field includes a link back to the original spreadsheet row (a reference like REF/KEY).
- We can generate:
  - Diff (HTML): a human‑readable table of fields, rules, and references.
  - Export (CSV): a simple file you can review or share.
  - Conditions Report: a lint of conditionality issues; available from each journey card (Admin).

## Tips for Reviewing Visibility

- Use the Explain visibility toggle at the top of the KYCP preview, or append `?explain=1` to the URL.
- The report `GET /api/conditions-report/:journey?format=html` highlights unresolved keys, option mismatches, and parse errors.

## Privacy & Security

- The prototype does not collect or store personal data.
- Admin controls are protected by a simple password and an HTTP‑only cookie.
- We use no third‑party analytics on login gates.

## What’s Out Of Scope (For Now)

- File uploads and complex integrations.
- Production sign‑in, role management, or analytics.

## Who To Contact

- Product/design lead: Tiernan (Nile) for flow and content questions.
- Prototype support: the Nile team maintaining the repo.
