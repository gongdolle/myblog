from fastapi import APIRouter,Request ,Depends,status,Form
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates

from sqlalchemy import text ,Connection
from sqlalchemy.exc import SQLAlchemyError

from routes import blog
from db.database import direct_get_conn , context_get_conn 
from schemas.blog_schema import Blog,BlogData
from services  import blog_svc
from utils import util

#router create
router = APIRouter(prefix="/blogs",tags=["blogs"])
#jinja2 Template engin create
templates=Jinja2Templates(directory="templates")

@router.get("/")
async def get_all_blogs(request:Request
                        ,conn : Connection = Depends(context_get_conn)
                        ):
    blog_svc.get_all_blogs(conn)
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
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail= "요청이 너무 많습니다")
    
    except Exception as e:
        print (e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="알수없는 이유로 서비스 오류발생함.")
    
    finally:
        if conn:
            conn.close()
            
@router.get("/show/{id}")
def get_blog_by_id(request:Request,id: int ,
                   conn: Connection = Depends(context_get_conn)):
    blog = blog_svc.get_blog_by_id(conn=conn,id=id)
    blog.content = util.newline_to_br(blog.content)
    
    return templates.TemplateResponse(
            request= request,
            name="show_blog.html",
            context={"blog":blog})
        


@router.get("/new")
def create_blog_ui(request: Request ):
    return templates.TemplateResponse(
        request=request,
        name="new_blog.html",
        context= {}
    )
    
@router.post("/new")
def create_blog(request: Request,
                title=Form(min_length=2,max_length=200),
                author=Form(max_length=100),
                content=Form(min_length=2,max_length=4000),
                conn: Connection=Depends(context_get_conn)
                ):
    blog_svc.create_blog(conn,title=title, author= author, content= content)
    return RedirectResponse ("/blogs",status_code=status.HTTP_302_FOUND)


@router.get("/modify/{id}")
def update_blog_ui(request : Request, id: int , conn = Depends(context_get_conn)):
        blog=blog_svc.get_blog_by_id(conn=conn,id=id)
        
        return templates.TemplateResponse(
            request=request,
            name="modify_blog.html",
            context= {"blog":blog}
        )           
 


@router.post("/modify/{id}")
def update_blog(requset:Request,id: int ,
                title=Form(min_length=2,max_length=200),
                author=Form(max_length=100),
                content=Form(min_length=2,max_length=4000),
                conn: Connection=Depends(context_get_conn)
                ):
    
    blog_svc.update_blog(conn=conn,id=id ,title=title,author=author,content=content)
    
      
    return RedirectResponse(f"/blogs/show/{id}",status_code=status.HTTP_302_FOUND)


    
@router.post("/delete/{id}")
def delete_blog(request: Request, id : int , conn: Connection = Depends(context_get_conn)):
    
    blog_svc.delete_blog(conn=conn , id = id)    
    return RedirectResponse("/blogs",status_code=status.HTTP_302_FOUND)
