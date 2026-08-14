"""A small, transparent retrieval-augmented generation chatbot.

The default path performs local retrieval and does not require an API key.
Optional generation uses the OpenAI API when OPENAI_API_KEY is configured.
"""
from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Passage:
    text: str
    score: int


def tokenize(text: str) -> set[str]:
    """Return normalized word tokens for simple, explainable retrieval."""
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def load_documents(path: str | Path) -> list[str]:
    """Load paragraphs from a plain-text knowledge base."""
    raw = Path(path).read_text(encoding="utf-8")
    return [paragraph.strip() for paragraph in re.split(r"\n\s*\n", raw) if paragraph.strip()]


def retrieve(query: str, documents: Iterable[str], top_k: int = 3) -> list[Passage]:
    """Rank passages by overlapping normalized query terms."""
    query_terms = tokenize(query)
    scored = [Passage(doc, len(query_terms & tokenize(doc))) for doc in documents]
    return sorted(scored, key=lambda item: item.score, reverse=True)[:top_k]


def build_prompt(query: str, passages: Iterable[Passage]) -> str:
    """Build a grounded prompt that instructs the model not to invent facts."""
    context = "\n\n".join(f"Source {i}: {p.text}" for i, p in enumerate(passages, 1))
    return (
        "Answer the question using only the supplied sources. If the sources do not "
        "contain the answer, say that the information is unavailable. Do not invent "
        "qualifications or experience.\n\n"
        f"Sources:\n{context}\n\nQuestion: {query}"
    )


def generate_with_openai(prompt: str) -> str:
    """Generate a response through the OpenAI SDK using environment configuration."""
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "You are a concise professional portfolio assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or "No response returned."


def answer(query: str, knowledge_path: str | Path, use_generation: bool = False) -> str:
    passages = retrieve(query, load_documents(knowledge_path))
    if not passages or passages[0].score == 0:
        return "No relevant portfolio information was found."
    if use_generation:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("Set OPENAI_API_KEY before using --generate.")
        return generate_with_openai(build_prompt(query, passages))
    evidence = "\n".join(f"[{i}] {p.text}" for i, p in enumerate(passages, 1))
    return f"Retrieved evidence:\n{evidence}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask questions about Joe Adely's portfolio.")
    parser.add_argument("query", help="Question to ask")
    parser.add_argument("--generate", action="store_true", help="Use OpenAI for a grounded answer")
    parser.add_argument("--knowledge-base", default="data/knowledge_base.txt")
    args = parser.parse_args()
    print(answer(args.query, args.knowledge_base, args.generate))


if __name__ == "__main__":
    main()
