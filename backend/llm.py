from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from tools import TOOLS
load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("MODEL"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)
llm_with_tools = llm.bind_tools(TOOLS)