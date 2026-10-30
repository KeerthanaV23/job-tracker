"""Resume <-> Job Description matching using TF-IDF + cosine similarity.

Final score = 40% cosine similarity (overall wording overlap)
            + 60% keyword coverage (how many of the JD's top keywords the resume contains).
Keyword coverage is weighted higher because raw cosine similarity between two
different kinds of documents is naturally low.
"""
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

TOP_N_KEYWORDS = 20
_TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9+#.]*")


def clean_text(text: str) -> str:
    return " ".join(_TOKEN_RE.findall(text.lower()))


def _contains(haystack: str, term: str) -> bool:
    return re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", haystack) is not None


def analyze(resume_text: str, job_description: str) -> dict:
    resume = clean_text(resume_text)
    jd = clean_text(job_description)
    if not resume or not jd:
        raise ValueError("Both resume text and job description are required.")

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), token_pattern=r"[a-z][a-z0-9+#.]*")
    try:
        matrix = vectorizer.fit_transform([resume, jd])
    except ValueError:  # only stop-words
        return {"score": 0, "matched_keywords": [], "missing_keywords": []}

    cosine = float(cosine_similarity(matrix[0], matrix[1])[0][0])

    terms = vectorizer.get_feature_names_out()
    jd_weights = matrix[1].toarray()[0]
    ranked = sorted(zip(terms, jd_weights), key=lambda x: x[1], reverse=True)
    # prefer single words first, keep list small and readable
    keywords = [t for t, w in ranked if w > 0 and " " not in t][:TOP_N_KEYWORDS]

    matched = [k for k in keywords if _contains(resume, k)]
    missing = [k for k in keywords if k not in matched]
    coverage = len(matched) / len(keywords) if keywords else 0.0

    score = round(100 * (0.4 * cosine + 0.6 * coverage))
    return {
        "score": max(0, min(100, score)),
        "matched_keywords": matched,
        "missing_keywords": missing,
    }
