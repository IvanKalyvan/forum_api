from pydantic import BaseModel

class Post_Schema(BaseModel):

    title: str
    content: str
    user_id: int

class POSTCommentSchema(BaseModel):

    content: str
    post_id: int
    user_id: int

class PUTCommentSchema(BaseModel):

    content: str
    user_id: int