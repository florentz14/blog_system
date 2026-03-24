from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from ..models.post import Post
from ..models.tag import Tag, post_tags


def get_tag(db: Session, tag_id: int):
    return db.scalars(select(Tag).where(Tag.id == tag_id)).first()


def get_tag_by_name(db: Session, name: str):
    return db.scalars(select(Tag).where(Tag.name == name)).first()


def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select(Tag).offset(skip).limit(limit)).all()


def search_tags(db: Session, query: str, skip: int = 0, limit: int = 100):
    pattern = f"%{query}%"
    stmt = (
        select(Tag)
        .where(or_(Tag.name.ilike(pattern), Tag.description.ilike(pattern)))
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(stmt).all()


def create_tag(db: Session, tag: dict):
    db_tag = Tag(**tag)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def update_tag(db: Session, tag_id: int, tag: dict):
    db_tag = get_tag(db, tag_id)
    if db_tag:
        for key, value in tag.items():
            setattr(db_tag, key, value)
        db.commit()
        db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, tag_id: int):
    db_tag = get_tag(db, tag_id)
    if db_tag:
        db.delete(db_tag)
        db.commit()
    return db_tag


def get_posts_by_tag(db: Session, tag_id: int, skip: int = 0, limit: int = 100):
    stmt = (
        select(Post)
        .join(post_tags)
        .where(post_tags.c.tag_id == tag_id, Post.is_published.is_(True))
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(stmt).all()


def add_tag_to_post(db: Session, post_id: int, tag_id: int):
    post = db.scalars(select(Post).where(Post.id == post_id)).first()
    tag = get_tag(db, tag_id)
    if post and tag and tag not in post.tags:
        post.tags.append(tag)
        db.commit()
        db.refresh(post)
    return post


def remove_tag_from_post(db: Session, post_id: int, tag_id: int):
    post = db.scalars(select(Post).where(Post.id == post_id)).first()
    tag = get_tag(db, tag_id)
    if post and tag and tag in post.tags:
        post.tags.remove(tag)
        db.commit()
        db.refresh(post)
    return post
