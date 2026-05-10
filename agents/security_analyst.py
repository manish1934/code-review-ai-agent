from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

def run_security_analyst(code: str) -> str:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert Security Analyst agent. Analyze the given code for security vulnerabilities including:
- SQL Injection risks
- XSS vulnerabilities
- Hardcoded secrets or credentials
- Insecure authentication or authorization
- Sensitive data exposure
Rate each vulnerability as: CRITICAL / HIGH / MEDIUM / LOW
Format as a numbered list. If no vulnerabilities found, say No security issues detected."""),
        ("human", "Review this code for security vulnerabilities:\n\n```\n{code}\n```")
    ])
    chain = prompt | llm
    result = chain.invoke({"code": code})
    return result.content
