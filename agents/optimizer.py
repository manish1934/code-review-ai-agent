from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

def run_optimizer(code: str) -> str:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert Code Optimizer agent. Analyze the given code for improvements:
- Time complexity improvements
- Memory usage optimization
- Pythonic improvements
- Redundant computations
- Better data structure choices
For each suggestion, show BEFORE and AFTER code snippet.
Format as a numbered list of improvements."""),
        ("human", "Review this code for optimization opportunities:\n\n```\n{code}\n```")
    ])
    chain = prompt | llm
    result = chain.invoke({"code": code})
    return result.content
