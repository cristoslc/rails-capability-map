# 4. Move Work Off-Request: Background Jobs & Async

[Back to Capability Map](capability-map.html)

**The situation:** Emails, exports, webhooks, integrations, scheduled work — the slow stuff that can't live in the request cycle. Sidekiq + Redis was the default stack for a decade; Rails 8 makes Solid Queue (database-backed, Redis-free) the default. Teams carry over either Redis folklore or Sidekiq muscle memory that doesn't map.

**What changes:** You judge job systems by durability and operations, not throughput mythology. Active Job is the portable abstraction — but you learn its serialization limits and what it does and doesn't normalize away. You design idempotent, retryable jobs, choose adapters per workload, and operate queues as production infrastructure: monitoring, backlogs, poison-job recovery. The Redis-vs-Solid decision becomes an articulated trade-off instead of inherited default.

**You're ready when:** You can defend an adapter choice per workload; write jobs that survive worker restarts and duplicate delivery; schedule recurring work; and keep an eye on queue health (mission-control dashboards, alerting on backlog) without Redis in the stack.

### Start here

| Resource | Format | Time | Why this one |
|----------|--------|------|-------------|
| [Active Job Basics](https://guides.rubyonrails.org/active_job_basics.html) — Rails Foundation | Article | 30 min | Job anatomy, queueing, retries and exception handling, and the adapter story — including Solid Queue as the Rails 8 default. |
| [Introducing Solid Queue](https://dev.37signals.com/introducing-solid-queue/) — 37signals | Article | 10 min | Why 37signals built a database-backed queue to replace Redis: design goals, durability model, and the reasoning behind the default switch. |
| [Solid Queue (Kaigi on Rails)](https://www.rubyevents.org/talks/solid-queue) — Shinichi Maeshima (RubyEvents) | Video | 30 min | A history of Rails background workers plus a Sidekiq-vs-Solid comparison framework — the fastest way to build your own selection criteria. |

### Go deeper

| Resource | Format | Time | What it adds |
|----------|--------|------|-------------|
| [Mission Control: Jobs](https://github.com/basecamp/mission_control-jobs) — Basecamp | Guide | 15 min | Production dashboards for Solid Queue/Solid Error: queue inspection, retries, discard. The observability half of the job decision. |
| [Rails Scales! (background work chapters)](https://pragprog.com/titles/cprpo/rails-scales/) — Cristian Planas | Book | ~30 min | Where jobs bite at scale — queue backpressure, priority lanes, and keeping the request cycle skinny — from the Zendesk tech lead who tunes giant Rails apps for a living. |
| [Agile Web Development with Rails 8 (job chapters)](https://pragprog.com/titles/rails8/agile-web-development-with-rails-8/) — Sam Ruby & Dave Thomas | Book | ~60 min | Active Job and integration patterns inside the canonical Rails 8 build. |

### Practice This

Take a synchronous flow from Cap 2 — upload → process → notify — and move it to Active Job on Solid Queue with retries and idempotency keys. Then kill a worker mid-job and verify nothing is lost or double-applied.
