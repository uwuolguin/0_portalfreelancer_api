from fastapi import  status, HTTPException,APIRouter,Form,Cookie,Request
from .. import schemas,oath2
import psycopg2
from psycopg2.extras import RealDictCursor
from ..config import settings
import time
from typing import Any
import os
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates



router= APIRouter(
    
    prefix="/donations",
    tags=["Donations"]
)





################################################# TEMPLATES ####################################################################
    
templates= Jinja2Templates(directory="./templates")

@router.get('/donations_html/',response_class=HTMLResponse)
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


            context={'login_role':login_role_value}
            return templates.TemplateResponse(request=request,name="12_donations.html",context=context)
        except:
            time.sleep(1)
            pass