from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from ..models.post import Post


def get_post(db: Session, post_id: int):
    return db.scalars(select(Post).where(Post.id == post_id)).first()


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    stmt = (
        select(Post)
        .where(Post.is_published.is_(True))
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(stmt).all()


def get_posts_by_author(db: Session, author_id: int, skip: int = 0, limit: int = 100):
    stmt = (
        select(Post)
        .where(Post.author_id == author_id)
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(stmt).all()


def search_posts(db: Session, query: str, skip: int = 0, limit: int = 100):
    pattern = f"%{query}%"
    stmt = (
        select(Post)
        .where(
            or_(
                Post.title.ilike(pattern),
                Post.content.ilike(pattern),
                Post.summary.ilike(pattern),
            ),
            Post.is_published.is_(True),
        )
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(stmt).all()


def create_post(db: Session, post: dict):
    db_post = Post(**post)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post_id: int, post: dict):
    db_post = get_post(db, post_id)
    if db_post:
        for key, value in post.items():
            setattr(db_post, key, value)
        db.commit()
        db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post


def publish_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if db_post:
        db_post.is_published = True
        db.commit()
        db.refresh(db_post)
    return db_post


def get_draft_posts(db: Session, skip: int = 0, limit: int = 100):
    stmt = (
        select(Post)
        .where(Post.is_published.is_(False))
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(stmt).all()


def get_posts_by_category(
    db: Session, category_id: int, skip: int = 0, limit: int = 100
):
    stmt = (
        select(Post)
        .where(
            Post.category_id == category_id,
            Post.is_published.is_(True),
        )
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(stmt).all()
