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

def getConnection():
    

    while True:
        try:

            conn_auth=psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
            break

        except Exception as error:

            print("Connecting to database failed")
            print("Error:",error)
            time.sleep(5)

    return conn_auth

@router.post("/login_talent_firm",status_code=status.HTTP_201_CREATED)
def login_function(
    email: Annotated[EmailStr,Form(),BeforeValidator(schemas.check_long_str_80)],
    password:Annotated[str,BeforeValidator(schemas.check_long_str_80),Form()]
    ) -> Any:
    
    os.chdir(settings.normal_directory)
    
    conn_auth=getConnection()
    cursor=conn_auth.cursor()

#######################YOU CAN LOG IN EVERY TWO SECONDS #########################
    email_2="""  SELECT * from log_in_attemp_2_seconds('%s');"""
    cursor.execute(email_2 % (email))
    email_today=cursor.fetchone()
    if not(email_today ==None):

        conn_auth.close()
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
    else: 
        superadmin=None

    if talent==None and firm ==None and superadmin== None:
        conn_auth.close()
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

            conn_auth.close()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BAD CREDENTIALS")

        token_data={'firm_id':firm.get("firm_id"),'firm_email':email,'role':role}
        token=oath2.create_access_token(token_data)
        content = {"message": "cookie set"}
        response = JSONResponse(content=content)
        response.set_cookie(key="login", value=token,max_age=settings.token_seconds,httponly=True)

        update_firm=""" SELECT * FROM firm_update_by_id_just_logged_at('%s');"""
        cursor.execute(update_firm % (str(firm.get("firm_id"))) )
        conn_auth.commit()

        conn_auth.close()
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
            conn_auth.close()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BAD CREDENTIALS")
        token_data={'talent_id':talent.get("talent_id"),'talent_email':email,'role':role}
        token=oath2.create_access_token(token_data)
        content = {"message": "cookie set"}
        response = JSONResponse(content=content)
        response.set_cookie(key="login", value=token,max_age=settings.token_seconds,httponly=True)

        update_talent=""" SELECT * FROM talent_update_by_id_just_logged_at('%s');"""
        cursor.execute(update_talent % (str(talent.get("talent_id"))) )
        conn_auth.commit()

        conn_auth.close()
        return response
    
    if not(superadmin==None):
        role= "superadmin"
        token_data={'superadmin_id':1,'superadmin_email':email,'role':role}
        token=oath2.create_access_token(token_data)
        content = {"message": "cookie set"}
        response = JSONResponse(content=content)
        response.set_cookie(key="login", value=token,max_age=settings.token_seconds,httponly=True)

        conn_auth.close()
        return response
    
    conn_auth.close()
    
@router.delete("/logout")
async def logout(response: Response,):
    response.delete_cookie("login")
    return {"status":"success"}

################################################# TEMPLATES ####################################################################
    
templates= Jinja2Templates(directory="./templates")

@router.get('/logIn/',response_class=HTMLResponse)
def indexLogIn(request: Request):
    while True:
        try:
            
            return templates.TemplateResponse(request=request,name="4_log_in.html")
        except:
            time.sleep(1)
            pass

@router.get('/SigInRouter/',response_class=HTMLResponse)
def SigInRoute(request: Request):

    while True:
        try:
            context={'request': request}
            return templates.TemplateResponse("3_sign_up.html",context)
        except:
            time.sleep(1)
            pass


@router.get('/settings_url_for_del_up/',response_class=HTMLResponse)
def redirect_del_up_firm_talent(request: Request,login: str = Cookie(None)):

    while True:
        try:

            conn_auth=getConnection()
            cursor=conn_auth.cursor()

            if login==None:
                    context={'request': request}
                    conn_auth.close()
                    return templates.TemplateResponse("4_log_in for_settings_del_up.html",context)
            
            credentials=oath2.decode_access_token(login)

            if dict(credentials).get("role") == "firm":
                    context={'request': request}
                    conn_auth.close()
                    return templates.TemplateResponse("8_del_up_firm.html",context)
            
            if dict(credentials).get("role") == "talent":

                cursor.execute(""" SELECT * FROM """+settings.table_name_for_select_all_skills+""" """)
                skills=cursor.fetchall()

                if not skills :
                    conn_auth.close()
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BBDD does not have any record")
                
                
                Skills_List=[]

                for  skill in skills:
                    skill_dict={'skill':skill.get("skill"),'skill_key':skill.get("skill").replace(' ','')}
                    Skills_List.append(skill_dict)


                cursor.execute(""" SELECT * FROM """+settings.table_name_for_select_all_categories+""" """)
                categories=cursor.fetchall()
                if not categories :
                    conn_auth.close()
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BBDD does not have any record")
                
                
                Categories_List=[]

                for  category in categories:
                    category_dict={'category':category.get("category"),'category_key':category.get("category").replace(' ','')}
                    Categories_List.append(category_dict)

                context={'request': request, 'categories':Categories_List,'skills':Skills_List}
                conn_auth.close()
                return templates.TemplateResponse("7_del_up_talent.html",context)



            context={'request': request}
            conn_auth.close()
            return templates.TemplateResponse("4_log_in for_settings_del_up.html",context)
        
        except:
            pass