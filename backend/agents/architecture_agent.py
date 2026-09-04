import json

from langchain_core.messages import (
    HumanMessage,
    SystemMessage
)

from llm import llm

from retrievers.architecture_retriever import (
    build_architecture_context
)


SYSTEM_PROMPT = """
You are the Architecture Agent for GitSense.

Your job is to analyze a software repository
and produce a reliable high-level architecture summary.

Only use information provided in the repository context.

Do not invent components, technologies, or relationships.

Return valid JSON only.
"""


class ArchitectureAgent:

    def analyze(self, repo_path):

        print("Building architecture context...")

        prompt = build_architecture_context(
            repo_path
        )

        messages = [
            SystemMessage(
                content=SYSTEM_PROMPT
            ),
            HumanMessage(
                content=prompt
            )
        ]

        print("Calling architecture LLM...")
        try:
            response = llm.invoke(messages)
            print("Architecture LLM response received.")
        except Exception as e:
            print("ARCHITECTURE LLM ERROR:")
            print(type(e).__name__)
            print(str(e))
            raise

        content = response.content.strip()

        if content.startswith("```"):

            content = content.replace(
                "```json",
                ""
            )

            content = content.replace(
                "```",
                ""
            )

            content = content.strip()

        architecture = json.loads(content)

        print("Architecture analysis completed.")

        return architecture


architecture_agent = ArchitectureAgent()