#!/usr/bin/env python3
"""Generate dist/capability-map.html, capability markdown sources, graph source,
and index.html from a single source of truth (this file).

Mirrors the tl-learning-plan pipeline: shells/ patches the tl capability-map.html
shell and swaps in the Rails DATA array, mermaid graph, header/footer/legend/books.
"""

import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHELL = ROOT.parent / "tl-learning-plan" / "dist" / "capability-map.html"
DIST = ROOT / "dist"

G = "https://guides.rubyonrails.org"
TLCAP = "https://github.com/cristoslc"

START, DEEPER = "startResources", "deeperResources"

def R(title, author, url, fmt, time, desc, summary=None):
    r = {"title": title, "author": author, "url": url, "format": fmt,
         "time": time, "desc": desc}
    if summary:
        r["summaryUrl"] = summary
    return r

CAPS = [
    # ------------------------------------------------------------------ 1
    dict(
        id=1, cls="c1", title="Master the Rails Core & Its Conventions",
        situation=("You're an experienced engineer — but Rails is new, or has been for a while. "
                   "Someone hands you a Rails 8 codebase, or you're evaluating Rails for a client "
                   "project and getting opinions from 2013. Convention-over-configuration is either "
                   "the thing that makes Rails feel magical or arbitrary, depending on whether you've "
                   "internalized the mental model."),
        changes=("Treat conventions as a design system, not magic. You learn the request lifecycle "
                 "cold — router → controller → model → view — and what each layer owns. You learn "
                 "what the generators emit and why, how the directory encodes responsibility, and "
                 "the Ruby idioms Rails is built on. Suddenly any Rails repo — including the framework "
                 "source itself — is readable in minutes, and the 'Rails Way' becomes a set of "
                 "predictable decisions rather than folklore."),
        ready=("You can trace any request through a Rails app and name what each layer does and "
               "doesn't own. You can scaffold a resource and explain every generated file. You can "
               "open an unfamiliar Rails codebase and orient yourself without asking anyone."),
        practice=("Spin up a fresh Rails 8 app. Build one small resource end to end — say, a Maine "
                  "coffee-shop catalog with a form — using only generators and manual edits. Then "
                  "write out (on paper) the full lifecycle of one POST request: URL, route match, "
                  "controller action, params, model save, redirect, and every file involved."),
        start=[
            R("Getting Started — The Official Rails Guide", "Rails Foundation", f"{G}/getting_started.html",
              "article", "45 min",
              "The canonical first app, end to end. Current to Rails 8.x and maintained by the Rails "
              "Foundation. Do this even as a senior dev — every generated file is explained."),
            R("Rails Routing from the Outside In", "Rails Foundation", f"{G}/routing.html",
              "article", "35 min",
              "Routing is the front door of the convention system: RESTful defaults, resources, "
              "namespacing, and the params flow controllers receive."),
            R("The Rails Command Line", "Rails Foundation", f"{G}/command_line.html",
              "article", "15 min",
              "Generators, rake tasks, and bin/ scripts — the tooling that makes conventions tangible."),
        ],
        deeper=[
            R("Action Controller Overview", "Rails Foundation", f"{G}/action_controller_overview.html",
              "article", "40 min",
              "The layer where conventions meet your code: params filtering, callbacks, responder "
              "defaults, and Strong Parameters."),
            R("Agile Web Development with Rails 8", "Sam Ruby & Dave Thomas",
              "https://pragprog.com/titles/rails8/agile-web-development-with-rails-8/",
              "book", "~8 hrs",
              "The book Rails is itself tested against — a full production-style store app on Rails 8, "
              "written in consultation with the core team."),
            R("Ruby on Rails Tutorial (online edition)", "Michael Hartl", "https://www.railstutorial.org/book",
              "book", "20+ hrs",
              "The classic TDD-first deep tutorial. The online version tracks current Rails releases; "
              "best when you want test-driven depth, not just breadth."),
            R("Programming Ruby (5th ed., 'The Pickaxe')", "Noel Rappin & Dave Thomas",
              "https://pragprog.com/titles/ruby5/programming-ruby-3-3-5th-edition",
              "book", "~15 hrs",
              "The definitive Ruby language reference. Rails fluency is Ruby fluency — this is the "
              "companion to keep on the desk."),
            R("Rails 8: 'No PaaS Required'", "DHH / rubyonrails.org",
              "https://rubyonrails.org/2024/9/27/rails-8-beta1-no-paas-required",
              "article", "10 min",
              "The 2024 announcement framing modern Rails: the Solid trifecta, built-in auth, Kamal 2, "
              "Thruster. Reads the current Rails thesis in one sitting."),
            R("Rails World 2024 Opening Keynote", "DHH (RubyEvents)",
              "https://www.rubyevents.org/talks/opening-keynote-rails-world-2024",
              "video", "50 min",
              "DHH ships the Rails 8 beta live and makes the one-person-framework case. Watch after the "
              "announcement post to see the philosophy in motion."),
        ]),
    # ------------------------------------------------------------------ 2
    dict(
        id=2, cls="c2", title="Model Data with Active Record & the Database",
        situation=("Active Record is where Rails apps live or die. Queries grow mysterious, N+1s "
                   "creep in, callbacks tangle domain logic, and nobody remembers which index backs "
                   "which association. Schema decisions made casually in month one cost quarters to fix."),
        changes=("You learn Active Record as a pattern library over SQL, not an ORM to fight. "
                 "Associations are query trees; validations are a boundary layer; callbacks are a "
                 "sharp tool with few correct uses; the relation API is a composable SQL builder you "
                 "can always interrogate with <code>to_sql</code> and <code>EXPLAIN ANALYZE</code>. "
                 "Migrations become a deliberate discipline — especially the zero-downtime patterns — "
                 "and the schema becomes something you design, not something that happens."),
        ready=("Given a domain, you can design a schema with the right associations, foreign keys, "
               "and indexes; predict the SQL any query chain emits; recognize callback abuse and "
               "reach for the right alternative (model split, service object, or straight SQL); and "
               "ship a migration against a live table without locking it."),
        practice=("Design the schema for a small multi-actor domain (e.g., clinic scheduling with "
                  "patients, providers, and appointments). Write the SQL five query chains generate, "
                  "run each through EXPLAIN ANALYZE on seeded data, and add the indexes (and counter "
                  "caches/find_by optimizations) the plans demand."),
        start=[
            R("Active Record Query Interface", "Rails Foundation", f"{G}/active_record_querying.html",
              "article", "45 min",
              "The relation API, eager loading (includes/eager_load/preload), scopes, and how each "
              "chain compiles to SQL. The single most-consulted Rails guide."),
            R("Active Record Associations", "Rails Foundation", f"{G}/association_basics.html",
              "article", "40 min",
              "belongs_to/has_many/has_many :through semantics, the options that matter, and common "
              "misuses."),
            R("Active Record Migrations", "Rails Foundation", f"{G}/active_record_migrations.html",
              "article", "30 min",
              "Schema evolution as code: migration anatomy, reference columns with real FKs, and "
              "the safety rails around destructive changes."),
        ],
        deeper=[
            R("High Performance PostgreSQL for Rails", "Andrew Atkinson",
              "https://pragprog.com/titles/aapsql/high-performance-postgresql-for-rails/",
              "book", "~12 hrs",
              "The definitive database book for modern Rails: indexing, EXPLAIN, zero-downtime "
              "migrations, partitioning, read/write splitting. PostgreSQL 16 / Rails 7.1+ throughout."),
            R("Layered Design for Ruby on Rails Applications", "Vladimir Dementyev",
              "https://pragprog.com/titles/npalka8/layered-design-for-ruby-on-rails-applications",
              "book", "~10 hrs",
              "Where does logic live? Models, services, form objects, and view layers on Rails 7+ — "
              "the best current book on organizing Rails application layers."),
            R("Active Record Validations", "Rails Foundation", f"{G}/active_record_validations.html",
              "article", "25 min",
              "Validation as a boundary discipline: declarative rules, context-dependent "
              "validations, and the DB constraints that back them up."),
            R("Bullet — the N+1 hunt is automated", "flyerhzm",
              "https://github.com/flyerhzm/bullet", "guide", "10 min",
              "Watch your dev/test suite for N+1 queries and unused eager loading — and fail CI on "
              "them. Retrofit onto any app in ten minutes."),
        ]),
    # ------------------------------------------------------------------ 3
    dict(
        id=3, cls="c3", title="Build the Frontend with Hotwire: HTML Over the Wire",
        situation=("The client says 'modern frontend' and means React. Rails' answer — Turbo plus "
                   "Stimulus sending HTML over the wire — is both the framework's default and its "
                   "biggest reframe. You need to know what Hotwire actually does, where it shines, "
                   "and when to genuinely reach for an SPA."),
        changes=("The mental model clicks: the server remains the owner of state; it sends HTML "
                 "fragments. Turbo Drive intercepts navigation and forms; Turbo Frames swap targeted "
                 "DOM regions; Turbo Streams push changes over SSE/WebSocket for live updates and "
                 "broadcasts. Stimulus ties behavior to server-rendered markup with data attributes. "
                 "You stop designing a JSON API for your own UI and let HTML be the interface — and "
                 "you can articulate the honest cases where React still wins."),
        ready=("You can build CRUD with live updates and zero client state; explain Drive vs Frames "
               "vs Streams and when Streams is overkill; keep logic in Stimulus controllers and the "
               "server; and defend the Hotwire architecture (and its limits) to an SPA-minded team."),
        practice=("Add live search-as-you-type and instant delete to the Cap 2 catalog: search via "
                  "Turbo Frame, deletion via Turbo Stream broadcast, focus management and stateful "
                  "bits via Stimulus controllers. Then rewrite one screen deliberately against Rails "
                  "(e.g., optimistic updates or a rich editor) and document why."),
        start=[
            R("Turbo Handbook — Introduction", "Hotwire", "https://turbo.hotwired.dev/handbook/introduction",
              "guide", "45 min",
              "The source-of-truth handbook: Drive, Frames, Streams, and the 'HTML over the wire' "
              "model they share."),
            R("Stimulus Handbook", "Hotwire", "https://stimulus.hotwired.dev/handbook/introduction",
              "guide", "40 min",
              "Progressive enhancement, targets/actions/values, and how behavior attaches to "
              "server-rendered HTML without a client framework."),
            R("Hotwire Demystified (keynote)", "Chris Oliver — Tropical on Rails 2025 (RubyEvents)",
              "https://www.rubyevents.org/talks/keynote-hotwire-demystified",
              "video", "60 min",
              "The clearest current talk on when Drive vs Frames vs Streams each fit — 'let your HTML "
              "guide your JavaScript' — from GoRails' Chris Oliver."),
        ],
        deeper=[
            R("The Rails and Hotwire Codex", "Ayush Newatia",
              "https://rubyandrails.info/books/the-rails-and-hotwire-codex",
              "book", "~20 hrs",
              "900+ pages of production-grade Rails + Hotwire: auth from scratch, every Action* "
              "sub-framework, Turbo Native apps, PostgreSQL search. The reference for 'how real "
              "modern Rails apps are built.'"),
            R("Hotwire Native for Rails Developers", "Joe Masilotti",
              "https://masilotti.com/hotwire-native-for-rails-developers/",
              "book", "~8 hrs",
              "Ship native iOS/Android shells around your Rails app without an API — the official "
              "path to mobile without a separate stack."),
            R("Action Cable Overview", "Rails Foundation", f"{G}/action_cable_overview.html",
              "article", "25 min",
              "WebSockets under Turbo Streams: channels, connections, Solid Cable as the default "
              "adapter in Rails 8, and broadcasting from models and callbacks."),
            R("The Great Mobile Hack: Hotwire Native", "Daniel Medina (RubyEvents)",
              "https://www.rubyevents.org/talks/the-great-mobile-hack-hotwire-native",
              "video", "40 min",
              "A conference's own web app turned into a native mobile app — a concrete end-to-end "
              "Hotwire Native story."),
        ]),
    # ------------------------------------------------------------------ 4
    dict(
        id=4, cls="c4", title="Move Work Off-Request: Background Jobs & Async",
        situation=("Emails, exports, webhooks, integrations, scheduled work — the slow stuff that "
                   "can't live in the request cycle. Sidekiq + Redis was the default stack for a "
                   "decade; Rails 8 makes Solid Queue (database-backed, Redis-free) the default. "
                   "Teams carry over either Redis folklore or Sidekiq muscle memory that doesn't map."),
        changes=("You judge job systems by durability and operations, not throughput mythology. "
                 "Active Job is the portable abstraction — but you learn its serialization limits and "
                 "what it does and doesn't normalize away. You design idempotent, retryable jobs, "
                 "choose adapters per workload, and operate queues as production infrastructure: "
                 "monitoring, backlogs, poison-job recovery. The Redis-vs-Solid decision becomes an "
                 "articulated trade-off instead of inherited default."),
        ready=("You can defend an adapter choice per workload; write jobs that survive worker "
               "restarts and duplicate delivery; schedule recurring work; and keep an eye on queue "
               "health (mission-control dashboards, alerting on backlog) without Redis in the stack."),
        practice=("Take a synchronous flow from Cap 2 — upload → process → notify — and move it to "
                  "Active Job on Solid Queue with retries and idempotency keys. Then kill a worker "
                  "mid-job and verify nothing is lost or double-applied."),
        start=[
            R("Active Job Basics", "Rails Foundation", f"{G}/active_job_basics.html",
              "article", "30 min",
              "Job anatomy, queueing, retries and exception handling, and the adapter story — "
              "including Solid Queue as the Rails 8 default."),
            R("Introducing Solid Queue", "37signals", "https://dev.37signals.com/introducing-solid-queue/",
              "article", "10 min",
              "Why 37signals built a database-backed queue to replace Redis: design goals, "
              "durability model, and the reasoning behind the default switch."),
            R("Solid Queue (Kaigi on Rails)", "Shinichi Maeshima (RubyEvents)",
              "https://www.rubyevents.org/talks/solid-queue",
              "video", "30 min",
              "A history of Rails background workers plus a Sidekiq-vs-Solid comparison framework — "
              "the fastest way to build your own selection criteria."),
        ],
        deeper=[
            R("Mission Control: Jobs", "Basecamp", "https://github.com/basecamp/mission_control-jobs",
              "guide", "15 min",
              "Production dashboards for Solid Queue/Solid Error: queue inspection, retries, "
              "discard. The observability half of the job decision."),
            R("Rails Scales! (background work chapters)", "Cristian Planas",
              "https://pragprog.com/titles/cprpo/rails-scales/",
              "book", "~30 min",
              "Where jobs bite at scale — queue backpressure, priority lanes, and keeping the request "
              "cycle skinny — from the Zendesk tech lead who tunes giant Rails apps for a living."),
            R("Agile Web Development with Rails 8 (job chapters)", "Sam Ruby & Dave Thomas",
              "https://pragprog.com/titles/rails8/agile-web-development-with-rails-8/",
              "book", "~60 min",
              "Active Job and integration patterns inside the canonical Rails 8 build."),
        ]),
    # ------------------------------------------------------------------ 5
    dict(
        id=5, cls="c5", title="Secure the App: Auth, Authorization & Safe Defaults",
        situation=("Rails 8 ships an authentication generator and leaves authorization out on "
                   "purpose. The pre-2024 habits — bolt on Devise, sprinkle admin flags, hope — don't "
                   "hold up in a codebase where the auth code is now yours. Meanwhile the actual "
                   "security surface (sessions, params, CSRF, secrets, mass assignment) is bigger "
                   "than the login form."),
        changes=("Authentication and authorization split cleanly in your head: Rails 8's "
                 "<code>bin/rails g authentication</code> gives you a minimal, auditable authN "
                 "starting point you're expected to extend; authZ is a policy layer (Pundit, "
                 "ActionPolicy) you design for your domain. You learn the Rails security defaults "
                 "you're trusting — encrypted cookie sessions, CSRF tokens, Strong Parameters — plus "
                 "the gaps: rate limiting, secure headers, secrets management, and continuous "
                 "scanning with Brakeman."),
        ready=("You can generate, read, and extend a Rails 8 auth stack (registrations, password "
               "reset, 2FA) without a gem; write policy classes that cover a multi-role domain and "
               "enforce them in controllers and views; pass a clean Brakeman audit; and write a "
               "one-page threat model naming what you trust and why."),
        practice=("Build auth from the generator for the Cap 2 app; add role-based policies with "
                  "Pundit (or ActionPolicy); run Brakeman + a dependency audit, fix everything it "
                  "raises, and write the one-page threat model for the session flow."),
        start=[
            R("The State of Security in Rails 8", "Greg Molnar (Rails World 2024)",
              "https://greg.molnar.io/blog/the-state-of-security-in-rails-8/",
              "article", "20 min",
              "The Rails World talk in written form: the auth generator, what it does and doesn't "
              "cover, and Rails 8's security posture."),
            R("Securing Rails Applications (the Security Guide)", "Rails Foundation",
              f"{G}/security.html", "article", "45 min",
              "Sessions, CSRF, XSS, mass assignment, secure headers, SSL, secrets — the framework's "
              "official security doctrine in one guide."),
            R("Rails 8 Adds a Built-in Authentication Generator", "Saeloun Blog",
              "https://blog.saeloun.com/2025/05/12/rails-8-adds-built-in-authentication-generator/",
              "article", "10 min",
              "What <code>rails g authentication</code> emits (sessions, password reset, "
              "has_secure_password, rate limiting) and what you must add yourself."),
        ],
        deeper=[
            R("Pundit — policy-object authorization", "Varvet", "https://github.com/varvet/pundit",
              "guide", "30 min",
              "Simple policy classes per model, scopes for listing, and how it composes with "
              "<code>Current.user</code> from the Rails 8 generator. Contrast with ActionPolicy and "
              "CanCanCan before choosing."),
            R("Brakeman — static security scanning", "PresidentBeef",
              "https://github.com/presidentbeef/brakeman", "guide", "15 min",
              "Rails-specific static analysis for injection, unsafe redirects, dynamic evals. "
              "Run it in CI from day one."),
            R("Rails Security Best Practices: A Comprehensive Guide", "Saeloun Blog",
              "https://blog.saeloun.com/2026/04/28/rails-security-best-practices-a-comprehensive-guide/",
              "article", "25 min",
              "The full checklist across Rails 7→8.1: auth generator, params.expect, local CI security "
              "checks, and where authorization deliberately stays out of core."),
            R("OWASP Cheat Sheet Series", "OWASP", "https://cheatsheetseries.owasp.org/",
              "guide", "browse",
              "When your threat model goes past Rails defaults — auth, sessions, secrets, API "
              "tokens — the cross-framework discipline lives here."),
        ]),
    # ------------------------------------------------------------------ 6
    dict(
        id=6, cls="c6", title="Test It: The Safety Net That Buys Freedom",
        situation=("A Rails app without a trustworthy suite is a codebase you can only fear-change. "
                   "Rails ships batteries included — Minitest, request/integration specs, system "
                   "tests over a real browser, fixtures and factories — and Rails 8.1 adds local CI. "
                   "The question is not whether to test but what each level should protect."),
        changes=("You adapt the testing pyramid to Rails reality: model and request specs as the "
                 "load-bearing layer, a small set of system tests guarding key user flows, factories "
                 "over fixtures, and deterministic state management as a first-class concern. Flaky "
                 "tests get diagnosed (ordering, time zones, async races) rather than retried into "
                 "oblivion. The suite's runtime becomes a design pressure, and with local CI the "
                 "pre-push loop finally has no excuse."),
        ready=("Your suite is green under ~10 minutes with fast feedback; request specs cover every "
               "endpoint, a handful of system tests guard real flows; CI is deterministic and flake "
               "free; you trust the suite enough to refactor the models underneath it."),
        practice=("Retrofit tests onto a legacy Rails controller: write request specs for each route, "
                  "then one system test of the full user flow. Introduce a deliberate data race and "
                  "watch randomized ordering catch it — then fix the test's hidden coupling."),
        start=[
            R("Testing Rails Applications (the Testing Guide)", "Rails Foundation",
              f"{G}/testing.html", "article", "45 min",
              "The official map: what Rails generates for tests, request vs integration vs system, "
              "fixtures, and the built-in helpers."),
            R("How We Test Rails Applications", "thoughtbot",
              "https://thoughtbot.com/blog/how-we-test-rails-applications",
              "article", "25 min",
              "A mature team's complete testing philosophy — factories, system tests, request specs "
              "as the workhorse — from the makers of FactoryBot and RSpec ecosystem staples."),
        ],
        deeper=[
            R("Flaky Tests, Be Gone", "Evil Martians",
              "https://evilmartians.com/chronicles/flaky-tests-be-gone-long-lasting-relief-chronic-ci-retry-irritation",
              "article", "30 min",
              "Ordering, time, transactional tests, and the quarantine discipline — the single "
              "best writeup on making test suites deterministic."),
            R("Layered Design for Ruby on Rails Applications (testing chapters)", "Vladimir Dementyev",
              "https://pragprog.com/titles/npalka8/layered-design-for-ruby-on-rails-applications",
              "book", "~60 min",
              "Testing each application layer in isolation — models, services, views, system — as an "
              "architecture concern, not just a habit."),
            R("Ruby on Rails Tutorial — the TDD chapters", "Michael Hartl", "https://www.railstutorial.org/book",
              "book", "20+ hrs (relevant chapters)",
              "Red-green-refactor practiced live across a growing app: integration tests, "
              "login-protected pages, Capybara system tests. The best full-course TDD education for "
              "Rails."),
            R("RailsConf 2025 talk index", "RubyEvents",
              "https://www.rubyevents.org/events/railsconf-2025",
              "video", "browse",
              "Current-condition conference talks including testing and flake war stories from "
              "teams running large Rails suites."),
        ]),
    # ------------------------------------------------------------------ 7
    dict(
        id=7, cls="c7", title="Grow the Codebase: Architecture Without Microservices",
        situation=("The codebase is three years old and the fat-model era shows: controllers with "
                   "business logic, callbacks with side effects, no seams. Rails' answer is emphatically "
                   "not a service fleet — 'extraction' here means layering (POROs, form/query objects, "
                   "ViewComponents), modular monoliths (engines, pack-werk), and knowing exactly when "
                   "a module should become a service."),
        changes=("You can reason about where logic belongs in a Rails app — and defend it — using "
                 "the layered-model vocabulary: plain Ruby objects at domain seams instead of God "
                 "objects. You know the modular monolith toolkit (engines, Packwerk) and its honest "
                 "critique: boundary tools prevent new coupling but don't fix design or organization. "
                 "You can evaluate extract-vs-keep decisions with evidence instead of aesthetics, and "
                 "when extraction is right, you know what good looks like in both worlds."),
        ready=("Given a large Rails app, you can map its module seams and coupling hot spots; design "
               "a bounded modularization (or argue against one) with an ADR-style note; and extract "
               "one well-bounded domain (service, engine, or query object layer) without breaking "
               "the monolith's advantages."),
        practice=("Pick the fattest controller or model in a large Rails app (yours or a well-known "
                  "open-source one). Extract one seam: a query object, a service object, or a "
                  "ViewComponent. Then write an ADR-style note: what boundary you created, why "
                  "you did NOT extract a service, and what Packwerk rule (if any) enforces it."),
        start=[
            R("The Majestic Monolith", "DHH / 37signals",
              "https://m.signalvnoise.com/the-majestic-monolith/",
              "article", "10 min",
              "The original articulation of Rails' architectural default — and the philosophy behind "
              "why the one-person (and one-hundred-person) framework stays single-deploy."),
            R("Modularizing Rails Monoliths One Bite at a Time", "Marc Reynolds / Doximity",
              "https://technology.doximity.com/articles/modularizing-rails-monoliths-one-bite-at-a-time",
              "article", "25 min",
              "A real team's phased Packwerk modularization — boundaries, enforcement, and what it "
              "did and didn't buy them."),
            R("The Myth of the Modular Monolith (EuRuKo 2025 closing keynote)", "Eileen M. Uchitelle (RubyEvents)",
              "https://www.rubyevents.org/talks/closing-keynote-the-myth-of-the-modular-monolith",
              "video", "45 min",
              "The essential counterweight, from a Rails core team alum with Shopify/GitHub/37signals "
              "scar tissue: most modularization pains are human and organizational, and tools like "
              "Packwerk can't fix that. Decide with both talks in mind."),
        ],
        deeper=[
            R("Under Deconstruction: The State of Shopify's Monolith", "Shopify Engineering",
              "https://shopify.engineering/shopify-monolith",
              "article", "30 min",
              "One of the largest Rails codebases ever, on engines, Packwerk, SOLID at component "
              "scale, and the developer-behavior realities of modularization."),
            R("Packwerk", "Shopify", "https://github.com/Shopify/packwerk",
              "guide", "20 min",
              "The dependency-enforcement gem: packages, dependency declarations, and violation "
              "gates in CI."),
            R("Layered Design for Ruby on Rails Applications", "Vladimir Dementyev",
              "https://pragprog.com/titles/npalka8/layered-design-for-ruby-on-rails-applications",
              "book", "~10 hrs",
              "The architectural vocabulary for where logic lives — the strongest current book-length "
              "treatment of Rails application layering."),
            R("RailsConf 2025 talk index", "RubyEvents",
              "https://www.rubyevents.org/events/railsconf-2025",
              "video", "browse",
              "Multiple current talks on monolith growth, modularization stories, and scaling orgs "
              "on shared codebases."),
        ]),
    # ------------------------------------------------------------------ 8
    dict(
        id=8, cls="c8", title="Ship & Operate: Kamal + the Zero-Dependency Production Stack",
        situation=("Heroku-era Rails muscle memory says deploys need a PaaS bill and production "
                   "needs a Redis cluster. Rails 8's thesis is the opposite: Kamal 2 + Kamal Proxy "
                   "for zero-downtime deploys on any plain VPS, Propshaft for assets, Thruster as "
                   "the app-level proxy, and the Solid trifecta (Cache, Queue, Cable) replacing "
                   "Redis entirely — your app needs one machine and Postgres."),
        changes=("You can run production deploys yourself: Kamal turns any server into an app host "
                 "with zero-downtime releases via its proxy, rolling deploys, and access bridging — "
                 "no Heroku, no Kubernetes, no yak-shave. You can articulate the Solid trifecta "
                 "trade-offs (SQLite vs MySQL/Postgres adapters, durability, latency) against a "
                 "Redis deployment. You know Thruster, Propshaft, and Mission Control, plus the ops "
                 "hygiene — backups, logs, observability — that running it yourself now makes yours."),
        ready=("One command boots your app on a fresh VPS with zero-downtime deploy, HTTPS via proxy, "
               "and the Solid stack — no Redis, no PaaS. You can explain each Solid swap's trade-offs "
               "per workload, roll back a bad release, and restore from backup."),
        practice=("Deploy the Cap 2–4 app to a $5 VPS with Kamal + Postgres + the Solid trifecta. "
                  "Run a zero-downtime deploy while hammering the app with a load script, then "
                  "purposefully roll back a bad release and restore a backup."),
        start=[
            R("Rails 8: 'No PaaS Required'", "DHH / rubyonrails.org",
              "https://rubyonrails.org/2024/9/27/rails-8-beta1-no-paas-required",
              "article", "10 min",
              "The manifesto: Kamal 2, Thruster, Solid trifecta, and built-in auth as the new default "
              "production stack."),
            R("Kamal — Introduction & Docs", "37signals", "https://kamal-deploy.org/docs/introduction",
              "guide", "30 min",
              "Deploy-anywhere Docker tooling: config, proxy, zero-downtime releases, and the "
              "commands you'll actually run."),
            R("Rails World 2024 Opening Keynote", "DHH (RubyEvents)",
              "https://www.rubyevents.org/talks/opening-keynote-rails-world-2024",
              "video", "50 min",
              "The full stack shipped live, from Solid Queue to Kamal Proxy — the fastest orientation "
              "to why these tools exist and how they compose."),
        ],
        deeper=[
            R("Kamal 2: Why and How You Should Leave the Cloud", "Guillaume Briday (RubyEvents)",
              "https://www.rubyevents.org/talks/kamal",
              "video", "25 min",
              "IaaS-vs-PaaS economics, server hardening, and a Kamal 2 deploy walkthrough from the "
              "community's most prolific Kamal speaker."),
            R("Mission Control: Jobs — operate Solid Queue", "Basecamp",
              "https://github.com/basecamp/mission_control-jobs",
              "guide", "15 min",
              "Queue health, retries, and failed-job triage in production — the operations console "
              "that pairs with the Solid trifecta."),
            R("Thruster — the app server proxy", "Basecamp", "https://github.com/basecamp/thruster",
              "guide", "10 min",
              "X-Accel-Buffering, static asset serving, HTTP/2 — what Thruster buys you between "
              "Kamal Proxy and Puma, and when you need it."),
            R("Rails Scales! (production operations chapters)", "Cristian Planas",
              "https://pragprog.com/titles/cprpo/rails-scales/",
              "book", "~90 min",
              "Monitoring, budgets, and product limits applied to real Rails production systems — "
              "the discipline that comes after 'kamal deploy' goes green."),
        ]),
    # ------------------------------------------------------------------ 9
    dict(
        id=9, cls="c9", title="Make It Fast: Performance That Survives Growth",
        situation=("p95 latency creeps, deploys get slower, memory balloons. 'Rails doesn't scale' "
                   "is folklore (Zendesk, Shopify, GitHub, GitHub Actions-scale Rails monoliths all "
                   "say otherwise) — but the folklore contains a real truth: Rails' defaults are "
                   "velocity-first, and performance is a discipline you apply on purpose."),
        changes=("Performance becomes budget discipline, not archaeology. You measure first "
                 "(benchmark-ips, log analysis, EXPLAIN), fix at the right layer (index, query shape, "
                 "cache tier, memory pressure), and know the caching menu cold: fragment caching, "
                 "Solid Cache as the Rails 8 default store, counter caches, eager loading — and "
                 "invalidation, the hard part. You can cite the real-world evidence (multi-billion-req/day "
                 "Rails monoliths) when someone proposes rewriting in Go as a 'fix.'"),
        ready=("You can take a slow page and produce a profiling → query → index → cache chain with "
               "measured before/after p95; you choose cache tiers and invalidation strategies that "
               "stay correct under load; and you can argue Rails' scaling case with evidence and "
               "know the thresholds where it stops arguing for you."),
        practice=("Profile the slowest page in your app (or a seeded clone of a public one). Find the "
                  "dominant cost, fix it at the right layer, and measure p95 before/after at two "
                  "data sizes (1× and 50×) to prove both the win and its durability at scale."),
        start=[
            R("Caching with Rails: An Overview (the Caching Guide)", "Rails Foundation",
              f"{G}/caching_with_rails.html", "article", "35 min",
              "Fragment caching, Russian-doll caching, cache stores (Solid Cache), and the "
              "invalidation model every Rails performance plan builds on."),
            R("Speed up Rails, Speed up Your Code", "Aaron Patterson (RubyEvents)",
              "https://www.rubyevents.org/talks/speed-up-rails-speed-up-your-code",
              "video", "45 min",
              "Inside Active Record performance from a Rails core perf lead: benchmarking tools, "
              "allocation profiling, and the memory-vs-speed trade-offs shaping recent Rails."),
            R("A Rails Performance Guidebook: from 0 to 1B requests/day", "Cristian Planas & Anatoly Mikhaylov (RubyEvents)",
              "https://www.rubyevents.org/talks/a-rails-performance-guidebook-from-0-to-1b-requests-day-helvetic-ruby-2023",
              "video", "50 min",
              "Zendesk-scale Rails: monitoring, error budgets, DB right-sizing, write-through "
              "caching, cold storage, product limits — the performance playbook at real scale."),
        ],
        deeper=[
            R("Rails Scales!", "Cristian Planas",
              "https://pragprog.com/titles/cprpo/rails-scales/",
              "book", "~8 hrs",
              "The current definitive book on Rails performance and growth — from monitoring and "
              "product design to memory-aware coding — by a Zendesk tech lead."),
            R("High Performance PostgreSQL for Rails", "Andrew Atkinson",
              "https://pragprog.com/titles/aapsql/high-performance-postgresql-for-rails/",
              "book", "~12 hrs",
              "The database deep dive: slow-query triage, index strategy, zero-downtime migrations, "
              "partitioning — where most Rails performance work actually happens."),
            R("Bullet", "flyerhzm", "https://github.com/flyerhzm/bullet",
              "guide", "10 min",
              "Automated N+1 detection — most Rails perf wins start here in dev and CI."),
            R("Under Deconstruction: The State of Shopify's Monolith", "Shopify Engineering",
              "https://shopify.engineering/shopify-monolith",
              "article", "30 min",
              "What 'Rails at extreme scale' concretely looks like — the reference evidence against "
              "the 'Rails doesn't scale' folklore."),
        ]),
    # ------------------------------------------------------------------ 10
    dict(
        id=10, cls="c0", title="Use AI as a Rails Thinking Partner",
        situation=("AI agents write Rails unusually well — the framework's conventions, maturity, "
                   "and stable APIs give models dense training signal. That cuts both ways: agents "
                   "generate confident, plausible code that can be subtly wrong or unsafe, and it's "
                   "tempting to skip the security and testing discipline Caps 5–6 build."),
        changes=("You use AI leverage in the places Rails makes it safe: migrations and specs as "
                 "reviewable diffs, schema and codebase Q&A, scaffolding the boring 70% — while "
                 "humans keep the correctness and security gates auth, policies, audit, test suite). "
                 "You bring the Rails convention knowledge that lets you constrain agents usefully "
                 "and review their output like a senior reviewing a junior. You know the honest "
                 "failure data: agents can slow experts down on familiar code, and Rails' stability "
                 "is the advantage that offsets it."),
        ready=("You have an agent-assisted Rails workflow that produces production-worthy code — "
               "tests, Brakeman audit, and review passing on agent output; and you can articulate "
               "where agents multiply your velocity versus where hand-writing it yourself stays "
               "faster and safer."),
        practice=("Build the same small feature twice: once fully hand-rolled (following Caps 1–6), "
                  "once agent-first with a conventions + security-prompted workflow. Compare diffs, "
                  "test coverage, security findings, and time; write down the reusable workflow that "
                  "emerged, and note which gates stayed human."),
        start=[
            R("Agentic Coding", "Armin Ronacher",
              "https://www.youtube.com/watch?v=bpWPEhO7RqE",
              "video", "71 min",
              "Flask's creator on a real production agentic workflow: when agents excel, where they "
              "fail, and the practical workflow that emerges.",
              summary="https://github.com/cristoslc/tl-learning-plan/blob/main/dist/summaries/agentic-coding-armin-ronacher.md"),
            R("AI Impact on Experienced Developer Productivity", "METR",
              "https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/",
              "research", "20 min",
              "The sobering RCT: experienced devs were 19% slower with AI on familiar code while "
              "believing they were 20% faster. The calibration every 'AI-assisted' claim needs."),
        ],
        deeper=[
            R("AI Tooling for Software Engineers in 2026", "Gergely Orosz / Pragmatic Engineer",
              "https://newsletter.pragmaticengineer.com/p/ai-tooling-2026",
              "article", "25 min",
              "Survey data from ~1,000 engineers on what AI tooling is actually used and trusted — "
              "the noise-free baseline."),
            R("Agentic Engineering Patterns", "Simon Willison",
              "https://simonwillison.net/guides/agentic-engineering-patterns/",
              "guide", "30 min",
              "Living guide to agent workflow patterns — review gates, sandboxing, and how to make "
              "agent output trustworthy."),
            R("A Year of Vibes", "Armin Ronacher",
              "https://lucumr.pocoo.org/2025/12/22/a-year-of-vibes/",
              "article", "15 min",
              "Twelve months of agentic coding in production: what held up, what fell over, and how "
              "the practice matured."),
        ]),
]

GRAPH = """%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#eef0fa',
    'primaryBorderColor': '#00049E',
    'primaryTextColor': '#00049E',
    'lineColor': '#706F6F',
    'fontSize': '13px',
    'fontFamily': 'Arial, sans-serif',
    'edgeLabelBackground': '#ffffff'
  }
}}%%
graph TD
    C1["1. Rails Core & Conventions"]
    C2["2. Active Record & Data"]
    C3["3. Hotwire Frontend"]
    C4["4. Background Jobs"]
    C5["5. Security & Auth"]
    C6["6. Testing"]
    C7["7. Growing the Codebase"]
    C8["8. Ship & Operate"]
    C9["9. Performance"]
    C10["10. AI Partner"]:::alongside

    C1 --> C2
    C1 --> C3
    C2 --> C4
    C2 --> C7
    C2 --> C9
    C3 --> C4
    C4 --> C8
    C5 --> C6
    C6 --> C7
    C7 --> C8
    C8 --> C9

    classDef default fill:#eef0fa,stroke:#00049E,stroke-width:2px,color:#00049E,font-weight:700,rx:20,ry:20
    classDef alongside fill:#f8f8f8,stroke:#706F6F,stroke-width:1.5px,stroke-dasharray:5 4,color:#4a4a49,font-weight:600,rx:20,ry:20

    style C2 fill:#e6f7f7,stroke:#006b6b,color:#005555
    style C3 fill:#ededfc,stroke:#1a1f99,color:#1a1f99
    style C4 fill:#e6f4fa,stroke:#00698f,color:#005a7a
    style C5 fill:#f2f0f8,stroke:#5a4a8a,color:#4a3d75
    style C6 fill:#edf7f1,stroke:#2d7a4a,color:#1f6338
    style C7 fill:#fef3e6,stroke:#8a4500,color:#6b3600
    style C8 fill:#f2e6e9,stroke:#8a1538,color:#6b0f2a
    style C9 fill:#f8edf4,stroke:#7a2d5a,color:#5e1d45
"""

HEADER_P = ("A capability-based learning map for modern Ruby on Rails — core conventions through "
            "AI-assisted shipping, current to Rails 8.x. Each capability has a situation, curated "
            "resources, and a practice exercise. Start with <strong>Capability 1</strong> or jump to "
            "whatever your project needs most.")

LEGEND = ("<strong>1. Rails Core &amp; Conventions</strong> is the gateway, feeding <strong>2. Active Record "
          "&amp; Data</strong> — the foundation for the <strong>3. Hotwire frontend</strong>, <strong>4. Background "
          "Jobs</strong>, and <strong>9. Performance</strong>, which all build on the data layer. "
          "<strong>5. Security &amp; Auth</strong> pairs with <strong>6. Testing</strong> — the correctness "
          "pair — and testing in turn feeds <strong>7. Growing the Codebase</strong> (you can only refactor "
          "what tests protect). <strong>7</strong> feeds <strong>8. Ship &amp; Operate</strong>, which closes "
          "the loop back into <strong>9. Performance</strong> in production. <strong>10. AI Partner</strong> "
          "is a force multiplier across all of it.")

BOOKS = [
    "<em>Agile Web Development with Rails 8</em> &mdash; Sam Ruby &amp; Dave Thomas",
    "<em>The Rails and Hotwire Codex</em> &mdash; Ayush Newatia",
    "<em>Layered Design for Ruby on Rails Applications</em> &mdash; Vladimir Dementyev",
    "<em>Rails Scales!</em> &mdash; Cristian Planas",
    "<em>High Performance PostgreSQL for Rails</em> &mdash; Andrew Atkinson",
    "<em>Hotwire Native for Rails Developers</em> &mdash; Joe Masilotti",
    "<em>Programming Ruby (5th ed., 'The Pickaxe')</em> &mdash; Noel Rappin &amp; Dave Thomas",
]

SLUGS = [
    "rails-core-and-conventions",
    "active-record-and-data-modeling",
    "hotwire-html-over-the-wire",
    "background-jobs-and-async",
    "security-and-auth",
    "testing",
    "growing-the-codebase",
    "ship-and-operate",
    "performance",
    "ai-partner",
]

REPO = "https://github.com/cristoslc/rails-capability-map"


def cap_to_markdown(cap):
    lines = [f"# {cap['id']}. {cap['title']}", "",
             "[Back to Capability Map](capability-map.html)", "",
             f"**The situation:** {cap['situation']}", "",
             f"**What changes:** {cap['changes']}", "",
             f"**You're ready when:** {cap['ready']}", "",
             "### Start here", "", "| Resource | Format | Time | Why this one |",
             "|----------|--------|------|-------------|"]
    for r in cap["startResources"]:
        s = f" ([summary]({r['summaryUrl']}))" if r.get("summaryUrl") else ""
        lines.append(f"| [{r['title']}]({r['url']}){s} — {r['author']} | {r['format'].title()} | "
                     f"{r['time']} | {r['desc']} |")
    lines += ["", "### Go deeper", "", "| Resource | Format | Time | What it adds |",
              "|----------|--------|------|-------------|"]
    for r in cap["deeperResources"]:
        s = f" ([summary]({r['summaryUrl']}))" if r.get("summaryUrl") else ""
        lines.append(f"| [{r['title']}]({r['url']}){s} — {r['author']} | {r['format'].title()} | "
                     f"{r['time']} | {r['desc']} |")
    lines += ["", "### Practice This", "", cap["practice"], ""]
    return "\n".join(lines)


def build_html():
    shell = SHELL.read_text(encoding="utf-8")
    repo_old = "https://github.com/cristoslc/tl-learning-plan"

    shell = shell.replace("<title>TL Capability Map</title>", "<title>Rails Capability Map</title>")
    shell = shell.replace("<h1>TL Capability Map", "<h1>Rails Capability Map")
    shell = shell.replace(f'<a href="{repo_old}" class="github-link"',
                          f'<a href="{REPO}" class="github-link"')
    shell = shell.replace(re.search(r"<p>A capability-based program.*?</p>", shell, re.S).group(0),
                          f"<p>{HEADER_P}</p>")
    shell = shell.replace(re.search(r"<div class=\"map-legend\">.*?</div>", shell, re.S).group(0),
                          f'<div class="map-legend">\n{LEGEND}\n    </div>')
    books_html = "\n".join(f"        <li>{b}</li>" for b in BOOKS)
    shell = shell.replace(re.search(r"<ul class=\"book-list\">.*?</ul>", shell, re.S).group(0),
                          f'<ul class="book-list">\n{books_html}\n      </ul>')
    shell = shell.replace(re.search(r"<span>TL Development Program.*?</span>", shell, re.S).group(0),
                          f"<span>Rails Capability Map &mdash; October 2026 &middot; "
                          f"<a href=\"{REPO}\" style=\"color: var(--accent);\">Source on GitHub</a></span>")
    shell = shell.replace("'tl-cap-progress'", "'rails-cap-progress'")

    # DATA block
    i = shell.index("const DATA = [")
    j = shell.index("const CHEVRON_SVG")
    caps_json = json.dumps(CAPS, ensure_ascii=False, indent=2)
    caps_json = re.sub(r'"(situation|changes|ready|practice)":', r'"\1":', caps_json)  # no-op, readability
    shell = shell[:i] + "const DATA =\n" + caps_json + ";\n\n" + shell[j:]

    # Mermaid block
    i = shell.index('<pre class="mermaid">')
    j = shell.index("</pre>", i) + len("</pre>")
    shell = shell[:i] + '<pre class="mermaid">\n' + GRAPH + "</pre>" + shell[j:]

    (DIST / "capability-map.html").write_text(shell, encoding="utf-8")


def main():
    for cap in CAPS:
        cap["startResources"] = cap.pop("start")
        cap["deeperResources"] = cap.pop("deeper")
    DIST.mkdir(parents=True, exist_ok=True)
    build_html()
    caps_dir = DIST / "capabilities"
    caps_dir.mkdir(exist_ok=True)
    for cap in CAPS:
        slug = SLUGS[cap["id"] - 1]
        (caps_dir / f"capability-{cap['id']:02d}-{slug}.md").write_text(
            cap_to_markdown(cap), encoding="utf-8")
    (DIST / "capability-graph.mmd").write_text(GRAPH, encoding="utf-8")
    (DIST / "index.html").write_text(
        '<!DOCTYPE html>\n<meta http-equiv="refresh" content="0;url=capability-map.html">\n'
        '<link rel="canonical" href="capability-map.html">\n', encoding="utf-8")
    print(f"OK: {len(CAPS)} capabilities -> {len(list(caps_dir.glob('*.md')))} markdown files, "
          f"capability-map.html, capability-graph.mmd, index.html")


if __name__ == "__main__":
    main()