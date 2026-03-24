from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.profile import Profile
from ..schemas.profile import ProfileUpdate


def get_profile_by_user_id(db: Session, user_id: int):
    return db.scalars(select(Profile).where(Profile.user_id == user_id)).first()


def update_profile(db: Session, user_id: int, data: ProfileUpdate):
    prof = get_profile_by_user_id(db, user_id)
    if not prof:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(prof, key, value)
    db.commit()
    db.refresh(prof)
    return prof
