# Mission Control Design Guide

## Purpose
Mission Control is the administrative dashboard for managing and accessing onboarding journeys. It serves as a neutral, journey-agnostic launcher that prioritizes clarity and functionality over branding.

## Design Principles

### 1. Flat & Minimal
- No shadows, gradients, or unnecessary depth
- Clean lines and clear boundaries
- Focus on content over decoration

### 2. Neutral & Professional
- No brand colors or logos
- Journey-agnostic aesthetic
- Enterprise-appropriate without being sterile

### 3. Clear Information Hierarchy
- Status and metadata are secondary to journey names
- Grouped logically by fund type
- Progressive disclosure of details

## Visual Language

### Color Palette
```
Primary:
- Background: #FFFFFF
- Surface: #F8F9FA
- Border: #E5E7EB

Text:
- Primary: #111827
- Secondary: #6B7280
- Muted: #9CA3AF

Status Colors (subtle):
- Alpha: #EF4444 (red)
- Beta: #F59E0B (amber)
- Live: #10B981 (emerald)
- Hidden: #6B7280 (gray)

Interactive:
- Link: #2563EB
- Link Hover: #1D4ED8
- Focus Ring: #3B82F6 (2px)
```

### Typography
```
Font Stack: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif

Sizes:
- Page Title: 32px (2rem) - font-weight: 600
- Card Title: 18px (1.125rem) - font-weight: 500
- Body: 14px (0.875rem) - font-weight: 400
- Metadata: 13px (0.8125rem) - font-weight: 400
- Badge: 12px (0.75rem) - font-weight: 500

Line Heights:
- Tight: 1.25
- Normal: 1.5
- Relaxed: 1.625
```

### Spacing System
Based on 4px grid:
```
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px
```

### Layout

#### Grid System
- Container: max-width 1200px, centered
- Cards: Responsive grid
  - Desktop: 3 columns
  - Tablet: 2 columns  
  - Mobile: 1 column
- Gap: 24px (lg)
- Padding: 24px (lg)

#### Card Structure
```
┌─────────────────────────────┐
│ [Title]                     │ 18px, weight-500
│ [Key · Version · Variant]   │ 13px, muted
│                             │
│ [status] [visibility]       │ 12px badges
│                             │
│ ─────────────────────────── │ Divider (admin only)
│                             │
│ [Open →]                    │ Primary action
│ [Diff] [Export]             │ Admin actions (small)
└─────────────────────────────┘
```

### Component Specifications

#### Header
- Height: 64px
- Padding: 0 24px
- Border-bottom: 1px solid #E5E7EB
- Title: 24px, weight-600
- Actions aligned right

#### Journey Cards
- Background: #FFFFFF
- Border: 1px solid #E5E7EB
- Border-radius: 8px
- Padding: 20px
- Min-height: 180px
- Hover: border-color: #D1D5DB

#### Status Badges
- Padding: 2px 8px
- Border-radius: 9999px
- Font-size: 12px
- Font-weight: 500
- Text-transform: lowercase
- Colors:
  - alpha: #FEE2E2 bg, #991B1B text
  - beta: #FED7AA bg, #92400E text
  - live: #D1FAE5 bg, #065F46 text
  - hidden: #F3F4F6 bg, #374151 text

#### Buttons
Primary (Open):
- Background: transparent
- Border: 1px solid #111827
- Color: #111827
- Padding: 8px 16px
- Border-radius: 6px
- Font-size: 14px
- Font-weight: 500
- Hover: background #F8F9FA

Secondary (Admin/About):
- Background: transparent
- Color: #2563EB
- Padding: 6px 12px
- Font-size: 14px
- Hover: color #1D4ED8
- Underline on hover

#### Admin Elements
Admin Badge:
- Background: #F3F4F6
- Color: #374151
- Padding: 4px 8px
- Border-radius: 4px
- Font-size: 12px
- Font-weight: 500

Admin Actions:
- Font-size: 13px
- Color: #2563EB
- Margin-top: 12px
- Gap: 12px

### States

#### Hover
- Cards: border-color transitions to #D1D5DB
- Buttons: background or color changes as specified
- Links: underline or color darkens

#### Focus
- 2px solid #3B82F6 ring
- 2px offset
- Visible on keyboard navigation only

#### Disabled
- Opacity: 0.5
- Cursor: not-allowed
- No hover effects

### Responsive Behavior

#### Mobile (< 640px)
- Single column layout
- Full-width cards
- Smaller spacing (16px padding)
- Stacked admin actions

#### Tablet (640px - 1024px)
- Two column grid
- Standard spacing

#### Desktop (> 1024px)
- Three column grid
- Maximum container width
- Optimal spacing

## Implementation Notes

1. Use CSS custom properties for colors and spacing to ensure consistency
2. Implement focus-visible for keyboard-only focus states
3. Ensure all interactive elements have minimum 44px touch targets on mobile
4. Test color contrast ratios meet WCAG AA standards
5. Use semantic HTML elements (nav, main, article) for better accessibility
6. Transitions should be subtle (150-200ms) and use ease-in-out timing

## What This Is Not

- Not branded to RBSI or any specific organization
- Not trying to match KYCP component styling (forms have their own design)
- Not a data-heavy dashboard (it's a launcher/gateway)
- Not using Material Design or other opinionated frameworks
- Not using custom fonts or icons libraries

## Future Considerations

- Dark mode support (using CSS custom properties)
- Filtering/search for many journeys
- Journey grouping indicators
- Progress indicators for multi-step setup