from langchain.text_splitter import CharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

import helpers

async def transcript_remove_unnecessary_information(vtt_transcription: str) -> list[str]:
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=377, chunk_overlap=0
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

    print(corrected_chunks)
    print(chunks_banter_for_testing)
    return corrected_chunks
        
async def clean_part_of_chunk(chunk: str) -> str:
    prompt = ChatPromptTemplate.from_template("You are a part of a transcript to knowledge base system for an AI automation development agency. You will help clean up the transcripts of meetings \n\n The following is a chunk of a transcript where a previous part of the system has detected a greeting, a personal catchup, or banter: \n\n {chunk} \n\n remove the lines that have a greeting, a personal catchup or banter. Keep the rest of the chunk in its original form")
    model = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser
        
    res = await chain.ainvoke({"chunk": chunk})

    return res