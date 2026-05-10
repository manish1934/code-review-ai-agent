from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from agents.bug_detector import run_bug_detector
from agents.security_analyst import run_security_analyst
from agents.optimizer import run_optimizer
from memory.memory_manager import get_memory, save_to_memory
import os
from dotenv import load_dotenv

load_dotenv()

def run_supervisor(code: str, session_id: str = "default") -> dict:
    print("\n[Supervisor] Starting multi-agent code review...")

    # Run all 3 agents in parallel conceptually (sequential for simplicity)
    print("[Agent 1/3] Bug Detector running...")
    bug_report = run_bug_detector(code)

    print("[Agent 2/3] Security Analyst running...")
    security_report = run_security_analyst(code)

    print("[Agent 3/3] Code Optimizer running...")
    optimization_report = run_optimizer(code)

    # Supervisor merges and summarizes
    llm = ChatGroq(
        model="llama3-70b-8192",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

    merge_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Senior Code Review Supervisor. 
You have received reports from 3 specialist agents. 
Synthesize them into a clean, professional code review report with:
1. Overall quality score (0-10)
2. Critical issues (must fix before merge)
3. Summary of bugs found
4. Summary of security vulnerabilities  
5. Top 3 optimization suggestions
6. Final verdict: APPROVE / REQUEST CHANGES / REJECT

Keep it concise and actionable."""),
        ("human", """Code submitted for review:
```
{code}
```

Bug Report:
{bug_report}

Security Report:
{security_report}

Optimization Report:
{optimization_report}

Please synthesize these into a final review.""")
    ])

    chain = merge_prompt | llm
    final_review = chain.invoke({
        "code": code,
        "bug_report": bug_report,
        "security_report": security_report,
        "optimization_report": optimization_report
    })

    result = {
        "bug_report": bug_report,
        "security_report": security_report,
        "optimization_report": optimization_report,
        "final_review": final_review.content
    }

    # Save to memory
    save_to_memory(session_id, code, result["final_review"])

    print("[Supervisor] Review complete!")
    return result
