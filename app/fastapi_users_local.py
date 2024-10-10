from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from auth.user_manager import get_user_manager
from pg_functions.database_connect import User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)