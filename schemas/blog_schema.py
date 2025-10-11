from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional
class BlogInput(BaseModel):
    title:str= Field(...,min_length=2,max_length=200)
    author:str= Field(...,max_length=100)
    content:str=Field(...,min_length=2,max_length=4000)
    image_loc:str | None =Field(None,max_length=400)


class Blog(BlogInput):
    id:int
    modified_dt:datetime

