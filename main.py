# Python
from typing import Optional
from enum import Enum
# PyDantic
from pydantic import BaseModel, Field, EmailStr
# FastApi
from fastapi import FastAPI, Body, Query, Path, status, Form, Header, Cookie, UploadFile, File, HTTPException

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    blonde = "blonde"
    red = "red"
    black = "black"

class Location(BaseModel):
    
    city: str = Field(...)
    state: str = Field(...)
    country: str = Field(...)
    
    class Config():
        
        schema_extra = {
            'example' : {
                'city': "Yare",
                'state': 'Miranda',
                'country': 'Venezuela'
            }
        }
        
class PersonBase(BaseModel):
    firts_name: str = Field(min_length=3, max_length=50,)
    last_name: str = Field(...,min_length=3, max_length=50)
    age: int = Field(gt = 1, lt = 100)
    hair_color: Optional[HairColor] = Field(default = None)
    is_married: Optional[bool] = Field(default = None)
    
    # class Config():
        
    #     schema_extra = {
    #         'example' : {
    #             'firts_name': "Alejandro",
    #             'last_name': 'Villamizar Lara',
    #             'age': 18,
    #             'hair_color': 'brown',
    #             'is_married': False,
    #             # 'password': 'passwordexample'
    #         }
    #     }
                
class Person(PersonBase):
    password: str = Field(..., min_length = 8)
    
    # class Config():
        
    #     schema_extra = {
    #         'example' : {
    #             'password': 'passwordexample'
    #         }}
    
class PersonOut(PersonBase):
    
    ...
    
class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example='alejandro998')
    message: str = Field(default="loggin succesfully")
    
    
@app.get('/', status_code=status.HTTP_200_OK, tags=["home"])
def home():
    return{'hello':'world'}     

# Request and Response body

@app.post('/person/new', response_model=PersonOut, status_code=status.HTTP_201_CREATED, tags=["persons"])
def create_person(person: Person = Body(...)):
    return person

# Validacion Query params
 
@app.get('/person/detail', status_code=status.HTTP_200_OK, tags=["persons"], deprecated = True)
def get_detail(
    name: Optional[str] = Query(
        None,
        min_length=3,
        max_length=50,
        title = "Person Name",
        description = "this is the person name. it's between 1 and 50 characters"
        ),
    age: int = Query(
        ...,
        title = "Person Age",
        description = "This is the person age, is REQUIRED"
        )
):
    """
    Get details: this function recives an age and a name and returns it in a JSON 

    Args:
        name (Optional[str]): _description_. Defaults to Query( None, min_length=3, max_length=50, title = "Person Name", description = "this is the person name. it's between 1 and 50 characters" ).
        age (int): _description_. Defaults to Query( ..., title = "Person Age", description = "This is the person age, is REQUIRED" ).

    Returns:
        _type_: _description_
    """
    return {name:age}    

# Validacion path parameters 

persons = [ 1, 2, 3, 4, 5]

@app.get('/person/detail/{person_id}',status_code=status.HTTP_200_OK,  tags=["persons"])
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title = "Person ID",
        description = "The ID of the person whose details you wanna display",
        example= 99
        )
):
    if person_id not in persons:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "This person doesn't exits")
    else:
        return {person_id: 'it exits'}

# validation request body

@app.put("/person/{person_id}",status_code=status.HTTP_202_ACCEPTED,  tags=["persons"])
def update_person(
    person_id: int = Path(
        ...,
        title = 'Person_id',
        description = "This is the person id",
        gt = 0 
    ),
    person: Person = Body(...),
    location: Location = Body(...)  
                ):
    result = dict(person)
    result.update(dict(location))
    return result

#forms

@app.post("/login",status_code=status.HTTP_200_OK, response_model=LoginOut, tags=["login"])
def login(username:str =  Form(...), password: str = Form(...)):
    return LoginOut(username=username)

# cookies and headers

@app.post('/contact', status_code = status.HTTP_200_OK, tags=["contact"])
def contact(firts_name: str = Form(max_length=20,min_length=3), 
            last_name: str = Form(max_length=20,min_length=3), 
            email: EmailStr = Form(),
            message: str = Form(min_length=20),
            user_agent: Optional[str] = Header(default=None),
            ads: Optional[str] = Cookie(default=None)):
    
    return user_agent

#files

@app.post("/post-image", tags=["post"])
def post_image(image: UploadFile = File()):
    return {
        "filename":image.filename,
        "format": image.content_type,
        "size(kb)": round(len(image.file.read())/1024,2)
    }