# AI Resume Analyzer

A Flask portfolio project that compares PDF/DOCX resumes against a job description and ranks candidates with Groq-powered structured AI analysis.

## Live Demo

Live demo: _coming after deployment_

GitHub repository: _coming after publication_

## Features

* Paste a job description
* Upload one or more resumes
* Supports PDF and DOCX files
* Extracts resume text temporarily
* Uses an LLM to parse job and resume details into structured JSON
* Validates AI output with Pydantic
* Scores and ranks candidates by match percentage
* Shows matching skills, missing skills, experience fit, and a concise verdict
* Includes a lightweight `/health` endpoint for hosting and uptime checks

## Tech Stack

* Python 3.13
* Flask
* HTML, CSS, and vanilla JavaScript
* Groq API
* Pydantic
* pypdf
* python-docx
* Gunicorn
* uv

## How It Works

1. The user enters a job description.
2. The user uploads PDF or DOCX resumes.
3. Flask stores each upload in a temporary directory during the request.
4. Python extracts text from each resume.
5. Groq analyzes the job description and resume content.
6. Pydantic validates the structured AI output.
7. Candidates are scored, ranked, and displayed in the browser.
8. Temporary files are automatically removed after processing.

## Local Setup

Clone the repository:

```bash
git clone <repository-url>
cd resume-analyzer
```

Install dependencies:

```bash
uv sync
```

Create a local environment file from the example:

```bash
cp .env.example .env
```

Then add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Run locally:

```bash
uv run python app.py
```

Open:

```text
http://127.0.0.1:5000
```

Health check:

```text
http://127.0.0.1:5000/health
```

## Deployment

This app is designed to deploy as a single Python web service.

Recommended Render settings:

* Runtime: Python
* Build command: `uv sync`
* Start command: `uv run gunicorn app:app --bind 0.0.0.0:$PORT`
* Health check path: `/health`
* Environment variable: `GROQ_API_KEY`

No database, authentication, persistent disk, or separate frontend service is required.

## Privacy

Uploaded resumes are processed temporarily by this application and are not intentionally stored permanently. Resume and job description content is sent to the configured external AI provider for analysis. For a public demo, use sample or non-sensitive documents.

## AI Limitation

The match score is AI-assisted guidance only. It should not be treated as a final hiring decision, and human review should remain part of any real recruiting process.

## Purpose

This project demonstrates practical use of Flask, document parsing, file uploads, LLM API integration, structured AI outputs, Pydantic validation, and a simple recruiter-facing web workflow.
