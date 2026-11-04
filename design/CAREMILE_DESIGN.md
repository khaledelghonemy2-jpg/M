# CareMile / Allocate Pro — design system

Our own look, taken from the CareMile theme in ALLOCATE_PRO.py and the redesign mockups
(https://claude.ai/artifact/Xur5tK17KHshb6dtmhVUjT). Start the website from this.

## Brand
- Logo: CareMile heart (purple heart, green "CareMile" wordmark) — in the app as `PARTNER_LOGO_PNG`.
- Product mark: Allocate Pro lightning bolt in a ring — `BRAND_MARK_PNG`.
- Personality: caring, organised, trustworthy. Calm purple, with green as the "good / done" signal.

## Colours
| Token | Hex | Use |
|---|---|---|
| Plum (sidebar / dark brand) | `#3B1350` | Navigation, footers, dark sections |
| Plum hover / active | `#4C1C64` / `#5A2475` | Hover and selected nav |
| Purple (primary) | `#6B2381` | Buttons, links, key numbers |
| Purple hover | `#5A1D6E` | Button hover |
| CareMile green | `#8CC63F` | Brand accents only (marker, badges) — not body text |
| Light green on dark | `#B8E07A` | Accent text on plum |
| Page background | `#F6F2F9` | Soft lilac-white |
| Card | `#FFFFFF` with border `#E6DCEE` | Panels |
| Text | `#1F1430` | Body |
| Text secondary | `#5E4E6E` | Labels, captions |
| Text muted | `#76668A` | Hints (still passes contrast on white) |
| Success | text `#2F6B0C` on `#EAF5DF` | On track / done |
| Warning | text `#94480A` on `#FFF1E0` | Near limit / to do |
| Danger | text `#B0154F` on `#FDE8F0`, line `#C2185B` | Over / clash |
| Info | text `#0B5F75` on `#E6F3F7`, line `#0E7490` | CareMile data, info |

## Type
- Font: Segoe UI (Windows app); website: Inter (Google Fonts) as the web equivalent.
- Sizes: page title 26px/700 · section title 16–17px/700 · body 14px · labels 12px/600 uppercase, 0.03em tracking.
- Numbers: tabular figures (`font-variant-numeric: tabular-nums`), money with commas: $56,940.00.

## Shape & spacing
- Radius: cards 14px, buttons/inputs 8px, chips 999px (pill).
- Spacing: 16px between cards, 18–20px card padding, 28px page gutter (16px on phones).
- Buttons ≥ 42px tall; primary = purple fill, secondary = white with `#D9CBE3` border.

## Components
- Status chip: pill, 12px/600 text, colour pair from the table above (On track / Near limit / Over).
- Progress bar: 8px, track `#EFE7F5`, fill by status colour.
- Sidebar nav: plum, selected item `#5A2475` with a 3px green marker on the left.
- Week picker: segmented control, track `#EFE7F5`, selected = white with soft shadow.
