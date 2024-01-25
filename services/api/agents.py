from typing import Any

from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage

from toolset.empty_tool import EmptyTool

PROMPT_STRUCTURED_CHAT = hub.pull("hwchase17/structured-chat-agent")

async def execute_chat_agent(msg: str) -> dict[str, Any]:
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview")

    empty_tool = EmptyTool()
    tools = [empty_tool]
    
    agent = create_structured_chat_agent(llm, tools, PROMPT_STRUCTURED_CHAT)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


    out = await agent_executor.ainvoke({"input": msg }) 

    return out
