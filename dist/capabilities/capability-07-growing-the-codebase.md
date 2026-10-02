# 7. Grow the Codebase: Architecture Without Microservices

[Back to Capability Map](capability-map.html)

**The situation:** The codebase is three years old and the fat-model era shows: controllers with business logic, callbacks with side effects, no seams. Rails' answer is emphatically not a service fleet — 'extraction' here means layering (POROs, form/query objects, ViewComponents), modular monoliths (engines, pack-werk), and knowing exactly when a module should become a service.

**What changes:** You can reason about where logic belongs in a Rails app — and defend it — using the layered-model vocabulary: plain Ruby objects at domain seams instead of God objects. You know the modular monolith toolkit (engines, Packwerk) and its honest critique: boundary tools prevent new coupling but don't fix design or organization. You can evaluate extract-vs-keep decisions with evidence instead of aesthetics, and when extraction is right, you know what good looks like in both worlds.

**You're ready when:** Given a large Rails app, you can map its module seams and coupling hot spots; design a bounded modularization (or argue against one) with an ADR-style note; and extract one well-bounded domain (service, engine, or query object layer) without breaking the monolith's advantages.

### Start here

| Resource | Format | Time | Why this one |
|----------|--------|------|-------------|
| [The Majestic Monolith](https://m.signalvnoise.com/the-majestic-monolith/) — DHH / 37signals | Article | 10 min | The original articulation of Rails' architectural default — and the philosophy behind why the one-person (and one-hundred-person) framework stays single-deploy. |
| [Modularizing Rails Monoliths One Bite at a Time](https://technology.doximity.com/articles/modularizing-rails-monoliths-one-bite-at-a-time) — Marc Reynolds / Doximity | Article | 25 min | A real team's phased Packwerk modularization — boundaries, enforcement, and what it did and didn't buy them. |
| [The Myth of the Modular Monolith (EuRuKo 2025 closing keynote)](https://www.rubyevents.org/talks/closing-keynote-the-myth-of-the-modular-monolith) — Eileen M. Uchitelle (RubyEvents) | Video | 45 min | The essential counterweight, from a Rails core team alum with Shopify/GitHub/37signals scar tissue: most modularization pains are human and organizational, and tools like Packwerk can't fix that. Decide with both talks in mind. |

### Go deeper

| Resource | Format | Time | What it adds |
|----------|--------|------|-------------|
| [Under Deconstruction: The State of Shopify's Monolith](https://shopify.engineering/shopify-monolith) — Shopify Engineering | Article | 30 min | One of the largest Rails codebases ever, on engines, Packwerk, SOLID at component scale, and the developer-behavior realities of modularization. |
| [Packwerk](https://github.com/Shopify/packwerk) — Shopify | Guide | 20 min | The dependency-enforcement gem: packages, dependency declarations, and violation gates in CI. |
| [Layered Design for Ruby on Rails Applications](https://pragprog.com/titles/npalka8/layered-design-for-ruby-on-rails-applications) — Vladimir Dementyev | Book | ~10 hrs | The architectural vocabulary for where logic lives — the strongest current book-length treatment of Rails application layering. |
| [RailsConf 2025 talk index](https://www.rubyevents.org/events/railsconf-2025) — RubyEvents | Video | browse | Multiple current talks on monolith growth, modularization stories, and scaling orgs on shared codebases. |

### Practice This

Pick the fattest controller or model in a large Rails app (yours or a well-known open-source one). Extract one seam: a query object, a service object, or a ViewComponent. Then write an ADR-style note: what boundary you created, why you did NOT extract a service, and what Packwerk rule (if any) enforces it.
