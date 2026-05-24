from fastapi import FastAPI
from claude import call_claude
from pydantic import BaseModel
from fastapi.responses import JSONResponse

class ResearchRequest(BaseModel):
    question: str

app = FastAPI()

@app.post("/research")
async def get_answer(request: ResearchRequest):
    response = await call_claude(request.question)
    if "answer" in response.keys():
        return JSONResponse(status_code=200, content=response)
    else:
        return JSONResponse(status_code=500, content=response)
    
