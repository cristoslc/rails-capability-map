# 10. Use AI as a Rails Thinking Partner

[Back to Capability Map](capability-map.html)

**The situation:** AI agents write Rails unusually well — the framework's conventions, maturity, and stable APIs give models dense training signal. That cuts both ways: agents generate confident, plausible code that can be subtly wrong or unsafe, and it's tempting to skip the security and testing discipline Caps 5–6 build.

**What changes:** You use AI leverage in the places Rails makes it safe: migrations and specs as reviewable diffs, schema and codebase Q&A, scaffolding the boring 70% — while humans keep the correctness and security gates auth, policies, audit, test suite). You bring the Rails convention knowledge that lets you constrain agents usefully and review their output like a senior reviewing a junior. You know the honest failure data: agents can slow experts down on familiar code, and Rails' stability is the advantage that offsets it.

**You're ready when:** You have an agent-assisted Rails workflow that produces production-worthy code — tests, Brakeman audit, and review passing on agent output; and you can articulate where agents multiply your velocity versus where hand-writing it yourself stays faster and safer.

### Start here

| Resource | Format | Time | Why this one |
|----------|--------|------|-------------|
| [Agentic Coding](https://www.youtube.com/watch?v=bpWPEhO7RqE) ([summary](https://github.com/cristoslc/tl-learning-plan/blob/main/dist/summaries/agentic-coding-armin-ronacher.md)) — Armin Ronacher | Video | 71 min | Flask's creator on a real production agentic workflow: when agents excel, where they fail, and the practical workflow that emerges. |
| [AI Impact on Experienced Developer Productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) — METR | Research | 20 min | The sobering RCT: experienced devs were 19% slower with AI on familiar code while believing they were 20% faster. The calibration every 'AI-assisted' claim needs. |

### Go deeper

| Resource | Format | Time | What it adds |
|----------|--------|------|-------------|
| [AI Tooling for Software Engineers in 2026](https://newsletter.pragmaticengineer.com/p/ai-tooling-2026) — Gergely Orosz / Pragmatic Engineer | Article | 25 min | Survey data from ~1,000 engineers on what AI tooling is actually used and trusted — the noise-free baseline. |
| [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/) — Simon Willison | Guide | 30 min | Living guide to agent workflow patterns — review gates, sandboxing, and how to make agent output trustworthy. |
| [A Year of Vibes](https://lucumr.pocoo.org/2025/12/22/a-year-of-vibes/) — Armin Ronacher | Article | 15 min | Twelve months of agentic coding in production: what held up, what fell over, and how the practice matured. |

### Practice This

Build the same small feature twice: once fully hand-rolled (following Caps 1–6), once agent-first with a conventions + security-prompted workflow. Compare diffs, test coverage, security findings, and time; write down the reusable workflow that emerged, and note which gates stayed human.
