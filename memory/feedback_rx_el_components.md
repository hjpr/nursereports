---
name: Use rx.el for custom-styled components
description: When Radix UI components cause styling conflicts, build from rx.el bare HTML elements instead
type: feedback
---

Prefer `rx.el.*` (bare HTML elements) over `rx.*` (Radix UI components) when we need full styling control. Radix components have their own internal styles and wrapper elements that compete with Tailwind classes — `rx.el.input`, `rx.el.button`, etc. have no competing styles.

**Why:** `rx.input` renders a Radix wrapper div around an inner `<input>`, making it impossible to cleanly apply background colors without `!important` hacks or complex child selectors like `[&>input]`.

**How to apply:** When a Reflex Radix component resists styling (background bleed, focus ring on wrong element, etc.), switch to the equivalent `rx.el.*` component first before reaching for workarounds.
