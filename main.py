from fastapi import FastAPI
from typing import Union
from configs.connection import DATABASE_URL 
from pydantic import BaseModel
from user import routes as AdminRoute
from tortoise.contrib.fastapi import register_tortoise
from user import api as apiroute
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware
from starlette.templating import Jinja2Templates

app=FastAPI() 



db_url=DATABASE_URL()
app.add_middleware(SessionMiddleware, secret_key="some-random-string", max_age=None)
templates = Jinja2Templates(directory="templates")



app.include_router(AdminRoute.router,tags=["Admin"])

register_tortoise(
    app,
    db_url=db_url,
    modules={'models':['user.models']},
    generate_schemas  = True,
    add_exception_handlers =True
)