from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from rag.retriever import retrieve_context
import os
from dotenv import load_dotenv

load_dotenv()

def run_security_analyst(code: str) -> str:
    llm = ChatGroq(
        model="llama3-70b-8192",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

    context = retrieve_context(f"OWASP security vulnerabilities SQL injection XSS: {code[:200]}")

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert Security Analyst agent. Analyze the given code for security vulnerabilities including:
- SQL Injection risks
- XSS (Cross-Site Scripting) vulnerabilities
- Hardcoded secrets or credentials
- Insecure authentication or authorization
- Sensitive data exposure
- CSRF vulnerabilities
- Insecure deserialization

Use this OWASP reference context:
{context}

Rate each vulnerability as: CRITICAL / HIGH / MEDIUM / LOW
Format as a numbered list. If no vulnerabilities found, say 'No security issues detected.'"""),
        ("human", "Review this code for security vulnerabilities:\n\n```\n{code}\n```")
    ])

    chain = prompt | llm
    result = chain.invoke({"code": code, "context": context})
    return result.content
