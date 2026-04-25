---
name: Serene Narrative
colors:
  surface: '#fff8f3'
  surface-dim: '#e1d9cf'
  surface-bright: '#fff8f3'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#fbf2e8'
  surface-container: '#f6ece3'
  surface-container-high: '#f0e7dd'
  surface-container-highest: '#eae1d7'
  on-surface: '#1f1b15'
  on-surface-variant: '#4d453c'
  inverse-surface: '#343029'
  inverse-on-surface: '#f8efe5'
  outline: '#7f766a'
  outline-variant: '#d1c5b8'
  surface-tint: '#725a39'
  primary: '#725a39'
  on-primary: '#ffffff'
  primary-container: '#d2b48c'
  on-primary-container: '#5b4526'
  inverse-primary: '#e1c299'
  secondary: '#5e604d'
  on-secondary: '#ffffff'
  secondary-container: '#e1e1c9'
  on-secondary-container: '#636451'
  tertiary: '#5e5f5d'
  on-tertiary: '#ffffff'
  tertiary-container: '#b9b9b6'
  on-tertiary-container: '#484a48'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#feddb3'
  primary-fixed-dim: '#e1c299'
  on-primary-fixed: '#281801'
  on-primary-fixed-variant: '#584324'
  secondary-fixed: '#e4e4cc'
  secondary-fixed-dim: '#c8c8b0'
  on-secondary-fixed: '#1b1d0e'
  on-secondary-fixed-variant: '#474836'
  tertiary-fixed: '#e3e2e0'
  tertiary-fixed-dim: '#c7c6c4'
  on-tertiary-fixed: '#1a1c1a'
  on-tertiary-fixed-variant: '#464745'
  background: '#fff8f3'
  on-background: '#1f1b15'
  surface-variant: '#eae1d7'
typography:
  display:
    fontFamily: Plus Jakarta Sans
    fontSize: 48px
    fontWeight: '600'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  h1:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  h2:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '500'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-caps:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.0'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1120px
  gutter: 24px
  margin-mobile: 20px
  stack-sm: 12px
  stack-md: 32px
  stack-lg: 64px
---

## Brand & Style

This design system is built upon a philosophy of "Quiet Luxury." It prioritizes the reader's emotional state by creating a digital environment that feels like a physical, sun-drenched sanctuary. The target audience is the thoughtful curator and the intentional reader who values slow consumption over rapid scrolling.

The visual style is **Soft Minimalism**. It leans heavily into generous whitespace and a restricted, tonal color palette. By eschewing loud decorative elements, the design allows the content—photography and prose—to breathe. The interface utilizes organic, soft-touch interactions and subtle depth to evoke a sense of tactility and premium craftsmanship.

## Colors

The palette is a sophisticated monochromatic exploration of warmth. 
- **Primary (#D2B48C):** Used for key actions, active states, and subtle accents. It provides a grounded, earthy contrast to the lighter surfaces.
- **Secondary (#F5F5DC):** The primary surface color for cards, buttons, and secondary containers. It creates a "paper-like" feel.
- **Tertiary (#FAF9F6):** The canvas color. It is a clean, off-white that prevents eye strain and feels more inviting than pure white.
- **Neutral (#4A453E):** A warm, deep charcoal used for typography to ensure high legibility while maintaining the "cozy" temperature of the design.

## Typography

The typography uses **Plus Jakarta Sans** across all levels to maintain a modern, friendly, and cohesive aesthetic. The font's soft curves mirror the UI's rounded corners. 

Headlines are set with tight tracking and leading to create a "locked-in" editorial look. Body text uses a generous 1.6 line-height to ensure a comfortable reading experience for long-form blog posts. For metadata and categories, the "label-caps" style provides a sophisticated architectural contrast to the fluid body text.

## Layout & Spacing

This design system employs a **Fixed Grid** model for desktop and a fluid single-column layout for mobile. On large screens, content is centered within a 1120px container to prevent excessive line lengths.

Spacing is based on an 8px rhythmic scale. Horizontal margins are kept wide to reinforce the feeling of "exclusivity" and "air." Use `stack-lg` for separating major sections (e.g., Article Header from Article Body) and `stack-md` for standard component grouping.

## Elevation & Depth

Depth is achieved through **Ambient Shadows** and tonal layering rather than traditional heavy borders. 

1.  **Base Layer:** The Tertiary color (#FAF9F6) acts as the foundation.
2.  **Raised Layer:** Cards and containers use the Secondary color (#F5F5DC) with a very soft, diffused shadow: `box-shadow: 0 4px 20px rgba(74, 69, 62, 0.05)`.
3.  **Active/Floating Layer:** Elements like navigation bars or active buttons use a slightly more pronounced shadow with a hint of the primary color tint: `box-shadow: 0 8px 30px rgba(210, 180, 140, 0.12)`.

Avoid using solid black for shadows; always tint them with the Neutral or Primary color to maintain the warmth of the palette.

## Shapes

The shape language is defined by **Rounded** geometry. Standard UI elements like buttons and input fields use a `0.5rem` (8px) radius. Larger containers, such as blog post cards and image wrappers, use `rounded-lg` (16px) or `rounded-xl` (24px) to emphasize the soft, cozy vibe. This consistency in curvature ensures that even complex layouts feel approachable and integrated.

## Components

- **Buttons:** Use a solid Primary color (#D2B48C) with Neutral-colored text for high-priority actions. Secondary buttons should have no fill, a 1px border of the Primary color, and a subtle background hover state of Secondary (#F5F5DC).
- **Cards:** Blog cards should be borderless. Use the Secondary color for the background and apply the `rounded-lg` radius. Images inside cards should always be top-aligned and inherit the top-corner radius.
- **Chips/Tags:** Used for categories. These should be small, Pill-shaped, and use the Primary color at 10% opacity with the "label-caps" typography style.
- **Input Fields:** Soft beige backgrounds (#F5F5DC) with a subtle 1px inset border. Focus states should be indicated by a 2px Primary color outline with a soft outer glow.
- **Editorial Components:** Include a "Pull Quote" component with a thick Primary color left-border and `body-lg` typography to break up long text blocks.
- **Interaction:** All hover states should include a gentle 200ms transition on the Y-axis (lifting 2px) and shadow intensity to provide tactile feedback.