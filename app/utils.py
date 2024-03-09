from passlib.context import CryptContext
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings
import os
import shutil
from PIL import Image
import cv2 
###############################################################################
pwd_context= CryptContext(schemes=["bcrypt"],deprecated=["auto"])

def hash(password: str):
        return pwd_context.hash(password)

def verify(plain_password, hashed_password):
        return pwd_context.verify(plain_password,hashed_password)
###############################################################################
#######CONECTION TO TALENT TABLE ######################################################################################

while True:
        try:
                conn_talent_utils=psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
                cursor=conn_talent_utils.cursor()
                break
        except Exception as error:
                print("Connecting to database failed")
                print("Error:",error)
                time.sleep(5)


def validate_Image(id_var,file_var,endpoint):

#################################################### DELETE IF IMAGE ALREDY EXISTS ##############################################################
        os.chdir(settings.picture_directory)
        
######################### VALIDATE IMGAE PNG ##################################################################################
        picture_name_user=str(id_var)+'.'+list(file_var.filename.split("."))[-1]

        with open(picture_name_user,"wb") as buffer:
                shutil.copyfileobj(file_var.file,buffer)

        img_source_2=settings.picture_directory+'/'+picture_name_user

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
                return(hola)
        





