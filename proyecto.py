# Python
import json
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

class User(BaseModel):
    user_id: UUID = Field(...,alias='id')
    email: EmailStr = Field(...,example="example@gmail.com")
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


class UserLogin(User):
    password: str = Field(..., min_length=8, max_length=60)
    

class Tweets(BaseModel):
    tweet_id: UUID = Field()
    content: str = Field(max_length=256, min_length=1)
    created_at: datetime.datetime = Field(default=datetime.datetime.now())
    created_at: datetime.datetime = Field(default=datetime.datetime.now())
    by: User = Field()
    

@app.get("/",response_model=List[Tweets],tags=['tweets'],status_code=status.HTTP_200_OK,summary="Show all tweets")
def home():
    return {"Twitter workig":"succesfull start"}

@app.post('/signup', response_model=User, tags=['Users'],status_code=status.HTTP_201_CREATED, summary='Register a user')
def singup_user(user:UserLogin = Body()):
    """
    Signup
    
    This path operations register an user in the app

    Args:
        user (UserLogin): An UserLogin object that contains an user_id, email, firts_name, last_name, password and a birth_Date
        
    returns:
        An User object that containst al the previus elements except the password
    """
    with open('users.json', 'r+', encoding='utf-8') as file:
        results = json.load(file)
        new_user = user.dict()
        new_user["user_id"] = str(new_user["user_id"])
        new_user["birth_date"] = str(new_user["birth_date"])
        results.append(new_user)
        file.seek(0)
        json.dump(results, file, indent=4, ensure_ascii=False)
        
    return user

@app.post('/login', response_model=User, tags=['Users'],status_code=status.HTTP_200_OK, summary='User Login')
def login_user(user:User = Body()):
    pass


@app.get('/users', response_model=List[User], tags=['Users'],status_code=status.HTTP_200_OK, summary='Show all users')
def show_users(user:User = Body()):
    pass


@app.get('/users/{user_id}', response_model=User, tags=['Users'],status_code=status.HTTP_200_OK, summary='Show an specific user')
def show_a_user(user:User = Body()):
    pass


@app.delete('/users/{user_id}/delete', response_model=User, tags=['Users'],status_code=status.HTTP_200_OK, summary='Delete a user')
def delete_user(user:User = Body()):
    pass


@app.put('/users/{user_id}/update', response_model=User, tags=['Users'],status_code=status.HTTP_200_OK, summary='Update a user')
def update_user(user:User = Body()):
    pass

@app.post("/post",response_model=Tweets,status_code=status.HTTP_201_CREATED,tags=['tweets'],summary="Create a tweet")
def post_a_tweet():
    pass

@app.get("/tweets/{tweet_id}",response_model=Tweets,status_code=status.HTTP_200_OK,tags=['tweets'],summary="Show a tweet")
def show_a_tweet():
    pass

@app.delete("/tweets/{tweet_id}/delete",response_model=Tweets,status_code=status.HTTP_200_OK,tags=['tweets'],summary="Delete a tweet")
def delete_a_tweet():
    pass

@app.put("/tweets/{tweet_id}/update",response_model=Tweets,status_code=status.HTTP_200_OK,tags=['tweets'],summary="Update a tweet")
def update_a_tweet():
    pass