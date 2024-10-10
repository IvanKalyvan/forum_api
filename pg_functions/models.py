from sqlalchemy import MetaData, Table, Column, BIGINT, BOOLEAN, String, Text, DATE, ForeignKey
from datetime import datetime, timezone

metadata = MetaData()

user = Table(

    "user",
    metadata,
    Column("id", BIGINT, primary_key=True),
    Column("username", String(length=50), nullable=False),
    Column("email", String(length=320), unique=True, index=True, nullable=False),
    Column("hashed_password", String(length=1024), nullable=False),
    Column("is_active", BOOLEAN, default=True, nullable=False),
    Column("is_superuser", BOOLEAN, default=False, nullable=False),
    Column("is_verified", BOOLEAN, default=False, nullable=False),

)

post = Table(

    "post",
    metadata,
    Column("id", BIGINT, primary_key=True, autoincrement=True),
    Column("title", String(100), nullable=False),
    Column("content", Text, nullable=False),
    Column("created_at", DATE, default=datetime.now(timezone.utc).date()),
    Column("update_at", DATE, default=datetime.now(timezone.utc).date()),
    Column("is_blocked", BOOLEAN, default=False),
    Column("user_id", BIGINT, ForeignKey("user.id")),

)

comment = Table(

    "comment",
    metadata,
    Column("id", BIGINT, primary_key=True, autoincrement=True),
    Column("content", Text, nullable=False),
    Column("created_at", DATE, default=datetime.now(timezone.utc).date()),
    Column("update_at", DATE, default=datetime.now(timezone.utc).date()),
    Column("is_blocked", BOOLEAN, default=False),
    Column("user_id", BIGINT, ForeignKey("user.id")),
    Column("post_id", BIGINT, ForeignKey("post.id")),
)
