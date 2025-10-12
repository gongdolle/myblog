from fastapi import APIRouter,Request ,Depends,status
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates

from sqlalchemy import text ,Connection
from sqlalchemy.exc import SQLAlchemyError

from routes import blog
from db.database import direct_get_conn , context_get_conn 
from schemas.blog_schema import Blog,BlogData
from utils import util
#router create
router = APIRouter(prefix="/blogs",tags=["blogs"])
#jinja2 Template engin create
templates=Jinja2Templates(directory="templates")

@router.get("/")
async def get_all_blogs(request:Request
                        
                        ):
    conn = None
    try:
        conn= direct_get_conn()
        query= """
        SELECT id, title, author, content, image_loc, modified_dt FROM blog
        """
        result=conn.execute(text(query))
        
        #rows = result.fetchall()
        all_blogs = [BlogData(id = row.id,
                     title =row.title,
                     author=row.author,
                     content=util.truncate_text(row.content),
                     image_loc=row.image_loc,
                     modified_dt=row.modified_dt)
                    for row in result]

        result.close()
        return templates.TemplateResponse(
            request= request,
            name="index.html",
            context={"all_blogs":all_blogs}
        )
    
    except  SQLAlchemyError as e:
        print(e)
        raise e
    
    finally:
        if conn:
            conn.close()
            
@router.get("/show/{id}")
def get_blog_by_id(request:Request,id: int ,
                   conn: Connection = Depends(context_get_conn)):
    try:
        query =f"""
            SELECT id,title, author, content, image_loc, modified_dt from blog
            where id = :id
        """
        stmt = text(query)
        bind_stmt = stmt.bindparams(id=id)
        
        result=conn.execute(bind_stmt)
        #result logic except ex)null
        if result.rowcount==0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"this id:{id} not exist.")
        
        row=result.fetchone()
        blog=BlogData(id=row[0],title=row[1],author=row[2],content=util.newline_to_br(row[3]),image_loc=row[4],modified_dt=row[5])
       
        result.close()
        return templates.TemplateResponse(
            request= request,
            name="show_blog.html",
            context={"blog":blog})
        
    
    except SQLAlchemyError as e :
        print(e)
        raise e


@router.get("/new")
def create_blog_ui(request: Request ):
    return templates.TemplateResponse(
        request=request,
        name="new_blog.html",
        context= {}
    )