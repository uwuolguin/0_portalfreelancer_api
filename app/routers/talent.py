from fastapi import  status, HTTPException, APIRouter, Response,File, UploadFile,Form,Cookie,Request
from .. import schemas,utils,oath2
import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import settings
import time
from typing import Any,Union
import os
from typing_extensions import Annotated
from pydantic.networks import EmailStr,Url
from pydantic import UrlConstraints
from pydantic.functional_validators import BeforeValidator
from shutil import copy
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates



router= APIRouter(
    
    prefix="/talent",
    tags=["Talent"]
)

while True:
    try:

        conn_talent=psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
        cursor=conn_talent.cursor()
        break

    except Exception as error:

        print("Connecting to database failed")
        print("Error:",error)
        time.sleep(5)

@router.get("/talent_get_all",response_model=list[schemas.talentResponse])
def get_all_talent(login: str = Cookie(None)) -> Any:

    os.chdir(settings.normal_directory)

    try:
        conn_talent.rollback()
    except:
        pass

    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")

    cursor.execute(""" SELECT * FROM """+settings.table_name_for_select_all_free_user+""" """)
    talent=cursor.fetchall()
    if not talent :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BBDD does not have any record")
    return talent




@router.get("/talent_get_id/id/{id}",response_model=schemas.talentResponse4)
def get_talent(id:int,login: str = Cookie(None)) -> Any:

    os.chdir(settings.normal_directory)
    try:
        conn_talent.rollback()
    except:
        pass

    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")

    id_2=""" SELECT * FROM get_by_id('%s');"""
    cursor.execute(id_2 % (str(id)))
    talent=cursor.fetchone()
    if talent ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with id: {id} does not exist")
    return talent



@router.get("/email_validated_2/{email}",response_model=schemas.talentResponse3)
def get_id_by_email_talent_2(email:EmailStr,login: str = Cookie(None)) -> Any:

    os.chdir(settings.normal_directory)
    try:
        conn_talent.rollback()
    except:
        pass

    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
  
    id_2=""" SELECT * FROM get_id_by_email('%s');"""
    cursor.execute(id_2 % (str(email)))
    talent=cursor.fetchone()
    if talent ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with email: {str(email)} does not exist")
    return talent



@router.post("/talent_post/",status_code=status.HTTP_201_CREATED)
def post_talent(

                email: Annotated[EmailStr,Form(),BeforeValidator(schemas.check_long_str_80)],
                password:Annotated[str,BeforeValidator(schemas.check_long_str_80),Form()],
                full_name:Annotated[str,BeforeValidator(schemas.check_long_str_80),Form()],
                profession:Annotated[str,BeforeValidator(schemas.check_long_str_80),Form()],
                rate:Annotated[int,Form(),BeforeValidator(schemas.check_long_int_10000)],
                description:Annotated[str,BeforeValidator(schemas.check_long_str_860),Form()],
                github: Annotated[Url,Form(),UrlConstraints(max_length=1000, allowed_schemes=["https"]),],
                linkedin:Annotated[Url,Form(),UrlConstraints(max_length=1000, allowed_schemes=["https"]),],
                skills:Annotated[str,Form(),BeforeValidator(schemas.check_long_str_1000)],
                categories:Annotated[str, Form(),BeforeValidator(schemas.check_long_str_1000)],
                file: Annotated[UploadFile, File()],
                instagram:Annotated[Union[Url,None],Form(),UrlConstraints(max_length=1000, allowed_schemes=["https"]),]=None,
                facebook:Annotated[Union[Url,None],Form(),UrlConstraints(max_length=1000, allowed_schemes=["https"]),]=None,

                 
                 )-> Any:

    os.chdir(settings.normal_directory)
    
    try:
        conn_talent.rollback()
    except:
        pass

    hashed_password=utils.hash(password)
    password=hashed_password
    github=str(github)
    linkedin=str(linkedin)
    instagram=str(instagram)
    facebook=str(facebook)
    email=email.replace('&','')
    email=email.replace('<','')
    email=email.replace('>','')
    email=email.replace('"','')
    email=email.replace("'",'')
    email=email.replace("/",'')

    cursor.execute(""" SELECT * FROM number_of_user_today();""")
    users_today=cursor.fetchone()
    for x in users_today.values():
        user_today_value=x 
    if user_today_value >=50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "We are only receiving 50 login requests per day, sorry :( ")

#################Validate Blacklist Email ###############

    validate_email=""" SELECT * FROM remove_user_by_black_list_email('%s');"""
    cursor.execute(validate_email % ((email.replace(" ", "").lower())))
    validate_0=cursor.fetchone()
    if validate_0 :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "YOUR EMAIL IS BANNED")

#################Validate Email is not a company###############
    validate_email=""" SELECT * FROM remove_talent_by_being_in_firm('%s');"""
    cursor.execute(validate_email % ((email.replace(" ", "").lower())))
    validate_0=cursor.fetchone()
    if validate_0 :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "YOUR EMAIL IS ALREDY BEING USED")

#################Validate Blacklist Words ###############

    validate_word=""" SELECT * FROM remove_user_by_black_list_word('%s','%s','%s');"""
    cursor.execute(validate_word % ((full_name.replace(" ", "").lower()),(profession.replace(" ", "").lower()),(description.replace(" ", "").lower())))
    validate_1=cursor.fetchone()
    if validate_1 :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "THIS SITE DOES NOT ACCEPT BAD WORDS")
    
#################Validate url contains words(linkedin,girhub,facebook,instagram) ###############
    if not (str(github).startswith('https://github.com') ):   
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "the string should start with https://github.com")
    
    if not (str(linkedin).startswith('https://linkedin.com') ):   
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "the string should start with https://linkedin.com")

    if not(str(facebook) == 'None') and not (str(facebook).startswith('https://facebook.com')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "the string should start with https://facebook.com")
    
    if not(str(instagram) == 'None') and not (str(instagram).startswith('https://instagram.com')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "the string should start with https://instagram.com")
    
###################CREATE USER#####################################################################

    talent_2="""  SELECT insert_talent('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"""
    cursor.execute(talent_2 % (email,password,full_name,profession,rate,description,github,linkedin,instagram,facebook,skills,categories))

    conn_talent.commit()

##### GET ID TO SAVE PICTURE ############################################################
    id_2=""" SELECT * FROM get_id_by_email('%s');"""
    cursor.execute(id_2 % (str(email)))
    id=cursor.fetchone()
    for x in id.values():
        id_data=x    
###### PICTURE  LOGIC ############################################################
    resultado_validacion_foto=utils.validate_Image(id_var=id_data,file_var=file,endpoint='post')
    print(resultado_validacion_foto)
    if not (resultado_validacion_foto == 'fotoPng1Rostro'):

        try:
            picture_name_user=str(id_data)+'.'+(list(file.filename.split("."))[-1]).lower()    
            img_source_2=settings.picture_directory+'/'+picture_name_user
            print(img_source_2)
            os.remove(img_source_2)
        except:
            pass

        delete=""" SELECT delete_talent_by_id('%s');"""
        cursor.execute(delete % (id_data))
        conn_talent.commit()

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "The file format is not valid or the picture does not contain a clear human face")

    

@router.delete("/talent_delete/id/",status_code=status.HTTP_204_NO_CONTENT)
def delete_talent(login: str = Cookie(None)):

    os.chdir(settings.picture_directory)

    try:
        conn_talent.rollback()
    except:
        pass

    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "talent":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    
    id=dict(credentials).get("talent_id")



    img_source=settings.picture_directory+'/'+str(id)+'.png'
    try:
        os.remove(img_source)
    except:
        pass
    
    os.chdir(settings.normal_directory)

    id_2=""" SELECT * FROM get_by_id('%s');"""
    cursor.execute(id_2 % (str(id)))
    talent=cursor.fetchone()
    if talent ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with id: {id} does not exist")

    delete=""" SELECT delete_talent_by_id('%s');"""
    cursor.execute(delete % (id))
    conn_talent.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/talent_put/")
def update_talent(
                
                
                password:Annotated[str,BeforeValidator(schemas.check_long_str_80),Form()],
                full_name:Annotated[str,BeforeValidator(schemas.check_long_str_80),Form()],
                profession:Annotated[str,BeforeValidator(schemas.check_long_str_80),Form()],
                rate:Annotated[int,Form(),BeforeValidator(schemas.check_long_int_10000)],
                description:Annotated[str,BeforeValidator(schemas.check_long_str_860),Form()],
                github: Annotated[Url,Form(),UrlConstraints(max_length=1000, allowed_schemes=["https"]),],
                linkedin:Annotated[Url,Form(),UrlConstraints(max_length=1000, allowed_schemes=["https"]),],
                skills:Annotated[str,Form(),BeforeValidator(schemas.check_long_str_1000)],
                categories:Annotated[str, Form(),BeforeValidator(schemas.check_long_str_1000)],
                file:UploadFile = File(None),
                instagram:Annotated[Union[Url,None],Form(),UrlConstraints(max_length=1000, allowed_schemes=["https"]),]=None,
                facebook:Annotated[Union[Url,None],Form(),UrlConstraints(max_length=1000, allowed_schemes=["https"]),]=None,
                login: str = Cookie(None)
                 
                 )-> Any:

    os.chdir(settings.normal_directory)

    try:
        conn_talent.rollback()
    except:
        pass
        
    if login==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "talent":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    
    id=dict(credentials).get("talent_id")

    hashed_password=utils.hash(password)
    password=hashed_password
    github=str(github)
    linkedin=str(linkedin)
    instagram=str(instagram)
    facebook=str(facebook)


    cursor.execute(""" SELECT * FROM number_of_user_today();""")
    users_today=cursor.fetchone()
    for x in users_today.values():
        user_today_value=x 
    if user_today_value >=50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "We are only receiving 50 login requests per day, sorry :( ")
##########################################CHECK RECOR EXISTS ################################################################

    id_2=""" SELECT * FROM get_by_id('%s');"""
    cursor.execute(id_2 % (str(id)))
    talent=cursor.fetchone()
    if talent ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with id: {id} does not exist")

#################Validate Blacklist Words ###############

    validate_word=""" SELECT * FROM remove_user_by_black_list_word('%s','%s','%s');"""
    cursor.execute(validate_word % ((full_name.replace(" ", "").lower()),(profession.replace(" ", "").lower()),(description.replace(" ", "").lower())))
    validate_1=cursor.fetchone()
    if validate_1 :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "THIS SITE DOES NOT ACCEPT BAD WORDS")
    
#################Validate url contains words(linkedin,girhub,facebook,instagram) ###############
    if not (str(github).startswith('https://github.com') ):   
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "the string should start with https://github.com")
    
    if not (str(linkedin).startswith('https://linkedin.com') ):   
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "the string should start with https://linkedin.com")

    if not(str(facebook) == 'None') and not (str(facebook).startswith('https://facebook.com')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "the string should start with https://facebook.com")
    
    if not(str(instagram) == 'None') and not (str(instagram).startswith('https://instagram.com')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "the string should start with https://instagram.com")
    
    
    update=""" SELECT * FROM update_by_id('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"""
    cursor.execute(update % (str(id),password,full_name,profession,str(rate),description,github,linkedin,instagram,facebook,skills,categories) )
    conn_talent.commit()

    if file  == None:
            return Response(status_code=status.HTTP_201_CREATED,content='Data Uploaded With No Picture') 
    

    resultado_validacion_foto=utils.validate_Image(id_var=id,file_var=file,endpoint='put')
    if not (resultado_validacion_foto == 'fotoPng1Rostro'):

        try:
            picture_name_user=str(id)+'.'+(list(file.filename.split("."))[-1]).lower() 
            img_source_2=settings.picture_directory+'/'+picture_name_user
            os.remove(img_source_2)

            src_path = settings.picture_directory+'/'+'default.png'
            destination_path = settings.picture_directory+'/'+str(id)+'.png'

            copy(src_path, destination_path)

            return Response(status_code=status.HTTP_201_CREATED,content='Data Uploaded and Default Profile Picture Assigned') 

        except:
            pass
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "The file format is not valid")
    
    return Response(status_code=status.HTTP_201_CREATED,content='Data and Profile Picture Updated') 

################################################# TEMPLATES ####################################################################
    
templates= Jinja2Templates(directory="./templates")


@router.get('/signUpTalent/',response_class=HTMLResponse)
def index(request: Request):

    try:
        conn_talent.rollback()
    except:
        pass

    cursor.execute(""" SELECT * FROM """+settings.table_name_for_select_all_skills+""" """)
    skills=cursor.fetchall()

    if not skills :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BBDD does not have any record")
    
    
    Skills_List=[]

    for  skill in skills:
        skill_dict={'skill':skill.get("skill")}
        Skills_List.append(skill_dict)

    context={'request': request, 'skills':Skills_List}
    return templates.TemplateResponse("5_sign_up_talent.html",context)