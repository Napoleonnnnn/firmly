from pydantic import BaseModel

class IdentifyResponse(BaseModel):
    component_name:str
    confidence:float
    package_type:str
    message:str