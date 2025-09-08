<template>
  <NuxtPage />
</template>

<style>
/* Global Design System Variables */
:root {
  /* Colors */
  --color-bg: #FAFBFC;
  --color-surface: #FFFFFF;
  --color-border: #E1E4E8;
  --color-border-hover: #C9CED5;
  
  --color-text-primary: #0D1117;
  --color-text-secondary: #57606A;
  --color-text-muted: #8B949E;
  
  --color-link: #0969DA;
  --color-link-hover: #0860CA;
  --color-focus: #0969DA;
  
  /* Status Colors */
  --status-alpha-bg: #DC2626;
  --status-alpha-text: #FFFFFF;
  --status-beta-bg: #F59E0B;
  --status-beta-text: #FFFFFF;
  --status-live-bg: #10B981;
  --status-live-text: #FFFFFF;
  --status-hidden-bg: #6B7280;
  --status-hidden-text: #FFFFFF;
  
  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  
  /* Typography */
  --font-system: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

body {
  margin: 0;
  padding: 0;
  background: var(--color-bg);
  font-family: var(--font-system);
  color: var(--color-text-primary);
}

* {
  box-sizing: border-box;
}
</style>