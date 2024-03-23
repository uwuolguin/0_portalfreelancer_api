from fastapi import  status, HTTPException,APIRouter,Form,Cookie,Response,Request
from .. import schemas,utils,oath2
import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import settings
import time
from typing import Any
import os
from typing_extensions import Annotated
from pydantic.networks import EmailStr
from pydantic.functional_validators import BeforeValidator
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router= APIRouter(
    
    prefix="/auth",
    tags=["Auth"]
)

while True:
    try:

        conn_auth=psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
        cursor=conn_auth.cursor()
        break

    except Exception as error:

        print("Connecting to database failed")
        print("Error:",error)
        time.sleep(5)

@router.post("/login_talent_firm",status_code=status.HTTP_201_CREATED)
def login_function(
    email: Annotated[EmailStr,Form(),BeforeValidator(schemas.check_long_str_80)],
    password:Annotated[str,BeforeValidator(schemas.check_long_str_80),Form()]
    ) -> Any:
    os.chdir(settings.normal_directory)
    try:
        conn_auth.rollback()
    except:
        pass

#######################YOU CAN LOG IN EVERY TWO SECONDS #########################
    email_2="""  SELECT * from log_in_attemp_2_seconds('%s');"""
    cursor.execute(email_2 % (email))
    email_today=cursor.fetchone()
    if not(email_today ==None):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "You can send 1 login attempt every two seconds max, sorry :(")
############################ INSERT RECORD ON LOGIN ATTEMP ######################
    email_4="""  SELECT insert_loginattempt('%s');"""
    cursor.execute(email_4 % (email))
    conn_auth.commit()

    
############################CHECK IF EMAIL EXISTS AND IF PASSWORD IS CORRECT################

    id_2=""" SELECT * FROM get_id_by_email('%s');"""
    cursor.execute(id_2 % (str(email)))
    talent=cursor.fetchone()

    id_3=""" SELECT * FROM firm_get_id_by_email('%s');"""
    cursor.execute(id_3 % (str(email)))
    firm=cursor.fetchone()

    if email== settings.superadmin_email and password==settings.superadmin_password:
        superadmin=1

    if talent==None and firm ==None and superadmin== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with email: {str(email)} does not exist")
    
    if not(firm==None):
        role= "firm"
        firm_data=""" SELECT * FROM firm_get_by_id_just_password('%s');"""
        cursor.execute(firm_data % (str(firm.get("firm_id"))))
        firm_payload=cursor.fetchone()

        try:
             hola=(not utils.verify(password,firm_payload.get("firm_password")))
        except:
             hola=not(password==firm_payload.get("firm_password"))
        if  hola:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BAD CREDENTIALS")

        token_data={'firm_id':firm.get("firm_id"),'firm_email':email,'role':role}
        token=oath2.create_access_token(token_data)
        content = {"message": "cookie set"}
        response = JSONResponse(content=content)
        response.set_cookie(key="login", value=token,max_age=settings.token_seconds,httponly=True)

        update_firm=""" SELECT * FROM firm_update_by_id_just_logged_at('%s');"""
        cursor.execute(update_firm % (str(firm.get("firm_id"))) )
        conn_auth.commit()

        return response
    
    if not(talent==None):
        role= "talent"
        talent_data=""" SELECT * FROM get_by_id_just_password('%s');"""
        cursor.execute(talent_data % (str(talent.get("talent_id"))))
        talent_payload=cursor.fetchone()
        try:
             hola=not (utils.verify(password,talent_payload.get("talent_password")))
        except:
             hola=not(password==talent_payload.get("talent_password"))
        if  hola:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BAD CREDENTIALS")
        token_data={'talent_id':talent.get("talent_id"),'talent_email':email,'role':role}
        token=oath2.create_access_token(token_data)
        content = {"message": "cookie set"}
        response = JSONResponse(content=content)
        response.set_cookie(key="login", value=token,max_age=settings.token_seconds,httponly=True)

        update_talent=""" SELECT * FROM talent_update_by_id_just_logged_at('%s');"""
        cursor.execute(update_talent % (str(talent.get("talent_id"))) )
        conn_auth.commit()

        return response
    
    if not(superadmin==None):
        role= "superadmin"
        token_data={'superadmin_id':1,'superadmin_email':email,'role':role}
        token=oath2.create_access_token(token_data)
        content = {"message": "cookie set"}
        response = JSONResponse(content=content)
        response.set_cookie(key="login", value=token,max_age=settings.token_seconds,httponly=True)
        return response
    
@router.delete("/logout")
async def logout(response: Response,):
    response.delete_cookie("login")
    return {"status":"success"}

################################################# TEMPLATES ####################################################################
    
templates= Jinja2Templates(directory="./templates")

@router.get('/logIn/',response_class=HTMLResponse)
def indexLogIn(request: Request):

    try:
        conn_auth.rollback()
    except:
        pass

    context={'request': request}
    return templates.TemplateResponse("4_log_in.html",context)

@router.get('/SigInRouter/',response_class=HTMLResponse)
def SigInRoute(request: Request):

    try:
        conn_auth.rollback()
    except:
        pass

    context={'request': request}
    return templates.TemplateResponse("3_sign_up.html",context)

@router.get('/settings_url_for_del_up/',response_class=HTMLResponse)
def redirect_del_up_firm_talent(request: Request,login: str = Cookie(None)):

    try:
        conn_auth.rollback()
    except:
        pass


    if login==None:
            context={'request': request}
            return templates.TemplateResponse("4_log_in for_settings_del_up.html",context)
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") == "firm":
            context={'request': request}
            return templates.TemplateResponse("8_del_up_firm.html",context)
    
    if dict(credentials).get("role") == "talent":
            context={'request': request}
            return templates.TemplateResponse("7_del_up_talent.html",context)

    context={'request': request}
    return templates.TemplateResponse("4_log_in for_settings_del_up.html",context)
    