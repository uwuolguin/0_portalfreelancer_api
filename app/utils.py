import bcrypt
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings
import os
import shutil
from PIL import Image
import cv2 
# Import SendinBlue library
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import requests
import re
from .oath2 import create_access_token
###############################################################################

def hash(password: str):
        salt = bcrypt.gensalt() 
        return bcrypt.hashpw(password=password.encode('utf-8'), salt=salt)

def verify(plain_password, hashed_password):
        plain_password=bytes(plain_password, 'utf-8')
        hashed_password=bytes(hashed_password, 'utf-8')
        
        return bcrypt.checkpw(plain_password,hashed_password)
###############################################################################
#######CONECTION TO TALENT TABLE ######################################################################################


def getConnection():
    

    while True:
        try:

            conn_talent_utils=psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
            break

        except Exception as error:

            print("Connecting to database failed")
            print("Error:",error)
            time.sleep(5)

    return conn_talent_utils


#####################CREATE ACCESS COOKIE FOR TESTING
def create_cookie_token_access_for_testing(email):


        conn_talent_utils=getConnection()
        cursor=conn_talent_utils.cursor()

        if email==settings.superadmin_email:

                token_data={'superadmin_id':1,'superadmin_email':email,'role':"superadmin"}
                token=create_access_token(token_data)

                conn_talent_utils.close()
                return token


        if email==settings.cloud_platform_user_for_email_password_changes:

                id_2=""" SELECT * FROM get_id_by_email('%s');"""
                cursor.execute(id_2 % (str(email)))
                talent=cursor.fetchone()

                token_data={'talent_id':talent.get("talent_id"),'talent_email':email,'role':'talent'}
                token=create_access_token(token_data)

                conn_talent_utils.close()
                return token
        if email==settings.cloud_platform_user_for_email_sending:

                id_3=""" SELECT * FROM firm_get_id_by_email('%s');"""
                cursor.execute(id_3 % (str(email)))
                firm=cursor.fetchone()

                token_data={'firm_id':firm.get("firm_id"),'firm_email':email,'role':'firm'}
                token=create_access_token(token_data)

                conn_talent_utils.close()
                return token
##############IMAGE MANAGEMENT LOGIC

def validate_Image(id_var,file_var,endpoint):

#################################################### DELETE IF IMAGE ALREDY EXISTS ##############################################################
        os.chdir(settings.picture_directory)
        
######################### VALIDATE IMGAE PNG ##################################################################################
        picture_name_user=str(id_var)+'.'+(list(file_var.filename.split("."))[-1]).lower()

        with open(picture_name_user,"wb") as buffer:
                shutil.copyfileobj(file_var.file,buffer)

        img_source_2=settings.picture_directory+'/'+picture_name_user
        conn_talent_utils=getConnection()
        cursor=conn_talent_utils.cursor()
        try:
                img = Image.open(img_source_2)
                format = img.format
                print(format !='PNG')
                if format !='PNG':
                        img.close()
                        if endpoint=='post':
                                try:
                                        delete=""" SELECT delete_talent_by_id('%s');"""
                                        cursor.execute(delete % (id_var))
                                        conn_talent_utils.commit()


                                        

                                except:
                                        pass
                        hola = 'fotoNoPng'
                        conn_talent_utils.close()
                        try:
                               img.close()
                        except:
                               pass

                        return(hola)
                        
                try:
                   
                   os.remove(img_source_2)
                   
                except:
                   
                   pass

                img.save(img_source_2)
                img.close()

        except:
                time.sleep(1)
                
                if endpoint=='post':
                        try:
                                delete=""" SELECT delete_talent_by_id('%s');"""
                                cursor.execute(delete % (id_var))
                                conn_talent_utils.commit()
                        except:
                                pass
                try:
                   
                   os.remove(settings.picture_directory+'/'+str(id_var)+'.png')
                   
                except:
                   
                   pass

                hola = 'NoEsFoto'
                conn_talent_utils.close()

                try:
                        img.close()
                except:
                        pass
                        
                return(hola)
        try:
                faceCascPath = 'haarcascade_frontalface_default.xml'
                faceCascade = cv2.CascadeClassifier(faceCascPath)
                image = cv2.imread(img_source_2)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(20, 20)
                )

                if len(faces) ==1:
                        
                        update=""" SELECT update_picture_directory_by_id('%s','%s');"""
                        cursor.execute(update % (img_source_2,id_var))
                        conn_talent_utils.commit()
                        hola = 'fotoPng1Rostro'
                        conn_talent_utils.close()

                        try:
                               img.close()
                        except:
                               pass
                        
                        return(hola)
                else:
                        if endpoint=='post':
                                try:

                                        delete=""" SELECT delete_talent_by_id('%s');"""
                                        cursor.execute(delete % (id_var))
                                        conn_talent_utils.commit()
                        
                                except:
                                        pass

                        hola = 'fotoPngNo1Rostro'
                        conn_talent_utils.close()

                        try:
                               img.close()
                        except:
                               pass
                        

                        return(hola)

        except:
                if endpoint=='post':
                        try:
                                delete=""" SELECT delete_talent_by_id('%s');"""
                                cursor.execute(delete % (id_var))
                                conn_talent_utils.commit()
                
                        except:
                                pass

                hola = 'fotoPngNoReconocidaPorAlgoritmoML'
                conn_talent_utils.close()
                
                try:
                        img.close()
                except:
                        pass
                        

                return(hola)
        
########SEND EMAIL TO ADMIN

def send_email_to_admin(text_to_send):
                
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

                                return {"message": "Email sent successfully!"}
                        except ApiException as e:
                                print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

                

                title = text_to_send
                html = f"<h2>{title}</h2>"

                subject = text_to_send
                to_address = settings.superadmin_email
                receiver_username = 'User'
                print("Sending mail...")

                # Send the email and store the response
                email_response = send_email(subject, html, to_address, receiver_username)

                # Print the status of the email sending process
                print(email_response)
                return {'Email Sent'}
##############################TABLEAU################################################
def tableauAuthentification():
        try:

                data = {
	        "credentials": {
		"personalAccessTokenName": settings.tableau_token_name,
		"personalAccessTokenSecret": settings.tableau_token_password,
		"site": {
			"contentUrl": settings.tableau_token_sitename
		        }
	                        }
                }

                api_url = "https://10ax.online.tableau.com/api/3.22/auth/signin"

                all_users = requests.post(url=api_url,json=data,headers = {"Content-Type" : "application/json"})

                response = all_users.text
                access_token = re.search('''credentials token="(.*)" estimatedTimeToExpiration=''', response)
                siteid=re.search('''site id="(.*)" contentUrl=''', response)

                access_token_text=access_token.group(1)
                siteid_text=siteid.group(1)


                return {"access_token_value":access_token_text,"siteid_value":siteid_text}
        except:
                send_email_to_admin('The Tableau Token has EXPIRED!!!!')
                return {"access_token_value":"fail","siteid_value":"fail"}
        
def tableauAllDatasources(siteid,token):
        try:
                
                api_url = "https://10ax.online.tableau.com/api/3.22/sites/"+siteid+"/datasources"

                all_datasources = requests.get(url=api_url,headers = {"X-tableau-auth" : token})

                response = all_datasources.text

                datasources=re.search('''<datasources>(.*)</datasources>''', response)

                datasources=datasources.group(1)

                datasource=datasources.split("</datasource>")
                

                datasource_list=[]

                for i in range(len(datasource)-1):
                       id=re.findall(''' id="(.*)" isCertified''' ,datasource[i])[0]
                       name=re.findall(''' name="(.*)" size''' ,datasource[i])[0]
                       site_id=re.findall('''><project id="(.*)" name="''' ,datasource[i])[0]
                       site_id=site_id.split()[0][:-1]
                       createdat=re.findall(''' createdAt="(.*)''' ,datasource[i])[0]
                       createdat=createdat.split()[0][:-1]


                       datasource_text="name="+name+" "+"**"+" "+"id="+id+" "+"**"+" "+"siteid="+site_id+" "+"**"+" "+"createdAt:"+createdat+";"
                       datasource_list.append(datasource_text)

                return datasource_list
        except:
                 send_email_to_admin('Could not get Datasources')
                 return 'Could not get Datasources'

def tableauCreateWebhook(siteid,token,webhookName,webhook_url,event):
        try:
                
                url ="https://10ax.online.tableau.com/api/3.22/sites/"+siteid+"/webhooks"

                #webhook_url="https://apiportalfreelancer.lat/tableau/tableau_webhook_fail_refresh_destination/"

                data={
                        "webhook": {
                        "webhook-destination": {
                                "webhook-destination-http": {
                                "method": "POST",
                                "url": webhook_url,
                                }
                        },
                        "event": event,
                        "name": webhookName
                        }
                        }

                headers = {
                'X-Tableau-Auth': token,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, json=data)

                return response.text
        except:
                 send_email_to_admin('Could not create Webhook')
                 return 'Could not create Webhook'
def tableauListWebhook(siteid,token):
        try:
                
                url ="https://10ax.online.tableau.com/api/3.22/sites/"+siteid+"/webhooks"
                                
                data={}

                headers = {
                'X-Tableau-Auth': token,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
                }
                response = requests.request("GET", url, headers=headers, json=data)

                webhooks=(response.text).replace("\\","").replace('''"''', "").replace("{","").replace("}","")

                webhook_list_html=[]  

                webhook_split_list=webhooks.split("owner:id")            
                
                for i in range(len(webhook_split_list)-1):

                        id_=(webhook_split_list[i+1].split(",")[2])
                        name_=(webhook_split_list[i+1].split(",")[3])
                        webhook_test=name_+" "+"**"+" "+id_+";"
                        webhook_list_html.append(webhook_test)
                
                
                return webhook_list_html
        except:
                 send_email_to_admin('Could not List Webhooks')
                 return 'Could not list Webhook'
        
def tableauDeleteWebhook(siteid,token,webhookId):
        try:
                
                url ="https://10ax.online.tableau.com/api/3.22/sites/"+siteid+"/webhooks/"+webhookId


                data={}

                headers = {
                'X-Tableau-Auth': token,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
                }
                response = requests.request("DELETE", url, headers=headers, json=data)

                return response.text
        except:
                 send_email_to_admin('Could not delete Webhook')
                 return 'Could not delete Webhook'
        
def tableauTestWebhook(siteid,token,webhookId):
        try:
                
                url ="https://10ax.online.tableau.com/api/3.22/sites/"+siteid+"/webhooks/"+webhookId+"/test"


                data={}

                headers = {
                'X-Tableau-Auth': token,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
                }
                response = requests.request("GET", url, headers=headers, json=data)

                return response.text
        except:
                 send_email_to_admin('Could not test Webhook')
                 return 'Could not test Webhook'