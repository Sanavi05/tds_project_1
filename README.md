# TDS Virtual TA – IITM Data Science Project

A FastAPI-powered Teaching Assistant that automatically answers student questions for the **Tools in Data Science (TDS)** course (Jan 2025 batch) using:

- Official course content from [tds.s-anand.net](https://tds.s-anand.net/#/2025-01)
- Discourse posts from Jan–Apr 2025
- AI-generated answers using [AI Pipe](https://github.com/sanand0/aipipe)

---

## Features

- Accepts questions with optional image (base64)
- Combines semantic search with AI responses
- Returns concise answers with **relevant links** to source
- Built with FastAPI, SentenceTransformers, and AI Pipe
- Handles both text-based and image-related queries (if supported)

---

## API Endpoint

### `POST /ask`

**Request Body:**

```json
{
  "question": "What is the difference between Docker and Podman?",
  "image": "<optional base64-encoded image>"
}
```
**Response:**

```json
{
  "answer": "Podman is preferred but Docker is also allowed...",
  "links": [
    {
      "url": "https://discourse.onlinedegree.iitm.ac.in/...",
      "text": "Relevant discussion on Podman vs Docker..."
    },
    {
      "url": "https://tds.s-anand.net/#/docker",
      "text": "Course content: Docker and Podman"
    }
  ]
}

