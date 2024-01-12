import pinecone
import os
from langchain_openai import OpenAIEmbeddings
from types_internal import MetaData

embeddings = OpenAIEmbeddings

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
    environment=os.getenv("PINECONE_ENV"),  # next to api key in console
)

index_name = "langchain-demo"

async def embed_timed_transcript(transcript_chunked: list[str], metadata: MetaData):
    pass

async def embed_summary(summary: str, metadata: MetaData):
    pass

async def create_index(index_name: str)
    pass
