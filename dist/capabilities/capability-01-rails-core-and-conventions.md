# 1. Master the Rails Core & Its Conventions

[Back to Capability Map](capability-map.html)

**The situation:** You're an experienced engineer — but Rails is new, or has been for a while. Someone hands you a Rails 8 codebase, or you're evaluating Rails for a client project and getting opinions from 2013. Convention-over-configuration is either the thing that makes Rails feel magical or arbitrary, depending on whether you've internalized the mental model.

**What changes:** Treat conventions as a design system, not magic. You learn the request lifecycle cold — router → controller → model → view — and what each layer owns. You learn what the generators emit and why, how the directory encodes responsibility, and the Ruby idioms Rails is built on. Suddenly any Rails repo — including the framework source itself — is readable in minutes, and the 'Rails Way' becomes a set of predictable decisions rather than folklore.

**You're ready when:** You can trace any request through a Rails app and name what each layer does and doesn't own. You can scaffold a resource and explain every generated file. You can open an unfamiliar Rails codebase and orient yourself without asking anyone.

### Start here

| Resource | Format | Time | Why this one |
|----------|--------|------|-------------|
| [Getting Started — The Official Rails Guide](https://guides.rubyonrails.org/getting_started.html) — Rails Foundation | Article | 45 min | The canonical first app, end to end. Current to Rails 8.x and maintained by the Rails Foundation. Do this even as a senior dev — every generated file is explained. |
| [Rails Routing from the Outside In](https://guides.rubyonrails.org/routing.html) — Rails Foundation | Article | 35 min | Routing is the front door of the convention system: RESTful defaults, resources, namespacing, and the params flow controllers receive. |
| [The Rails Command Line](https://guides.rubyonrails.org/command_line.html) — Rails Foundation | Article | 15 min | Generators, rake tasks, and bin/ scripts — the tooling that makes conventions tangible. |

### Go deeper

| Resource | Format | Time | What it adds |
|----------|--------|------|-------------|
| [Action Controller Overview](https://guides.rubyonrails.org/action_controller_overview.html) — Rails Foundation | Article | 40 min | The layer where conventions meet your code: params filtering, callbacks, responder defaults, and Strong Parameters. |
| [Agile Web Development with Rails 8](https://pragprog.com/titles/rails8/agile-web-development-with-rails-8/) — Sam Ruby & Dave Thomas | Book | ~8 hrs | The book Rails is itself tested against — a full production-style store app on Rails 8, written in consultation with the core team. |
| [Ruby on Rails Tutorial (online edition)](https://www.railstutorial.org/book) — Michael Hartl | Book | 20+ hrs | The classic TDD-first deep tutorial. The online version tracks current Rails releases; best when you want test-driven depth, not just breadth. |
| [Programming Ruby (5th ed., 'The Pickaxe')](https://pragprog.com/titles/ruby5/programming-ruby-3-3-5th-edition) — Noel Rappin & Dave Thomas | Book | ~15 hrs | The definitive Ruby language reference. Rails fluency is Ruby fluency — this is the companion to keep on the desk. |
| [Rails 8: 'No PaaS Required'](https://rubyonrails.org/2024/9/27/rails-8-beta1-no-paas-required) — DHH / rubyonrails.org | Article | 10 min | The 2024 announcement framing modern Rails: the Solid trifecta, built-in auth, Kamal 2, Thruster. Reads the current Rails thesis in one sitting. |
| [Rails World 2024 Opening Keynote](https://www.rubyevents.org/talks/opening-keynote-rails-world-2024) — DHH (RubyEvents) | Video | 50 min | DHH ships the Rails 8 beta live and makes the one-person-framework case. Watch after the announcement post to see the philosophy in motion. |

### Practice This

Spin up a fresh Rails 8 app. Build one small resource end to end — say, a Maine coffee-shop catalog with a form — using only generators and manual edits. Then write out (on paper) the full lifecycle of one POST request: URL, route match, controller action, params, model save, redirect, and every file involved.
