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
  
  /* KYCP Design Tokens - Updated to match actual platform */
  --kycp-primary: #3b82f6;
  --kycp-primary-hover: #2563eb;
  --kycp-error: #ef4444;
  --kycp-success: #10b981;
  --kycp-warning: #f59e0b;
  
  /* KYCP Grays */
  --kycp-gray-50: #f9fafb;
  --kycp-gray-100: #f3f4f6;
  --kycp-gray-200: #e5e7eb;
  --kycp-gray-300: #d1d5db;
  --kycp-gray-400: #9ca3af;
  --kycp-gray-500: #6b7280;
  --kycp-gray-600: #4b5563;
  --kycp-gray-700: #374151;
  --kycp-gray-800: #1f2937;
  --kycp-gray-900: #111827;
  
  /* KYCP Component Specific */
  --kycp-input-bg: #ffffff;
  --kycp-input-border: #d1d5db;
  --kycp-input-border-hover: #9ca3af;
  --kycp-input-border-focus: #3b82f6;
  --kycp-input-disabled-bg: #f9fafb;
  --kycp-placeholder-color: #9ca3af;
  --kycp-label-color: #374151;
  --kycp-required: #ef4444;
  --kycp-section-border: #d1d5db;
  
  /* KYCP Spacing */
  --kycp-spacing-xs: 4px;
  --kycp-spacing-sm: 8px;
  --kycp-spacing-md: 12px;
  --kycp-spacing-lg: 20px;
  --kycp-spacing-xl: 24px;
  
  /* KYCP Typography */
  --kycp-font-family: system-ui, -apple-system, sans-serif;
  --kycp-font-size-xs: 12px;
  --kycp-font-size-sm: 13px;
  --kycp-font-size-base: 14px;
  --kycp-font-size-lg: 16px;
  
  /* KYCP Transitions */
  --kycp-transition-fast: 0.15s ease;
  --kycp-transition-base: 0.2s ease;
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