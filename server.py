from fastapi import FastAPI
from pydantic import BaseModel
from api import AutomationAPI

app = FastAPI()
automation_api = AutomationAPI()

class UserRequest(BaseModel):
    text: str

@app.post("/generate")
def generate_message(request: UserRequest):
    result = automation_api.generate_system_message(request.text)
    return result

@app.get("/")
def root():
    return {"message": "Automation Prompt API Running"}
