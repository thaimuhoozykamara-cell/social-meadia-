from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.like import Like
from app.schemas import LikeCreate, LikeResponse
from app.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/likes", tags=["likes"])

@router.get("/", response_model=list[LikeResponse])
def get_likes(db: Session = Depends(get_db)):
    return db.query(Like).all()

@router.get("/post/{post_id}", response_model=list[LikeResponse])
def get_likes_by_post(post_id: int, db: Session = Depends(get_db)):
    return db.query(Like).filter(Like.post_id == post_id).all()

@router.post("/", response_model=LikeResponse, status_code=status.HTTP_201_CREATED)
def create_like(
    like: LikeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_like = db.query(Like).filter(
        Like.post_id == like.post_id,
        Like.user_id == current_user.id
    ).first()
    if existing_like:
        raise HTTPException(status_code=400, detail="Already liked")
    
    new_like = Like(
        post_id=like.post_id,
        user_id=current_user.id
    )
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return new_like

@router.delete("/{like_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_like(
    like_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_like = db.query(Like).filter(Like.id == like_id).first()
    if not db_like:
        raise HTTPException(status_code=404, detail="Like not found")
    if db_like.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(db_like)
    db.commit()
    return None