from pydantic import BaseModel, Field

class Photographer(BaseModel):
    name:str = Field(min_length=3, max_length=20)
    state:bool = Field()

class PhotographerWithId(Photographer):
    id:int

class PhotographicStyle(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    style_name:str = Field(min_length=3, max_length=20)

class StyleWithId(PhotographicStyle):
    id:int

