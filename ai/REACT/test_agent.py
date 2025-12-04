import time
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq  # Change this
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import asyncio
import os


def get_detailed_stream(agent, query):
    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="values",
    ):
        latest_message = chunk["messages"][-1]

        # Print tool calls (the "Action" step)
        if hasattr(latest_message, "tool_calls") and latest_message.tool_calls:
            for tool_call in latest_message.tool_calls:
                print(f"🔧 Calling tool: {tool_call['name']}")
                print(f"   Args: {tool_call['args']}")

        # Print reasoning/final answer (the "Thought" and "Final Answer" steps)
        elif latest_message.content:
            print(f"🧠 Agent: {latest_message.content}\n")

    print("\n=== FINAL RESULT ===")

    # Get the final answer
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})

    print(result["messages"][-1].content)


@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


# around 6 seconds latency for add then multiply with gpt-4o-mini
openai_llm = ChatOpenAI(
    model="gpt-4o-mini",  # or "gpt-4o", "gpt-3.5-turbo", etc.
    api_key=os.environ.get("OPENAI_API_KEY"),  # or set OPENAI_API_KEY env var
)

# Latency: 0.3927 seconds
# Latency: 392.74 ms
groq_llm = ChatGroq(
    model="llama-3.1-8b-instant",  # Or "llama-3.1-70b-versatile"
    temperature=0,
    timeout=10,
    max_retries=2,
)

system_prompt = """Answer questions as best you can. Use this format:
Thought: think about what to do
Action: the action to take
Action Input: JSON input like {"a": 5, "b": 3}
Observation: the result
... (repeat as needed)
Thought: I now know the answer
Final Answer: the answer
"""


async def main():

    # Get tools
    #  tools = await client.get_tools()

    agent = create_agent(
        model=groq_llm,
        tools=[add, multiply],  # Add your tools here
        system_prompt=system_prompt,
    )
    start_time = time.perf_counter()
    # get_detailed_stream(agent, "What's 3 + 4, then multiply by 3?")
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "What's 8 + 4, then multiply by 2?"}]}
    )
    print(f"Final Answer: {result['messages'][-1].content}\n")
    end_time = time.perf_counter()

    latency_seconds = end_time - start_time
    print(f"Latency: {latency_seconds:.4f} seconds")
    # or in milliseconds
    print(f"Latency: {latency_seconds * 1000:.2f} ms")


if __name__ == "__main__":
    asyncio.run(main())
