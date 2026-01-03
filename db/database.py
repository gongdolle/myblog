from sqlalchemy import create_engine,Connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool,NullPool
from contextlib import contextmanager
from fastapi import status
from fastapi.exceptions  import HTTPException
from dotenv import load_dotenv
import os,sys
#debug path
#sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from env.config import settings

#env stlye
#____________________________________________________
#load_dotenv()
#DATABASE_CONN = os.getenv()

 
DATABASE_URL = f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine =create_engine(DATABASE_URL,
                      poolclass=QueuePool,
                      pool_size=10,max_overflow=0,
                      pool_recycle=300
                      )

def direct_get_conn():
    conn=None
    try:
        conn= engine.connect()
        return conn
    except SQLAlchemyError as e :
         print(e)
         raise e
     
     
     
def context_get_conn():
    try:
        conn=engine.connect()
        yield conn
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail= "요청이 너무 많습니다")
    
    finally:
        if conn:
            conn.close()
        