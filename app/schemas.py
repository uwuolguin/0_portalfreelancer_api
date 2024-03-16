from datetime import datetime
from pydantic import BaseModel, Field,UrlConstraints
from typing_extensions import Annotated
from pydantic.networks import EmailStr,Url
from fastapi import  Form

from pydantic.functional_validators import BeforeValidator

####################  Before / After Validation ##############################

email_html=Annotated[EmailStr,Form()]

def check_facebook(fb: str) -> str:
    assert str(fb).startswith('https://facebook.com') or str(fb) == 'None', f'{fb} is not a facebook url'
    return fb
def check_instagram(insta: str) -> str:
    assert str(insta).startswith('https://instagram.com')or str(insta) == 'None', f'{insta} is not a instagram url'
    return insta

def check_long_str_80(text: str) -> str:
    assert len(text)>=1 and len(text)<=80, f'{text} this text input should be more than 0 and less than 81 long'
    return text

def check_long_str_860(text: str) -> str:
    assert len(text)>=1 and len(text)<=860, f'{text} this text input should be more than 0 and less than 861 long'
    return text

def check_long_str_1000(text: str) -> str:
    assert len(text)>=1 and len(text)<=1000, f'{text} this text input should be more than 0 and less than 1001 long'
    return text

def check_long_int_10000(rate: str) -> str:
    assert int(rate)>=1 and int(rate )<=10000, f'{rate} rate has to be more than 0 but less than 10000 (us/hr)'
    return rate
###################################     IN AND OUT SCHEMAS                  ###########################################################################


class talentResponse(BaseModel):
    email: Annotated[EmailStr, Field(min_length=5,max_length=80)]
    full_name:Annotated[str, Field(min_length=1,max_length=80)]
    profession:Annotated[str, Field(min_length=1,max_length=80)]
    rate:Annotated[int, Field(ge=1,lt=10000)]
    description:Annotated[str, Field(min_length=1,max_length=860)]
    github: Annotated[Url,UrlConstraints(max_length=1000, allowed_schemes=["https"]),]
    linkedin:Annotated[Url,UrlConstraints(max_length=1000, allowed_schemes=["https"]),]
    skills:Annotated[str, Field(min_length=1,max_length=1000)]
    categories:Annotated[str,Field(min_length=1,max_length=1000)]
    facebook:Annotated[str,BeforeValidator(check_facebook)]
    instagram:Annotated[str,BeforeValidator(check_instagram)]
    created_at:datetime
    last_updated_at:datetime
    last_logged_at:datetime

class talentResponse3(BaseModel):
    talent_id: Annotated[int, Field(ge=1)]

class talentResponse4(BaseModel):
    talent_email: Annotated[EmailStr, Field(min_length=5,max_length=80)]
    talent_full_name:Annotated[str, Field(min_length=1,max_length=80)]
    talent_profession:Annotated[str, Field(min_length=1,max_length=80)]
    talent_rate:Annotated[int, Field(ge=1,lt=10000)]
    talent_description:Annotated[str, Field(min_length=1,max_length=860)]
    talent_github: Annotated[Url,UrlConstraints(max_length=1000, allowed_schemes=["https"]),]
    talent_linkedin:Annotated[Url,UrlConstraints(max_length=1000, allowed_schemes=["https"]),]
    talent_skills:Annotated[str, Field(min_length=1,max_length=1000)]
    talent_categories:Annotated[str,Field(min_length=1,max_length=1000)]
    talent_facebook:Annotated[str,BeforeValidator(check_facebook)]
    talent_instagram:Annotated[str,BeforeValidator(check_instagram)]
    talent_created_at:datetime
    talent_last_updated_at:datetime
    talent_last_logged_at:datetime

class blacklistemailResponse(BaseModel):
        email: Annotated[EmailStr, Field(min_length=5,max_length=80)]

class blacklistwordsResponse(BaseModel):
        words: Annotated[str, Field(min_length=1,max_length=1000)]

class firmResponse(BaseModel):

    email: Annotated[EmailStr, Field(min_length=5,max_length=80)]
    full_name:Annotated[str, Field(min_length=1,max_length=80)]
    contact_email:  Annotated[EmailStr, Field(min_length=5,max_length=80)]
    contact_phone: Annotated[int, Field(ge=1)]
    email_template_to_send:Annotated[str, Field(min_length=1,max_length=860)]
    linkedin:Annotated[Url,UrlConstraints(max_length=1000, allowed_schemes=["https"]),]
    instagram:Annotated[str,BeforeValidator(check_instagram)]
    created_at:datetime
    last_updated_at:datetime
    last_logged_at:datetime

class firmResponse3(BaseModel):
    firm_id: Annotated[int, Field(ge=1)]

class firmResponse4(BaseModel):
    firm_email: Annotated[EmailStr, Field(min_length=5,max_length=80)]
    firm_full_name:Annotated[str, Field(min_length=1,max_length=80)]
    firm_contact_email:  Annotated[EmailStr, Field(min_length=5,max_length=80)]
    firm_contact_phone: Annotated[int, Field(ge=1)]
    firm_email_template_to_send:Annotated[str, Field(min_length=1,max_length=860)]
    firm_linkedin:Annotated[Url,UrlConstraints(max_length=1000, allowed_schemes=["https"]),]
    firm_instagram:Annotated[str,BeforeValidator(check_instagram)]
    firm_created_at:datetime
    firm_last_updated_at:datetime
    firm_last_logged_at:datetime


class contactResponse(BaseModel):
    talent_id:Annotated[int, Field(ge=1)]
    firm_id:Annotated[int, Field(ge=1)]
    created_at:datetime

class contactResponse4(BaseModel):

    contacts_talent_id:Annotated[int, Field(ge=1)]
    contacts_firm_id:Annotated[int, Field(ge=1)]
    contacts_created_at:datetime


class createTokenInputTalent(BaseModel):

  talent_id: Annotated[int, Field(ge=1)]
  talent_email:EmailStr
  role: str
class createTokenInputFirm(BaseModel):

  firm_id: Annotated[int, Field(ge=1)]
  firm_email:EmailStr
  role: str

class createTokenInputSuperAdmin(BaseModel):
  
  superadmin_id: Annotated[int, Field(ge=1)]
  superadmin_email:EmailStr
  role: str


class responseTokenInputTalent(BaseModel):

  talent_id: Annotated[int, Field(ge=1)]
  talent_email:EmailStr
  role: str
  exp:Annotated[int, Field(ge=1)]

class responseTokenInputFirm(BaseModel):

  firm_id: Annotated[int, Field(ge=1)]
  firm_email:EmailStr
  role: str
  exp:Annotated[int, Field(ge=1)]

class responseTokenInputSuperAdmin(BaseModel):

  superadmin_id: Annotated[int, Field(ge=1)]
  superadmin_email:EmailStr
  role: str
  exp:Annotated[int, Field(ge=1)]

class complaintResponse(BaseModel):

    email: Annotated[EmailStr, Field(min_length=5,max_length=80)]
    email_sent:Annotated[str, Field(min_length=1,max_length=1000)]
    created_at:datetime

class categoryResponse(BaseModel):
    category:Annotated[str, Field(min_length=1,max_length=1000)]

class skillResponse(BaseModel):
    skill:Annotated[str, Field(min_length=1,max_length=1000)]
