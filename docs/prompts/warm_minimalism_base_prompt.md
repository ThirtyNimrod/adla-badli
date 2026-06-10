# Warm Minimalism & Editorial Elegance: Base Design Setup Prompt

Use this prompt to establish the core user interface, styling tokens, typography pairings, grid structure, and micro-interactions for any web project. This style is inspired by boutique architecture, high-end editorial magazines, and tactile paper elements, moving away from sterile, cold tech interfaces.

---

## The Design Style Prompt

Copy the text below and paste it as the initial instruction for setting up the UI or designing the layout.

```markdown
You are an expert front-end designer and engineer. Implement a unified layout and visual design system based on **Warm Minimalism** (also referred to as **Editorial Minimalism** or **"Neomorphic Elegance"**). 

This design style represents a deliberate departure from the cold, sterile, high-contrast tech aesthetics (stark white, pure #000000 text, bubbly components). Instead, it borrows from print media, fine paper, and boutique architecture to create a digital experience that feels tactile, human, and premium.

Follow these layout, token, typography, and motion guidelines exactly:

---

### 🎨 1. Color Palette: Organic & Low-Contrast

Instead of stark pitch-black and pure-white, use organic earth tones:

*   **The Canvas (`--color-canvas`):** Use cream, bone, or alabaster (`#FAF7F2` or `#FFFDF9`). These shades mimic high-quality linen/paper and are soft on the eyes.
*   **The Text & Line Elements (`--color-text-main`):** Replace pure black with a deep espresso brown (`#2E2018`). This provides a warm, sophisticated contrast.
*   **Secondary/Muted Text (`--color-text-muted`):** Use a medium warm gray-brown (`#6B5A50`) for labels and helper elements.
*   **The Accent (`--color-accent`):** Use a muted terracotta (`#C4714A`) as the singular accent color.
*   **The Low-Contrast Accent Background (`--color-accent-light`):** Use a low-opacity terracotta tint (`#EBD6CC` or similar) for focus states or tags.
*   **Ambient Atmospheric Lighting (Gradient Blobs):** Create two ultra-large, blurry background blobs with $\le 6\%$ opacity. Position one in the top-right (terracotta) and one in the bottom-left (espresso) to give the canvas a sense of sunlight filtering into a room.

---

### ✍️ 2. Typography: The "Editorial" Pairing

Load and pair two Google Fonts to establish clear typographic hierarchy:

*   **The Serif (Cormorant Garamond):**
    *   **Usage:** Primary headings (`h1`, `h2`), blockquotes, and special highlighted phrases.
    *   **Style:** Light weight (`300` or `400`). Use italics (`font-style: italic`) for subtitle highlights or quotes to bring a poetic, human touch.
*   **The Sans-Serif (DM Sans):**
    *   **Usage:** Buttons, input fields, labels, body text, and utility menus.
    *   **Style:** Set weights between `300` and `500` to keep functional parts highly legible.
*   **Print-Style Micro-Details:** For utility labels, tags, and small descriptors:
    *   Set font size to `11px` or `12px`.
    *   Use `text-transform: uppercase`.
    *   Add letter spacing of `0.1em` to `0.15em` (`letter-spacing: 0.1em`).
    *   Use `--color-text-muted` at font-weight `500` or `700`.

---

### 🏛️ 3. Structural Geometry & Physical Constraints

Make components look structured, deliberate, and expensive:

*   **Sharp, Paper-like Edges (`--radius-sharp`):** Use a strict, rigid border radius of `2px` for all cards, buttons, inputs, and dropdowns. Avoid bubbly, round edges.
*   **Tactile Cards & Containers:** Card backgrounds should be alabaster (`#FFFDF9`) or slightly lighter than the canvas. Give them a thin border (`1px solid rgba(46, 32, 24, 0.1)`) and layered, low-opacity shadows (`box-shadow: 0 12px 32px rgba(46, 32, 24, 0.06), 0 2px 8px rgba(46, 32, 24, 0.02)`) to make them feel like a printed card resting on a soft surface.
*   **Generous Whitespace:** Treat whitespace as an active component. Use ample padding (`48px` to `52px` on desktop) inside cards and main wrapper layouts.
*   **Organic Separators:** Use a horizontal line with a linear gradient fading at the edges to softly divide sections:
    `background: linear-gradient(to right, rgba(46,32,24,0) 0%, rgba(46,32,24,0.15) 20%, rgba(46,32,24,0.15) 80%, rgba(46,32,24,0) 100%)`

---

### ⚡ 4. Interaction, Focus, & Motion

Keep animations subtle and physical:

*   **Staggered Fade-Up Entry:** On page load, stagger the entrance of cards and text blocks using a cubic-bezier easing curve:
    `animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards`.
*   **Interactive Inputs:** On focus, the background of form inputs should shift slightly, the border color should transition to `--color-accent` or `--color-border-hover`, and a soft, low-intensity terracotta outline glow should appear:
    `box-shadow: 0 0 0 3px rgba(196, 113, 74, 0.12)`.
*   **Bespoke Buttons:** On hover, buttons should shift up slightly (`transform: translateY(-1px)`) and increase shadow intensity. On click/active, they should snap back down (`transform: translateY(0)`), providing physical tactile feedback.

---

### 📐 5. Base CSS Variables & Styling Setup

Define the base styles as follows:

```css
:root {
  --color-canvas: #FAF7F2;
  --color-canvas-light: #FFFDF9;
  --color-text-main: #2E2018;
  --color-text-muted: #6B5A50;
  --color-accent: #C4714A;
  --color-accent-light: rgba(196, 113, 74, 0.12);
  --color-border: rgba(46, 32, 24, 0.1);
  --color-border-hover: rgba(196, 113, 74, 0.4);

  --font-serif: 'Cormorant Garamond', Georgia, serif;
  --font-sans: 'DM Sans', system-ui, sans-serif;

  --radius-sharp: 2px;
  
  --shadow-subtle: 0 2px 8px rgba(46, 32, 24, 0.04);
  --shadow-tactile: 0 12px 32px rgba(46, 32, 24, 0.06), 0 2px 8px rgba(46, 32, 24, 0.02);

  --transition-smooth: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  --transition-fast: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

body {
  background-color: var(--color-canvas);
  color: var(--color-text-main);
  font-family: var(--font-sans);
  margin: 0;
  padding: 0;
  min-height: 100vh;
}
```
```
