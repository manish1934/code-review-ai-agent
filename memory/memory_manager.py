from datetime import datetime

_memory_store: dict = {}

def save_to_memory(session_id: str, code: str, review: str):
    if session_id not in _memory_store:
        _memory_store[session_id] = []
    _memory_store[session_id].append({
        "timestamp": datetime.now().isoformat(),
        "code_snippet": code[:200],
        "review_summary": review[:300]
    })

def get_memory(session_id: str) -> list:
    return _memory_store.get(session_id, [])

def get_memory_summary(session_id: str) -> str:
    history = get_memory(session_id)
    if not history:
        return "No previous reviews in this session."
    summary = f"Previous {len(history)} review(s):\n"
    for i, item in enumerate(history[-3:], 1):
        summary += f"\n[{i}] {item['timestamp'][:19]}: {item['review_summary'][:100]}..."
    return summary
