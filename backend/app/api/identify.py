from fastapi import APIRouter, UploadFile, File
from app.models.component import IdentifyResponse

router = APIRouter()

@router.post("/identify",response_model=IdentifyResponse)
async def identify_component(file:UploadFile = File(...)):
    #dummy response
    return IdentifyResponse(
        component_name="ESP32",
        confidence=0.95,
        package_type="Module",
        message="component identified succesfully"
    )