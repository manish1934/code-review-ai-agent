import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.supervisor import run_supervisor
from eval.ragas_eval import simple_eval

st.set_page_config(page_title="Code Review AI Agent", page_icon="🤖", layout="wide")
st.title("Code Review AI Agent")
st.caption("Multi-agent system powered by Groq + Llama 3 + RAG")

with st.sidebar:
    st.header("About")
    st.markdown("""
**Tech Stack:**
- LangChain + Groq (Llama 3.3 70B)
- FAISS Vector Store
- Sentence Transformers Embeddings
- RAGAS Evaluation

**Agents:**
- 🐛 Bug Detector
- 🔒 Security Analyst
- ⚡ Code Optimizer
- 🎯 Supervisor
    """)
    session_id = st.text_input("Session ID", value="user_001")

sample_codes = {
    "🐍 Python — SQL Injection": 'def get_user(username):\n    query = "SELECT * FROM users WHERE name = \'" + username + "\'"\n    return db.execute(query)',
    "🐍 Python — Nested Loop Bug": 'def find_duplicates(lst):\n    duplicates = []\n    for i in range(len(lst)):\n        for j in range(len(lst)):\n            if i != j and lst[i] == lst[j]:\n                if lst[i] not in duplicates:\n                    duplicates.append(lst[i])\n    return duplicates',
    "🐍 Python — Multiple Bugs": 'def find_common_elements(list1, list2):\n    result = []\n    for i in range(len(list1) + 1):\n        for j in range(len(list2)):\n            if list1[i] == list2[j]:\n                result.append(list1[i])\n    return result\n\ndef bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(n):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr',
    "🐍 Python — Hardcoded Credentials": 'import mysql.connector\n\ndef connect_db():\n    conn = mysql.connector.connect(\n        host="localhost",\n        user="root",\n        password="admin123",\n        database="mydb"\n    )\n    return conn',
    "🟨 JavaScript — XSS Vulnerability": 'function displayUserInput(userInput) {\n    document.getElementById("output").innerHTML = userInput;\n}\n\nvar password = "supersecret123";\nconsole.log("Password is: " + password);',
    "🟨 JavaScript — Async Bug": 'async function getUserData(userId) {\n    let response = fetch("https://api.example.com/users/" + userId);\n    let data = response.json();\n    return data.name;\n}',
    "☕ Java — Null Pointer & SQL Injection": 'public String getUser(String username) {\n    Statement stmt = conn.createStatement();\n    String query = "SELECT * FROM users WHERE name = \'" + username + "\'";\n    ResultSet rs = stmt.executeQuery(query);\n    if (rs.next()) return rs.getString("name");\n    return null;\n}\n\npublic int divide(int a, int b) {\n    return a / b;\n}',
    "⚙️ C++ — Buffer Overflow": '#include <string.h>\n\nvoid copyInput(char* input) {\n    char buffer[10];\n    strcpy(buffer, input);\n}\n\nint* createArray(int size) {\n    int* arr = new int[size];\n    for (int i = 0; i <= size; i++) arr[i] = i * 2;\n    return arr;\n}',
    "🗄️ SQL — Injection & Bad Practices": "CREATE PROCEDURE GetUser @username VARCHAR(50)\nAS BEGIN\n    DECLARE @sql NVARCHAR(500)\n    SET @sql = 'SELECT * FROM users WHERE username = ''' + @username + ''''\n    EXEC(@sql)\nEND\n\nINSERT INTO users (username, password)\nVALUES ('john', 'password123')",
    "🔷 TypeScript — Type Safety Issues": 'async function fetchUsers(): Promise<any> {\n    const response = await fetch(\'/api/users\');\n    return await response.json();\n}\n\nconst apiKey = "sk-abc123secretkey456";\nconst baseUrl = "http://api.example.com";',
    "🐹 Go — Race Condition": 'package main\n\nvar counter int\n\nfunc incrementCounter() {\n    counter++\n}\n\nfunc main() {\n    for i := 0; i < 1000; i++ {\n        go incrementCounter()\n    }\n}',
}

st.subheader("Paste your code or load a sample")
col1, col2 = st.columns([2, 1])
with col2:
    selected = st.selectbox("Load a sample:", [""] + list(sample_codes.keys()))

code_input = st.text_area(
    "Code to review:",
    value=sample_codes.get(selected, ""),
    height=250,
    placeholder="Paste any code here — Python, JS, Java, C++, SQL, Go, TypeScript..."
)

if st.button("🚀 Run Code Review", type="primary", disabled=not code_input.strip()):
    with st.spinner("Running multi-agent review... (~20 seconds)"):
        try:
            results = run_supervisor(code_input, session_id=session_id)
            eval_scores = simple_eval(code_input, results["final_review"])
            st.success("✅ Review Complete!")
            c1, c2, c3 = st.columns(3)
            c1.metric("Overall Score", f"{eval_scores['overall']*10:.1f}/10")
            c2.metric("Coverage", f"{eval_scores['coverage']*100:.0f}%")
            c3.metric("Completeness", f"{eval_scores['completeness']*100:.0f}%")
            st.divider()
            st.subheader("📋 Final Review (Supervisor)")
            st.markdown(results["final_review"])
            st.divider()
            t1, t2, t3 = st.tabs(["🐛 Bugs", "🔒 Security", "⚡ Optimization"])
            with t1: st.markdown(results["bug_report"])
            with t2: st.markdown(results["security_report"])
            with t3: st.markdown(results["optimization_report"])
        except Exception as e:
            st.error(f"Error: {str(e)}")
