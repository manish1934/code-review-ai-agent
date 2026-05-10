from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from rag.retriever import retrieve_context
import os
from dotenv import load_dotenv

load_dotenv()

def run_optimizer(code: str) -> str:
    llm = ChatGroq(
        model="llama3-70b-8192",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

    context = retrieve_context(f"code performance optimization best practices: {code[:200]}")

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert Code Optimizer agent. Analyze the given code for performance and quality improvements:
- Time complexity improvements (O(n²) → O(n) etc.)
- Memory usage optimization
- Pythonic improvements (list comprehensions, generators)
- Redundant computations
- Better data structure choices
- Code readability and maintainability

Use this performance reference context:
{context}

For each suggestion, show the BEFORE and AFTER code snippet.
Format as a numbered list of improvements."""),
        ("human", "Review this code for optimization opportunities:\n\n```\n{code}\n```")
    ])

    chain = prompt | llm
    result = chain.invoke({"code": code, "context": context})
    return result.content
