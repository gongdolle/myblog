from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import text ,Connection
from sqlalchemy.exc import SQLAlchemyError

from routes import blog
from db.database import direct_get_conn , context_get_conn 
from schemas.blog_schema import Blog,BlogData
from utils import util

from typing import List


def get_all_blogs(conn: Connection)-> List:
 
    try:
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
    
    except  SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail= "요청이 너무 많습니다")
    
    except Exception as e:
        print (e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="알수없는 이유로 서비스 오류발생함.")

    result.close()
    return all_blogs
            

def get_blog_by_id(id: int ,
                   conn: Connection):
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
        blog=BlogData(id=row[0],title=row[1],author=row[2],content=row[3],image_loc=row[4],modified_dt=row[5])
       
        result.close()
        return blog
        
    
    except SQLAlchemyError as e :
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail= "요청이 너무 많습니다")
    


def create_blog( conn: Connection,
                title:str,
                author: str,
                content: str,
                ):
    
    try:
        query=f"""
            INSERT INTO blog(title,author,content,modified_dt)
            values('{title}','{author}','{content}',now())
        """
        
        conn.execute(text(query))
        conn.commit()
        
    
    except SQLAlchemyError as e:
        print(e)
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="요청데이터가 제대로 전달되지않았습니다.")
        



def update_blog(
                conn : Connection,
                id: int ,
                title:str,
                author: str,
                content: str,
                ):
    
    
    try:
        query= f"""
            UPDATE blog
            SET title=:title,author=:author,content=:content
            where id = :id
            
        """
        bind_stmt=text(query).bindparams(id=id,title=title,author=author,content=content)
        
        result= conn.execute(bind_stmt)

        if result.rowcount  == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"this id:{id} not exist.") 
            
        conn.commit()
        
    except SQLAlchemyError as e :
        print( e)
        conn.rollback()
        raise e
    

def delete_blog(conn: Connection ,id : int):
    try:
        query= f"""
            DELETE FROM blog
            where id = :id
        """
        bind_stmt= text(query).bindparams(id=id)
        result= conn.execute(bind_stmt)
        
        if result.rowcount  == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"this id:{id} not exist.") 
            
        conn.commit()

    except SQLAlchemyError as e :
        print( e)
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail="요청서비스가 너무 많습니다")
        