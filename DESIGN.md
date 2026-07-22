---
name: Cyan Horizon
colors:
  surface: '#f5fafd'
  surface-dim: '#d6dbdd'
  surface-bright: '#f5fafd'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4f7'
  surface-container: '#e9eff1'
  surface-container-high: '#e4e9eb'
  surface-container-highest: '#dee3e6'
  on-surface: '#171c1e'
  on-surface-variant: '#3d494d'
  inverse-surface: '#2c3133'
  inverse-on-surface: '#ecf1f4'
  outline: '#6d797e'
  outline-variant: '#bcc8cd'
  surface-tint: '#00677c'
  primary: '#00677c'
  on-primary: '#ffffff'
  primary-container: '#1aafd0'
  on-primary-container: '#003d4b'
  inverse-primary: '#58d6f8'
  secondary: '#525e7d'
  on-secondary: '#ffffff'
  secondary-container: '#cdd9fe'
  on-secondary-container: '#525f7e'
  tertiary: '#515e7a'
  on-tertiary: '#ffffff'
  tertiary-container: '#94a1c0'
  on-tertiary-container: '#2b3852'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#b2ebff'
  primary-fixed-dim: '#58d6f8'
  on-primary-fixed: '#001f27'
  on-primary-fixed-variant: '#004e5e'
  secondary-fixed: '#d9e2ff'
  secondary-fixed-dim: '#b9c6ea'
  on-secondary-fixed: '#0d1b36'
  on-secondary-fixed-variant: '#3a4664'
  tertiary-fixed: '#d7e2ff'
  tertiary-fixed-dim: '#b9c6e7'
  on-tertiary-fixed: '#0d1b34'
  on-tertiary-fixed-variant: '#3a4762'
  background: '#f5fafd'
  on-background: '#171c1e'
  surface-variant: '#dee3e6'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  title-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-base:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-bold:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '700'
    lineHeight: 16px
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-padding: 2rem
  gutter: 1.5rem
  stack-sm: 0.5rem
  stack-md: 1rem
  stack-lg: 1.5rem
  card-inner-padding: 1.5rem
---

## Brand & Style

This design system is engineered for a high-efficiency booking dashboard that balances professional utility with a contemporary, airy aesthetic. The brand personality is dependable yet forward-thinking, utilizing a spacious layout to reduce cognitive load during complex scheduling tasks.

The visual style blends **Corporate Modern** with **Glassmorphism** influences. It prioritizes clarity through generous whitespace and a restricted color palette, while using soft mesh gradients and high-radius containers to create a "friendly enterprise" atmosphere. The emotional response should be one of calm control and systematic organization.

## Colors

The palette is anchored by a vibrant Cyan primary color, used for calls to action and key brand moments. The core typography uses a deep Navy for maximum legibility and a muted Slate for secondary information.

*   **Primary:** #1AAFD0 is the functional driver for active states and primary buttons.
*   **Neutrals:** The background transitions between #F5F7FA (canvas) and #ECF0F5 (subtle sectioning) to create soft depth.
*   **Mesh Gradients:** Metric tiles utilize a duotone mesh blending #1AAFD0 with its lighter tint and the secondary background color to create a soft, luminous effect without introducing high-contrast hues.

## Typography

This design system uses **Plus Jakarta Sans** across all levels to maintain a soft, approachable, and modern feel. The typeface’s open counters ensure high legibility in data-dense dashboard environments.

*   **Headlines:** Utilize semi-bold and bold weights with slight negative letter-spacing for a premium, "locked-in" editorial look.
*   **Body:** Standardized at 16px for primary reading and 14px for secondary metadata.
*   **Labels:** Small caps or bold 12px variants are used for categories and table headers to provide clear hierarchy without consuming excessive vertical space.

## Layout & Spacing

The layout follows a **Fixed Grid** philosophy for the main content area (max-width 1440px) to ensure consistent line lengths in data displays, while the background fills the viewport.

*   **Desktop:** 12-column grid with 24px gutters. A standard dashboard view typically uses a 3-column "sidebar/main/action-panel" split (e.g., 2:7:3).
*   **Rhythm:** An 8px linear scale governs all padding and margins. 
*   **Density:** Airy spacing is prioritized; cards never touch the viewport edge, maintaining a minimum 32px safety margin on desktop.

## Elevation & Depth

Hierarchy is achieved through **Tonal Layers** and **Ambient Shadows**. This design system avoids harsh borders in favor of soft shadows that suggest physical lift.

*   **Level 0 (Background):** #F5F7FA.
*   **Level 1 (Cards):** Pure white (#FFFFFF) with a `0px 10px 30px rgba(20, 33, 61, 0.05)` shadow. This creates a soft, floating effect.
*   **Level 2 (Dropdowns/Modals):** Pure white with a more pronounced `0px 20px 40px rgba(20, 33, 61, 0.12)` shadow.
*   **Interactive State:** On hover, primary cards should subtly lift by increasing shadow spread and decreasing Y-offset.

## Shapes

The shape language is defined by extreme roundedness to offset the technical nature of a booking system. 

*   **Core Containers:** All primary dashboard cards must use a **24px corner radius**.
*   **Secondary Elements:** Buttons and input fields use a **12px radius** (Soft).
*   **Iconography:** Action icons are housed within circular (#FFFFFF or tinted) badges to create a friendly, "app-like" touch target.

## Components

### Buttons
*   **Primary:** Solid #1AAFD0 with white text. 12px radius.
*   **Secondary:** Ghost style with #515E7A borders or soft cyan tinted backgrounds.

### Metric Tiles
*   Backgrounds must use the duotone mesh gradient (#1AAFD0 to #BEE9F2). 
*   Typography inside tiles remains high-contrast (Dark Navy or White depending on gradient intensity).
*   Include a 32px circular icon badge in the top right corner of the tile.

### Cards
*   Always white background.
*   24px corner radius.
*   Internal padding is 24px.
*   Headings within cards use `title-sm`.

### Input Fields
*   Background: #ECF0F5.
*   Border: None or 1px solid #D1D9E6 on focus.
*   Radius: 12px.
*   Padding: 12px 16px.

### Lists & Activity
*   Items separated by subtle 1px horizontal lines (#ECF0F5).
*   Hover states use a very pale cyan tint (#F0F9FB).
*   Circular avatars/initials for user entities.