# Project context – RBSI Institutional Onboarding

## Why this project exists
RBS International wants an intuitive, digital‑first onboarding journey for Institutional Banking customers that reduces time to onboard and improves Right First Time (RFT). The current estate is fragmented and includes outdated processes such as PDF forms. We will streamline the experience and the underlying data capture so onboarding teams receive complete, usable submissions at first pass.

Who we are – Nile

Nile is a service and product design consultancy specialising in complex, regulated customer journeys in financial services. We design high-fidelity, code-based prototypes that de-risk delivery and give build teams a clear path to assembly.
	•	What we do – map end-to-end journeys, align data, policy and UI, and validate decisions with SMEs and customers. We improve customer and operations outcomes together, not one at the expense of the other.
	•	How we work – schema-first, component-faithful, accessibility-led. We ship clickable, build-able flows and clear handovers rather than production code.
	•	Why it matters – better RFT, cleaner inputs to downstream systems, and fewer rework cycles for onboarding teams.

	•	We will lift Right First Time by simplifying questions, embedding guidance and accessibility, and aligning inputs to the data contract from day one.
	•	Prototypes will use KYCP-faithful components and constraints so FinOpz can assemble flows without surprises.
	•	We will measure what matters – RFT, data quality at first submission and interaction proxies – to prove impact before build.

## Outcomes we are accountable for (from the SOW)
- **Raise RFT to 80% for onboarding applications** and reduce rework cycles.
- **Improve customer experience metrics** such as NPS and CSAT for onboarding.
- **Consolidate and simplify application routes**, retiring outdated paths and PDFs.
- **Embed guidance and accessibility best practice** directly into the journeys.
- **Enable better data quality at first submission** so ops effort drops and downstream systems receive clean inputs.
- **Improve customer and employee experience simultaneously**, not one at the expense of the other.

## What we will deliver
- **Validated journey designs** – end‑to‑end clickable prototypes for SDD, CDD and EDD cases, ready for FinOpz assembly.
- **Revised onboarding question sets** – customer‑centred, accessible, compliant screens and copy.
- **SME reviews** – compliance and onboarding reviews baked into sprint cadence.
- **Customer testing** – fortnightly rounds to validate design choices and lift RFT.
- **Development handovers** – specs and assets for any new componentry not present in KYCP.
- **Formal playbacks** – two milestone playbacks for validation and sign‑off.
- **Success Measurement Framework** – metrics, instrumentation plan and a baseline to track performance of new journeys over time.
- **Sprint output packages** – lightweight documentation of scope, progress and key decisions.

## How we are working
- **Timeline** – two‑week sprints over 14 weeks.
- **Team** – Nile partners with RBSI and FinOpz (KYCP). Three product designers working collaboratively.
- **Prototypes** – code‑based Nuxt (Vue 3) app using recreated KYCP components. Interaction fidelity is the priority.
- **Source of truth** – a normalised schema per journey in the repo. Client spreadsheets are mapped to and from this schema with a diffed audit trail.
- **Protection** – preview routes are password‑gated per prototype. Mission Control includes an admin mode protected by a single hashed password; admin toggles control global visibility of journeys. No analytics on gate pages.
- **Testing cadence** – customer testing every second week. Evidence packs stored in `/docs/playbacks/` with commit hashes.
- **Sign‑off** – Stephen (client) is the final approver at milestones.
- **Accessibility** – aim for WCAG 2.2 AA. Content is plain English with a clear style guide.

## Scope boundaries
- We design journeys and produce high‑fidelity, build‑able prototypes. We do **not** ship production code. FinOpz assembles the final flows in KYCP.
- We only use components that FinOpz can build. Where a gap exists, we document it and propose alternatives.
- Jurisdiction and entity variants will be phased as prioritised with the client.

## Dependencies and what we need from FinOpz (KYCP)
- Component catalogue and behaviours – names, props, constraints and error patterns.
- Validation rules and any regexes in production.
- Conditional logic capabilities and limits (nesting, cross‑section dependencies).
- Navigation model – save‑as‑you‑go, back behaviour, timeouts.
- Token theme, grid and spacing rules so prototypes look and feel realistic.
- Data contract to CRM – field names, types and allowed values.
- Preferred handover format for copy and logic updates.
- Non‑functional constraints – performance targets, max fields per screen, anti‑patterns to avoid.

## Success measures and how we track them
- **Primary** – RFT rate for onboarding applications. Target 80%.
- **Secondary** – NPS and CSAT for onboarding, time to complete, error rates per step.
- **In prototype** – we log local interaction proxies during moderated tests only (no PII): `field_error`, `backtrack`, `abandon`, `time_to_complete`. These inform the Success Measurement Framework.

## Inputs we expect from the client
- Master spreadsheets listing 600+ questions with IDs, labels, dependencies, validation rules, mappings and mandatory flags.
- SME access for Compliance and Onboarding for review cycles.
- Prior research and policy references relevant to each jurisdiction and entity.

## Risks and mitigations
- **Platform mismatch** – a pattern works in prototype but not in KYCP. *Mitigation:* build with faithful component facsimiles, keep a platform‑gap log, get early confirmation from FinOpz.
- **Spreadsheet drift** – client updates outside our cycle. *Mitigation:* schema‑first workflow with round‑trip diff and clear ownership of updates.
- **Scope creep** – new variants mid‑sprint. *Mitigation:* maintain a visible backlog and change log, re‑baseline at sprint reviews.
- **Accessibility regressions** – rushed changes reduce compliance. *Mitigation:* CI with automated checks and manual checklists on PRs.

## Definition of done for a journey increment
- Screens render from schema with no hard‑coded copy.
- Content meets style guide and accessibility checks pass.
- Conditions and validation verified with SME.
- Diff report attached and audit trail links present.
- Evidence from the latest test round filed and referenced.
- Platform gaps (if any) raised with FinOpz and tracked.

## References
- SOW extract held in internal notes. This context file reflects its objectives and deliverables. See `/docs/notes/` for source links and playbacks.
