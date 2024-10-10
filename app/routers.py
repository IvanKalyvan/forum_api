import io

from fastapi import APIRouter, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update, func
from PyPDF2 import PdfReader
from datetime import datetime, timezone, date

from fastapi_users_local import fastapi_users
from pg_functions.database_connect import User, get_async_session
from pg_functions.models import post, comment
from schemas import Post_Schema, POSTCommentSchema, PUTCommentSchema
from gpt_management.gpt_utils import create_tasks_for_gpt

# POST ROUTERS
# ====================================================================================
post_router = APIRouter(

    prefix="/posts",
    tags=["Posts"]

)

current_active_verified_user = fastapi_users.current_user(active=True, verified=True)

@post_router.get("/get/my-posts")
async def get_all_private_posts_id(

        user: User = Depends(current_active_verified_user),
        session: AsyncSession = Depends(get_async_session)

):

    try:

        query = select(post).where(post.c.user_id == user.id)
        result = await session.execute(query)
        result = result.all()

        return [[id[0], id[1], id[5]] for id in result]

    except:

        raise HTTPException(

            status_code=404,
            headers={'404': 'Record not found!'}

        )

@post_router.get("/get")
async def get_all_posts_id(

        session: AsyncSession = Depends(get_async_session)

):

    try:

        query = select(post)
        result = await session.execute(query)
        result = result.all()

        return [[id[0], id[1]] for id in result if id[5] != True]

    except:

        raise HTTPException(

            status_code=404,
            headers={'404': 'Record not found!'}

        )

@post_router.get("/get/{post_id}")
async def get_post_by_id(

        post_id: int,
        session: AsyncSession = Depends(get_async_session)

                    ):

    try:

        query = select(post).where(post.c.id == post_id)
        result = await session.execute(query)
        result = result.fetchone()

        if result[5] == True:

            return {

                "Error": "This post was blocked"

            }

        return {

            "title": result[1],
            "content": result[2],

        }

    except:

        raise HTTPException(

            status_code=404,
            headers={'404': 'Record not found!'}

        )

@post_router.post("/post")
async def post_post(

        post_info: Post_Schema,
        user: User = Depends(current_active_verified_user),
        session: AsyncSession = Depends(get_async_session)

):

    try:

        params = []
        validate_result = ''

        post_info.user_id = user.id
        post_info = post_info.dict()

        for item in post_info:

            if item != "user_id":

                params.append({f'{item}': f'{post_info[item]}'})

            if item in ("title", "content"):

                if (len(post_info[item]) < 5 and item == "title") or (len(post_info[item]) < 20 and item == "content"):

                    raise HTTPException(

                        status_code=422,
                        detail={'422': f'Missed field ({item})'},
                        headers={'422': f'Missed field ({item})'}

                    )

        results = await create_tasks_for_gpt(params)

        for validate in results:

            if validate["answer"] != "good":
                validate_result = validate
                post_info["is_blocked"] = True

                break

        stmt = insert(comment).values(**post_info)
        await session.execute(stmt)
        await session.commit()

        if post_info["is_blocked"] == False:

            return {'201': 'successful'}

        else:

            raise HTTPException(

                status_code=422,
                detail={'422': f'{validate_result}'},
                headers={'422': f'{validate_result}'}
            )

    except Exception as e:

        print(e)

        return e

@post_router.delete("/delete/{post_id}")
async def delete_post(

        post_id: int,
        user: User = Depends(current_active_verified_user),
        session: AsyncSession = Depends(get_async_session)

):

    try:

        stmt = delete(post).where(post.c.id == post_id, post.c.user_id == user.id)
        await session.execute(stmt)
        await session.commit()

        return HTTPException(

            status_code=204,
            headers={'204': 'Successful delete!'}

        )

    except:

        raise HTTPException(

            status_code=404,
            headers={'404': 'Record not found!'}

        )

@post_router.put("/put/{post_id}")
async def put_post(

        post_id: int,
        post_info: Post_Schema,
        user: User = Depends(current_active_verified_user),
        session: AsyncSession = Depends(get_async_session)

):
    try:

        params = []
        validate_result = ''

        post_info.user_id = user.id
        post_info = post_info.dict()

        for item in post_info:

            if item != "user_id":
                params.append({f'{item}': f'{post_info[item]}'})

            if item in ("title", "content"):

                if (len(post_info[item]) < 5 and item == "title") or (
                        len(post_info[item]) < 20 and item == "content"):
                    raise HTTPException(

                        status_code=422,
                        detail={'422': f'Missed field ({item})'},
                        headers={'422': f'Missed field ({item})'}

                    )

        results = await create_tasks_for_gpt(params)

        for validate in results:

            if validate["answer"] != "good":

                validate_result = validate
                post_info["is_blocked"] = True

                break

        if not post_info.get("is_blocked", False) or post_info["is_blocked"] == False:

            post_info["is_blocked"] = False
            post_info["update_at"] = datetime.now(timezone.utc).date()
            stmt = update(post).where(post.c.id == post_id, post.c.user_id == user.id).values(**post_info)
            await session.execute(stmt)
            await session.commit()

            return {'201': 'successful'}

        else:

            raise HTTPException(

                status_code=422,
                detail={'422': f'{validate_result}'},
                headers={'422': f'{validate_result}'}
            )

    except Exception as e:

        raise e

@post_router.patch("/patch/{post_id}")
async def patch_post(

        post_id: int,
        post_info: Post_Schema,
        user: User = Depends(current_active_verified_user),
        session: AsyncSession = Depends(get_async_session)

):
    try:

        params = []
        skipped_params = []
        validate_result = ''

        post_info.user_id = user.id
        post_info = post_info.dict()

        for item in post_info:

            if item != "user_id":

                params.append({f'{item}': f'{post_info[item]}'})

            if item in ("title", "content"):

                if ((len(post_info[item]) < 5 and item == "title") or (len(post_info[item]) < 20 and item == "content")) \
                        and len(post_info[item]) != 0:

                    raise HTTPException(

                        status_code=422,
                        detail={'422': f'Missed field ({item})'},
                        headers={'422': f'Missed field ({item})'}

                    )

                if len(post_info[item]) == 0:

                    skipped_params.append(item)

        results = await create_tasks_for_gpt(params)

        for param in skipped_params:

            del post_info[param]

        for validate in results:

            if validate["answer"] != "good":
                validate_result = validate
                post_info["is_blocked"] = True

                break

        if not post_info.get("is_blocked", False) or post_info["is_blocked"] == False:

            post_info["is_blocked"] = False
            post_info["update_at"] = datetime.now(timezone.utc).date()
            stmt = update(post).where(post.c.id == post_id, post.c.user_id == user.id).values(**post_info)
            await session.execute(stmt)
            await session.commit()

            return {'201': 'successful'}

        else:

            raise HTTPException(

                status_code=422,
                detail={'422': f'{validate_result}'},
                headers={'422': f'{validate_result}'}
            )

    except Exception as e:

        raise e

# ====================================================================================

# COMMENT ROUTERS
# ====================================================================================


comment_router = APIRouter(

    prefix="/comments",
    tags=["Comments"]

)

@comment_router.get("/get/my-comments")
async def get_all_private_comments_id(

        user: User = Depends(current_active_verified_user),
        session: AsyncSession = Depends(get_async_session)

):

    try:

        query = select(comment).where(comment.c.user_id == user.id)
        result = await session.execute(query)
        result = result.all()

        return [[id[0], id[4], id[6]] for id in result]

    except:

        raise HTTPException(

            status_code=404,
            headers={'404': 'Record not found!'}

        )

@comment_router.get("/get-post-comments/{post_id}")
async def get_all_comments_id(


        post_id: int,
        session: AsyncSession = Depends(get_async_session)

):

    try:

        query = select(comment).where(comment.c.post_id == post_id)
        result = await session.execute(query)
        result = result.all()

        return [[id[0], id[1]] for id in result if id[4] != True]

    except:

        raise HTTPException(

            status_code=404,
            headers={'404': 'Record not found!'}

        )

@comment_router.get("/get/{comment_id}")
async def get_comment_by_id(

        comment_id: int,
        session: AsyncSession = Depends(get_async_session)

                    ):

    try:

        query = select(comment).where(comment.c.id == comment_id)
        result = await session.execute(query)
        result = result.fetchone()

        return {

            "content": result[1],

        }

    except:

        raise HTTPException(

            status_code=404,
            headers={'404': 'Record not found!'}

        )

@comment_router.post("/post")
async def post_comment(

        comment_info: POSTCommentSchema,
        user: User = Depends(current_active_verified_user),
        session: AsyncSession = Depends(get_async_session)

):

    try:

        params = []
        validate_result = ''

        comment_info.user_id = user.id
        comment_info = comment_info.dict()

        for item in comment_info:

            if item != "user_id":

                params.append({f'{item}': f'{comment_info[item]}'})

            if item == "content" and len(comment_info[item]) < 10:

                raise HTTPException(

                    status_code=422,
                    detail={'422': f'Missed field ({item})'},
                    headers={'422': f'Missed field ({item})'}

                )

        results = await create_tasks_for_gpt(params)

        for validate in results:

            if validate["answer"] != "good":

                validate_result = validate
                comment_info["is_blocked"] = True

                break

        stmt = insert(comment).values(**comment_info)
        await session.execute(stmt)
        await session.commit()

        if comment_info["is_blocked"] == False:

            return {'201': 'successful'}

        else:

            raise HTTPException(

                status_code=422,
                detail={'422': f'{validate_result}'},
                headers={'422': f'{validate_result}'}
            )

    except Exception as e:

        print(e)

        return e

@comment_router.delete("/delete/{comment_id}")
async def delete_comment(

        comment_id: int,
        user: User = Depends(current_active_verified_user),
        session: AsyncSession = Depends(get_async_session)

):

    try:

        stmt = delete(comment).where(comment.c.id == comment_id, comment.c.user_id == user.id)
        await session.execute(stmt)
        await session.commit()

        return HTTPException(

            status_code=204,
            headers={'204': 'Successful delete!'}

        )

    except:

        raise HTTPException(

            status_code=404,
            headers={'404': 'Record not found!'}

        )

@comment_router.put("/put/{comment_id}")
async def put_comment(

        comment_id: int,
        comment_info: PUTCommentSchema,
        user: User = Depends(current_active_verified_user),
        session: AsyncSession = Depends(get_async_session)

):
    try:

        params = []
        validate_result = ''

        comment_info.user_id = user.id
        comment_info = comment_info.dict()

        for item in comment_info:

            if item != "user_id":
                params.append({f'{item}': f'{comment_info[item]}'})

            if item == "content" and len(comment_info[item]) < 10:

                raise HTTPException(

                    status_code=422,
                    detail={'422': f'Missed field ({item})'},
                    headers={'422': f'Missed field ({item})'}

                )

        results = await create_tasks_for_gpt(params)

        for validate in results:

            if validate["answer"] != "good":
                validate_result = validate
                comment_info["is_blocked"] = True

                break

        if not comment_info.get("is_blocked", False) or comment_info["is_blocked"] == False:

            comment_info["is_blocked"] = False
            comment_info["update_at"] = datetime.now(timezone.utc).date()
            stmt = update(comment).where(comment.c.id == comment_id, comment.c.user_id == user.id).values(**comment_info)
            await session.execute(stmt)
            await session.commit()

            return {'201': 'successful'}

        else:

            raise HTTPException(

                status_code=422,
                detail={'422': f'{validate_result}'},
                headers={'422': f'{validate_result}'}
            )

    except Exception as e:

        raise e

# ====================================================================================

# SUMMARIZE ROUTER
# ====================================================================================

pdf_file_router = APIRouter(

    prefix='/summarize',
    tags=['Summarize']

)

@pdf_file_router.post("/")
async def create_summary(

    file: UploadFile | None = None

):

    if file.content_type != "application/pdf":

        raise HTTPException(status_code=400, detail="File must be in .pdf format")

    contents = await file.read()

    pdf_reader = PdfReader(io.BytesIO(contents))
    num_pages = len(pdf_reader.pages)

    if num_pages > 1:

        raise HTTPException(status_code=400, detail="PDF must have not more than 1 page!")

    page = pdf_reader.pages[0]
    text = page.extract_text()

    results = await create_tasks_for_gpt([{"text": text}])

    return {"summary": f"{results[0]['summary']}"}

# ====================================================================================

# ANALYTICS ROUTER
# ====================================================================================

analytics_router = APIRouter(

    prefix='/analytics',
    tags=['Analytics']

)

@analytics_router.post("/comments-daily-breakdown")
async def get_comments_analytic(

        date_from: date,
        date_to: date,
        post_id: int,
        user: User = Depends(current_active_verified_user),
        session: AsyncSession = Depends(get_async_session)

):
    query = (

        select(

            func.date(comment.c.created_at).label('day'),
            func.count(comment.c.id).label('total_comments'),
            func.count().filter(comment.c.is_blocked).label('blocked_comments')

        )
        .where(

            comment.c.created_at.between(date_from, date_to),
            comment.c.user_id == user.id,
            comment.c.post_id == post_id

        )
        .group_by(func.date(comment.c.created_at))
        .order_by(func.date(comment.c.created_at))
    )

    result = await session.execute(query)
    daily_stats = result.fetchall()

    return {

        "analytics": [

            {

                "date": stat.day.strftime('%Y-%m-%d'),
                "created_count": stat.total_comments,
                "blocked_count": stat.blocked_comments

            }

            for stat in daily_stats
        ]

    }