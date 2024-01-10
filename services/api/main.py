import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.openapi.models import APIKey

from typing import Any
from pydantic import BaseModel

import logging

from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_structured_chat_agent

from toolset.empty_tool import EmptyTool

API_KEY = "your_actual_api_key"
API_KEY_NAME = "access_token"
API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

logging.basicConfig(filename='/home/app/logs/print.log', level=logging.INFO, format='%(asctime)s - %(message)s')

app = FastAPI()

@app.get("/ping")
async def ping():
    return "pong"

async def get_api_key(api_key_header: str = Security(API_KEY_HEADER)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), api_key: APIKey = Depends(get_api_key)):
    # Your file handling logic here
    return {"filename": file.filename}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
