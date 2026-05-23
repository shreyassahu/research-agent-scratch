from fastapi import FastAPI
from claude import call_claude
from pydantic import BaseModel

class ResearchRequest(BaseModel):
    question: str

app = FastAPI()

@app.post("/research")
async def get_answer(request: ResearchRequest):
    return call_claude(request.question)
