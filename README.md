# SHL AI Assessment Recommendation System

## Overview

This project is an AI-powered recommendation system that suggests the most relevant SHL assessments based on a recruiter's hiring requirements. It uses Large Language Models (Google Gemini) to understand hiring needs and semantic search (FAISS + Sentence Transformers) to retrieve the most appropriate assessments from the SHL assessment catalog.

The API is stateless and accepts the complete conversation history on every request.



## Features

* Stateless REST API built with FastAPI
* Accepts full conversation history
* Uses Google Gemini to extract hiring requirements
* Semantic search using Sentence Transformers
* Fast similarity search using FAISS
* Returns relevant SHL assessments with URLs and test types
* Swagger UI for interactive API testing
* Health check endpoint
* Evaluation script for testing conversation traces



## Tech Stack

* Python 3.9+
* FastAPI
* Google Gemini API
* Sentence Transformers (all-MiniLM-L6-v2)
* FAISS
* Pydantic
* NumPy
* Uvicorn



## Project Structure


shl-ai-recommender/

├── app/
│   ├── main.py
│   ├── retriever.py
│   ├── gemini_service.py
│   ├── schemas.py
│   ├── logger.py
│   └── utils.py
│
├── data/
│   ├── raw_catalog.json
│   └── clean_catalog.json
│
├── vectorstore/
│   ├── index.faiss
│   └── metadata.pkl
│
├── scripts/
│   ├── clean_catalog.py
│   ├── build_index.py
│   └── evaluate.py
│
├── traces/
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── ...




## Installation

### 1. Clone the repository


git clone <repository-url>
cd shl-ai-recommender


### 2. Create a virtual environment


python -m venv venv


### 3. Activate the environment

Windows


venv\Scripts\activate


Linux / macOS


source venv/bin/activate


### 4. Install dependencies


pip install -r requirements.txt




## Environment Variables

Create a `.env` file in the project root.


GEMINI_API_KEY=YOUR_API_KEY




## Build the Vector Index

Clean the catalog


python scripts/clean_catalog.py


Build embeddings and FAISS index


python scripts/build_index.py




## Run the API


uvicorn app.main:app --reload


The API will be available at:


http://127.0.0.1:8000


Swagger UI:


http://127.0.0.1:8000/docs


Health Check:


http://127.0.0.1:8000/health




## API Endpoints

### GET /health

Returns the application status.

Example Response

json
{
  "status": "ok"
}




### POST /chat

Accepts the full conversation history and returns recommended SHL assessments.

Example Request

json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring a Java backend developer with AWS experience"
    }
  ]
}


Example Response

json
{
  "reply": "Based on your requirements, here are the most relevant SHL assessments.",
  "recommendations": [
    {
      "name": "Java 8 (New)",
      "url": "...",
      "test_type": "K"
    }
  ],
  "end_of_conversation": true
}




## Recommendation Pipeline

1. Receive complete conversation history.
2. Gemini extracts hiring requirements.
3. Requirements are converted into a semantic search query.
4. Sentence Transformer generates embeddings.
5. FAISS retrieves the most relevant SHL assessments.
6. Results are formatted and returned through the API.



## Evaluation

Conversation traces can be evaluated using:


python scripts/evaluate.py




## Future Improvements

* Hybrid semantic + keyword ranking
* Better business-rule based re-ranking
* Migration to the latest Google GenAI SDK
* Multi-language support
* Caching frequently searched queries
* Docker deployment


## Author
Anuj Kushwaha
