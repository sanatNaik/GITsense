import json
from langchain_core.tools import tool


@tool
def architecture_tool(query: str):
    """
    Provides a high-level overview of the repository, including its
    purpose, technology stack, entry points, directory structure,
    key modules, and architectural patterns.
    """

    try:
        with open(
            "repo_cache/architecture.json",
            "r",
            encoding="utf-8"
        ) as f:

            architecture_data = json.load(f)

        return json.dumps(
            architecture_data,
            indent=2
        )

    except FileNotFoundError:

        return "No architecture analysis is available. Load a repository first."