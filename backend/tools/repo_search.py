from langchain_core.tools import tool
from retrievers.repo_retriever import retrieve_repo_context


@tool
def repo_search_tool(query: str):
    """
    Search the indexed repository for relevant code and documentation.
    """
    return retrieve_repo_context(query)