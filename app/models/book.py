from typing import Union
from pydantic import BaseModel


class Book(BaseModel):
    url : str

class BookResponse(BaseModel):
    url : str
    title : str
    author : str
    editorial : str
    price : str
    cover : str
    description : str
    

