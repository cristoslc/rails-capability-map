# 5. Secure the App: Auth, Authorization & Safe Defaults

[Back to Capability Map](capability-map.html)

**The situation:** Rails 8 ships an authentication generator and leaves authorization out on purpose. The pre-2024 habits — bolt on Devise, sprinkle admin flags, hope — don't hold up in a codebase where the auth code is now yours. Meanwhile the actual security surface (sessions, params, CSRF, secrets, mass assignment) is bigger than the login form.

**What changes:** Authentication and authorization split cleanly in your head: Rails 8's <code>bin/rails g authentication</code> gives you a minimal, auditable authN starting point you're expected to extend; authZ is a policy layer (Pundit, ActionPolicy) you design for your domain. You learn the Rails security defaults you're trusting — encrypted cookie sessions, CSRF tokens, Strong Parameters — plus the gaps: rate limiting, secure headers, secrets management, and continuous scanning with Brakeman.

**You're ready when:** You can generate, read, and extend a Rails 8 auth stack (registrations, password reset, 2FA) without a gem; write policy classes that cover a multi-role domain and enforce them in controllers and views; pass a clean Brakeman audit; and write a one-page threat model naming what you trust and why.

### Start here

| Resource | Format | Time | Why this one |
|----------|--------|------|-------------|
| [The State of Security in Rails 8](https://greg.molnar.io/blog/the-state-of-security-in-rails-8/) — Greg Molnar (Rails World 2024) | Article | 20 min | The Rails World talk in written form: the auth generator, what it does and doesn't cover, and Rails 8's security posture. |
| [Securing Rails Applications (the Security Guide)](https://guides.rubyonrails.org/security.html) — Rails Foundation | Article | 45 min | Sessions, CSRF, XSS, mass assignment, secure headers, SSL, secrets — the framework's official security doctrine in one guide. |
| [Rails 8 Adds a Built-in Authentication Generator](https://blog.saeloun.com/2025/05/12/rails-8-adds-built-in-authentication-generator/) — Saeloun Blog | Article | 10 min | What <code>rails g authentication</code> emits (sessions, password reset, has_secure_password, rate limiting) and what you must add yourself. |

### Go deeper

| Resource | Format | Time | What it adds |
|----------|--------|------|-------------|
| [Pundit — policy-object authorization](https://github.com/varvet/pundit) — Varvet | Guide | 30 min | Simple policy classes per model, scopes for listing, and how it composes with <code>Current.user</code> from the Rails 8 generator. Contrast with ActionPolicy and CanCanCan before choosing. |
| [Brakeman — static security scanning](https://github.com/presidentbeef/brakeman) — PresidentBeef | Guide | 15 min | Rails-specific static analysis for injection, unsafe redirects, dynamic evals. Run it in CI from day one. |
| [Rails Security Best Practices: A Comprehensive Guide](https://blog.saeloun.com/2026/04/28/rails-security-best-practices-a-comprehensive-guide/) — Saeloun Blog | Article | 25 min | The full checklist across Rails 7→8.1: auth generator, params.expect, local CI security checks, and where authorization deliberately stays out of core. |
| [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) — OWASP | Guide | browse | When your threat model goes past Rails defaults — auth, sessions, secrets, API tokens — the cross-framework discipline lives here. |

### Practice This

Build auth from the generator for the Cap 2 app; add role-based policies with Pundit (or ActionPolicy); run Brakeman + a dependency audit, fix everything it raises, and write the one-page threat model for the session flow.
