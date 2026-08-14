# Joe Adely — Python RAG Website Chatbot



A portfolio-ready **retrieval-augmented generation (RAG)** application built in Python. The project demonstrates document ingestion, transparent relevance ranking, source-grounded context assembly, optional OpenAI generation, and basic automated tests.



## Why this project matters



RAG applications combine search with language-model generation. Instead of asking a model to answer from memory alone, this project first retrieves relevant passages from a small knowledge base and then uses those passages as the answer context. The design makes the evidence used for each response visible to the user.



## Skills demonstrated



- Python application development
- 
- Text preprocessing and document ingestion
- 
- Retrieval-pipeline design
- 
- Prompt construction and source grounding
- 
- OpenAI API integration
- 
- Configuration through environment variables
- 
- Automated testing with `pytest`
- 
- Clear technical documentation
- 


## Project structure



```text

joe-adely-rag-chatbot/

├── data/knowledge_base.txt

├── src/rag_chatbot.py

├── tests/test_rag_chatbot.py

├── .env.example

├── requirements.txt

└── README.md

```



## Quick start



```bash

git clone https://github.com/Josephadely-bit/Hi-I-m-Joseph-adely.git

cd Hi-I-m-Joseph-adely/joe-adely-rag-chatbot

python -m venv .venv

source .venv/bin/activate       # Windows: .venv\\Scripts\\activate

pip install -r requirements.txt

python -m src.rag_chatbot "What AI skills does Joe demonstrate?"

```



The default mode works without an API key and returns retrieved evidence. To enable answer generation, copy `.env.example` to `.env` and set `OPENAI_API_KEY`.



```bash

cp .env.example .env

python -m src.rag_chatbot "What scientific experience does Joe have?" --generate

```



## Test



```bash

pytest -q

```



## Responsible-use note



The sample knowledge base contains professional portfolio information only. Do not place private, protected health information, credentials, or confidential employer material in the repository.









