# DESIGN.md

## Overview
A clean, professional peer-review platform for nurses. Inspired by Mintlify: generous whitespace, near-black dark mode, pill-shaped buttons, and large rounded cards. Minimal chrome — borders and subtle background contrast carry depth instead of shadows. The tone is trustworthy and community-driven, not clinical or corporate. Both light and dark modes are fully supported; dark mode uses near-black backgrounds rather than gray.

## Colors
- **Primary** (#0d9488): CTAs, active states, accent icons, key interactive elements
- **Primary Dark** (#14b8a6): Primary variant in dark mode
- **Primary Muted** (#ccfbf1 / #042f2e): Badge backgrounds, callout tints, hover surfaces
- **Neutral** (#737373): Body text, borders, metadata, non-chromatic UI
- **Surface Light** (#ffffff): Page and card backgrounds in light mode
- **Surface Soft** (#f5f5f5): Subtle section backgrounds, alternating fills in light mode
- **Surface Dark** (#0a0a0a): Page background in dark mode
- **Surface Raised Dark** (#1a1a1a): Card and panel backgrounds in dark mode
- **Warning** (#d97706): Limited data callouts, amber badges
- **Error** (#e11d48): No data callouts, rose badges

## Typography
- **Headline Font**: Inter
- **Body Font**: Inter
- **Label Font**: Inter
- **Data Font**: Geist Mono

Headlines use semi-bold weight with tight letter-spacing (`tracking-tight`). Body text uses regular weight. Labels use medium weight at 12px with uppercase and wide tracking for section metadata. Geist Mono is reserved strictly for numeric data displays such as pay figures and ratings — never for prose.

## Elevation
This design uses no shadows. Depth is conveyed through background color contrast between the page surface (`#ffffff` / `#0a0a0a`) and raised card surfaces (`#ffffff` / `#1a1a1a`), combined with a 1px `border-neutral-200 dark:border-neutral-800` outline. In dark mode, borders are barely visible — they exist to define edges, not to add visual weight.

## Components
- **Buttons**: Three variants — solid (teal fill, white text), outline (white/dark bg with neutral border), ghost (transparent with hover bg). All variants use `rounded-full` pill shape and `font-medium text-sm`. Available as `solid_button`, `outline_button`, `ghost_button` in `components/button.py`.
- **Cards**: No shadow, `rounded-2xl` corner radius, 1px neutral border, white/`#1a1a1a` background. Composed using `card`, `card_header`, and `card_section` from `components/card.py`. Section headers use a `border-b` separator with no background fill.
- **Inputs**: `rounded-lg`, neutral border, neutral-50/neutral-900 background, teal focus ring (`ring-teal-500/40`). Available as `input` in `components/input.py`.
- **Badges**: `rounded-full` pill, four variants — teal (default), neutral, amber (warnings), rose (errors). Available as `badge` in `components/badge.py`.
- **Text/Headings**: `text` for body copy, `heading` for headings with `level` param (`sm/md/lg/xl/2xl/3xl`). Available in `components/text.py`.
- **Links**: Two variants — default neutral muted, accent teal. Available as `link` in `components/link.py`.
- **Icons**: Wraps `rx.icon` with neutral default color; `accent=True` for teal, `muted=True` for dimmer neutral. Available as `icon` in `components/icon.py`.
- **Navbar**: Sticky, `h-16`, frosted glass (`bg-white/80 dark:bg-[#0a0a0a]/80 backdrop-blur-md`), single `border-b`. Logo has "Nurse" in teal and "Reports" in neutral. Mobile menu uses a right-side drawer.
- **Footer**: `bg-neutral-50 dark:bg-[#0d0d0d]`, single `border-t`. Two-column layout on desktop (logo/social left, links right).

## Do's and Don'ts
- Do use `neutral-*` scale instead of `zinc-*` — neutral has no blue tint and reads cleaner against teal
- Do use `divide-neutral-200 dark:divide-neutral-800` for all list dividers — never `dark:divide-zinc-700`
- Do replace empty states (`rx.icon("ellipsis")`) with short muted text, e.g. "Nothing saved yet."
- Do use `font-semibold` for all headings — never `font-bold`
- Do use `tracking-tight` on all headings `text-2xl` and above
- Don't use `shadow-lg` on cards — depth comes from background contrast and borders only
- Don't mix rounded and pill shapes — cards are `rounded-2xl`, all buttons and badges are `rounded-full`
- Don't use Geist Mono outside of numeric data displays (pay figures, ratings)
- Don't use gradients in dark mode — plain `#0a0a0a` background only
- Don't add asymmetric corner radii (no `rounded-t-[48px]` style overrides) — all cards are uniformly `rounded-2xl`
