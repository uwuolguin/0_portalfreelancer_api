from fastapi import  APIRouter,Cookie,Request,status,HTTPException
from .. import oath2
from ..config import settings
import time
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import psycopg2
from psycopg2.extras import RealDictCursor
from ..utils import tableauAuthentification,tableauAllDatasources,send_email_to_admin,tableauCreateWebhook,tableauListWebhook,tableauDeleteWebhook,tableauTestWebhook

templates= Jinja2Templates(directory="./templates")

def getConnection():
    

    while True:
        try:

            conn_tableau=psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
            break

        except Exception as error:

            print("Connecting to database failed")
            print("Error:",error)
            time.sleep(5)

    return conn_tableau


router= APIRouter(
    
    prefix="/tableau",
    tags=["Tableau"]
)



@router.post('/tableau_create_webhook/',status_code=status.HTTP_201_CREATED)
def tableau_create_webhook(webhookname:str,webhookUrl:str,event:str,login: str = Cookie(None)):

    try:
        credentials=oath2.decode_access_token(login)

        if dict(credentials).get("role") == "superadmin":

            authentification_response=tableauAuthentification()

            if authentification_response["access_token_value"] == "fail":
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
            
            response=tableauCreateWebhook(siteid=authentification_response["siteid_value"] ,token=authentification_response["access_token_value"] ,webhookName=webhookname,webhook_url=webhookUrl,event=event)

            
            return response
        
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    

@router.delete('/tableau_delete_webhook/',status_code=status.HTTP_204_NO_CONTENT)
def tableau_delete_webhook(webhookId:str,login: str = Cookie(None)):

    try:
        credentials=oath2.decode_access_token(login)

        if dict(credentials).get("role") == "superadmin":

            authentification_response=tableauAuthentification()

            if authentification_response["access_token_value"] == "fail":
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
            
            response=tableauDeleteWebhook(siteid=authentification_response["siteid_value"] ,token=authentification_response["access_token_value"] ,webhookId=webhookId)

            
            return response
        
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")

@router.get('/tableau_test_webhook/',status_code=status.HTTP_200_OK)
def tableau_test_webhook(webhookId:str,login: str = Cookie(None)):

    try:
        credentials=oath2.decode_access_token(login)

        if dict(credentials).get("role") == "superadmin":

            authentification_response=tableauAuthentification()

            if authentification_response["access_token_value"] == "fail":
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
            
            response=tableauTestWebhook(siteid=authentification_response["siteid_value"] ,token=authentification_response["access_token_value"] ,webhookId=webhookId)

            
            return response
        
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")


@router.post('/tableau_webhook_fail_refresh_destination/',status_code=status.HTTP_201_CREATED)
def tableau_create_webhook(resource_name="Test"):

    conn_tableau=getConnection()
    cursor=conn_tableau.cursor()
    
    cursor.execute(""" select count(tableau_url) from public.tableau_failed_refreshed where last_updated_at + interval '1 day' >=NOW() :: TIMESTAMP WITH TIME ZONE and tableau_url = 'failed_refreshed_webhook'; """)
    
    counter=complaint=cursor.fetchone()
    
    if counter<3:

        send_email_to_admin('refresh of extraction failed'+' datasourceName='+resource_name)
        
        cursor.execute(""" INSERT INTO public.tableau_failed_refreshed (tableau_url) VALUES ('failed_refreshed_webhook'); """)

        conn_tableau.commit()

    
    conn_tableau.close()
    return status.HTTP_201_CREATED





@router.get('/tableau_html_panel/',response_class=HTMLResponse)
def tableau_html(request: Request,login: str = Cookie(None)):

    while True:

        try:
            try:
                credentials=oath2.decode_access_token(login)

                if dict(credentials).get("role") == "superadmin":
                    login_role_value="superadmin"
                elif dict(credentials).get("role") == "firm":
                    login_role_value="firm"
                else:
                    login_role_value="talent"


            except:
                login_role_value="None"
                pass

            if login_role_value=="superadmin":

                context={'request': request}
                return templates.TemplateResponse("14_tableau.html",context)
            else:
                                
                context={'request': request}
                return templates.TemplateResponse("4_log_in.html",context)
        except:
            time.sleep(1)
            pass

@router.get('/tableau_html_query_all_datasources/',response_class=HTMLResponse)
def tableau_query_all_datasources(request: Request,login: str = Cookie(None)):

    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") == "superadmin":

        authentification_response=tableauAuthentification()

        if authentification_response["access_token_value"] == "fail":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
        
        response=tableauAllDatasources(siteid=authentification_response["siteid_value"] ,token=authentification_response["access_token_value"] )

        context={'request': request,'response':response}
        return templates.TemplateResponse("15_tableau_datasource.html",context)
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    
@router.get('/tableau_list_webhooks/',response_class=HTMLResponse)
def tableau_list_webhooks(request: Request,login: str = Cookie(None)):

    try:
        credentials=oath2.decode_access_token(login)

        if dict(credentials).get("role") == "superadmin":

            authentification_response=tableauAuthentification()

            if authentification_response["access_token_value"] == "fail":
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
            
            response=tableauListWebhook(siteid=authentification_response["siteid_value"] ,token=authentification_response["access_token_value"])

            
            context={'request': request,'response':response}
            return templates.TemplateResponse("15_tableau_datasource.html",context)
        
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")