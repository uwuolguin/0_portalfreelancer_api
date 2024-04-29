from fastapi import  APIRouter,Cookie,Request
from .. import oath2
import time
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..utils import testTableau

templates= Jinja2Templates(directory="./templates")

router= APIRouter(
    
    prefix="/tableau",
    tags=["Tableau"]
)


@router.get('/tableau_html_panel/',response_class=HTMLResponse)
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

            if login_role_value=="superadmin":

                context={'request': request}
                return templates.TemplateResponse("14_tableau.html",context)
            else:
                                
                context={'request': request}
                return templates.TemplateResponse("4_log_in.html",context)
        except:
            time.sleep(1)
            pass

@router.get('/tableau_html_test/')
def complaints_html():

    testTableau()

    return 'test'