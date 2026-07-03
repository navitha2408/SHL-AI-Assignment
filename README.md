# SHL AI Assignment

## Overview

This project is an AI-powered chatbot API built using FastAPI and Google's Gemini API.

The chatbot answers user queries by retrieving relevant information from a product catalog and generating intelligent responses using Retrieval-Augmented Generation (RAG).

---

## Features

- FastAPI REST API
- Gemini AI integration
- Product catalog search
- Context-aware responses
- Health endpoint
- JSON API
- Environment variable support
- Easy deployment

---

## Project Structure

```
SHL-AI-Assignment/
│
├── app.py              # FastAPI application
├── chatbot.py          # Chatbot logic
├── scraper.py          # Product scraping
├── catalog.json        # Product database
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/navitha2408/SHL-AI-Assignment.git
```

Move into the project

```bash
cd SHL-AI-Assignment
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```
GEMINI_API_KEY=YOUR_API_KEY
```

Run the application

```bash
uvicorn app:app --reload
```

---

## API Endpoints

### Health Check

```
GET /health
```

Example response

```json
{
  "status": "ok"
}
```

---

### Chat

```
POST /chat
```

Example Request

```json
{
  "message": "Tell me about the latest laptops."
}
```

Example Response

```json
{
  "response": "..."
}
```

---

## Technologies Used

- Python
- FastAPI
- Google Gemini API
- Uvicorn
- JSON

---

## Environment Variables

Create a `.env` file.

```
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Repository

https://github.com/navitha2408/SHL-AI-Assignment

---

## Deployment

Deployment is supported on platforms such as:

- Render
- Railway
- Northflank
- Fly.io

---

## Author

Daruri Navitha
