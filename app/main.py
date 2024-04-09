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

origins = ["https://apiportalfreelancer.lat/"
]

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
    

    try:
        conn.close()
    except:
        pass

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
                else:
                    login_role_value="not_superadmin"
                
                id_firm=dict(credentials).get("firm_id")

            except:
                pass

            cursor.execute(""" SELECT * FROM """+settings.table_name_for_select_all_categories+""" """)
            categories=cursor.fetchall()
            if not categories :
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BBDD does not have any record")
            
            
            conn.close()


            Categories_List=[]

            for  category in categories:
                category_dict={'category':category.get("category"),'category_key':category.get("category").replace(' ','')}
                Categories_List.append(category_dict)

            context={'request': request, 'categories':Categories_List,'login_role':login_role_value}

            return templates.TemplateResponse("1_index.html",context)
        
        except:

            time.sleep(1)

            
            try:
                conn.close()
            except:
                pass

            return RedirectResponse("https://apiportalfreelancer.lat/")
