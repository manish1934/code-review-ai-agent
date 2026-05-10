def simple_eval(code: str, review: str) -> dict:
    scores = {}
    code_keywords = set(code.split())
    review_words = set(review.lower().split())
    common = code_keywords & review_words
    scores["relevancy"] = min(1.0, len(common) / max(len(code_keywords), 1))
    sections = ["bug", "security", "optim", "score", "verdict"]
    found = sum(1 for s in sections if s in review.lower())
    scores["coverage"] = found / len(sections)
    scores["completeness"] = min(1.0, len(review) / 500)
    scores["overall"] = round(
        (scores["relevancy"] * 0.3 +
         scores["coverage"] * 0.4 +
         scores["completeness"] * 0.3), 2
    )
    return scores
