from pydantic import BaseModel, Field
from typing import Optional

class Fotografo(BaseModel):
    name:str = Field(min_length=3, max_length=20)
    estado:bool = Field()

class EstiloFotografico(BaseModel):
    estilo:str = Field(min_length=3, max_length=20)

class FotografoWithId(Fotografo):
    id:int

class EstiloWithId(EstiloFotografico):
    id:int

