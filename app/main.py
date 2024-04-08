from contextlib import asynccontextmanager
from fastapi import FastAPI,status, HTTPException,Cookie,Request
from .routers import contacts, firm, talent,complaints,donations,blacklistemail,blacklistwords,changepassword,auth,tableau,categories,skills
from fastapi.middleware.cors import CORSMiddleware
from .utils import conn_talent_utils
from .routers.talent import conn_talent
from .routers.firm import conn_firm
from .routers.contacts import conn_contacts
from .routers.blacklistemail import conn_blacklistemail
from .routers.blacklistwords import conn_blacklistwords
from .routers.changepassword import conn_changepassword
from .routers.auth import conn_auth
from .routers.complaints import conn_complaints
from .routers.categories import conn_categories
from .routers.skills import conn_skills
from fastapi.staticfiles import StaticFiles
from .config import settings
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import Optional
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    conn_talent_utils.close()
    conn_talent.close()
    conn_firm.close()
    conn_blacklistemail.close()
    conn_blacklistwords.close()
    conn_contacts.close()
    conn_changepassword.close()
    conn_auth.close()
    conn_complaints.close()
    conn_categories.close()
    conn_skills.close()

app= FastAPI(lifespan=lifespan)

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
    

    cursor.execute(""" SELECT * FROM """+settings.table_name_for_select_all_categories+""" """)
    categories=cursor.fetchall()
    if not categories :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "BBDD does not have any record")
    
    
    Categories_List=[]

    for  category in categories:
        category_dict={'category':category.get("category"),'category_key':category.get("category").replace(' ','')}
        Categories_List.append(category_dict)
    
###################################### Talent Cache #######################
        

    if category_string !="None":
        category_string_list=category_string.replace(' ','').lower().split('.')


    context={'request': request, 'categories':Categories_List}
    return templates.TemplateResponse("1_index.html",context)