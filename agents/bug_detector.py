from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

def run_bug_detector(code: str) -> str:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert Bug Detector agent. Analyze the given code and identify:
- Logic errors and off-by-one mistakes
- Null/None pointer issues
- Exception handling problems
- Memory leaks or resource mismanagement
- Incorrect data type usage
Be specific - mention exact line numbers or variable names when possible.
Format your response as a numbered list of bugs found. If no bugs, say No bugs detected."""),
        ("human", "Review this code for bugs:\n\n```\n{code}\n```")
    ])
    chain = prompt | llm
    result = chain.invoke({"code": code})
    return result.content
