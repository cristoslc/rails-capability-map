# 3. Build the Frontend with Hotwire: HTML Over the Wire

[Back to Capability Map](capability-map.html)

**The situation:** The client says 'modern frontend' and means React. Rails' answer — Turbo plus Stimulus sending HTML over the wire — is both the framework's default and its biggest reframe. You need to know what Hotwire actually does, where it shines, and when to genuinely reach for an SPA.

**What changes:** The mental model clicks: the server remains the owner of state; it sends HTML fragments. Turbo Drive intercepts navigation and forms; Turbo Frames swap targeted DOM regions; Turbo Streams push changes over SSE/WebSocket for live updates and broadcasts. Stimulus ties behavior to server-rendered markup with data attributes. You stop designing a JSON API for your own UI and let HTML be the interface — and you can articulate the honest cases where React still wins.

**You're ready when:** You can build CRUD with live updates and zero client state; explain Drive vs Frames vs Streams and when Streams is overkill; keep logic in Stimulus controllers and the server; and defend the Hotwire architecture (and its limits) to an SPA-minded team.

### Start here

| Resource | Format | Time | Why this one |
|----------|--------|------|-------------|
| [Turbo Handbook — Introduction](https://turbo.hotwired.dev/handbook/introduction) — Hotwire | Guide | 45 min | The source-of-truth handbook: Drive, Frames, Streams, and the 'HTML over the wire' model they share. |
| [Stimulus Handbook](https://stimulus.hotwired.dev/handbook/introduction) — Hotwire | Guide | 40 min | Progressive enhancement, targets/actions/values, and how behavior attaches to server-rendered HTML without a client framework. |
| [Hotwire Demystified (keynote)](https://www.rubyevents.org/talks/keynote-hotwire-demystified) — Chris Oliver — Tropical on Rails 2025 (RubyEvents) | Video | 60 min | The clearest current talk on when Drive vs Frames vs Streams each fit — 'let your HTML guide your JavaScript' — from GoRails' Chris Oliver. |

### Go deeper

| Resource | Format | Time | What it adds |
|----------|--------|------|-------------|
| [The Rails and Hotwire Codex](https://rubyandrails.info/books/the-rails-and-hotwire-codex) — Ayush Newatia | Book | ~20 hrs | 900+ pages of production-grade Rails + Hotwire: auth from scratch, every Action* sub-framework, Turbo Native apps, PostgreSQL search. The reference for 'how real modern Rails apps are built.' |
| [Hotwire Native for Rails Developers](https://masilotti.com/hotwire-native-for-rails-developers/) — Joe Masilotti | Book | ~8 hrs | Ship native iOS/Android shells around your Rails app without an API — the official path to mobile without a separate stack. |
| [Action Cable Overview](https://guides.rubyonrails.org/action_cable_overview.html) — Rails Foundation | Article | 25 min | WebSockets under Turbo Streams: channels, connections, Solid Cable as the default adapter in Rails 8, and broadcasting from models and callbacks. |
| [The Great Mobile Hack: Hotwire Native](https://www.rubyevents.org/talks/the-great-mobile-hack-hotwire-native) — Daniel Medina (RubyEvents) | Video | 40 min | A conference's own web app turned into a native mobile app — a concrete end-to-end Hotwire Native story. |

### Practice This

Add live search-as-you-type and instant delete to the Cap 2 catalog: search via Turbo Frame, deletion via Turbo Stream broadcast, focus management and stateful bits via Stimulus controllers. Then rewrite one screen deliberately against Rails (e.g., optimistic updates or a rich editor) and document why.
