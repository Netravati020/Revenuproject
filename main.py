
from fastapi import APIRouter, status, Depends, HTTPException, FastAPI, Request
from passlib.context import CryptContext
from datetime import datetime, timedelta

from database import engine, SessionLocal,Base
from sqlalchemy.orm import Session
import models
import schema
import hashing
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

models.Base.metadata.create_all(bind=engine)

app=FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(data, credentials_exception)

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/user', tags=['Userlogin'])
def create_user(request: schema.User, db:Session=Depends(get_db)):

    new_user= models.User( Name=request.Name,email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", tags=['Authentication'],response_model=schema.Token)
async def login_access(request:OAuth2PasswordRequestForm= Depends(),db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect username or password")

    # if not hashing.Hash.verify(user.password, request.password):
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Incorrect  password")

    access_token = create_access_token(data={"sub": user.email})
    return  {"access_token": access_token, "token_type": "bearer"}

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schema.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    return verify_token()



# revenue api
@app.post('/', tags=['Revenue'])
def create(info:Request, req:schema.Access, db:Session=Depends(get_db),current_user: schema.User=Depends(get_current_user)):
    # items_list: await info.json()
    reven= db.execute("SELECT revenue_target.`sno`,revenue_target.`branch`, (target), round(((`adm_revenue`.`total_net_revenue`/1000000)),2), round(((`adm_revenue`.`total_net_revenue`)/((`revenue_target`.`target`)*10000000)*1000),2),revenue_target.`clustername`, (status) FROM `revenue_target` INNER JOIN `adm_revenue` ON `adm_revenue`.`branch` = `revenue_target`.`branch` WHERE DATE(`adm_revenue`.`rdate`)='2022/07/21'GROUP BY `revenue_target`.`branch` ORDER BY (`revenue_target`.`sno`)")

    response=({"message":"successful","data":[]})

    for x in reven:
        response['data'].append({'sno':x[0], 'branch':x[1], 'target':x[2],'Achieved':x[3],'Achieved_percentage':x[4], 'clustername':x[5], 'status':x[6]})


    return response







