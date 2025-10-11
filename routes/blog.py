from fastapi import APIRouter,Request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from routes import blog
from db.database import direct_get_conn
from schemas.blog_schema import Blog
#router create
router = APIRouter(prefix="/blogs",tags=["blogs"])

@router.get("/")
async def get_all_blogs(request:Request):
    conn = None
    try:
        conn= direct_get_conn()
        query= """
        SELECT id, title, author, content, image_loc, modified_dt FROM blog
        """
        result=conn.execute(text(query))
        #rows = result.fetchall()
        rows = [Blog(id = row.id,
                     title =row.title,
                     author=row.author,
                     content=row.content,
                     image_loc=row.image_loc,
                     modified_dt=row.modify_dt)
                    for row in result]

        result.close()
        return rows
    except  SQLAlchemyError as e:
        print(e)
        raise e
    finally:
        if conn:
            conn.close()