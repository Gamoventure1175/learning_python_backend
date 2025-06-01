from fastapi import APIRouter, Depends, status, HTTPException, Body
from sqlalchemy import func
from sqlmodel import select
from app.models.posts import Post
from app.models.vote import Vote
from app.db.connection import SessionDep
from typing import Annotated
from app.utility.oauth2 import get_current_user
from app.validation.post import CreatePost, GetPost, PostWithVotes, UpdatePost
from app.validation.users import UserResponse

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=GetPost)
async def create_post(
    post: Annotated[CreatePost, Body(embed=True)],
    session: SessionDep,
    current_user: UserResponse = Depends(get_current_user),
):
    db_post = Post(owner_id=current_user.id, **post.model_dump())
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[PostWithVotes])
async def get_all_posts(
    session: SessionDep,
    current_user: UserResponse = Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
):
    statement = (
        select(Post, func.count(Vote.post_id).label("votes"))  # type:ignore
        .outerjoin(Vote)
        .where(Post.owner_id == current_user.id)
        .group_by(Post.id)  # type:ignore
        .limit(limit)
        .offset(skip)
    )
    result = session.exec(statement).all()

    response = [
        PostWithVotes(post=GetPost.model_validate(post), votes=votes)
        for post, votes in result
    ]
    return response


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostWithVotes)
async def get_post_by_id(
    id: int, session: SessionDep, current_user: UserResponse = Depends(get_current_user)
):
    statement = (
        select(Post, func.count(Vote.post_id).label("votes"))  # type: ignore
        .outerjoin(Vote)
        .where(Post.id == id)
        .group_by(Post.id)  # type: ignore
    )

    result = session.exec(statement).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find post with id {id}",
        )
        
    post, votes = result


    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorised to perform this request",
        )

    response = PostWithVotes(post=GetPost.model_validate(post), votes=votes)
    return response


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=GetPost)
async def update_post(
    session: SessionDep,
    post: UpdatePost,
    id: int,
    current_user: UserResponse = Depends(get_current_user),
):
    post_to_update = session.get(Post, id)
    if not post_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find post to update with id {id}",
        )

    if post_to_update.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorised to perform this request",
        )

    post_data = post.model_dump()
    post_to_update.sqlmodel_update(post_data)
    session.add(post_to_update)
    session.commit()
    session.refresh(post_to_update)
    return post_to_update


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int, session: SessionDep, current_user: UserResponse = Depends(get_current_user)
):
    post = session.get(Post, id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find post with id {id}",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorised to perform this request",
        )

    session.delete(post)
    session.commit()

    return {"deleted": True}
