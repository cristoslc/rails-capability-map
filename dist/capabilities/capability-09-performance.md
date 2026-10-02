# 9. Make It Fast: Performance That Survives Growth

[Back to Capability Map](capability-map.html)

**The situation:** p95 latency creeps, deploys get slower, memory balloons. 'Rails doesn't scale' is folklore (Zendesk, Shopify, GitHub, GitHub Actions-scale Rails monoliths all say otherwise) — but the folklore contains a real truth: Rails' defaults are velocity-first, and performance is a discipline you apply on purpose.

**What changes:** Performance becomes budget discipline, not archaeology. You measure first (benchmark-ips, log analysis, EXPLAIN), fix at the right layer (index, query shape, cache tier, memory pressure), and know the caching menu cold: fragment caching, Solid Cache as the Rails 8 default store, counter caches, eager loading — and invalidation, the hard part. You can cite the real-world evidence (multi-billion-req/day Rails monoliths) when someone proposes rewriting in Go as a 'fix.'

**You're ready when:** You can take a slow page and produce a profiling → query → index → cache chain with measured before/after p95; you choose cache tiers and invalidation strategies that stay correct under load; and you can argue Rails' scaling case with evidence and know the thresholds where it stops arguing for you.

### Start here

| Resource | Format | Time | Why this one |
|----------|--------|------|-------------|
| [Caching with Rails: An Overview (the Caching Guide)](https://guides.rubyonrails.org/caching_with_rails.html) — Rails Foundation | Article | 35 min | Fragment caching, Russian-doll caching, cache stores (Solid Cache), and the invalidation model every Rails performance plan builds on. |
| [Speed up Rails, Speed up Your Code](https://www.rubyevents.org/talks/speed-up-rails-speed-up-your-code) — Aaron Patterson (RubyEvents) | Video | 45 min | Inside Active Record performance from a Rails core perf lead: benchmarking tools, allocation profiling, and the memory-vs-speed trade-offs shaping recent Rails. |
| [A Rails Performance Guidebook: from 0 to 1B requests/day](https://www.rubyevents.org/talks/a-rails-performance-guidebook-from-0-to-1b-requests-day-helvetic-ruby-2023) — Cristian Planas & Anatoly Mikhaylov (RubyEvents) | Video | 50 min | Zendesk-scale Rails: monitoring, error budgets, DB right-sizing, write-through caching, cold storage, product limits — the performance playbook at real scale. |

### Go deeper

| Resource | Format | Time | What it adds |
|----------|--------|------|-------------|
| [Rails Scales!](https://pragprog.com/titles/cprpo/rails-scales/) — Cristian Planas | Book | ~8 hrs | The current definitive book on Rails performance and growth — from monitoring and product design to memory-aware coding — by a Zendesk tech lead. |
| [High Performance PostgreSQL for Rails](https://pragprog.com/titles/aapsql/high-performance-postgresql-for-rails/) — Andrew Atkinson | Book | ~12 hrs | The database deep dive: slow-query triage, index strategy, zero-downtime migrations, partitioning — where most Rails performance work actually happens. |
| [Bullet](https://github.com/flyerhzm/bullet) — flyerhzm | Guide | 10 min | Automated N+1 detection — most Rails perf wins start here in dev and CI. |
| [Under Deconstruction: The State of Shopify's Monolith](https://shopify.engineering/shopify-monolith) — Shopify Engineering | Article | 30 min | What 'Rails at extreme scale' concretely looks like — the reference evidence against the 'Rails doesn't scale' folklore. |

### Practice This

Profile the slowest page in your app (or a seeded clone of a public one). Find the dominant cost, fix it at the right layer, and measure p95 before/after at two data sizes (1× and 50×) to prove both the win and its durability at scale.
