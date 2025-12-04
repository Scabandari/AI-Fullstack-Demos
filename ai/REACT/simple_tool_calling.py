import time
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage, HumanMessage


@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


# around 4 seconds latency for add then multiply with gpt-4o-mini
openai_llm = ChatOpenAI(model="gpt-4o-mini")

# test_agent with ReAct is slightly faster when using Groq for some reason
# Latency: 0.5012 seconds
# Latency: 501.20 ms
groq_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    timeout=10,
    max_retries=2,
)


model_with_tools = groq_llm.bind_tools([add, multiply])

# ONE invocation
messages = [HumanMessage("Add 5 and 3, then multiply by 2")]
start_time = time.perf_counter()
response = model_with_tools.invoke(messages)

# Execute tools in parallel if you want
tool_results = []
for tc in response.tool_calls:
    if tc["name"] == "add":
        result = add.invoke(tc["args"])
    else:
        result = multiply.invoke(tc["args"])
    tool_results.append(ToolMessage(content=result, tool_call_id=tc["id"]))

# Feed results back if needed (still faster than full ReAct loop)
messages.append(response)
messages.extend(tool_results)
final = groq_llm.invoke(messages)

end_time = time.perf_counter()
latency_seconds = end_time - start_time
print(f"Latency: {latency_seconds:.4f} seconds")
# or in milliseconds
print(f"Latency: {latency_seconds * 1000:.2f} ms")
