from contextlib import asynccontextmanager
from fastapi import FastAPI 
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
#PROBLEMAS DE CONTRASEÑA EL SERVIDOR LO ARREGLA Y POR GMAIL TE MANDA BOTON QUE TE CAMBIA LA PASSWORD Y LUEGO TE MANDA DENUEVO UN CORREO PERO CON LA PASSWORD QUE CREO
#
#En el front end, solo por si acaso, le voy a meter un html injection, aca por defecto ya se genera



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

origins = ["*"
#add the domain of the front end server when its complete
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

@app.get("/")
async def root():
    return {"message": "Hello World"}


