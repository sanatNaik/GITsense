from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from llm import llm_with_tools
from tools import TOOLS
import json

def build_system_prompt():

    tool_descriptions = ""

    for tool in TOOLS:
        tool_descriptions += f"""
Tool Name:
{tool.name}

Description:
{tool.description}
"""

    return f"""
You are the planning agent for GitSense.

Your responsibility is to decide which tools are needed
to answer the user's question and execute those tools.

Available Tools:

{tool_descriptions}

Rules:

- Use architecture_tool for high-level repository questions.
- Use repo_search_tool for specific repository/code questions.
- Use web_search_tool for general programming concepts,
  documentation, libraries, and technologies.
- Use multiple tools when necessary.
- Do not answer the user's question yourself.
"""


class Orchestrator:

    def __init__(self):

        self.tool_map = {
            tool.name: tool
            for tool in TOOLS
        }

    def run(self, question: str, history=None):
        print("Orchestrator: Running with question:", question)
        messages = [
            SystemMessage(
                content=build_system_prompt()
            )
        ]

        if history:
            messages.extend(history)

        messages.append(
            HumanMessage(
                content=question
            )
        )
        print("Orchestrator: Asking which tools are needed..")
        # Ask the LLM which tools are needed
        ai_message = llm_with_tools.invoke(
            messages
        )

        # No tools needed
        if not ai_message.tool_calls:
            return {
                "tool_calls": [],
                "messages": messages,
                "response": None
            }

        messages.append(ai_message)
        print("Orchestrator: Tool calls received:", ai_message.tool_calls)
        # Execute tools
        for tool_call in ai_message.tool_calls:

            tool = self.tool_map[
                tool_call["name"]
            ]

            result = tool.invoke(
                tool_call["args"]
            )
            print("=" * 50)
            print(f"TOOL: {tool_call['name']}")
            print("RESULT:")
            print(result)
            print("=" * 50)
            
            content = (
                result
                if isinstance(result, str)
                else json.dumps(result, indent=2)
            )

            messages.append(
                ToolMessage(
                    content=content,
                    tool_call_id=tool_call["id"]
                )
            )
        print("Orchestrator: All tools executed. Returning to LLM for final answer.")
        return {
            "tool_calls": ai_message.tool_calls,
            "messages": messages,
            "response": None
        }


orchestrator = Orchestrator()