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



#<script data-name="BMC-Widget" data-cfasync="false" src="https://cdnjs.buymeacoffee.com/1.0.0/widget.prod.min.js" data-id="uwuolguin" data-description="Support me on Buy me a coffee!" data-message="Thanks for visiting. I hope you found the App and Documentation Useful" data-color="#BD5FFF" data-position="Right" data-x_margin="18" data-y_margin="18"></script>

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
                pass


            context={'request': request,'login_role':login_role_value}
            return templates.TemplateResponse("12_donations.html",context)
        except:
            time.sleep(1)
            pass