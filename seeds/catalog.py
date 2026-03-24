"""Static catalog for seed data (permissions, roles, categories, tags)."""

# (code, description)
PERMISSIONS: list[tuple[str, str]] = [
    ("users:read", "List and view users"),
    ("users:create", "Create users"),
    ("users:update", "Update users"),
    ("users:delete", "Delete users"),
    ("profiles:read", "View profiles"),
    ("profiles:update", "Update profiles"),
    ("posts:read", "View published posts and allowed drafts"),
    ("posts:create", "Create posts"),
    ("posts:update", "Edit posts"),
    ("posts:delete", "Delete posts"),
    ("posts:publish", "Publish / unpublish posts"),
    ("comments:read", "View comments"),
    ("comments:create", "Create comments"),
    ("comments:update", "Edit comments"),
    ("comments:delete", "Delete comments"),
    ("comments:moderate", "Approve / moderate comments"),
    ("tags:read", "View tags"),
    ("tags:create", "Create tags"),
    ("tags:update", "Edit tags"),
    ("tags:delete", "Delete tags"),
    ("categories:read", "View categories"),
    ("categories:create", "Create categories"),
    ("categories:update", "Edit categories"),
    ("categories:delete", "Delete categories"),
    ("rbac:read", "View roles and permissions"),
    ("rbac:manage", "Manage roles, permissions, and assignments"),
]

# name, description, is_system
ROLES: list[tuple[str, str, bool]] = [
    ("superadmin", "Full system access", True),
    ("editor", "Content management and moderation", True),
    ("author", "Create and edit own posts (enforce in app layer)", True),
    ("reader", "Public read-only access", True),
]

# role name -> permission codes (superadmin gets all permissions at runtime)
ROLE_PERMISSION_CODES: dict[str, list[str]] = {
    "reader": [
        "posts:read",
        "comments:read",
        "tags:read",
        "categories:read",
    ],
    "author": [
        "posts:read",
        "posts:create",
        "posts:update",
        "posts:delete",
        "comments:read",
        "comments:create",
        "tags:read",
        "categories:read",
    ],
    "editor": [
        "users:read",
        "profiles:read",
        "posts:read",
        "posts:create",
        "posts:update",
        "posts:delete",
        "posts:publish",
        "comments:read",
        "comments:create",
        "comments:update",
        "comments:delete",
        "comments:moderate",
        "tags:read",
        "tags:create",
        "tags:update",
        "tags:delete",
        "categories:read",
        "categories:create",
        "categories:update",
        "categories:delete",
        "rbac:read",
    ],
    "superadmin": [],
}

# name, slug, description
CATEGORIES: list[tuple[str, str, str | None]] = [
    ("News", "news", "Announcements and updates"),
    ("Tutorials", "tutorials", "Step-by-step technical guides"),
    ("Opinion", "opinion", "Opinion pieces"),
]

# name, description
TAGS: list[tuple[str, str | None]] = [
    ("python", "Posts about Python"),
    ("fastapi", "APIs and FastAPI"),
    ("sqlalchemy", "ORM and databases"),
    ("tutorial", "How-to guides"),
]

# Development admin (change password in production)
SEED_ADMIN_USERNAME = "admin"
SEED_ADMIN_EMAIL = "admin@example.com"
SEED_ADMIN_PASSWORD = "changeme"
SEED_ADMIN_FULL_NAME = "Administrator"
SEED_ADMIN_ROLE = "superadmin"
