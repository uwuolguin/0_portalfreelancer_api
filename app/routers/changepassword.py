from fastapi import  status, HTTPException,APIRouter,Form,Request
from .. import schemas
import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import settings
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
import time
from typing import Any
import os
# Import SendinBlue library
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import secrets
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router= APIRouter(
    
    prefix="/changepassword",
    tags=["ChangePassword"]
)


def getConnection():
    

    while True:
        try:

            conn_changepassword=psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
            break

        except Exception as error:

            print("Connecting to database failed")
            print("Error:",error)
            time.sleep(5)
    return conn_changepassword


@router.post("/changepassword_part1")
def changepassword_part1(email:schemas.email_html) -> Any:

    os.chdir(settings.normal_directory)

    conn_changepassword=getConnection()
    cursor=conn_changepassword.cursor()

#################################### YOU CAN  CHANGE YOUR PASSWORD 1 TIME PER DAY ################################################################

    email=email.replace(" ", "").lower()
    email_2="""  SELECT * from change_password_get_by_email_origin('%s');"""
    cursor.execute(email_2 % (email))
    email_today=cursor.fetchone()
    if not(email_today ==None):
        conn_changepassword.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "You can send 1 petition per day, sorry :(")

#################################### EMAIL HAS TO EXIST EITHER IN TALENT OR IN FIRM ################################################################
    
    id_2=""" SELECT * FROM get_id_by_email('%s');"""
    cursor.execute(id_2 % (str(email)))
    talent=cursor.fetchone()

    id_3=""" SELECT * FROM firm_get_id_by_email('%s');"""
    cursor.execute(id_3 % (str(email)))
    firm=cursor.fetchone()

    if talent==None and firm ==None:
        conn_changepassword.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with email: {str(email)} does not exist")

   
#########################################################    INSERT RECORD OF CHANGEPASSWORD PART1 ##############################################
    
    password_length = 13
    password=secrets.token_urlsafe(password_length)
    origin='part1'

    changepassword_part1="""  SELECT insert_change_password_part_1('%s','%s','%s');"""
    cursor.execute(changepassword_part1 % (str(email),password,origin))
    conn_changepassword.commit()


########################################################## EMAIL SENDING LOGIC ###############################################################################
    # Create a SendinBlue API configuration
    configuration = sib_api_v3_sdk.Configuration()

    # Replace "<your brevo api key here>" with your actual SendinBlue API key
    configuration.api_key['api-key'] = settings.api_password_for_email_password_cahnges

    # Initialize the SendinBlue API instance
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # Define the email sender function
    def send_email(subject, html, to_address=None, receiver_username=None):
        # SendinBlue mailing parameters
        subject = subject
        sender = {"name": settings.api_name_for_email_password_cahnges, "email": settings.cloud_platform_user_for_email_password_changes}
        html_content = html

        # Define the recipient(s)
        # You can add multiple email accounts to which you want to send the mail in this list of dicts
        to = [{"email": to_address, "name": receiver_username}]

        # Create a SendSmtpEmail object
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)

        try:
            # Send the email
            api_response = api_instance.send_transac_email(send_smtp_email)
            print(api_response)
            conn_changepassword.close()
            return {"message": "Email sent successfully!"}
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

    

    title = "Hello Dear User,"
    secondLine=f"Please enter these credentials:"



    html = f"<h2>{title}</h2>"+ f"<h3>{secondLine}</h3>"+f"<ul><li><h3>Email:<a href=mailto:{email}>{email}</a></h3></li><li><h3>Password:{password}</h3></li></ul><h3>In this Url:<ul><li>Url:<a href={settings.change_password_url}>{settings.change_password_url}</a></li></ul><h3></h3><h3>Kind Regards</h3><h3>Portal Freelancer Team</h3>"


    subject = "Portal Freelancer Password Change Request"
    to_address = email
    receiver_username = 'User'
    print("Sending mail...")

    # Send the email and store the response
    email_response = send_email(subject, html, to_address, receiver_username)

    # Print the status of the email sending process
    print(email_response)

    conn_changepassword.close()
    return {'Email Sent'}

@router.post("/changepassword_part2")
def changepassword_part2(email:schemas.email_html,password:Annotated[str,BeforeValidator(schemas.check_long_str_80),Form()]) -> Any:

    os.chdir(settings.normal_directory)

    conn_changepassword=getConnection()
    cursor=conn_changepassword.cursor()

    
#################################### YOU CAN  CHANGE YOUR PASSWORD 1 TIME PER DAY ################################################################

    email=email.replace(" ", "").lower()
    
    email_2="""  SELECT * from change_password_get_by_email_origin_p2('%s');"""
    cursor.execute(email_2 % (email))
    email_today=cursor.fetchone()
    if not(email_today ==None):
        conn_changepassword.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "You can send 1 petition per day, sorry :(")
#################################### CHECK THAT PART 1 HAS HAPPENED ################################################################

    email_2="""  SELECT * from change_password_get_by_email_origin_v22('%s');"""
    cursor.execute(email_2 % (email))
    email_today=cursor.fetchone()

    if email_today.get("changepassword_password") != password:
        conn_changepassword.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "BAD CREDENTIALS")
    
#################################### EMAIL HAS TO EXIST EITHER IN TALENT OR IN FIRM ################################################################
    
    id_2=""" SELECT * FROM get_id_by_email('%s');"""
    cursor.execute(id_2 % (str(email)))
    talent=cursor.fetchone()

    id_3=""" SELECT * FROM firm_get_id_by_email('%s');"""
    cursor.execute(id_3 % (str(email)))
    firm=cursor.fetchone()

    if talent==None and firm ==None:
        conn_changepassword.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with email: {str(email)} does not exist")


   

# #########################################################    CHANGEPASSWORD PASSWORD LOGIC ##############################################
    
    password_length = 13
    password=secrets.token_urlsafe(password_length)

    if talent==None:

        firm_id=firm.get("firm_id")

        update=""" SELECT * FROM update_firm_by_id_only_password('%s','%s');"""
        cursor.execute(update % (str(firm_id),password) )
        conn_changepassword.commit()

    if firm==None:
        
        talent_id=talent.get("talent_id")

        update=""" SELECT * FROM update_talent_by_id_only_password('%s','%s');"""
        cursor.execute(update % (str(talent_id),password) )
        conn_changepassword.commit()


# #########################################################    INSERT RECORD OF CHANGEPASSWORD PART2 ##############################################

    origin='part2'
    changepassword_part2="""  SELECT insert_change_password_part_2('%s','%s');"""
    cursor.execute(changepassword_part2 % (str(email),origin))
    conn_changepassword.commit()

# ########################################################## EMAIL SENDING LOGIC ###############################################################################
    # Create a SendinBlue API configuration
    configuration = sib_api_v3_sdk.Configuration()

    # Replace "<your brevo api key here>" with your actual SendinBlue API key
    configuration.api_key['api-key'] = settings.api_password_for_email_password_cahnges

    # Initialize the SendinBlue API instance
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # Define the email sender function
    def send_email(subject, html, to_address=None, receiver_username=None):
        # SendinBlue mailing parameters
        subject = subject
        sender = {"name": settings.api_name_for_email_password_cahnges, "email": settings.cloud_platform_user_for_email_password_changes}
        html_content = html

        # Define the recipient(s)
        # You can add multiple email accounts to which you want to send the mail in this list of dicts
        to = [{"email": to_address, "name": receiver_username}]

        # Create a SendSmtpEmail object
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)

        try:
            # Send the email
            api_response = api_instance.send_transac_email(send_smtp_email)
            print(api_response)
            conn_changepassword.close()
            return {"message": "Email sent successfully!"}
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

    

    title = "Hello Dear User,"
    secondLine=f"Please login with these credentials:"



    html = f"<h2>{title}</h2>"+ f"<h3>{secondLine}</h3>"+f"<ul><li><h3>Email:<a href=mailto:{email}>{email}</a></h3></li><li><h3>Password:{password}</h3></li></ul><h3>In this Url:<ul><li>Url:<a href={settings.login_url}>{settings.login_url}</a></li></ul><h3></h3><h3>After login, please go to the <a href={settings.settingsuwu_url}>settings </a>section and change the password with your own</h3><h3>Kind Regards</h3><h3>Portal Freelancer Team</h3>"


    subject = "Portal Freelancer Password Change Request"
    to_address = email
    receiver_username = 'User'
    print("Sending mail...")

    # Send the email and store the response
    email_response = send_email(subject, html, to_address, receiver_username)

    # Print the status of the email sending process
    print(email_response)

    conn_changepassword.close()
    return {'Email Sent'}


################################################# TEMPLATES ####################################################################
    
templates= Jinja2Templates(directory="./templates")

@router.get('/changePasswordP1/',response_class=HTMLResponse) 
    
async def cp1(request:Request):

    while True:
        try:
            
            return templates.TemplateResponse(request=request,name="9_recover_password.html")
        except:
            pass

@router.get('/changePasswordP2/',response_class=HTMLResponse)
def cp2(request: Request):

    while True:
        try:
            
            return templates.TemplateResponse(request=request,name="10_recover_password_p2.html")
        except:
            pass