<template>
  <div class="container">
    <header class="header">
      <NuxtLink to="/">← Mission Control</NuxtLink>
      <h1>About This Prototype</h1>
    </header>

    <section>
      <p>This is a high‑fidelity, schema‑driven prototype of the onboarding journey. It helps us agree flows, wording, and rules before build. It is not production software and does not store personal data.</p>
      <ul>
        <li>Journeys are listed on Mission Control as cards.</li>
        <li>Screens render from a simple schema (a structured list of fields and rules).</li>
        <li>Admin can show/hide journeys and generate a Diff report or Export CSV.</li>
      </ul>
    </section>

    <section>
      <h2>How To Use It</h2>
      <ol>
        <li>Open Mission Control and choose a journey.</li>
        <li>Answer the questions; use Next/Back to move through steps.</li>
        <li>If errors appear, use the links in the summary to jump and fix.</li>
        <li>(Admin) Click Admin on Mission Control to view Diff/Export links.</li>
      </ol>
      <p>More plain‑English guides:</p>
      <ul>
        <li><a href="/Documents/01%20Areas/guide/QuickStart.md" target="_blank" rel="noopener">Quick Start</a></li>
        <li><a href="/Documents/01%20Areas/guide/README.md" target="_blank" rel="noopener">Using the Prototype</a></li>
        <li><a href="/Documents/01%20Areas/guide/Operations.md" target="_blank" rel="noopener">Operations Guide (Import → Diff/Export)</a></li>
      </ul>
    </section>

    <section>
      <h2>Privacy & Security</h2>
      <ul>
        <li>No PII; use dummy data in tests.</li>
        <li>Admin uses a simple password and an HTTP‑only cookie.</li>
        <li>No third‑party analytics on login gates.</li>
      </ul>
    </section>

    <section>
      <h2>FAQ</h2>
      <details open>
        <summary>Is this the final system?</summary>
        <p>No. It’s a high‑fidelity prototype to test and agree decisions quickly.</p>
      </details>
      <details>
        <summary>Can we use real customer data here?</summary>
        <p>No. Please use dummy answers. We don’t store personal data in the prototype.</p>
      </details>
      <details>
        <summary>Why do some questions appear and disappear?</summary>
        <p>The flow adapts based on your answers to reduce effort and errors.</p>
      </details>
      <details>
        <summary>What does “alpha” vs “beta” mean on a card?</summary>
        <p>Alpha: early shaping. Beta: more complete; suitable for wider testing.</p>
      </details>
      <details>
        <summary>How do I get the admin password?</summary>
        <p>Ask the Nile team. Admin reveals “View Diff” and “Export CSV”.</p>
      </details>
      <details>
        <summary>Can we get the questions in a spreadsheet?</summary>
        <p>Yes. Use Export CSV on the journey card (admin view). It mirrors the schema and includes references back to the source rows where available.</p>
      </details>
    </section>
  </div>
</template>

<style scoped>
.container{max-width:900px;margin:40px auto;padding:0 16px}
.header{display:flex;align-items:center;gap:12px;margin-bottom:16px}
h1{margin:0}
section{margin-bottom:20px}
details{margin:8px 0}
summary{cursor:pointer}
</style>

