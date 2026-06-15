from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.post import Post
from app.schemas import PostCreate, PostResponse, PostUpdate
from app.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_post = Post(
        title=post.title,
        content=post.content,
        owner_id=current_user.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    for key, value in post.model_dump(exclude_unset=True).items():
        setattr(db_post, key, value)
    
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(db_post)
    db.commit()
    return None