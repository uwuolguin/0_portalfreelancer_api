from fastapi import  status, HTTPException, Depends, APIRouter
from .. import models,schemas,utils
from ..database import get_db
from sqlalchemy.orm import Session
router= APIRouter(
    
    prefix="/donations",
    tags=["Donations"]
)

@router.get("/")
async def root():
    return {"message": "Hello World"}

#<script data-name="BMC-Widget" data-cfasync="false" src="https://cdnjs.buymeacoffee.com/1.0.0/widget.prod.min.js" data-id="uwuolguin" data-description="Support me on Buy me a coffee!" data-message="Thanks for visiting. I hope you found the App and Documentation Useful" data-color="#BD5FFF" data-position="Right" data-x_margin="18" data-y_margin="18"></script>

################################################# TEMPLATES ####################################################################
    
# templates= Jinja2Templates(directory="./templates")

# @router.get('/complaints_html/',response_class=HTMLResponse)
# def complaints_html(request: Request,login: str = Cookie(None)):

#     while True:
#         try:

#             if login==None:
#                     context={'request': request}
#                     return templates.TemplateResponse("4_log_in_complaints.html",context)
#             try:
#                 credentials=oath2.decode_access_token(login)

#                 if dict(credentials).get("role") == "superadmin":
#                     login_role_value="superadmin"
#                 elif dict(credentials).get("role") == "firm":
#                     login_role_value="firm"
#                 else:
#                     login_role_value="talent"


#             except:
#                 pass


#             context={'request': request,'login_role':login_role_value}
#             return templates.TemplateResponse("11_complaints.html",context)
#         except:
#             time.sleep(1)
#             pass