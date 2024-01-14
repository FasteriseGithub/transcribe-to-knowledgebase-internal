from datetime import date
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.openapi.models import APIKey
import shutil
import os

from openai import AsyncOpenAI
from langchain.text_splitter import CharacterTextSplitter

import logging

import chains
import discord
from pinecone_upload import embed_summary, embed_timed_transcript
from types_internal import MeetingTypeEnum, MetaData

API_KEY_INTERNAL = os.getenv("API_KEY_INTERNAL")
API_KEY_NAME = "access_token"
API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME, auto_error=True)
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

logging.basicConfig(filename='/home/app/logs/print.log', level=logging.INFO, format='%(asctime)s - %(message)s')

app = FastAPI()
client = AsyncOpenAI()

@app.get("/ping")
async def ping():
    return "pong"

async def get_api_key(api_key_header: str = Security(API_KEY_HEADER)):
    if api_key_header == API_KEY_INTERNAL:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

@app.post("/replace-with-your-uuid")
async def upload_file(meeting_type: MeetingTypeEnum, meeting_date: date,file: UploadFile = File(...), api_key: APIKey = Depends(get_api_key)):
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

    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=233, chunk_overlap=0
    )
    
    chunks = text_splitter.split_text(analysis)
    await discord.post_to_discord_webhook_async(DISCORD_WEBHOOK_URL, f"## {meeting_type} Meeting \n {meeting_date}")
    for chunk in chunks:
        await discord.post_to_discord_webhook_async(DISCORD_WEBHOOK_URL, chunk)

    metadata = {
            "date": meeting_date,
            "meeting_type": meeting_type,
            "summary": True
    }

    metadata = MetaData(**metadata)
    await embed_summary(analysis, metadata )
    metadata.summary = False
    await embed_timed_transcript(corrected_chunks, metadata)

    return {"response": "OK"}
    
@app.get("/test-hook")
async def test_hook():
    await discord.post_to_discord_webhook_async(DISCORD_WEBHOOK_URL, "test")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
