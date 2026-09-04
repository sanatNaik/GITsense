
from llm import llm
from agents.orchestrator import orchestrator
from langchain_core.messages import HumanMessage, SystemMessage
from memory import get_chat_history


ANSWER_SYSTEM_PROMPT = """
You are GitSense, an AI assistant that helps users understand
software repositories and programming concepts.

You have been given:
1. The user's question
2. The conversation history
3. Results from tools selected by the planning agent

Use the tool results as context to answer the user's question.

Rules:
- Answer the user's question directly.
- Use the provided tool results when relevant.
- Do not mention tools, tool calls, planning, or internal processes.
- If the question is repository-specific, prioritize repository context.
- If the question is general, use the web search context when provided.
- If the available context is insufficient, clearly say so.
- Keep the answer concise.
- Respond using Markdown.
"""


class ChatAgent:

    def chat(self, session_id: str, question: str):
        history = get_chat_history(session_id)
        print("ChatAgent: Sending question to orchestrator...")
        result = orchestrator.run(
			question,
			history.messages
		)
        answer_messages = [
			SystemMessage(
				content=ANSWER_SYSTEM_PROMPT
			),
			HumanMessage(
				content=question
			)
		]
        answer_messages.extend(
			result["messages"][1:]
		)
        print(
			"ChatAgent: Sending context to LLM for final answer..."
		)
        final_response = llm.invoke(
			answer_messages
		)
        answer = final_response.content
        history.add_user_message(question)
        history.add_ai_message(answer)

        print("=" * 50) 
        print("FINAL LLM RESPONSE:")
        print(final_response)
        print("CONTENT:")
        print(final_response.content)
        print("=" * 50)
        return answer


chat_agent = ChatAgent()