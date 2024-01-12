import pinecone
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone
from types_internal import MetaData

INDEX_NAME = "transcription-api"
NAMESPACE_INTERNAL = "internal"
NAMESPACE_DISCOVERY_CALLS = "discovery"

embeddings = OpenAIEmbeddings()

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
    environment=os.getenv("PINECONE_ENV"),  # next to api key in console
)

async def embed_timed_transcript(transcript_chunked: list[str], metadata: MetaData):
    vectorstore = await create_index_if_not_exists(NAMESPACE_INTERNAL)
    meta_dict = metadata.model_dump()

    await vectorstore.aadd_texts(transcript_chunked, meta_dict)

async def embed_summary(summary: str, metadata: MetaData):
    vectorstore = await create_index_if_not_exists(NAMESPACE_INTERNAL)

async def create_index_if_not_exists(namespace: str) -> Pinecone:
    if INDEX_NAME not in pinecone.list_indexes():
        pinecone.create_index(name=INDEX_NAME, metric="cosine", dimension=1536)

    index = pinecone.Index(INDEX_NAME)
    vectorstore = Pinecone(index, embeddings, namespace)

    return vectorstore
