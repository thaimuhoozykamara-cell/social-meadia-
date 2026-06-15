from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.comment import Comment
from app.schemas import CommentCreate, CommentResponse, CommentUpdate
from app.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/comments", tags=["comments"])

@router.get("/", response_model=list[CommentResponse])
def get_comments(db: Session = Depends(get_db)):
    return db.query(Comment).all()

@router.get("/post/{post_id}", response_model=list[CommentResponse])
def get_comments_by_post(post_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.post_id == post_id).all()

@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_comment = Comment(
        content=comment.content,
        post_id=comment.post_id,
        owner_id=current_user.id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db_comment.content = comment.content
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(db_comment)
    db.commit()
    return None