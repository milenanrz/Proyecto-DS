from pydantic import BaseModel, Field
#from typing import Optional

class Photographer(BaseModel):
    name:str = Field(..., min_length=3, max_length=20)
    condition:bool = Field(...)

class PhotographerWithId(Photographer):
    id:int

class PhotographicStyle(BaseModel):
    style:str = Field(min_length=3, max_length=20)

class StyleWithId(PhotographicStyle):
    id:int

