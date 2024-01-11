import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.openapi.models import APIKey
import shutil
import os
from openai import AsyncOpenAI

from langchain.text_splitter import CharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

import logging

import helpers

API_KEY = "your_actual_api_key"
API_KEY_NAME = "access_token"
API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

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

    return {"transcription": transcript}

async def transcript_remove_unnecessary_information(vtt_transcription: str):
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=987, chunk_overlap=0
    )
    
    chunks = text_splitter.split_text(vtt_transcription)
    print(type(chunks))
    
    corrected_chunks = []
    chunks_banter_for_testing = []
    for chunk in chunks:
        prompt = ChatPromptTemplate.from_template("You are a part of a transcript to knowledge base system for an AI automation development agency. You will help clean up the transcripts of meetings \n\n The following is a chunk of a transcript, assess if it contains a greeting, a personal catchup, or banter: \n\n {chunk} \n\n indicate your assessment by outputting a blob that says YES if it does, NO if it doesn't or PARTIAL if parts of it do")
        model = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
        output_parser = StrOutputParser()

        chain = prompt | model | output_parser
        
        res = await chain.ainvoke({"chunk": chunk})

        cleaned = helpers.detect_string(res)

        if cleaned == "NO":
            corrected_chunks.append(chunk)
        elif cleaned == "YES":
            chunks_banter_for_testing.append(chunk)
        elif cleaned == "PARTIAL":
            corrected_chunks.append(await clean_part_of_chunk(chunk))
        elif cleaned == "UNKNOWN":
            print(f"FATAL ERROR on chunk: {chunk} with output: {res}")
        
async def clean_part_of_chunk(chunk: str) -> str:
    prompt = ChatPromptTemplate.from_template("You are a part of a transcript to knowledge base system for an AI automation development agency. You will help clean up the transcripts of meetings \n\n The following is a chunk of a transcript where a previous part of the system has detected a greeting, a personal catchup, or banter: \n\n {chunk} \n\n remove the lines that have a greeting, a personal catchup or banter. Keep the rest of the chunk in its original form")
    model = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser
        
    res = await chain.ainvoke({"chunk": chunk})

    return res
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
