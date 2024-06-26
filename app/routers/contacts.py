from fastapi import  status, HTTPException, APIRouter,Cookie,Request
from .. import schemas,oath2
import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import settings
import time
from typing import Any,Optional
import os
# Import SendinBlue library
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates

router= APIRouter(
    
    prefix="/contacts",
    tags=["Contacts"]
)

def getConnection():
    

    while True:
        try:

            conn_contacts=psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
            break

        except Exception as error:

            print("Connecting to database failed")
            print("Error:",error)
            time.sleep(5)

    return conn_contacts


@router.get("/contacts_get_all",response_model=list[schemas.contactResponse])
def get_all_contacts(login: str = Cookie(None)) -> Any:

    os.chdir(settings.normal_directory)

    conn_contacts=getConnection()
    cursor=conn_contacts.cursor()

    if login==None:

        conn_contacts.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        conn_contacts.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")

    cursor.execute(""" SELECT * FROM """+settings.table_name_for_select_all_contacts+""" """)
    contact=cursor.fetchall()
    if not contact :
        conn_contacts.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BBDD does not have any record")
    conn_contacts.close()
    return contact



@router.get("/contact_get_id/id_firm/{id}",response_model=list[schemas.contactResponse4])
def get_contact_firm(id:int,login: str = Cookie(None)) -> Any:

    os.chdir(settings.normal_directory)

    conn_contacts=getConnection()
    cursor=conn_contacts.cursor()

    if login==None:
        conn_contacts.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        conn_contacts.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")

    id_2=""" SELECT * FROM contacts_get_by_id_firm('%s');"""
    cursor.execute(id_2 % (str(id)))
    firm=cursor.fetchall()
    if firm ==None:
        conn_contacts.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with id: {id} does not exist")
    conn_contacts.close()
    return firm


@router.get("/contact_get_id/id_talent/{id}",response_model=list[schemas.contactResponse4])
def get_contact_talent(id:int,login: str = Cookie(None)) -> Any:

    os.chdir(settings.normal_directory)

    conn_contacts=getConnection()
    cursor=conn_contacts.cursor()

    if login==None:
        conn_contacts.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        conn_contacts.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")


    id_2=""" SELECT * FROM contacts_get_by_id_talent('%s');"""
    cursor.execute(id_2 % (str(id)))
    talent=cursor.fetchall()
    if talent ==None:
        conn_contacts.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with id: {id} does not exist")
    conn_contacts.close()
    return talent

@router.get("/contact_get_id/id_talent_firm/{id_talent}/{id_firm}",response_model=list[schemas.contactResponse4])
def get_contact_talent_firm(id_talent:int,id_firm:int,login: str = Cookie(None)) -> Any:

    os.chdir(settings.normal_directory)

    conn_contacts=getConnection()
    cursor=conn_contacts.cursor()

    if login==None:
        conn_contacts.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "superadmin":
        conn_contacts.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")


    id_2=""" SELECT * FROM contacts_get_by_id_talent_firm('%s','%s');"""
    cursor.execute(id_2 % (str(id_talent),str(id_firm)))
    talent_firm=cursor.fetchall()
    if talent_firm ==None:
        conn_contacts.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with id: {id_talent} or {id_firm} does not exist")
    conn_contacts.close()
    return talent_firm





@router.post("/contacts/post/{id_talent}")
async def contacting_talent(id_talent:int,login: str = Cookie(None)):

    os.chdir(settings.normal_directory)

    conn_contacts=getConnection()
    cursor=conn_contacts.cursor()

    if login==None:
        conn_contacts.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    credentials=oath2.decode_access_token(login)

    if dict(credentials).get("role") != "firm":
        conn_contacts.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BAD CREDENTIALS")
    
    id_firm=dict(credentials).get("firm_id")

############################################################300 email max per day ##########################################################################################################3
    cursor.execute(""" SELECT * FROM number_of_email_today();""")
    users_today=cursor.fetchone()
    for x in users_today.values():
        user_today_value=x 
    if user_today_value >=300:
        conn_contacts.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "We can send only 300 emails per day, sorry :(")


########################################################### TALENT CAN RECEIVE 1 EMAIL PER DAY ##########################################################################################

    contacts_5="""  SELECT * FROM number_of_email_received_by_talent_today('%s');"""
    cursor.execute(contacts_5 % (id_talent))

    users_today=cursor.fetchone()
    for x in users_today.values():
        user_today_value=x 
    if user_today_value >=1:
        conn_contacts.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Our Talent can only receive 1 email per day, and this user has already received an offer, sorry :(")

 
########################################################### FIRM CAN SEND 1 EMAIL PER DAY ##########################################################################################

    contacts_3="""  SELECT * FROM number_of_email_sent_by_firm_today('%s');"""
    cursor.execute(contacts_3 % (id_firm))

    users_today=cursor.fetchone()
    for x in users_today.values():
        user_today_value=x 
    if user_today_value >=1:
        conn_contacts.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "You can send only 1 email per day, sorry :( ")

########################################################## EMAIL SENDING LOGIC ###############################################################################
    # Create a SendinBlue API configuration
    configuration = sib_api_v3_sdk.Configuration()

    # Replace "<your brevo api key here>" with your actual SendinBlue API key
    configuration.api_key['api-key'] = settings.api_password_for_email_sending

    # Initialize the SendinBlue API instance
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # Define the email sender function
    def send_email(subject, html, to_address=None, receiver_username=None):
        # SendinBlue mailing parameters
        subject = subject
        sender = {"name": settings.api_name_for_email_sending, "email": settings.cloud_platform_user_for_email_sending}
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
            conn_contacts.close()
            return {"message": "Email sent successfully!"}
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

    
    id_2=""" SELECT * FROM firm_get_by_id('%s');"""
    cursor.execute(id_2 % (str(id_firm)))
    firm=cursor.fetchone()
    if firm ==None:
        conn_contacts.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with id: {id_firm} does not exist")
    
    company_name=firm.get("firm_full_name")
    company_messeage=firm.get("firm_email_template_to_send")
    company_contact_email=firm.get("firm_contact_email")
    company_contact_phone=firm.get("firm_contact_phone")
    company_linkedin=firm.get("firm_linkedin")
    company_instagram=firm.get("firm_instagram")


    id_2=""" SELECT * FROM get_by_id('%s');"""
    cursor.execute(id_2 % (str(id_talent)))
    talent=cursor.fetchone()
    if talent ==None:
        conn_contacts.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"BBDD with id: {id_talent} does not exist")
    
    talent_name=talent.get("talent_full_name")
    talent_email=talent.get("talent_email")

    title = "Hello Dear Developer,"
    secondLine=f"The company {company_name} is interested in you and have send you this message:"



    html = f"<h2>{title}</h2>"+ f"<h3>{secondLine}</h3>"+f"<h3>{company_messeage}</h3>"+"<h3>Information About The Company:</h3>"+f"<ul><li><h3>Company's Contact Email:<a href=mailto:{company_contact_email}>{company_contact_email}</a></h3></li><li><h3>Company's Contact Phone:{company_contact_phone}</h3></li><li><h3>Company's Linkedin Url:<a href={company_linkedin}>{company_linkedin}</a></h3></li><li><h3>Company's Instagram:<a href={company_instagram}>{company_instagram}</a></h3></li></ul><h3>Kind Regards</h3><h3>Portal Freelancer Team</h3>"


    subject = "Portal Freelancer Company Proposal"
    to_address = talent_email
    receiver_username = talent_name
    print("Sending mail...")

    # Send the email and store the response
    email_response = send_email(subject, html, to_address, receiver_username)

    # Print the status of the email sending process
    print(email_response)


################################################################ SAVE THE EMAIL SENDING    #############################################################################################

    conn_contacts=getConnection()
    cursor=conn_contacts.cursor()
    contacts_2="""  SELECT insert_contacts('%s','%s');"""
    cursor.execute(contacts_2 % (id_talent,id_firm))

    conn_contacts.commit()

    conn_contacts.close()
    return {'Email Sent'}

################################################# TEMPLATES ####################################################################
    
templates= Jinja2Templates(directory="./templates")
#####FUNCTIONS TO ASSIST IN THE SCENARIOS########################################

def PAGINATE_A_LIST(list_to_paginate,pagination_value_var):
        lenght_talents=len(list_to_paginate)

        if (pagination_value_var-1)*3 <lenght_talents:
            talents_part1=[list_to_paginate[(pagination_value_var-1)*3]]
        else:
            talents_part1=[]

        if ((pagination_value_var-1)*3)+1 <lenght_talents:
            talents_part2=[list_to_paginate[((pagination_value_var-1)*3)+1]]
        else:
            talents_part2=[]
        
        if ((pagination_value_var-1)*3)+2 <lenght_talents:
            talents_part3=[list_to_paginate[((pagination_value_var-1)*3)+2]]
        else:
            talents_part3=[]

        talents=talents_part1+talents_part2+talents_part3

        return talents


@router.get('/contacts_normal/',response_class=HTMLResponse)
def contacts_normal(  request: Request,
                      login: str = Cookie(None),
                      skills_string: Optional[str] = "None",
                      skills_state_string: Optional[str] = "None",
                      category_string: Optional[str] = "None",
                      category_state_string: Optional[str] = "None",
                      pagination_state:Optional[str] = "1.2.3.4.5.6.7.8.9.10",
                      pagination_value:Optional[int] = 1, 
                      magic_word:Optional[str] = "None"
                      ):
    
    while True:
        try:
            time.sleep(0.2)
            conn_contacts=getConnection()
            cursor=conn_contacts.cursor()

            if login==None:
                    context={'request': request}
                    conn_contacts.close()
                    return templates.TemplateResponse("4_log_in_contacts.html",context)
            
            try:
                credentials=oath2.decode_access_token(login)

                if dict(credentials).get("role") == "superadmin":
                    login_role_value="superadmin"
                elif dict(credentials).get("role") == "firm":
                    login_role_value="firm"
                else:
                    login_role_value="talent"
            except:
                pass


            cursor.execute(""" SELECT * FROM """+settings.table_name_for_select_all_skills+""" """)
            skills=cursor.fetchall()

            if not skills :
                conn_contacts.close()
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BBDD does not have any record")
            
            
            Skills_List=[]

            for  skill in skills:
                skill_dict={'skill':skill.get("skill"),'skill_key':skill.get("skill").replace(' ','')}
                Skills_List.append(skill_dict)


            cursor.execute(""" SELECT * FROM """+settings.table_name_for_select_all_categories+""" """)
            categories=cursor.fetchall()
            if not categories :
                conn_contacts.close()
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BBDD does not have any record")
            
            
            Categories_List=[]

            for  category in categories:
                category_dict={'category':category.get("category"),'category_key':category.get("category").replace(' ','')}
                Categories_List.append(category_dict)
            
        ###################################### Talent Cache #######################
                
            # credentials=oath2.decode_access_token(login)
            # print(dict(credentials))

            if skills_string !="None":
                skills_string_list=skills_string.replace(' ','').lower().split('.')

            if category_string !="None":
                category_string_list=category_string.replace(' ','').lower().split('.')



        ####################################3  SCENARIOS , they are 8  for now

            if magic_word =="None" and skills_string=="None" and category_string == "None":

                query_part_1= "SELECT id,email,full_name,profession,rate,description,github,linkedin,instagram,facebook,skills,categories,created_at FROM "+settings.table_name_for_select_all_free_user+" ORDER by CREATED_AT DESC;"

                cursor.execute(query_part_1)
                talents=cursor.fetchall()#THIS IS A LIST

                talents=PAGINATE_A_LIST(talents,pagination_value)

            if magic_word !="None" and skills_string=="None" and category_string == "None":

                magic_word_c ="'"+(magic_word.replace(" ", "")).lower()+"'"

                query_part_1= "SELECT id,email,full_name,profession,rate,description,github,linkedin,instagram,facebook,skills,categories,created_at FROM "+settings.table_name_for_select_all_free_user+" WHERE position("+magic_word_c+" in LOWER(REPLACE(full_name,' ','')))>0  OR position("+magic_word_c+" in LOWER(REPLACE(profession,' ','')))>0 OR position("+magic_word_c+" in LOWER(REPLACE(description,' ','')))>0 ORDER by CREATED_AT DESC ;"

                cursor.execute(query_part_1)
                talents=cursor.fetchall() #THIS IS A LIST

                talents=PAGINATE_A_LIST(talents,pagination_value)

            if magic_word =="None" and skills_string!="None" and category_string == "None":


                talents=[]
                id_alredy_used=[]
                for i in skills_string_list:

                    query_part_1= "SELECT id,email,full_name,profession,rate,description,github,linkedin,instagram,facebook,skills,categories,created_at FROM "+settings.table_name_for_select_all_free_user+" where position( '"+i+"' in LOWER(REPLACE(skills,' ','')))>0 ORDER by CREATED_AT DESC ;"

                    cursor.execute(query_part_1)
                    talents_part=cursor.fetchall()# LIST OF REALDICROW ELEMENTS
                    
                    try:
                    
                        for x in talents_part:
                            current_id=x.get("id")
                            if current_id not in id_alredy_used:
                                id_alredy_used.append(current_id)
                                talents.append(x)
                    
                    except:
                        pass

                
                talents=PAGINATE_A_LIST(talents,pagination_value)


            if magic_word =="None" and skills_string=="None" and category_string != "None":

                
                talents=[]
                id_alredy_used=[]
                for i in category_string_list:

                    query_part_1= "SELECT id,email,full_name,profession,rate,description,github,linkedin,instagram,facebook,skills,categories,created_at FROM "+settings.table_name_for_select_all_free_user+" where position( '"+i+"' in LOWER(REPLACE(categories,' ','')))>0 ORDER by CREATED_AT DESC ;"

                    cursor.execute(query_part_1)
                    talents_part=cursor.fetchall()# LIST OF REALDICROW ELEMENTS
                    
                    try:
                    
                        for x in talents_part:
                            current_id=x.get("id")
                            if current_id not in id_alredy_used:
                                id_alredy_used.append(current_id)
                                talents.append(x)
                    
                    except:
                        pass

                
                talents=PAGINATE_A_LIST(talents,pagination_value)

            if magic_word !="None" and skills_string=="None" and category_string != "None":

                magic_word_c ="'"+(magic_word.replace(" ", "")).lower()+"'"
                talents=[]
                id_alredy_used=[]
                for i in category_string_list:

                    query_part_1= "SELECT id,email,full_name,profession,rate,description,github,linkedin,instagram,facebook,skills,categories,created_at FROM "+settings.table_name_for_select_all_free_user+" where position( '"+i+"' in LOWER(REPLACE(categories,' ','')))>0 AND (position("+magic_word_c+" in LOWER(REPLACE(full_name,' ','')))>0  OR position("+magic_word_c+" in LOWER(REPLACE(profession,' ','')))>0 OR position("+magic_word_c+" in LOWER(REPLACE(description,' ','')))>0 ) ORDER by CREATED_AT DESC ;"

                    cursor.execute(query_part_1)
                    talents_part=cursor.fetchall()# LIST OF REALDICROW ELEMENTS
                    
                    try:
                    
                        for x in talents_part:
                            current_id=x.get("id")
                            if current_id not in id_alredy_used:
                                id_alredy_used.append(current_id)
                                talents.append(x)
                    
                    except:
                        pass

                
                talents=PAGINATE_A_LIST(talents,pagination_value)

            if magic_word !="None" and skills_string!="None" and category_string == "None":

                magic_word_c ="'"+(magic_word.replace(" ", "")).lower()+"'"
                talents=[]
                id_alredy_used=[]
                for i in skills_string_list:

                    query_part_1= "SELECT id,email,full_name,profession,rate,description,github,linkedin,instagram,facebook,skills,categories,created_at FROM "+settings.table_name_for_select_all_free_user+" where position( '"+i+"' in LOWER(REPLACE(skills,' ','')))>0 AND (position("+magic_word_c+" in LOWER(REPLACE(full_name,' ','')))>0  OR position("+magic_word_c+" in LOWER(REPLACE(profession,' ','')))>0 OR position("+magic_word_c+" in LOWER(REPLACE(description,' ','')))>0 ) ORDER by CREATED_AT DESC ;"

                    cursor.execute(query_part_1)
                    talents_part=cursor.fetchall()# LIST OF REALDICROW ELEMENTS
                    
                    try:
                    
                        for x in talents_part:
                            current_id=x.get("id")
                            if current_id not in id_alredy_used:
                                id_alredy_used.append(current_id)
                                talents.append(x)
                    
                    except:
                        pass

                
                talents=PAGINATE_A_LIST(talents,pagination_value)

            if magic_word =="None" and skills_string!="None" and category_string != "None":


                talents=[]
                id_alredy_used=[]
                for i in skills_string_list:

                    for x in category_string_list: 

                        query_part_1= "SELECT id,email,full_name,profession,rate,description,github,linkedin,instagram,facebook,skills,categories,created_at FROM "+settings.table_name_for_select_all_free_user+" where position( '"+i+"' in LOWER(REPLACE(skills,' ','')))>0  AND position( '"+x+"' in LOWER(REPLACE(categories,' ','')))>0 ORDER by CREATED_AT DESC ;"

                        cursor.execute(query_part_1)
                        talents_part=cursor.fetchall()# LIST OF REALDICROW ELEMENTS
                        
                        try:
                        
                            for x in talents_part:
                                current_id=x.get("id")
                                if current_id not in id_alredy_used:
                                    id_alredy_used.append(current_id)
                                    talents.append(x)
                        
                        except:
                            pass

                
                talents=PAGINATE_A_LIST(talents,pagination_value)

            if magic_word !="None" and skills_string!="None" and category_string != "None":

                magic_word_c ="'"+(magic_word.replace(" ", "")).lower()+"'"
                talents=[]
                id_alredy_used=[]
                for i in skills_string_list:

                    for x in category_string_list: 

                        query_part_1= "SELECT id,email,full_name,profession,rate,description,github,linkedin,instagram,facebook,skills,categories,created_at FROM "+settings.table_name_for_select_all_free_user+" where position( '"+i+"' in LOWER(REPLACE(skills,' ','')))>0  AND position( '"+x+"' in LOWER(REPLACE(categories,' ','')))>0  AND (position("+magic_word_c+" in LOWER(REPLACE(full_name,' ','')))>0  OR position("+magic_word_c+" in LOWER(REPLACE(profession,' ','')))>0 OR position("+magic_word_c+" in LOWER(REPLACE(description,' ','')))>0 ) ORDER by CREATED_AT DESC ;"

                        cursor.execute(query_part_1)
                        talents_part=cursor.fetchall()# LIST OF REALDICROW ELEMENTS
                        
                        try:
                        
                            for x in talents_part:
                                current_id=x.get("id")
                                if current_id not in id_alredy_used:
                                    id_alredy_used.append(current_id)
                                    talents.append(x)
                        
                        except:
                            pass

                
                talents=PAGINATE_A_LIST(talents,pagination_value)


        ###############CRITICAL ERROR MANAGEMENT#################################################
            if not talents :
                    talents=[]
        #####################################################################################################################
            
            Talents_List=[]

            try:
                for  talent in talents:
                    

                    facebook_c=talent.get("facebook")
                    if facebook_c =='None':
                        facebook_c=''

                    instagram_c=talent.get("instagram")
                    if instagram_c =='None':
                        instagram_c =''
            


                    talent_dict={'id':str(talent.get("id")),'email':talent.get("email"),'full_name':talent.get("full_name"),'profession':talent.get("profession"),'rate':str(talent.get("rate")),'description':talent.get("description"),'github':talent.get("github"),'linkedin':talent.get("linkedin"),'instagram':instagram_c,'facebook':facebook_c,'skills':talent.get("skills"),'categories':talent.get("categories")}

                    Talents_List.append(talent_dict)
            except:
                pass


            paginationStateListInt=[eval(i) for i in pagination_state.split(".")]

            context={'categories':Categories_List,'skills':Skills_List,'talents':Talents_List,'skillState':skills_state_string,'categoryState':category_state_string,'magic_word':magic_word,'paginationState':paginationStateListInt,'paginationValue':pagination_value,'login_role':login_role_value}
            conn_contacts.close()
            return templates.TemplateResponse(request=request,name="2_find_talent.html",context=context)
        except:
            pass