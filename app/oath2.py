from fastapi import  status, HTTPException
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from .config import settings
from . import schemas

def create_access_token(data:schemas.createTokenInputTalent | schemas.createTokenInputFirm | schemas.createTokenInputSuperAdmin):
    
    to_encode=dict(data)

    expire = datetime.now() + timedelta(settings.access_token_expire_minutes)

    to_encode.update({"exp":expire})

    encoded_jwt= jwt.encode(to_encode,settings.secret_key,settings.algorithm)
   
    return encoded_jwt

def decode_access_token(token:str):

    try:
        payload=jwt.decode(token,settings.secret_key,settings.algorithm)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "You need to be logged in to use this feature")
    
    if payload.get("role")== 'talent':
        payload_data= schemas.responseTokenInputTalent(talent_id=payload.get("talent_id"),talent_email=payload.get("talent_email"),role=payload.get("role"),exp=payload.get("exp"))

    if payload.get("role")== 'firm':
        payload_data= schemas.responseTokenInputFirm(firm_id=payload.get("firm_id"),firm_email=payload.get("firm_email"),role=payload.get("role"),exp=payload.get("exp"))

    if payload.get("role")== 'superadmin':
        payload_data= schemas.responseTokenInputSuperAdmin(superadmin_id=payload.get("superadmin_id"),superadmin_email=payload.get("superadmin_email"),role=payload.get("role"),exp=payload.get("exp"))

    return payload_data
