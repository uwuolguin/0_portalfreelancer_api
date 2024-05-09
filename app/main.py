from fastapi import FastAPI,status, HTTPException,Cookie,Request
from .routers import contacts, firm, talent,complaints,donations,blacklistemail,blacklistwords,changepassword,auth,tableau,categories,skills
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import Optional
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from . import oath2



app= FastAPI()

origins = ["https://apiportalfreelancer.lat/","https://10ax.online.tableau.com/"
]
# origins = ["*"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(changepassword.router)
app.include_router(contacts.router)
app.include_router(talent.router)
app.include_router(firm.router)
app.include_router(donations.router)
app.include_router(complaints.router)
app.include_router(blacklistemail.router)
app.include_router(blacklistwords.router)
app.include_router(auth.router)
app.include_router(tableau.router)
app.include_router(categories.router)
app.include_router(skills.router)
app.mount("/static", StaticFiles(directory=settings.picture_directory), name="static")


templates= Jinja2Templates(directory="./templates")

@app.get('/',response_class=HTMLResponse)
def root(  request: Request,
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

            conn=psycopg2.connect(host=settings.database_hostname,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
            cursor=conn.cursor()
            break

        except Exception as error:

            print("Connecting to database failed")
            print("Error:",error)
            time.sleep(5)


    while True:
        try:
            login_role_value="None"
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

            cursor.execute(""" select * from categories where category <>'Other';""")
            categories=cursor.fetchall()
            if not categories :
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BBDD does not have any record")
            
            
            conn.close()


            Categories_List=[]

            for  category in categories:

                url="https://apiportalfreelancer.lat/contacts/contacts_normal/?skills_string=None&skills_state_string=None&category_string="+category.get("category").replace(' ','')+"&category_state_string="+category.get("category").replace(' ','')+"-category&pagination_state=1.2.3.4.5.6.7.8.9.10&pagination_value=1&magic_word=None"

                category_dict={'category':category.get("category"),'category_key':category.get("category").replace(' ',''),'url':url}
                Categories_List.append(category_dict)

            context={ 'categories':Categories_List,'login_role':login_role_value}

            return templates.TemplateResponse(request=request,name="1_index.html",context=context)
        except:
            time.sleep(1)
            pass        

@app.get('/purpose_html/',response_class=HTMLResponse)
def complaints_html(request: Request,login: str = Cookie(None)):

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


            context={'request': request,'login_role':login_role_value}
            return templates.TemplateResponse("13_Purpose.html",context)
        except:
            time.sleep(1)
            pass