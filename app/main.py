import os
import sys

from fastapi import FastAPI

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '../'))
sys.path.append(root_dir)

from auth.auth import auth_backend
from auth.schemas import UserRead, UserCreate
from routers import post_router, comment_router, pdf_file_router, analytics_router
from fastapi_users_local import fastapi_users

app = FastAPI(

    title="Forum"

)

app.include_router(

    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],

)

app.include_router(

    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],

)

app.include_router(

    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],

)

app.include_router(post_router)
app.include_router(comment_router)
app.include_router(pdf_file_router)
app.include_router(analytics_router)
