# Blog System

A blog API built with **FastAPI**, **SQLAlchemy 2.0**, **SQLite**, **Alembic**, **RBAC** (roles and permissions), **user profiles**, **categories**, **tags**, moderated comments, and database seeders.

**Repository:** [github.com/florentz14/blog_system](https://github.com/florentz14/blog_system)

## Requirements

- Python 3.10+
- A virtual environment is recommended

## Installation

```bash
cd blog_system
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Import the project as package `blog_system` from the **parent** directory of the project folder (e.g. `Documents`), not from inside `blog_system` alone.

## Database and migrations

```powershell
$env:PYTHONPATH = "path\to\parent\of\blog_system"
cd path\to\blog_system
alembic upgrade head
```

## Seeders (initial data)

Creates permissions, roles, role–permission links, a development admin user, **categories**, and tags. **Idempotent** (safe to run multiple times).

```powershell
$env:PYTHONPATH = "path\to\parent\of\blog_system"
python -m blog_system.seeds
```

### Development admin credentials

| Field | Value |
|--------|--------|
| **Username** | `admin` |
| **Email** | `admin@example.com` |
| **Password** | `changeme` |

Defined in `seeds/catalog.py` (`SEED_ADMIN_*`). **Change these in production**; the password is stored with **bcrypt**.

## Run the API

```powershell
$env:PYTHONPATH = "path\to\parent\of\blog_system"
cd path\to\blog_system
python -m uvicorn blog_system.main:app --reload --host 0.0.0.0 --port 8000
```

Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Layout (overview)

```
blog_system/
├── alembic/              # migrations
├── crud/                 # data access
├── models/               # ORM (User, Profile, Post, Category, Tag, Comment, RBAC, …)
├── schemas/              # Pydantic
├── seeds/                # seed scripts
├── database.py
├── main.py
├── pyrightconfig.json    # extraPaths for static analysis
└── requirements.txt
```

## Main models

- **User** — basic account (hashed password in the current API).
- **Profile** — one-to-one with user (bio, avatar URL, etc.).
- **Category** — flat taxonomy (`name`, unique `slug`, `description`). Complements **tags**: usually one stable category per post vs many flexible tags. A **Post** may optionally reference a category (`category_id`, `ON DELETE SET NULL`).
- **Post** — author, optional category, publish flag, many-to-many tags via `post_tags`.
- **Tag** — tags and `post_tags` pivot.
- **Comment** — threaded via `parent_id`, moderation via `is_approved`.
- **RBAC** — `Permission`, `Role`, `role_permissions`, `user_roles`, `user_permissions` (direct grant/deny rows).

## Notable endpoints

- Users and profile: `POST /users/`, `GET /users/{id}`, `PUT /users/{id}/profile`
- Categories: `POST /categories/`, `GET /categories/`, `GET /categories/{id}`, `GET /categories/{id}/posts`
- Posts: `POST /posts/` (optional `category_id`), publish, listings
- Tags and posts-by-tag
- Comments and approval

## Tooling

- **Alembic** — schema versioning
- **Pydantic** — request/response validation
- **Pyright / basedpyright** — `extraPaths: [".."]` so `import blog_system` resolves

## License

Internal / educational use per your project policy.
