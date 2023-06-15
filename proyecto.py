# Python
import datetime
from uuid import UUID
from typing import Optional, List
from enum import Enum
# PyDantic
from pydantic import BaseModel, Field, EmailStr, validator
# FastApi
from fastapi import FastAPI, Body, Query, Path, status, Form, Header, Cookie, UploadFile, File, HTTPException
app =  FastAPI()

# Modelos 
class UserBase(BaseModel):
    user_id: UUID = Field(...,alias='id')
    email: EmailStr = Field(...,example="example@gmail.com")

class UserLogin(UserBase):
    password: str = Field(..., min_length=8, max_length=60)
    
class User(UserBase):
    first_name: str = Field(..., min_length=2, max_length=20,example='John')
    last_name: str = Field(...,min_length=2, max_length=20,example='Doe')
    birth_date: Optional[datetime.date] = Field(default=None, example="2005-03-15")
    
    @validator ("birth_date")
    def is_over_18(cls, v):
        today_year = datetime.date.today().year
        delta = today_year - v.year
        
        if delta < 18:
            raise ValueError('Must be over 18!')
        else:
            return v

class Tweets(BaseModel):
    tweet_id: UUID = Field()
    content: str = Field(max_length=256, min_length=1)
    created_at: datetime.datetime = Field(default=datetime.datetime.now())
    created_at: datetime.datetime = Field(default=datetime.datetime.now())
    by: User = Field()
    

@app.get("/")
def home():
    return {"Twitter workig":"succesfull start"}

@app.post('/signup', response_model=User, tags=['Users'],status_code=status.HTTP_201_CREATED, summary='Register a user')
def singup_user(user:User = Body()):
    pass


@app.post('/login', response_model=User, tags=['Users'],status_code=status.HTTP_200_OK, summary='User Login')
def login_user(user:User = Body()):
    pass


@app.get('/users', response_model=List[User], tags=['Users'],status_code=status.HTTP_200_OK, summary='Show all users')
def show_users(user:User = Body()):
    pass


@app.get('/users/{user_id}', response_model=User, tags=['Users'],status_code=status.HTTP_200_OK, summary='Show an specific user')
def show_a_user(user:User = Body()):
    pass


@app.delete('/users/{user_id}/delete', response_model=User, tags=['Users'],status_code=status.HTTP_201_OK, summary='Delete a user')
def delete_user(user:User = Body()):
    pass


@app.put('/users/{user_id}/update', response_model=User, tags=['Users'],status_code=status.HTTP_201_OK, summary='Update a user')
def update_user(user:User = Body()):
    pass
