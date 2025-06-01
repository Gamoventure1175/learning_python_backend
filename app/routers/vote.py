from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select, delete
from app.db.connection import SessionDep
from app.models.posts import Post
from app.models.vote import Vote
from app.validation.vote import Vote as VoteValidation
from app.utility.oauth2 import get_current_user
from app.validation.users import UserResponse


router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_a_post(
    vote: VoteValidation,
    session: SessionDep,
    current_user: UserResponse = Depends(get_current_user),
):
    post = session.exec(select(Post).where(Post.id == vote.post_id)).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist",
        )
    voted_post = session.exec(
        select(Vote).where(
            Vote.user_id == current_user.id, Vote.post_id == vote.post_id
        )
    )
    found_post = voted_post.first()
    if vote.direction == 1:
        if found_post:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"You have already voted this post",
            )
        vote_data = Vote(**vote.model_dump(), user_id=current_user.id)
        session.add(vote_data)
        session.commit()
        return {"message": "Successfully voted the post"}
    else:
        if not found_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You have not voted for this post yet",
            )
        session.delete(found_post)
        session.commit()
        return {"message": "Succesfully removed the vote"}
