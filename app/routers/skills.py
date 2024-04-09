from fastapi import  status, HTTPException, APIRouter, Response,Form,Cookie
from .. import schemas,oath2
import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import settings
import time
from typing import Any
import os
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

router= APIRouter(
    
    prefix="/skills",
    tags=["Skills"]
)

def getConnection():
    

    while True:
        try:

            conn_skills=psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
            break

        except Exception as error:

            print("Connecting to database failed")
            print("Error:",error)
            time.sleep(5)

    return conn_skills


@router.get("/skills_get_all",response_model=list[schemas.skillResponse])
def get_all_skills() -> Any:

    os.chdir(settings.normal_directory)

    conn_skills=getConnection()
    cursor=conn_skills.cursor()


    cursor.execute(""" SELECT * FROM """+settings.table_name_for_select_all_skills+""" """)
    skill=cursor.fetchall()
    if not skill :
        conn_skills.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BBDD does not have any record")
    conn_skills.close()
    return skill


@router.post("/skill_post/",status_code=status.HTTP_201_CREATED)
def post_skill(

                skill_input:Annotated[str,BeforeValidator(schemas.check_long_str_1000),Form()],

                login: str = Cookie(None))-> Any:

    os.chdir(settings.normal_directory)
    
    conn_skills=getConnection()
    cursor=conn_skills.cursor()

    if login==None:
        conn_skills.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        conn_skills.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
   
###################CREATE USER#####################################################################

    category_2="""  SELECT insert_skill('%s');"""
    cursor.execute(category_2 % (skill_input))
    conn_skills.commit()
    conn_skills.close()

@router.delete("/skill_delete/id/{skill_input}",status_code=status.HTTP_204_NO_CONTENT)
def delete_category(skill_input:str, login: str = Cookie(None)):

    os.chdir(settings.normal_directory)
    
    conn_skills=getConnection()
    cursor=conn_skills.cursor()

    if login==None:
        conn_skills.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        conn_skills.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    
    id_2=""" SELECT * FROM get_by_skill('%s');"""
    cursor.execute(id_2 % (skill_input))
    skill=cursor.fetchone()
    if skill ==None:
        conn_skills.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with category: {skill_input} does not exist")

    delete=""" SELECT * from delete_skill('%s');"""
    cursor.execute(delete % (str(skill_input)))
    conn_skills.commit()
    
    conn_skills.close()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/skill_put/{skill_input}/{new_skill_input}")
def update_firm(skill_input:str,new_skill_input:str, login: str = Cookie(None)):

    os.chdir(settings.normal_directory)
    
    conn_skills=getConnection()
    cursor=conn_skills.cursor()

    if login==None:
        conn_skills.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        conn_skills.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    

    id_2=""" SELECT * FROM get_by_skill('%s');"""
    cursor.execute(id_2 % (skill_input))
    skill=cursor.fetchone()
    if skill ==None:
        conn_skills.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with skill: {skill_input} does not exist")
    
    update=""" SELECT * FROM update_skill('%s','%s');"""
    cursor.execute(update % (skill_input,new_skill_input) )
    conn_skills.commit()
    conn_skills.close()
    return Response(status_code=status.HTTP_201_CREATED,content='Data Updated') 
