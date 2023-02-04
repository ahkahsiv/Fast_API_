from user.pydantic_models import *
# from http.client import HTTPResponse, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Request , Form, status
from fastapi.templating import Jinja2Templates
from user.models import User
from passlib.context import CryptContext
from fastapi_login import LoginManager
import secrets
import flash
import typing


router= APIRouter()
SECRET= 'your-secret-key'
manager = LoginManager(SECRET, token_url='/auth/token')
templates= Jinja2Templates ( directory = "user/templates" )

def flash(request: Request, message: typing.Any, category: str = "primary") -> None:
   if "_messages" not in request.session:
       request.session["_messages"] = []
       request.session["_messages"].append({"message": message, "category": category})

def get_flashed_messages(request: Request):
   print(request.session)
   return request.session.pop("_messages") if "_messages" in request.session else []

templates.env.globals['get_flashed_messages'] = get_flashed_messages
pwd_context=CryptContext(schemes=["bcrypt"], deprecated ="auto")



def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



@router.get("/", response_class= HTMLResponse)
def read_item(request : Request):
    return templates.TemplateResponse("login.html",{
        "request": request,
    })


@router.post("/add/",)
async def create_user( request : Request , email:str = Form(...),
                        name:str = Form(...),
                        phone:str = Form(...),
                        password:str = Form(...)):

    if "_messages" in request.session:
        print(request.session["_message"][0]["phone"])
        phone=request.session["_message"][0]["phone"]
    
    elif "_messages" in request.session:
        print(request.session["_message"][0]["email"])
        email=request.session["_message"][0]["email"]

    else:
        user_obj=await User.create(email=email,name=name,
                                     phone=phone
                                     ,password= get_password_hash(password))

        print(user_obj)                              
        return RedirectResponse("/",  status_code=status.HTTP_302_FOUND)

@manager.user_loader()
async def load_user(email:str):
    if await User.exists(email=email):
        newapi= await User.get(email=email)
        return newapi



@router.post('/login/')
async def login(request:Request, email:str =Form(...),
                                password :str = Form(...)):
    
    email=email
    user = await load_user(email)
    
    if not user:
        flash(request, 'User not exists', "danger")
        return templates.TemplateResponse("login.html", {'request':request})
    elif not verify_password(password, user.password):
        flash(request, 'Password Incorrect', "danger")
        return templates.TemplateResponse("login.html", {'request':request})
    else:
        # request.session['id'] = user.id
        request.session['name']= user.name
        print(user.name)
        flash(request, 'Login Successfull', "success")
        data= await User.all()
        return templates.TemplateResponse("welcome.html", {'request':request,'data':data})

    



# @router.get("/login/", response_class=HTMLResponse)
# def read_item(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})

@router.get("/welcome/", response_class=HTMLResponse)
def read_item(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


