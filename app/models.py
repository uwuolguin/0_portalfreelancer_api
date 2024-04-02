from sqlalchemy import Column, BigInteger,String,ForeignKey,Float
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base



class talent(Base):    
    __tablename__= "talent"
    id= Column(BigInteger,primary_key=True,autoincrement=True)
    email=Column(String(80),unique=True,nullable=False)
    password= Column(String(1000),nullable=False)#en el frontend esta limitado a 80 caracteres, la bbdd las guarda hasheadas
    picture_directory=Column(String(10000),nullable=False,server_default='directory')
    full_name=Column(String(80),nullable=False)
    profession=Column(String(80),nullable=False)
    rate=Column(BigInteger,nullable=False)
    description=Column(String(860),nullable=False)
    github=Column(String(1000),nullable=False)
    linkedin=Column(String(1000),nullable=False)
    instagram=Column(String(1000),nullable=True)
    facebook=Column(String(1000),nullable=True)
    #skills and categories are going to be words separated by . (dot) 
    skills=Column(String(1000),nullable=False)
    categories=Column(String(1000),nullable=False)
    created_at= Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))
    last_updated_at= Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))
    last_logged_at= Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))

class firm(Base):    
    __tablename__= "firm"
    id= Column(BigInteger,primary_key=True,autoincrement=True)
    email=Column(String(80),unique=True,nullable=False)
    password= Column(String(1000),nullable=False)
    full_name=Column(String(80),nullable=False)
    contact_email=Column(String(80),nullable=False)
    contact_phone=Column(String(80),nullable=False)
    email_template_to_send=Column(String(860),nullable=False)
    linkedin=Column(String(1000),nullable=False)
    instagram=Column(String(1000),nullable=False)
    created_at= Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))
    last_updated_at= Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))
    last_logged_at= Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))



class contacts(Base):
    __tablename__= "contacts"
    talent_id= Column(BigInteger,ForeignKey("user.id",ondelete="CASCADE"),primary_key=True)
    firm_id=Column(BigInteger,ForeignKey("firm.id",ondelete="CASCADE"),primary_key=True) 
    created_at= Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'),primary_key=True)


class donations(Base):    
    __tablename__= "donations"
    id= Column(BigInteger,primary_key=True,autoincrement=True)
    email=Column(String(80),unique=True,nullable=False)
    full_name=Column(String(80),nullable=False)
    amount=Column(Float(),nullable=False)    
    created_at= Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'),primary_key=True)

class complaints(Base):    
    __tablename__= "complaints"
    id= Column(BigInteger,primary_key=True,autoincrement=True)
    email=Column(String(80),unique=True,nullable=False)
    email_sent=Column(String(1000),nullable=False)
    created_at= Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'),primary_key=True)

class black_list_email(Base):    
    __tablename__= "blacklistemail"
    id= Column(BigInteger,primary_key=True,autoincrement=True)
    email=Column(String(80),unique=True,nullable=False)
    created_at= Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'),primary_key=True)

class black_list_words(Base):    #INCLUDES SQL COMMANDS AND RACIAL SLURS
    __tablename__= "blacklistwords"
    id= Column(BigInteger,primary_key=True,autoincrement=True)
    words=Column(String(1000),unique=True,nullable=False)


class change_password(Base):    
    __tablename__= "changepassword"
    id= Column(BigInteger,primary_key=True,autoincrement=True)
    email=Column(String(80),unique=False,nullable=False)
    created_at= Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))
    password= Column(String(1000),nullable=True)
    origin= Column(String(80),nullable=True)

class login_attempt(Base):    
    __tablename__= "loginAttempt"
    id= Column(BigInteger,primary_key=True,autoincrement=True)
    email=Column(String(80),unique=False,nullable=False)
    created_at= Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))

class skill(Base):    
    __tablename__= "skills"
    skill= Column(String(1000),primary_key=True)

class category(Base):    
    __tablename__= "categories"
    category= Column(String(1000),primary_key=True)

class talent_cache_normal(Base):    
    __tablename__= "talent_cache_normal"
    id= Column(BigInteger,primary_key=True)
    email=Column(String(80),nullable=False)
    full_name=Column(String(80),nullable=False)
    profession=Column(String(80),nullable=False)
    rate=Column(BigInteger,nullable=False)
    description=Column(String(860),nullable=False)
    github=Column(String(1000),nullable=False)
    linkedin=Column(String(1000),nullable=False)
    instagram=Column(String(1000),nullable=True)
    facebook=Column(String(1000),nullable=True)
    skills=Column(String(1000),nullable=False)
    categories=Column(String(1000),nullable=False)
    pagination=Column(BigInteger)
    email_login=Column(String(80),primary_key=True)