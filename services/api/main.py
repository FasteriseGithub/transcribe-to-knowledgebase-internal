import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.openapi.models import APIKey
import shutil
import os
from openai import AsyncOpenAI

import logging

import chains
import discord

API_KEY = "your_actual_api_key"
API_KEY_NAME = "access_token"
API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME, auto_error=True)
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

SUPPORTED_AUDIO_TYPES = [
    "audio/flac", "audio/m4a", "audio/mp3", "video/mp4", "audio/mpeg", 
    "audio/mpga", "audio/oga", "audio/ogg", "audio/wav", "audio/webm"
]

logging.basicConfig(filename='/home/app/logs/print.log', level=logging.INFO, format='%(asctime)s - %(message)s')

app = FastAPI()
client = AsyncOpenAI()

@app.get("/ping")
async def ping():
    return "pong"

async def get_api_key(api_key_header: str = Security(API_KEY_HEADER)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), api_key: APIKey = Depends(get_api_key)):
    print(f"Detected MIME type: {file.content_type}")

    if file.content_type not in SUPPORTED_AUDIO_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    temp_file_path = f"temp_{file.filename}"

    with open(temp_file_path, 'wb') as temp_file:
        shutil.copyfileobj(file.file, temp_file)

    try:
        transcript = await client.audio.transcriptions.create(
            model="whisper-1", 
            file=open(temp_file_path, 'rb'),
            response_format="vtt"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await file.close()
        os.remove(temp_file_path)    

    corrected_chunks = await chains.transcript_remove_unnecessary_information(transcript)

    joined_chunks = "\n".join(corrected_chunks)

    analysis = await chains.critical_conversation_analysis(joined_chunks)

    return {"corrected_chunks": corrected_chunks}
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
