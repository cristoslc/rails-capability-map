# 8. Ship & Operate: Kamal + the Zero-Dependency Production Stack

[Back to Capability Map](capability-map.html)

**The situation:** Heroku-era Rails muscle memory says deploys need a PaaS bill and production needs a Redis cluster. Rails 8's thesis is the opposite: Kamal 2 + Kamal Proxy for zero-downtime deploys on any plain VPS, Propshaft for assets, Thruster as the app-level proxy, and the Solid trifecta (Cache, Queue, Cable) replacing Redis entirely — your app needs one machine and Postgres.

**What changes:** You can run production deploys yourself: Kamal turns any server into an app host with zero-downtime releases via its proxy, rolling deploys, and access bridging — no Heroku, no Kubernetes, no yak-shave. You can articulate the Solid trifecta trade-offs (SQLite vs MySQL/Postgres adapters, durability, latency) against a Redis deployment. You know Thruster, Propshaft, and Mission Control, plus the ops hygiene — backups, logs, observability — that running it yourself now makes yours.

**You're ready when:** One command boots your app on a fresh VPS with zero-downtime deploy, HTTPS via proxy, and the Solid stack — no Redis, no PaaS. You can explain each Solid swap's trade-offs per workload, roll back a bad release, and restore from backup.

### Start here

| Resource | Format | Time | Why this one |
|----------|--------|------|-------------|
| [Rails 8: 'No PaaS Required'](https://rubyonrails.org/2024/9/27/rails-8-beta1-no-paas-required) — DHH / rubyonrails.org | Article | 10 min | The manifesto: Kamal 2, Thruster, Solid trifecta, and built-in auth as the new default production stack. |
| [Kamal — Introduction & Docs](https://kamal-deploy.org/docs/introduction) — 37signals | Guide | 30 min | Deploy-anywhere Docker tooling: config, proxy, zero-downtime releases, and the commands you'll actually run. |
| [Rails World 2024 Opening Keynote](https://www.rubyevents.org/talks/opening-keynote-rails-world-2024) — DHH (RubyEvents) | Video | 50 min | The full stack shipped live, from Solid Queue to Kamal Proxy — the fastest orientation to why these tools exist and how they compose. |

### Go deeper

| Resource | Format | Time | What it adds |
|----------|--------|------|-------------|
| [Kamal 2: Why and How You Should Leave the Cloud](https://www.rubyevents.org/talks/kamal) — Guillaume Briday (RubyEvents) | Video | 25 min | IaaS-vs-PaaS economics, server hardening, and a Kamal 2 deploy walkthrough from the community's most prolific Kamal speaker. |
| [Mission Control: Jobs — operate Solid Queue](https://github.com/basecamp/mission_control-jobs) — Basecamp | Guide | 15 min | Queue health, retries, and failed-job triage in production — the operations console that pairs with the Solid trifecta. |
| [Thruster — the app server proxy](https://github.com/basecamp/thruster) — Basecamp | Guide | 10 min | X-Accel-Buffering, static asset serving, HTTP/2 — what Thruster buys you between Kamal Proxy and Puma, and when you need it. |
| [Rails Scales! (production operations chapters)](https://pragprog.com/titles/cprpo/rails-scales/) — Cristian Planas | Book | ~90 min | Monitoring, budgets, and product limits applied to real Rails production systems — the discipline that comes after 'kamal deploy' goes green. |

### Practice This

Deploy the Cap 2–4 app to a $5 VPS with Kamal + Postgres + the Solid trifecta. Run a zero-downtime deploy while hammering the app with a load script, then purposefully roll back a bad release and restore a backup.
