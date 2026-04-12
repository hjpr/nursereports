# DESIGN.md

## Overview
A clean, professional peer-review platform for nurses. Inspired by Mintlify: generous whitespace, near-black dark mode, pill-shaped buttons, and large rounded cards. Minimal chrome — borders and subtle background contrast carry depth instead of shadows. The tone is trustworthy and community-driven, not clinical or corporate. Both light and dark modes are fully supported; dark mode uses near-black backgrounds rather than gray.

## Colors

### Brand & Interactive (Emerald)
Emerald is the **primary brand color** for all interactive and brand elements.

- **Primary** (`emerald-600` / `emerald-500` dark): CTAs, buttons, active states, accent icons, logo
- **Primary Hover** (`emerald-700` / `emerald-400` dark): Button hover states
- **Primary Muted** (`emerald-100` / `emerald-950` dark): Badge backgrounds, callout tints, hover surfaces

### Data Accent (Sky)
Sky is the **data/information accent** — used for numeric figures, informational badges, and navigational links.

- **Data** (`sky-600` / `sky-400` dark): Stat numbers, pay figures, ratings
- **Data Muted** (`sky-50` / `sky-950` dark): Data badge backgrounds
- **Links** (`sky-600` / `sky-400` dark): Accent in-content links (`link(accent=True)`)

**The rule:** Emerald = action/brand. Sky = data/information/navigation. Never apply sky to primary CTA buttons. Never mix both on the same element.

### Surfaces
- **Surface Light** (`neutral-50`): Page background in light mode
- **Surface Card** (`white`): Card and panel backgrounds in light mode
- **Surface Subtle** (`neutral-100`): Alternating section backgrounds, stat/CTA bands
- **Surface Dark** (`#07100a`): Page background in dark mode — near-black with a faint emerald cast, shared across all pages
- **Surface Raised Dark** (`neutral-900`): Card and panel backgrounds in dark mode

### Borders
- **Border Light** (`neutral-300`): Standard borders in light mode
- **Border Dark** (`neutral-800/50`): Standard borders in dark mode
- **Glassmorphism Light** (`neutral-200`): Frosted band borders
- **Glassmorphism Dark** (`white/[0.06]`): Frosted band borders

### Text
- **Primary** (`neutral-950` / `neutral-50` dark): Headings, page titles
- **Body** (`neutral-700` / `neutral-300` dark): Paragraph copy
- **Secondary** (`neutral-500` / `neutral-400` dark): Metadata, captions, labels
- **Muted** (`neutral-400` / `neutral-600` dark): Placeholder, disabled
- **Brand** (`emerald-600` / `emerald-500` dark): Logo "Nurse", section accent text
- **Data** (`cyan-600` / `cyan-400` dark): Numeric stat values

### Semantic
- **Success**: `emerald-600` / `emerald-400` dark
- **Warning**: `amber-600` / `amber-400` dark
- **Error**: `rose-600` / `rose-400` dark
- **Info**: `sky-600` / `sky-400` dark

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
This design uses no shadows. Depth is conveyed through background color contrast between the page surface (`neutral-50` / `neutral-950`) and raised card surfaces (`white` / `neutral-900`), combined with a `ring-[1.5px]` outline. In dark mode, borders are barely visible — they exist to define edges, not to add visual weight.

## Borders
- **Standard border (light)**: `neutral-300`
- **Standard border (dark)**: `neutral-800/50`
- **Glassmorphism border (light)**: `neutral-300`
- **Glassmorphism border (dark)**: `white/[0.06–0.08]`
- **Cards and buttons**: use `ring-[1.5px]` instead of `border` — CSS `box-shadow` (what `ring` compiles to) renders at sub-pixel precision uniformly around curved corners, eliminating the optical aliasing artifact where straight edges appear thicker than rounded corners on `border`-based outlines.

## Components
- **Buttons**: Three variants — solid (emerald fill, white text), outline (white/dark bg with `ring-[1.5px] ring-neutral-300 dark:ring-neutral-700`), ghost (transparent with hover bg). All variants use `rounded-full` pill shape and `font-medium text-sm`. Default `color="emerald"`. Available as `button` in `components/button.py`.
- **Cards**: No shadow, `rounded-2xl` corner radius, `ring-[1.5px] ring-neutral-300 dark:ring-neutral-800/50`, white/`neutral-900` background. Always pair with `overflow-hidden` to clip child elements (textures, absolute overlays) to the rounded boundary. Composed using `card`, `card_header`, and `card_section` from `components/card.py`.
- **Inputs**: `rounded-lg`, neutral border, neutral-50/neutral-900 background, emerald focus ring (`ring-emerald-500/40 focus:border-emerald-500`). Available as `input` in `components/input.py`.
- **Badges**: `rounded-full` pill, six variants — sky (default, informational), neutral, amber (warnings), rose (errors), emerald, teal (legacy). Available as `badge` in `components/badge.py`.
- **Text/Headings**: `text` for body copy, `heading` for headings — defaults to `font-bold tracking-tight`. Pass `weight=` param to override (e.g. `weight="semibold"`). Available in `components/text.py`.
- **Links**: Two variants — default neutral muted, accent sky (`link(accent=True)`). Available as `link` in `components/link.py`.
- **Icons**: Wraps `rx.icon` with neutral default color; `accent=True` for emerald (`text-emerald-600 dark:text-emerald-500`), `muted=True` for dimmer neutral. Available as `icon` in `components/icon.py`.
- **Navbar**: Sticky, `h-16`, frosted glass (`bg-white/80 dark:bg-neutral-950/80 backdrop-blur-md`), single `border-b border-neutral-200 dark:border-white/[0.08]`. Logo has "Nurse" in emerald and "Reports" in neutral. Mobile menu uses a right-side drawer.
- **Footer**: Gradient background — light: `from-emerald-500/20 to-transparent`, dark: `from-transparent to-black/60` (darkens toward the bottom). Single `border-t border-neutral-200 dark:border-neutral-800`. Two-column layout on desktop (logo/tagline/social left, link columns right). Bottom bar has copyright left and light/dark mode toggle right.

## Glassmorphism
Used on horizontal bands (stats, CTA) and navbar. Pattern:
- Background: `bg-white/50 dark:bg-white/[0.03]`
- Blur: `backdrop-blur-md`
- Border: `border-neutral-200 dark:border-white/[0.06]`

For section bands that sit adjacent to each other (e.g. CTA above footer), use `border-t` only on the top band — not `border-y` — to avoid double-stacked divider lines.

## Hero Glow Orb
Absolutely positioned behind hero content. Light: `bg-emerald-500/20 blur-[140px]`, dark: `bg-emerald-600/15 blur-[140px]`. Container must NOT have `overflow-hidden` or the orb will be clipped.

## SVG Wiggle Texture
Fine vertical-wiggle texture used as a repeating background pattern on hero sections, CTA bands, card headers, stat tiles, and action cards. Injected once per page via a `<style>` block using `rx.html()` so the CSS class is globally available.

**Pattern definition** (in each page's `_WIGGLE_STYLE`):
```css
.wiggle-texture {
  background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='9' height='22'>
    <path d='M4.5 0 Q7.5 5.5 4.5 11 Q1.5 16.5 4.5 22' stroke='%2310b981' stroke-width='0.75' fill='none'/>
  </svg>");
  background-repeat: repeat;
  background-size: 9px 22px;
}
```

**Application pattern** — always use an absolutely positioned overlay box so the wiggle never affects child element opacity:
```python
rx.box(class_name="wiggle-texture absolute inset-0 opacity-50 dark:opacity-10 pointer-events-none")
```
The parent container must have `relative` and `overflow-hidden`. Child content elements need `relative` to stack above the overlay (z-index stacking context).

**Opacity calibration by surface:**
- `opacity-80 dark:opacity-10` — light neutral/white surfaces (index hero, CTA, feature card headers)
- `opacity-60 dark:opacity-10` — light emerald-tinted surfaces where emerald-on-emerald reads slightly darker (my-account profile header)
- `opacity-50 dark:opacity-10` — dashboard green cards (welcome header, stat tiles, card headers, action cards) — calibrated so the emerald wiggle on `bg-emerald-500/20` reads the same visual weight as `opacity-80` on white

**Moth blob** — a soft blurred circle (`blur-[60px]`, `bg-neutral-50/80 dark:bg-transparent`) layered between the wiggle and content in full-bleed hero/CTA sections to improve text legibility against the texture without reducing its overall presence.

## Sponsor Marquee
Infinite horizontal scroll using duplicated content (two copies in a flex row). The animation shifts `translateX(0)` → `translateX(-50%)` so the loop is seamless. Edge fade via `mask-image: linear-gradient(to right, transparent, black 12%, black 88%, transparent)`. Pauses on hover. Speed: 56s per cycle.

## Do's and Don'ts
- Do use `emerald` for all interactive and brand elements — buttons, focus rings, logo, feature icons
- Do use `sky` for data display and informational links — stat values, pay figures, ratings, `link(accent=True)`
- Do use `neutral-*` scale instead of `zinc-*` — neutral has no blue tint and reads cleaner
- Do use `neutral-300` for borders in light mode, `neutral-800/50` in dark mode
- Do use `ring-[1.5px]` instead of `border` on cards and buttons — box-shadow renders at uniform sub-pixel width around curved corners, eliminating aliasing artifacts
- Do add `overflow-hidden` to all cards that contain wiggle texture or absolute overlays so they clip to `rounded-2xl`
- Do use `divide-neutral-200 dark:divide-neutral-800/50` for all list dividers
- Do use `font-bold` for all headings via the `heading()` component default
- Do use `tracking-tight` on all headings `text-2xl` and above
- Do add `assets/stylesheet.css` explicitly to `rx.App(stylesheets=[...])` — it is NOT auto-linked
- Do add `relative` to every child element inside a wiggle overlay container so they stack above the `absolute` texture box
- Don't use custom hex colors (`#xxxxxx`) — use Tailwind tokens exclusively (exception: `#07100a` dark page bg has no Tailwind equivalent)
- Don't use `teal` in new components — the system has migrated to `emerald` (brand) and `sky` (data/links)
- Don't apply `sky` to primary CTA buttons — those are always `emerald`
- Don't mix `emerald` and `sky` on the same element
- Don't use `shadow-lg` on cards — depth comes from background contrast and `ring` outlines only
- Don't mix rounded and pill shapes — cards are `rounded-2xl`, all buttons and badges are `rounded-full`
- Don't use Geist Mono outside of numeric data displays (pay figures, ratings)
- Don't use gradients in dark mode except the footer's `to-black/60` depth fade
- Don't add asymmetric corner radii — all cards are uniformly `rounded-2xl`
- Don't use `font-weight: inherit` as a global rule — it blocks Tailwind font-weight utilities due to CSS layer cascade order
- Don't rely on `font-bold` or other Tailwind weight classes overriding a component's baked-in weight class — use the `weight=` param on `heading()` or inline `style=` instead
- Don't add `overflow-hidden` to containers that hold absolutely positioned glow orbs (orbs must bleed outside their container)
