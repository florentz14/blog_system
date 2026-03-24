from __future__ import annotations

import bcrypt
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Category, Permission, Profile, Role, Tag, User
from . import catalog


def _get_or_create_permission(
    db: Session, code: str, description: str
) -> Permission:
    existing = db.scalars(select(Permission).where(Permission.code == code)).first()
    if existing:
        return existing
    row = Permission(code=code, description=description)
    db.add(row)
    db.flush()
    return row


def seed_permissions(db: Session) -> dict[str, Permission]:
    by_code: dict[str, Permission] = {}
    for code, desc in catalog.PERMISSIONS:
        by_code[code] = _get_or_create_permission(db, code, desc)
    return by_code


def _get_or_create_role(
    db: Session, name: str, description: str, *, is_system: bool
) -> Role:
    existing = db.scalars(select(Role).where(Role.name == name)).first()
    if existing:
        return existing
    row = Role(name=name, description=description, is_system=is_system)
    db.add(row)
    db.flush()
    return row


def seed_roles(db: Session) -> dict[str, Role]:
    by_name: dict[str, Role] = {}
    for name, desc, is_sys in catalog.ROLES:
        by_name[name] = _get_or_create_role(db, name, desc, is_system=is_sys)
    return by_name


def seed_role_permissions(
    db: Session,
    permissions_by_code: dict[str, Permission],
    roles_by_name: dict[str, Role],
) -> None:
    all_perms = list(permissions_by_code.values())

    for role_name, role in roles_by_name.items():
        codes = catalog.ROLE_PERMISSION_CODES.get(role_name, [])
        if role_name == "superadmin":
            want = set(all_perms)
        else:
            want = {permissions_by_code[c] for c in codes}
        current = set(role.permissions)
        for p in want - current:
            role.permissions.append(p)
        db.flush()


def seed_admin_user(db: Session, roles_by_name: dict[str, Role]) -> User | None:
    username = catalog.SEED_ADMIN_USERNAME
    existing = db.scalars(select(User).where(User.username == username)).first()
    if existing:
        role = roles_by_name.get(catalog.SEED_ADMIN_ROLE)
        if role and role not in existing.roles:
            existing.roles.append(role)
            db.flush()
        return None

    pwd = catalog.SEED_ADMIN_PASSWORD.encode("utf-8")
    hashed = bcrypt.hashpw(pwd, bcrypt.gensalt()).decode("utf-8")
    user = User(
        username=username,
        email=catalog.SEED_ADMIN_EMAIL,
        hashed_password=hashed,
        full_name=catalog.SEED_ADMIN_FULL_NAME,
        is_active=True,
    )
    db.add(user)
    db.flush()
    profile = Profile(user=user)
    db.add(profile)
    db.flush()
    role = roles_by_name.get(catalog.SEED_ADMIN_ROLE)
    if role:
        user.roles.append(role)
    db.flush()
    return user


def _get_or_create_tag(db: Session, name: str, description: str | None) -> Tag:
    existing = db.scalars(select(Tag).where(Tag.name == name)).first()
    if existing:
        return existing
    row = Tag(name=name, description=description)
    db.add(row)
    db.flush()
    return row


def seed_tags(db: Session) -> None:
    for name, desc in catalog.TAGS:
        _get_or_create_tag(db, name, desc)


def _get_or_create_category(
    db: Session, name: str, slug: str, description: str | None
) -> Category:
    existing = db.scalars(select(Category).where(Category.slug == slug)).first()
    if existing:
        return existing
    row = Category(name=name, slug=slug, description=description)
    db.add(row)
    db.flush()
    return row


def seed_categories(db: Session) -> None:
    for name, slug, desc in catalog.CATEGORIES:
        _get_or_create_category(db, name, slug, desc)


def run_seeds() -> None:
    """Run all seed steps idempotently."""
    db = SessionLocal()
    try:
        perms = seed_permissions(db)
        roles = seed_roles(db)
        seed_role_permissions(db, perms, roles)
        seed_admin_user(db, roles)
        seed_categories(db)
        seed_tags(db)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def main() -> None:
    run_seeds()
    print("Seeds OK (idempotent).")
    print(
        f"  Dev admin: username={catalog.SEED_ADMIN_USERNAME!r} "
        f"password={catalog.SEED_ADMIN_PASSWORD!r} (change in production)."
    )
