---
name: Developer Console Workspace
colors:
  surface: '#faf9fd'
  surface-dim: '#dbd9dd'
  surface-bright: '#faf9fd'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f4f3f7'
  surface-container: '#efedf1'
  surface-container-high: '#e9e7eb'
  surface-container-highest: '#e3e2e6'
  on-surface: '#1a1b1e'
  on-surface-variant: '#424753'
  inverse-surface: '#2f3033'
  inverse-on-surface: '#f1f0f4'
  outline: '#727785'
  outline-variant: '#c2c6d5'
  surface-tint: '#005ac1'
  primary: '#0058bd'
  on-primary: '#ffffff'
  primary-container: '#2771df'
  on-primary-container: '#fefcff'
  inverse-primary: '#adc6ff'
  secondary: '#006e2c'
  on-secondary: '#ffffff'
  secondary-container: '#86f898'
  on-secondary-container: '#00722f'
  tertiary: '#765700'
  on-tertiary: '#ffffff'
  tertiary-container: '#956e00'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a41'
  on-primary-fixed-variant: '#004494'
  secondary-fixed: '#89fa9b'
  secondary-fixed-dim: '#6ddd81'
  on-secondary-fixed: '#002108'
  on-secondary-fixed-variant: '#005320'
  tertiary-fixed: '#ffdea0'
  tertiary-fixed-dim: '#fbbc06'
  on-tertiary-fixed: '#261a00'
  on-tertiary-fixed-variant: '#5c4300'
  background: '#faf9fd'
  on-background: '#1a1b1e'
  surface-variant: '#e3e2e6'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '600'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: 0em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0.01em
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.03em
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-desktop: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1rem
  space-xl: 1.5rem
---

## Brand & Style

This design system embodies the focused, utility-first clarity of premier cloud runtime and model experimentation interfaces. Engineered for high-cognitive-load developer workspaces, the interface prioritizes immediate legibility, functional hierarchy, and deterministic spatial cadence. 

The aesthetic is Modern Enterprise Minimalist: structured white canvases, micro-borders, quiet secondary containers, and calibrated semantic highlights. It avoids ornamental distractions in favor of ergonomic data visualization, monospace precision, and instantaneous visual feedback. Interactions feel immediate, robust, and mathematically grounded.

## Colors

The palette establishes an ultra-clean, clinical workspace where chromatic saturation is reserved strictly for interactive affordances and critical system states.

### Primary Canvas & Surfaces
- **Canvas Base**: `#FFFFFF` for primary work surfaces, document canvases, and elevated cards.
- **Surface Dim**: `#F8F9FA` for global side navigation, toolbars, and muted page backdrops.
- **Surface Container High**: `#F1F3F4` for inset code blocks, interactive hover states, and segmented control wells.
- **Structural Outlines**: `#E8EAED` for low-contrast borders, partition rules, and grid dividers.

### Semantics & Accents
- **Primary / Active (`#4285F4`)**: Action buttons, active navigation markers, selection handles, and active step nodes.
- **Success / Verified (`#34A853`)**: Health checks, deployment confirmations, and sustainability markers.
- **Error / Anomaly (`#EA4335`)**: Trace exceptions, broken builds, pipeline failures, and critical alert tags.
- **Warning / Pending (`#FBBC05`)**: Throttling thresholds, build queues, pending diffs, and resource saturation warnings.

### Typography & Content Neutrals
- **Text Primary (`#202124`)**: High-contrast body, headers, active tabs, and primary metrics.
- **Text Secondary (`#5F6368`)**: Metadata, field labels, keyboard shortcuts, and descriptive subtext.
- **Text Disabled (`#9AA0A6`)**: Deactivated actions, disabled inputs, and terminal timestamps.

## Typography

The typography strategy leverages two distinct functional families: **Inter** for user interface layout and continuous analytical reading, and **JetBrains Mono** for code blocks, terminal logs, tabular values, and technical IDs.

All numerical tables, dashboard cards, and telemetry outputs must enable open-type tabular lining numerals (`tnum`) to ensure aligned vertical scanning. Monospace elements maintain strict line heights to avoid fractional jitter during live terminal rendering.

## Layout & Spacing

The workspace uses an operational fluid-column grid paired with a persistent left application rail. Density is dense yet breathable, minimizing excessive scrolling for complex data graphs.

- **Desktop (>= 1280px)**: 12-column layout, `gutter-desktop` (1.5rem / 24px), dynamic margins with a fixed 240px collapsable left navigation rail.
- **Tablet (768px - 1279px)**: 8-column layout, `gutter` (1rem / 16px), navigation rail compresses to an icon-only strip (56px).
- **Mobile (< 768px)**: 4-column layout, `margin` (1rem / 16px), floating overlay navigation drawers; multi-pane editors collapse into segmented tab sequences.

## Elevation & Depth

Visual hierarchy is maintained primarily through structured 1px outline boundaries (`#E8EAED`) and light, multi-tier surface nesting rather than pronounced shadows. Shadows serve strictly to indicate floating, detached states (popovers, active modal dialogues, dropdown menus).

- **Surface Level 0 (Canvas)**: Flat `#FFFFFF` with no shadow.
- **Surface Level 1 (Resting Cards & Panels)**: Background `#FFFFFF`, border `1px solid #E8EAED`, subtle ambient elevation: `0 1px 3px rgba(60,64,67,0.08), 0 4px 8px rgba(60,64,67,0.04)`.
- **Surface Level 2 (Hover & Active Dragging)**: Border `1px solid #DADCE0`, elevation: `0 2px 6px rgba(60,64,67,0.12), 0 8px 16px rgba(60,64,67,0.06)`.
- **Surface Level 3 (Menus, Flyouts & Modals)**: Background `#FFFFFF`, elevation: `0 4px 12px rgba(60,64,67,0.15), 0 12px 28px rgba(60,64,67,0.1)`.
- **Inset Recesses (Terminal Windows & Diff Blocks)**: Background `#F8F9FA` or `#F1F3F4`, border `1px solid #E8EAED`, inset shadow `none`.

## Shapes

The geometric framework balances friendly accessibility with industrial precision:

- **Cards & Panes**: `rounded-lg` (12px to 16px), ensuring comfortable framing for data visualization without sacrificing space.
- **Input Controls, Menus, & Chips**: `rounded` (8px), establishing sharp, accurate click targets.
- **Action Buttons & Badges**: Pill treatment (`rounded-xl` to full pill `9999px`) for high-level status tags, primary callouts, and filter switches.

## Components

### Buttons
- **Primary**: Solid `#4285F4` background, `#FFFFFF` text, pill-shaped (`9999px`), 36px height, font `label-lg`. Hover: `#3367D6`. Active: `#2A56C6`.
- **Secondary / Outlined**: `#FFFFFF` background, `1px solid #DADCE0` outline, `#4285F4` or `#202124` text. Hover: `#F8F9FA` background.
- **Tonal / Flat**: `#F1F3F4` fill, `#202124` text, no border. Hover: `#E8EAED`.

### Input Fields & Controls
- **Text Inputs**: Height 36px, `rounded` (8px), background `#FFFFFF`, border `1px solid #DADCE0`, text `body-md` (`#202124`). Focus: border `2px solid #4285F4`, margin offset to maintain baseline alignment.
- **Checkboxes & Radios**: 16px square/circle, border `2px solid #5F6368`. Checked state: background `#4285F4`, border `#4285F4` with white inner glyph.

### Status Chips & Badges
- **Structure**: 24px height, full pill radius (`9999px`), font `label-sm`, inline SVG status dot (6px).
- **Success / Verified**: Background `#E6F4EA`, text `#137333`, dot `#34A853`.
- **Error / Anomaly**: Background `#FCE8E6`, text `#C5221F`, dot `#EA4335`.
- **Warning**: Background `#FEF7E0`, text `#B06000`, dot `#FBBC05`.
- **Informational**: Background `#E8F0FE`, text `#1A73E8`, dot `#4285F4`.

### Code Blocks, Diffs & Terminal Views
- **Terminal Shell**: Background `#F8F9FA`, border `1px solid #E8EAED`, inner padding `space-lg`, font `code-md`.
- **Diff Highlights**: Additions render `#E6F4EA` row tint with `#137333` marker; deletions render `#FCE8E6` row tint with `#C5221F` marker.
- **Gutter**: Monospace line numbers rendered in `#9AA0A6` with zero background fill.

### Timeline Nodes & Metrics Cards
- **Timeline Rails**: 2px vertical stroke in `#E8EAED`. Active nodes feature a 12px circle filled with `#FFFFFF` and a 3px border in `#4285F4`.
- **Dashboard Cards**: Encased in Level 1 elevation, featuring 16px padding, subtle 1px `#E8EAED` border, and high-contrast typography metrics (`headline-lg`) aligned with tabular subtext.