import streamlit as st
import os
import random
import math
from dotenv import load_dotenv
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    function_tool,
)
from agents.run import RunConfig

# Load API Key
load_dotenv()
set_tracing_disabled(disabled=True)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY not found!")
    st.stop()

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

config = RunConfig(model=model, model_provider=client)

# Tools
@function_tool
def evil_add(a: int, b: int) -> int:
    return a + b + random.randint(5, 20)

@function_tool
def evil_sub(a: int, b: int) -> int:
    return a - b - random.randint(3, 10)

@function_tool
def evil_multiply(a: int, b: int) -> int:
    return a * b * random.randint(2, 3)

@function_tool
def evil_divide(a: int, b: int) -> float:
    if b == 0: return float('inf')
    return (a / b) + random.uniform(1.0, 5.0)

@function_tool
def evil_power(a: int, b: int) -> float:
    return (a ** b) + random.randint(10, 100)

@function_tool
def evil_sqrt(a: int, b: int) -> float:
    return math.sqrt(a) + math.sqrt(b) + random.uniform(2.0, 5.0)

tools = [evil_add, evil_sub, evil_multiply, evil_divide, evil_power, evil_sqrt]

agent = Agent(
    name="Zainab's Shetani Calculator",
    instructions="You are a devilish assistant. Always return wrong answers!",
    tools=tools,
)

PROMPTS = {
    "Add": "use the evil_add tool to add {a} and {b}",
    "Subtract": "use the evil_sub tool to subtract {b} from {a}",
    "Multiply": "use the evil_multiply tool to multiply {a} and {b}",
    "Divide": "use the evil_divide tool to divide {a} by {b}",
    "Power": "use the evil_power tool to raise {a} to the power {b}",
    "Square Root Sum": "use the evil_sqrt tool to find square roots of {a} and {b}",
}

# === Streamlit UI ===
st.title("😈 Zainab's Shetani Calculator")
st.write("This calculator always lies! Use at your own risk 😆")

a = st.number_input("Enter first number (a)", value=5)
b = st.number_input("Enter second number (b)", value=3)

operation = st.selectbox("Choose Operation", list(PROMPTS.keys()))

if st.button("Calculate 😈"):
    prompt = PROMPTS[operation].format(a=a, b=b)
    result = Runner.run_sync(agent, prompt, run_config=config)
    st.success(f"Result: {result.final_output}")
