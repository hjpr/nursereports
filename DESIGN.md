# DESIGN.md

## Overview
A clean, professional peer-review platform for nurses. Inspired by Mintlify: generous whitespace, near-black dark mode, pill-shaped buttons, and large rounded cards. Minimal chrome — borders and subtle background contrast carry depth instead of shadows. The tone is trustworthy and community-driven, not clinical or corporate. Both light and dark modes are fully supported; dark mode uses near-black backgrounds rather than gray.

## Colors
- **Primary** (#0d9488 / teal-600): CTAs, active states, accent icons, key interactive elements
- **Primary Dark** (#14b8a6 / teal-500): Primary variant in dark mode
- **Primary Muted** (#ccfbf1 / #042f2e): Badge backgrounds, callout tints, hover surfaces
- **Neutral** (#737373): Body text, borders, metadata, non-chromatic UI
- **Surface Light** (#ffffff): Page and card backgrounds in light mode
- **Surface Soft** (#f5f5f5): Subtle section backgrounds, alternating fills in light mode
- **Surface Dark** (#0a0a0a): Page background in dark mode
- **Surface Raised Dark** (#1a1a1a): Card and panel backgrounds in dark mode
- **Warning** (#d97706): Limited data callouts, amber badges
- **Error** (#e11d48): No data callouts, rose badges

## Typography
- **Headline Font**: Inter Variable (self-hosted via jsDelivr `@fontsource-variable/inter`)
- **Body Font**: Inter Variable
- **Label Font**: Inter Variable
- **Data Font**: Geist Mono (self-hosted via jsDelivr `@fontsource/geist-mono`)

Headlines use **bold** weight (700) with tight letter-spacing (`tracking-tight`). Body text uses weight 450 (fractional variable font weight, set globally via `font-weight: 450` on `body`). Labels use medium weight at 12px with uppercase and wide tracking for section metadata. Geist Mono is reserved strictly for numeric data displays such as pay figures and ratings — never for prose.

### Font Setup
Fonts are loaded via jsDelivr CDN in `nursereports/nursereports.py` `stylesheets=[]`, and global styles are applied in `assets/stylesheet.css`:
- `--default-font-family`, `--heading-font-family` overridden on `:root` and `.radix-themes` to use Inter Variable (overrides Radix UI defaults)
- `--default-font-weight: 450` set on `.radix-themes`
- `body { font-weight: 450; -webkit-font-smoothing: antialiased; }`
- `assets/stylesheet.css` must be explicitly listed in `rx.App(stylesheets=[...])` — Reflex does not auto-link it

### Dark Mode
Dark mode is class-based (`.dark` on `<html>`), NOT `prefers-color-scheme`. Configured via:
```python
rx.plugins.TailwindV4Plugin(config={"darkMode": "class", ...})
```
Reflex's `react-theme.js` adds/removes `.dark` when `rx.toggle_color_mode` is called.

## Elevation
This design uses no shadows. Depth is conveyed through background color contrast between the page surface (`#ffffff` / `#0a0a0a`) and raised card surfaces (`#ffffff` / `#1a1a1a`), combined with a 1px border outline. In dark mode, borders are barely visible — they exist to define edges, not to add visual weight.

## Borders
- **Standard border color (light)**: `neutral-300` — not `neutral-200` which is too faint on white
- **Standard border color (dark)**: `neutral-800`
- **Glassmorphism borders (light)**: `neutral-300`
- **Glassmorphism borders (dark)**: `white/[0.06–0.08]`
- **Feature cards**: use `outline outline-1` instead of `border` — CSS outline follows `border-radius` without anti-aliasing thinning at corners. Use `border-0` to suppress the card component's built-in border before applying outline.

## Components
- **Buttons**: Three variants — solid (teal fill, white text), outline (white/dark bg with `neutral-300` border in light / `neutral-800` in dark), ghost (transparent with hover bg). All variants use `rounded-full` pill shape and `font-medium text-sm`. Available as `solid_button`, `outline_button`, `ghost_button` in `components/button.py`.
- **Cards**: No shadow, `rounded-2xl` corner radius, 1px `neutral-300 dark:neutral-800` border, white/`#1a1a1a` background. Composed using `card`, `card_header`, and `card_section` from `components/card.py`.
- **Inputs**: `rounded-lg`, neutral border, neutral-50/neutral-900 background, teal focus ring (`ring-teal-500/40`). Available as `input` in `components/input.py`.
- **Badges**: `rounded-full` pill, four variants — teal (default), neutral, amber (warnings), rose (errors). Available as `badge` in `components/badge.py`.
- **Text/Headings**: `text` for body copy, `heading` for headings — defaults to `font-bold tracking-tight`. Pass `weight=` param to override (e.g. `weight="font-semibold"`). Available in `components/text.py`.
- **Links**: Two variants — default neutral muted, accent teal. Available as `link` in `components/link.py`.
- **Icons**: Wraps `rx.icon` with neutral default color; `accent=True` for teal, `muted=True` for dimmer neutral. Available as `icon` in `components/icon.py`.
- **Navbar**: Sticky, `h-16`, frosted glass (`bg-white/80 dark:bg-[#0a0a0a]/80 backdrop-blur-md`), single `border-b border-neutral-300 dark:border-white/[0.08]`. Logo has "Nurse" in teal and "Reports" in neutral. Mobile menu uses a right-side drawer.
- **Footer**: Gradient background — light: `from-teal-500/30 to-teal-500/10`, dark: `from-[#0a0a0a] to-[#1c1c1c]`. Single `border-t border-neutral-300 dark:border-neutral-800`. Two-column layout on desktop (logo/tagline/social left, link columns right). Bottom bar has copyright left and light/dark mode toggle right.

## Glassmorphism
Used on horizontal bands (stats, CTA) and feature cards. Pattern:
- Background: `bg-white/60 dark:bg-white/[0.03]` (or teal-tinted variant)
- Blur: `backdrop-blur-md`
- Border: `border-neutral-300 dark:border-white/[0.06]`

For section bands that sit adjacent to each other (e.g. CTA above footer), use `border-t` only on the top band — not `border-y` — to avoid double-stacked divider lines.

## Hero Glow Orb
Absolutely positioned behind hero content. Light: `bg-teal-500/50 blur-[140px]`, dark: `bg-teal-600/20 blur-[140px]`. Container must NOT have `overflow-hidden` or the orb will be clipped.

## Sponsor Marquee
Infinite horizontal scroll using duplicated content (two copies in a flex row). The animation shifts `translateX(0)` → `translateX(-50%)` so the loop is seamless. Edge fade via `mask-image: linear-gradient(to right, transparent, black 12%, black 88%, transparent)`. Pauses on hover. Speed: 56s per cycle.

## Do's and Don'ts
- Do use `neutral-*` scale instead of `zinc-*` — neutral has no blue tint and reads cleaner against teal
- Do use `neutral-300` for borders in light mode — `neutral-200` is too faint on white backgrounds
- Do use `divide-neutral-200 dark:divide-neutral-800` for all list dividers
- Do use `font-bold` for all headings via the `heading()` component default
- Do use `tracking-tight` on all headings `text-2xl` and above
- Do use `outline outline-1` instead of `border` on elements with `rounded-2xl` to avoid corner anti-aliasing artifacts
- Do use `border-0` to suppress a component's built-in border before applying `outline`
- Do add `assets/stylesheet.css` explicitly to `rx.App(stylesheets=[...])` — it is NOT auto-linked
- Don't use `shadow-lg` on cards — depth comes from background contrast and borders only
- Don't mix rounded and pill shapes — cards are `rounded-2xl`, all buttons and badges are `rounded-full`
- Don't use Geist Mono outside of numeric data displays (pay figures, ratings)
- Don't use gradients in dark mode — plain `#0a0a0a` background only (footer fade to `#1c1c1c` is acceptable)
- Don't add asymmetric corner radii — all cards are uniformly `rounded-2xl`
- Don't use `font-weight: inherit` as a global rule — it blocks Tailwind font-weight utilities due to CSS layer cascade order
- Don't rely on `font-bold` or other Tailwind weight classes overriding a component's baked-in weight class — use the `weight=` param on `heading()` or inline `style=` instead
- Don't add `overflow-hidden` to containers that hold absolutely positioned glow orbs
