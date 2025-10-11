from fastapi import APIRouter
from routes import blog
#router create
router = APIRouter(prefix="/blogs",tags=["blogs"])

