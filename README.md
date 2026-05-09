# SHL Assessment Recommendation Agent

An AI-powered FastAPI backend that recommends SHL assessments based on hiring requirements.

## Features

- SHL assessment recommendation
- Conversational multi-turn support
- Clarification questions
- Assessment comparison support
- Off-topic refusal handling
- FastAPI backend
- Swagger/OpenAPI documentation

## Tech Stack

- Python
- FastAPI
- Sentence Transformers
- FAISS
- BeautifulSoup
- Uvicorn

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Docs

```text
http://127.0.0.1:8000/docs
```

## Deployment

Deployed on Render.

## GitHub Repository

https://github.com/boddupallykavya9-cloud/shl-assessment-agent