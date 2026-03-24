from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.comment import Comment


def get_comment(db: Session, comment_id: int):
    return db.scalars(select(Comment).where(Comment.id == comment_id)).first()


def get_comments_by_post(
    db: Session, post_id: int, skip: int = 0, limit: int = 100
):
    stmt = (
        select(Comment)
        .where(Comment.post_id == post_id)
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(stmt).all()


def approve_comment(db: Session, comment_id: int):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        db_comment.is_approved = "approved"
        db.commit()
        db.refresh(db_comment)
    return db_comment


def create_comment(db: Session, comment: dict):
    db_comment = Comment(**comment)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def update_comment(db: Session, comment_id: int, comment: dict):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        for key, value in comment.items():
            setattr(db_comment, key, value)
        db.commit()
        db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: int):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment
