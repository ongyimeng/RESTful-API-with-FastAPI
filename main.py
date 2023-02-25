import models
from fastapi import FastAPI, Depends, HTTPException, status
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Union, Optional
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing_extensions import Literal


SECRET_KEY = "881E8D37B7486DD879DFCDC1379D6"
ALGORITHM = "HS256"

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class User(BaseModel):
    email: str
    password: str
    role: Literal["ADMIN", "MEMBER", "TECHNICIAN"]
    firstName: str
    lastName: str
    company: Union[str, None] = None
    designation: Union[str, None] = None


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(password, hashed_password):
    return bcrypt_context.verify(password, hashed_password)


def authenticate_user(email: str, password: str, db):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(email: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {"sub": email, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("id")
        if email is None or user_id is None:
            raise HTTPException(status_code=400, detail="User not found")
        return {"email": email, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=400, detail="User not found")

# for testing purposes
@app.get("/")
async def all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.get("/info")
async def get_user_info(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user is None:
        raise_bad_request()
    user_model = db.query(models.User).filter(models.User.email == current_user.get("email")).first()
    if user_model is None:
        raise_bad_request()
    return {"firstName": user_model.firstName,
            "lastName": user_model.lastName,
            "email": user_model.email,
            "role": user_model.role,
            "company": user_model.company,
            "designation": user_model.designation}


@app.post("/register")
async def register(user: User, db: Session = Depends(get_db)):
    user_model = models.User()
    user_model.email = user.email

    hash_password = get_password_hash(user.password)

    user_model.password = hash_password
    user_model.firstName = user.firstName
    user_model.lastName = user.lastName
    user_model.company = user.company
    user_model.designation = user.designation
    user_model.role = user.role

    db.add(user_model)
    db.commit()
    return "register success"


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    token_expires = timedelta(minutes=30)
    token = create_access_token(user.email, user.id, expires_delta=token_expires)
    return {"token": token}


@app.put("/update")
async def update_user_info(user: User, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user is None:
        raise_bad_request()

    user_model = db.query(models.User).filter(models.User.email == current_user.get("email")).first()

    if user_model is None:
        raise_bad_request()

    user_model.email = user.email

    hash_password = get_password_hash(user.password)

    user_model.password = hash_password
    user_model.firstName = user.firstName
    user_model.lastName = user.lastName
    user_model.company = user.company
    user_model.designation = user.designation
    user_model.role = user.role

    db.add(user_model)
    db.commit()
    return "update success"


@app.delete("/delete")
async def delete_user_info(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user is None:
        raise_bad_request()

    user_model = db.query(models.User).filter(models.User.email == current_user.get("email")).first()

    if user_model is None:
        raise_bad_request()

    db.query(models.User).filter(models.User.email == current_user.get("email")).delete()
    db.commit()
    return "delete success"


def raise_bad_request():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)