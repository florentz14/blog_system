from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.category import Category


def get_category(db: Session, category_id: int):
    return db.scalars(select(Category).where(Category.id == category_id)).first()


def get_category_by_slug(db: Session, slug: str):
    return db.scalars(select(Category).where(Category.slug == slug)).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select(Category).offset(skip).limit(limit)).all()


def create_category(db: Session, category: dict):
    row = Category(**category)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def update_category(db: Session, category_id: int, category: dict):
    row = get_category(db, category_id)
    if row:
        for key, value in category.items():
            setattr(row, key, value)
        db.commit()
        db.refresh(row)
    return row


def delete_category(db: Session, category_id: int):
    row = get_category(db, category_id)
    if row:
        db.delete(row)
        db.commit()
    return row
