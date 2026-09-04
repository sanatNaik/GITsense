from agents.chat_agent import chat_agent

response = chat_agent.chat(
    "test-session",
    "What is JWT?"
)

print(response)

response = chat_agent.chat(
    "test-session",
    "Can you explain it in simpler terms?"
)

print(response)