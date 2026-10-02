# 2. Model Data with Active Record & the Database

[Back to Capability Map](capability-map.html)

**The situation:** Active Record is where Rails apps live or die. Queries grow mysterious, N+1s creep in, callbacks tangle domain logic, and nobody remembers which index backs which association. Schema decisions made casually in month one cost quarters to fix.

**What changes:** You learn Active Record as a pattern library over SQL, not an ORM to fight. Associations are query trees; validations are a boundary layer; callbacks are a sharp tool with few correct uses; the relation API is a composable SQL builder you can always interrogate with <code>to_sql</code> and <code>EXPLAIN ANALYZE</code>. Migrations become a deliberate discipline — especially the zero-downtime patterns — and the schema becomes something you design, not something that happens.

**You're ready when:** Given a domain, you can design a schema with the right associations, foreign keys, and indexes; predict the SQL any query chain emits; recognize callback abuse and reach for the right alternative (model split, service object, or straight SQL); and ship a migration against a live table without locking it.

### Start here

| Resource | Format | Time | Why this one |
|----------|--------|------|-------------|
| [Active Record Query Interface](https://guides.rubyonrails.org/active_record_querying.html) — Rails Foundation | Article | 45 min | The relation API, eager loading (includes/eager_load/preload), scopes, and how each chain compiles to SQL. The single most-consulted Rails guide. |
| [Active Record Associations](https://guides.rubyonrails.org/association_basics.html) — Rails Foundation | Article | 40 min | belongs_to/has_many/has_many :through semantics, the options that matter, and common misuses. |
| [Active Record Migrations](https://guides.rubyonrails.org/active_record_migrations.html) — Rails Foundation | Article | 30 min | Schema evolution as code: migration anatomy, reference columns with real FKs, and the safety rails around destructive changes. |

### Go deeper

| Resource | Format | Time | What it adds |
|----------|--------|------|-------------|
| [High Performance PostgreSQL for Rails](https://pragprog.com/titles/aapsql/high-performance-postgresql-for-rails/) — Andrew Atkinson | Book | ~12 hrs | The definitive database book for modern Rails: indexing, EXPLAIN, zero-downtime migrations, partitioning, read/write splitting. PostgreSQL 16 / Rails 7.1+ throughout. |
| [Layered Design for Ruby on Rails Applications](https://pragprog.com/titles/npalka8/layered-design-for-ruby-on-rails-applications) — Vladimir Dementyev | Book | ~10 hrs | Where does logic live? Models, services, form objects, and view layers on Rails 7+ — the best current book on organizing Rails application layers. |
| [Active Record Validations](https://guides.rubyonrails.org/active_record_validations.html) — Rails Foundation | Article | 25 min | Validation as a boundary discipline: declarative rules, context-dependent validations, and the DB constraints that back them up. |
| [Bullet — the N+1 hunt is automated](https://github.com/flyerhzm/bullet) — flyerhzm | Guide | 10 min | Watch your dev/test suite for N+1 queries and unused eager loading — and fail CI on them. Retrofit onto any app in ten minutes. |

### Practice This

Design the schema for a small multi-actor domain (e.g., clinic scheduling with patients, providers, and appointments). Write the SQL five query chains generate, run each through EXPLAIN ANALYZE on seeded data, and add the indexes (and counter caches/find_by optimizations) the plans demand.
