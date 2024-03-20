from fastapi import  status, HTTPException,APIRouter, Response,Form,Cookie,Request
from .. import schemas,utils,oath2
import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import settings
import time
from typing import Any
import os
from typing_extensions import Annotated
from pydantic.networks import EmailStr,Url
from pydantic import UrlConstraints
from pydantic.functional_validators import BeforeValidator
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

while True:
    try:

        conn_firm=psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
        cursor=conn_firm.cursor()
        break

    except Exception as error:

        print("Connecting to database failed")
        print("Error:",error)
        time.sleep(5)



router= APIRouter(
    
    prefix="/firm",
    tags=["Firm"]
)

@router.get("/firm_get_all",response_model=list[schemas.firmResponse])
def get_all_firm(login: str = Cookie(None)) -> Any:

    os.chdir(settings.normal_directory)
    try:
        conn_firm.rollback()
    except:
        pass

    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    
    cursor.execute(""" SELECT * FROM """+settings.table_name_for_select_all_no_free_user+""" """)
    firm=cursor.fetchall()
    if not firm :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BBDD does not have any record")
    return firm

@router.get("/firm_get_id/id/{id}",response_model=schemas.firmResponse4)
def get_firm(id:int,login: str = Cookie(None)) -> Any:

    os.chdir(settings.normal_directory)
    try:
        conn_firm.rollback()
    except:
        pass
    
    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    

    id_2=""" SELECT * FROM firm_get_by_id('%s');"""
    cursor.execute(id_2 % (str(id)))
    firm=cursor.fetchone()
    if firm ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with id: {id} does not exist")
    return firm



@router.get("/firm_email_validated_2/{email}",response_model=schemas.firmResponse3)
def get_id_by_email_firm_2(email:EmailStr,login: str = Cookie(None)) -> Any:

    os.chdir(settings.normal_directory)
    try:
        conn_firm.rollback()
    except:
        pass
   
    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    
  
    id_2=""" SELECT * FROM firm_get_id_by_email('%s');"""
    cursor.execute(id_2 % (str(email)))
    talent=cursor.fetchone()
    if talent ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with email: {str(email)} does not exist")
    return talent






@router.post("/firm_post/",status_code=status.HTTP_201_CREATED)
def post_firm(

                email: Annotated[EmailStr,Form(),BeforeValidator(schemas.check_long_str_80)],
                password:Annotated[str,BeforeValidator(schemas.check_long_str_80),Form()],
                full_name:Annotated[str,BeforeValidator(schemas.check_long_str_80),Form()],
                contact_email:  Annotated[EmailStr,Form(),BeforeValidator(schemas.check_long_str_80)],
                contact_phone: Annotated[int,Form()],
                email_template_to_send:Annotated[str,BeforeValidator(schemas.check_long_str_860),Form()],
                linkedin:Annotated[Url,Form(),UrlConstraints(max_length=1000, allowed_schemes=["https"]),],
                instagram:Annotated[Url,Form(),UrlConstraints(max_length=1000, allowed_schemes=["https"]),],

                 
                 )-> Any:

    os.chdir(settings.normal_directory)
    try:
        conn_firm.rollback()
    except:
        pass

    hashed_password=utils.hash(password)
    password=hashed_password
    
    linkedin=str(linkedin)
    instagram=str(instagram)

    email=email.replace(" ", "").lower()
    contact_email=contact_email.replace(" ", "").lower()

    if email==settings.superadmin_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    if contact_email==settings.superadmin_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    cursor.execute(""" SELECT * FROM number_of_user_today();""")
    users_today=cursor.fetchone()
    for x in users_today.values():
        user_today_value=x 
    if user_today_value >=50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "We are only receiving 50 login requests per day, sorry :( ")

#################Validate Email is not a company###############
    validate_email=""" SELECT * FROM remove_firm_by_being_in_talent('%s');"""
    cursor.execute(validate_email % ((email)))
    validate_0=cursor.fetchone()
    if validate_0 :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "YOUR EMAIL IS ALREDY BEING USED")
#################Validate Email is not a company###############
    validate_email=""" SELECT * FROM remove_firm_by_being_in_talent('%s');"""
    cursor.execute(validate_email % ((contact_email)))
    validate_0=cursor.fetchone()
    if validate_0 :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "YOUR EMAIL IS ALREDY BEING USED")



#################Validate Blacklist Email ###############
    validate_email=""" SELECT * FROM remove_user_by_black_list_email('%s');"""
    cursor.execute(validate_email % ((email)))
    validate_0=cursor.fetchone()
    if validate_0 :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "YOUR EMAIL IS BANNED")
    
    validate_email_2=""" SELECT * FROM remove_user_by_black_list_email('%s');"""
    cursor.execute(validate_email_2 % ((contact_email)))
    validate_0=cursor.fetchone()
    if validate_0 :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "YOUR EMAIL IS BANNED")

#################Validate Blacklist Words ###############

    validate_word=""" SELECT * FROM remove_user_by_black_list_word_v2('%s','%s');"""
    cursor.execute(validate_word % ((full_name.replace(" ", "").lower()),(email_template_to_send.replace(" ", "").lower())))
    validate_1=cursor.fetchone()
    if validate_1 :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "THIS SITE DOES NOT ACCEPT BAD WORDS")
    
#################Validate url contains words(linkedin,girhub,facebook,instagram) ###############
    
    if not (str(linkedin).startswith('https://linkedin.com') ):   
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "the string should start with https://linkedin.com")
    
    if not (str(instagram).startswith('https://instagram.com')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "the string should start with https://instagram.com")
    #################Validate url contains words(linkedin,girhub,facebook,instagram) ###############
    if len (str(contact_phone) )>80:   
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "The number is too long")
    
###################CREATE USER#####################################################################

    firm_2="""  SELECT insert_firm('%s','%s','%s','%s','%s','%s','%s','%s');"""
    cursor.execute(firm_2 % (email,password,full_name,contact_email,str(contact_phone),email_template_to_send,linkedin,instagram))

    conn_firm.commit()


@router.delete("/firm_delete/id/",status_code=status.HTTP_204_NO_CONTENT)
def delete_firm(login: str = Cookie(None)):
    
    os.chdir(settings.normal_directory)
    try:
        conn_firm.rollback()
    except:
        pass

    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "firm":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    
    id=dict(credentials).get("firm_id")

    id_2=""" SELECT * FROM firm_get_by_id('%s');"""
    cursor.execute(id_2 % (str(id)))
    firm=cursor.fetchone()
    if firm ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with id: {id} does not exist")

    delete=""" SELECT delete_firm_by_id('%s');"""
    cursor.execute(delete % (id))
    conn_firm.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/firm_put/")
def update_firm(
                password:Annotated[str,BeforeValidator(schemas.check_long_str_80),Form()],
                full_name:Annotated[str,BeforeValidator(schemas.check_long_str_80),Form()],
                contact_email:  Annotated[EmailStr,Form(),BeforeValidator(schemas.check_long_str_80)],
                contact_phone: Annotated[int,Form()],
                email_template_to_send:Annotated[str,BeforeValidator(schemas.check_long_str_860),Form()],
                linkedin:Annotated[Url,Form(),UrlConstraints(max_length=1000, allowed_schemes=["https"]),],
                instagram:Annotated[Url,Form(),UrlConstraints(max_length=1000, allowed_schemes=["https"]),],
                login: str = Cookie(None), 
                 )-> Any:

    os.chdir(settings.normal_directory)
    try:
        conn_firm.rollback()
    except:
        pass

    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "firm":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    
    id=dict(credentials).get("firm_id")


    hashed_password= utils.hash(password)
    password=hashed_password
    linkedin=str(linkedin)
    instagram=str(instagram)
    contact_email=contact_email.replace(" ", "").lower()




    cursor.execute(""" SELECT * FROM number_of_user_today();""")
    users_today=cursor.fetchone()
    for x in users_today.values():
        user_today_value=x 
    if user_today_value >=50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "We are only receiving 50 login requests per day, sorry :( ")

#################Validate Email is not a company###############
    validate_email=""" SELECT * FROM remove_firm_by_being_in_talent('%s');"""
    cursor.execute(validate_email % ((contact_email)))
    validate_0=cursor.fetchone()
    if validate_0 :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "YOUR EMAIL IS ALREDY BEING USED")
#################Validate Blacklist Email ###############
    
    validate_email_2=""" SELECT * FROM remove_user_by_black_list_email('%s');"""
    cursor.execute(validate_email_2 % ((contact_email)))
    validate_0=cursor.fetchone()
    if validate_0 :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "YOUR EMAIL IS BANNED")

#################Validate Blacklist Words ###############

    validate_word=""" SELECT * FROM remove_user_by_black_list_word_v2('%s','%s');"""
    cursor.execute(validate_word % ((full_name.replace(" ", "").lower()),(email_template_to_send.replace(" ", "").lower())))
    validate_1=cursor.fetchone()
    if validate_1 :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "THIS SITE DOES NOT ACCEPT BAD WORDS")
    
#################Validate url contains words(linkedin,girhub,facebook,instagram) ###############
    
    if not (str(linkedin).startswith('https://linkedin.com') ):   
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "the string should start with https://linkedin.com")
    
    if not (str(instagram).startswith('https://instagram.com')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "the string should start with https://instagram.com")
    #################Validate url contains words(linkedin,girhub,facebook,instagram) ###############
    if len (str(contact_phone) )>80:   
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "The number is too long")
    

    id_2=""" SELECT * FROM firm_get_by_id('%s');"""
    cursor.execute(id_2 % (str(id)))
    firm=cursor.fetchone()
    if firm ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with id: {id} does not exist")

    
    update=""" SELECT * FROM update_firm_by_id('%s','%s','%s','%s','%s','%s','%s','%s');"""
    cursor.execute(update % (str(id),password,full_name,contact_email,str(contact_phone),email_template_to_send,linkedin,instagram) )
    conn_firm.commit()


    
    return Response(status_code=status.HTTP_201_CREATED,content='Data Updated') 


################################################# TEMPLATES ####################################################################
    
templates= Jinja2Templates(directory="./templates")


@router.get('/signUpFirm/',response_class=HTMLResponse)
def index(request: Request):

    try:
        conn_firm.rollback()
    except:
        pass

    context={'request': request}
    return templates.TemplateResponse("6_sign_up_firm.html",context)

@router.get('/delUpFirm/',response_class=HTMLResponse)
def delup(request: Request):

    try:
        conn_firm.rollback()
    except:
        pass

    context={'request': request}
    return templates.TemplateResponse("6_sign_up_firm.html",context)
    

# fetch("https://apiportalfreelancer.lat/firm/firm_put/", {
#   body: "password=hola&full_name=actualizado&contact_email=acos201460083665%40gmail.com&contact_phone=944338593&email_template_to_send=actualizado&linkedin=https%3A%2F%2Flinkedin.com%2F&instagram=https%3A%2F%2Finstagram.com%2F",
#   headers: {
#     Accept: "application/json",
#     "Content-Type": "application/x-www-form-urlencoded"
#   },
#   method: "PUT"
# })


