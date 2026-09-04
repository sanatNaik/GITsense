from langchain_core.tools import tool
from retrievers.web_retriever import retrieve_web_context


@tool
def web_search_tool(query: str) -> str:
    """
    Search the web for programming concepts, documentation,
    libraries, frameworks, and general software engineering questions.
    Use this when the answer cannot be obtained from the indexed repository.
    """
    return retrieve_web_context(query)