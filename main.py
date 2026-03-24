from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud
from .database import get_db
from .schemas import (
    CategoryCreate,
    CategoryRead,
    CommentCreate,
    CommentRead,
    PostCreate,
    PostRead,
    ProfileRead,
    ProfileUpdate,
    TagCreate,
    TagRead,
    UserCreate,
    UserRead,
    UserReadWithProfile,
)

app = FastAPI(
    title="Blog System API",
    description=(
        "Blog API with users, profiles, RBAC, categories, tags, posts, "
        "and moderated comments."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to Blog System API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/users/", response_model=UserReadWithProfile)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, email=str(user.email)):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user_in=user)


@app.get("/users/", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=UserReadWithProfile)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id, with_profile=True)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}/profile", response_model=ProfileRead)
def update_user_profile(
    user_id: int, body: ProfileUpdate, db: Session = Depends(get_db)
):
    if crud.get_user(db, user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    prof = crud.update_profile(db, user_id=user_id, data=body)
    if prof is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return prof


@app.post("/categories/", response_model=CategoryRead)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db=db, category=category.model_dump())


@app.get("/categories/", response_model=List[CategoryRead])
def read_categories(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_categories(db, skip=skip, limit=limit)


@app.get("/categories/{category_id}", response_model=CategoryRead)
def read_category(category_id: int, db: Session = Depends(get_db)):
    row = crud.get_category(db, category_id=category_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return row


@app.get("/categories/{category_id}/posts", response_model=List[PostRead])
def read_category_posts(
    category_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    if crud.get_category(db, category_id) is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.get_posts_by_category(
        db, category_id=category_id, skip=skip, limit=limit
    )


@app.post("/posts/", response_model=PostRead)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post.model_dump())


@app.get("/posts/", response_model=List[PostRead])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_posts(db, skip=skip, limit=limit)


@app.get("/posts/{post_id}", response_model=PostRead)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@app.put("/posts/{post_id}/publish", response_model=PostRead)
def publish_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.publish_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@app.post("/comments/", response_model=CommentRead)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, comment=comment.model_dump())


@app.get("/posts/{post_id}/comments", response_model=List[CommentRead])
def read_post_comments(
    post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_comments_by_post(db, post_id=post_id, skip=skip, limit=limit)


@app.put("/comments/{comment_id}/approve", response_model=CommentRead)
def approve_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.approve_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@app.post("/tags/", response_model=TagRead)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    return crud.create_tag(db=db, tag=tag.model_dump())


@app.get("/tags/", response_model=List[TagRead])
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tags(db, skip=skip, limit=limit)


@app.get("/tags/{tag_id}/posts", response_model=List[PostRead])
def read_tag_posts(
    tag_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_posts_by_tag(db, tag_id=tag_id, skip=skip, limit=limit)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
