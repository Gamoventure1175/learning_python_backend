from fastapi import APIRouter, Depends, status, HTTPException, Body
from sqlmodel import select
from app.models.posts import Post
from app.db.connection import SessionDep
from typing import Annotated, List
from app.utility.oauth2 import get_current_user
from app.validation.post import CreatePost, GetPost, UpdatePost
from app.validation.users import UserResponse

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=GetPost)
async def create_post(
    post: Annotated[CreatePost, Body(embed=True)],
    session: SessionDep,
    current_user: UserResponse = Depends(get_current_user),
):
    db_post = Post(**post.model_dump())
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[GetPost])
async def get_all_posts(
    sessoin: SessionDep,
    session: SessionDep,
    current_user: UserResponse = Depends(get_current_user),
):
    all_posts = sessoin.exec(select(Post)).all()
    if all_posts == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Could not find posts"
        )

    return all_posts


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=GetPost)
async def get_post_by_id(
    id: int, session: SessionDep, current_user: UserResponse = Depends(get_current_user)
):
    post = session.exec(select(Post).where(Post.id == id)).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find post with id {id}",
        )
    return post


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=GetPost)
async def update_post(
    session: SessionDep,
    post: UpdatePost,
    id: int,
    user_id: int = Depends(get_current_user),
):
    post_to_update = session.get(Post, id)
    if not post_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find post to update with id {id}",
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
    session.delete(post)
    session.commit()

    return {"deleted": True}
