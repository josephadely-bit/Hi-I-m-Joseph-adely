from src.rag_chatbot import build_prompt, retrieve, tokenize


def test_tokenize_normalizes_words():
    assert tokenize("Python, Python API!") == {"python", "api"}


def test_retrieve_ranks_relevant_passage_first():
    docs = ["Joe uses Python for AI projects.", "Joe has experience with microscopy."]
    results = retrieve("Python AI", docs, top_k=2)
    assert results[0].text == docs[0]
    assert results[0].score == 2


def test_prompt_requires_grounding():
    prompt = build_prompt("What skills are documented?", retrieve("skills", ["Python and RAG skills."]))
    assert "Do not invent qualifications" in prompt
    assert "Python and RAG skills" in prompt
