# Rails Capability Map

A capability-based learning map for modern Ruby on Rails, current to **Rails 8.x** (2025–2026).

Live site: **https://cristoslc.github.io/rails-capability-map/capability-map.html**

Sister project of [tl-learning-plan](https://github.com/cristoslc/tl-learning-plan) — same page design, same interaction model, different domain: this map exists to get an experienced engineer fluent in *modern* Rails (post-Rails 7), not to re-teach web development.

## The capabilities

| # | Capability | Focus |
|---|-----------|-------|
| 1 | Rails Core & Conventions | Request lifecycle, generators, the mental model |
| 2 | Active Record & Data | Querying, associations, migrations, schema design |
| 3 | Hotwire (HTML over the Wire) | Turbo + Stimulus, when not to build an SPA |
| 4 | Background Jobs & Async | Active Job, Solid Queue vs Sidekiq, job durability |
| 5 | Security & Auth | Rails 8 auth generator, Pundit, Brakeman, threat models |
| 6 | Testing | Request specs, system tests, deterministic CI |
| 7 | Growing the Codebase | Layered design, modular monoliths — and the honest critique |
| 8 | Ship & Operate | Kamal 2, Thruster, Propshaft, the Solid trifecta |
| 9 | Performance | Profiling, caching, index strategy, evidence for "Rails scales" |
| 10 | AI Partner (alongside) | Agent-assisted Rails with human review gates |

## How it's built

Single source of truth: `scripts/gen.py` holds every capability's text and resources, and generates:

- `dist/capability-map.html` — the interactive map (filters, progress checkboxes, dark mode, clickable mermaid graph)
- `dist/capabilities/*.md` — one plain-markdown source per capability
- `dist/capability-graph.mmd` — the mermaid source

To regenerate after editing content: `python3 scripts/gen.py`

The page shell is reused from [`tl-learning-plan/dist/capability-map.html`](https://github.com/cristoslc/tl-learning-plan) (WCAG-AAA-adapted palette, aria-complete, no build step).

## Deploy

GitHub Pages via the included workflow (`.github/workflows/pages.yml`, uploads `dist/` with `build_type: workflow`) — same setup as tl-learning-plan. Any push to `main` redeploys.

## Progress tracking

Checkboxes persist in `localStorage` under the key `rails-cap-progress` (separate from tl's key, so both maps stay independently tracked).