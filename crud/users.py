from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from ..models.profile import Profile
from ..models.user import User
from ..schemas.user import UserCreate


def get_user(db: Session, user_id: int, *, with_profile: bool = False):
    stmt = select(User).where(User.id == user_id)
    if with_profile:
        stmt = stmt.options(selectinload(User.profile))
    return db.scalars(stmt).first()


def get_user_by_email(db: Session, email: str):
    return db.scalars(select(User).where(User.email == email)).first()


def get_user_by_username(db: Session, username: str):
    return db.scalars(select(User).where(User.username == username)).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select(User).offset(skip).limit(limit)).all()


def search_users(db: Session, query: str, skip: int = 0, limit: int = 100):
    pattern = f"%{query}%"
    stmt = (
        select(User)
        .where(
            or_(
                User.username.ilike(pattern),
                User.email.ilike(pattern),
                User.full_name.ilike(pattern),
            )
        )
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(stmt).all()


def create_user(db: Session, user_in: UserCreate) -> User:
    data = user_in.model_dump(exclude={"profile"})
    profile_in = user_in.profile
    db_user = User(**data)
    db.add(db_user)
    db.flush()
    profile_kwargs = (
        profile_in.model_dump(exclude_unset=True) if profile_in else {}
    )
    db_profile = Profile(**profile_kwargs)
    db_profile.user = db_user
    db.add(db_profile)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: dict):
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in user.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
