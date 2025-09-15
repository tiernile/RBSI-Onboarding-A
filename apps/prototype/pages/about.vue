<template>
  <div class="about">
    <header class="hero">
      <NuxtLink class="hero__back" to="/">← Mission Control</NuxtLink>
      <h1 class="hero__title">Improving Onboarding Through Rapid Prototyping</h1>
      <p class="hero__lede">We've been working on a better way to improve the onboarding journey. The traditional approach of going straight from requirements to development takes too long and often misses the mark. Instead, we're using rapid prototyping to test ideas quickly and get real feedback before committing to expensive builds.</p>
    </header>

    <main class="wrap">
      <section>
        <h2>The Problem We're Solving</h2>
        <p>If you've ever tried to explain a complex onboarding flow using spreadsheets or static mockups, you know how difficult it can be to get everyone on the same page. Stakeholders struggle to visualize the user experience, developers interpret requirements differently, and by the time you discover issues, it's often too late and too expensive to fix them.</p>
        
        <p>Tools like Figma are great for visual design, but they can't handle the complex logic, validation rules, and conditional flows that make up real onboarding journeys. You end up with beautiful pictures that don't actually show how the system will behave.</p>
      </section>

      <section>
        <h2>How This Works</h2>
        <p>Our approach is refreshingly simple. We start with your existing spreadsheets — the ones you're probably already using to track requirements. We transform these into a structured data schema that defines every question, validation rule, and conditional logic. Then our system automatically renders this as a fully interactive prototype using pre-built components.</p>
        
        <p>The magic is that when you want to test a different approach, you just update the schema and the changes appear immediately. No waiting for design iterations or development sprints. You can test five different versions of a flow in the time it would normally take to mock up one.</p>
      </section>

      <section>
        <h2>What Makes This Different</h2>
        <p>Unlike traditional prototyping tools, this creates real, working forms with actual validation and conditional logic. When a user selects "UK" as their country, the relevant UK-specific questions actually appear. When they enter an invalid email, they see the real error message. It's not a simulation — it's the actual experience, just not connected to production systems.</p>
        
        <p>This means you can put it in front of real users and get meaningful feedback. They're not looking at static screens and imagining what might happen. They're clicking through the actual journey, experiencing the real flow, and hitting the same friction points they would in production.</p>
      </section>

      <section>
        <h2>Getting Started</h2>
        <p>When you first visit Mission Control, you'll see all the available journey prototypes. Each one represents a different onboarding flow we're testing. Click on any journey to experience it as a user would. Try filling it out with different scenarios — select different countries, toggle different options, and see how the flow adapts.</p>
        
        <p>As you go through, make notes about what works and what doesn't. Does the flow make sense? Is the wording clear? Are we asking for the right information at the right time? Your feedback directly shapes what we build.</p>
      </section>

      <section>
        <h2>Important Context</h2>
        <p>These prototypes aren't the final design and they're not production-ready code. Think of them as functional sketches — accurate enough to test the experience but built for speed rather than polish. The components don't exactly match our KYC platform yet, but they demonstrate the flow and logic effectively.</p>
        
        <p>Everything is data-driven, which means we can track exactly what's being tested and maintain consistency across different versions. And because this is just for testing, please use dummy data rather than real customer information.</p>
      </section>

      <section>
        <h2>Questions You Might Have</h2>
        <details class="faq">
          <summary>How is this different from Figma prototypes?</summary>
          <p>The biggest difference is that this isn't just pictures of forms — it's actual working forms. When you click a dropdown, real options appear. When you submit with errors, you see real validation messages. The conditional logic actually works, so if you select "UK" as your country, you'll see UK-specific questions appear. Figma is great for showing what something looks like, but this shows how it actually works.</p>
        </details>
        <details class="faq">
          <summary>Can I test my own journey ideas?</summary>
          <p>Absolutely. If you have a journey you want to prototype, just share your requirements with us. If you already have them in a spreadsheet (which most people do), we can usually get a working prototype up within a day or two. Then you can test it, refine it, and iterate as much as you need.</p>
        </details>
        <details class="faq">
          <summary>How quickly can we make changes?</summary>
          <p>Changes happen almost instantly. Once we update the schema, the prototype reflects those changes immediately. There's no waiting for a designer to update mockups or a developer to change code. If we decide in a meeting that a question should be worded differently or a field should be optional instead of required, we can make that change and test it right away.</p>
        </details>
        <details class="faq">
          <summary>What happens after we test and validate a flow?</summary>
          <p>Once we've tested a flow and everyone's happy with it, the validated journey becomes the blueprint for what gets built in production. The development team knows exactly what to build because they can see it working. There's no ambiguity or interpretation needed — what you tested is what you get.</p>
        </details>
        <details class="faq">
          <summary>Who looks after all of this?</summary>
          <p>The Nile team maintains the prototype platform itself, making sure it runs smoothly and adding new capabilities as needed. Product owners control the actual journey content — what questions to ask, in what order, with what validation rules. It's a partnership where we provide the tools and you provide the requirements.</p>
        </details>
        <details class="faq">
          <summary>Can we get a copy of what we've tested?</summary>
          <p>Yes, if you have admin access, you can export any journey as a CSV file. This gives you a complete record of all the questions, validation rules, and conditional logic. It's useful for documentation, compliance reviews, or handing over to development teams.</p>
        </details>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
// Use KYCP design tokens for consistent spacing, color, and radius
import '~/assets/kycp-design.css'
</script>

<style scoped>
.about {
  min-height: 100vh;
  padding: 24px;
  max-width: 900px;
  margin: 0 auto;
}

.hero__back {
  display: inline-block;
  margin-bottom: 16px;
  color: var(--color-link, #0969DA);
  text-decoration: none;
}

.hero__back:hover {
  text-decoration: underline;
}

.hero__title {
  margin: 0 0 16px 0;
  font-size: 32px;
  font-weight: 600;
  color: var(--color-text-primary, #0D1117);
}

.hero__lede {
  margin: 0 0 32px 0;
  font-size: 16px;
  line-height: 1.6;
  color: var(--color-text-secondary, #57606A);
}

.wrap section {
  margin-bottom: 32px;
}

.wrap h2 {
  margin: 0 0 12px 0;
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary, #0D1117);
}

.wrap p {
  margin: 0 0 12px 0;
  color: var(--color-text-secondary, #57606A);
  line-height: 1.5;
}

.wrap ul,
.wrap ol {
  margin: 0 0 16px 0;
  padding-left: 24px;
  line-height: 1.6;
}

.wrap li {
  margin-bottom: 8px;
}

.faq {
  border-bottom: 1px solid var(--color-border, #E1E4E8);
  padding: 12px 0;
}

.faq:last-child {
  border-bottom: none;
}

.faq summary {
  cursor: pointer;
  font-weight: 500;
  color: var(--color-text-primary, #0D1117);
}

.faq summary:hover {
  color: var(--color-link, #0969DA);
}

.faq p {
  margin: 8px 0 0 0;
  color: var(--color-text-secondary, #57606A);
}
</style>
