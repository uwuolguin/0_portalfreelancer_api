from passlib.context import CryptContext
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

###############################################################################
pwd_context= CryptContext(schemes=["bcrypt"],deprecated=["auto"])

def hash(password: str):
        return pwd_context.hash(password)

def verify(plain_password, hashed_password):
        return pwd_context.verify(plain_password,hashed_password)
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


                       datasource_text="name:"+name+"== id:"+id+" && siteid:"+site_id+" && createdAt:"+createdat+";"
                       datasource_list.append(datasource_text)

                return datasource_list
        except:
                 send_email_to_admin('Could not get Datasources')
                 return 'Could not get Datasources'
