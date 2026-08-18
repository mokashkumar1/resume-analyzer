# AI Resume Analyzer

A Flask-based learning project that helps students and job seekers compare their resume against a job description using AI.

## Live Demo & Repository

* **Live Demo**: [https://ai-resume-analyzer-y4ns.onrender.com](https://ai-resume-analyzer-y4ns.onrender.com)  
  *(Note: Free-tier Render hosting may experience a short cold-start delay after periods of inactivity.)*
* **GitHub Repository**: [https://github.com/mokashkumar1/resume-analyzer](https://github.com/mokashkumar1/resume-analyzer)

## Purpose & Project Overview

This application was created as a practical learning project to explore Python web development, file processing, and structured AI integrations.

Using the web interface, job seekers and students can:
* Paste a job description
* Upload a PDF or DOCX resume
* Extract structured resume information automatically
* Identify matching skills between the resume and job requirements
* Highlight key missing skills needed for the role
* Check if minimum experience requirements are satisfied
* Receive an AI-generated match score percentage
* Read a concise verdict summarizing candidate fit before submitting a job application

## Features

* **Job Description Parsing**: Analyzes unstructured job postings into structured skill and experience requirements.
* **Resume Text Extraction**: Extracts plain text safely from PDF and DOCX files without permanent disk persistence.
* **Structured AI Analysis**: Uses Groq-powered LLMs to extract resume metadata and match candidate profiles against target roles.
* **Pydantic Validation**: Validates AI-generated JSON responses against strict Python schemas.
* **Small Comparison Support**: Supports analyzing individual resumes or comparing up to 3 candidates at a time.
* **Health Endpoint**: Includes a `/health` endpoint for platform health checks and monitoring.

## Tech Stack

* **Language**: Python 3.13
* **Web Framework**: Flask
* **Frontend**: HTML5, CSS3, Vanilla JavaScript
* **AI Provider**: Groq API (`openai/gpt-oss-120b`)
* **Data Validation**: Pydantic v2
* **Document Parsers**: `pypdf`, `python-docx`
* **WSGI Server**: Gunicorn
* **Package & Environment Manager**: `uv`

## How It Works

1. **Input**: The user enters a target job description and uploads a PDF or DOCX resume via the web form.
2. **Temporary File Handling**: Uploaded files are saved to a temporary directory created specifically for the request.
3. **Text Extraction**: `pypdf` or `python-docx` extracts raw text from the document.
4. **Structured AI Processing**:
   - The job description is parsed into structured JSON matching a Pydantic schema (`Job_D`).
   - The resume text is parsed into a structured candidate schema (`Resume`).
   - The candidate profile is evaluated against job requirements (`MatchResult`).
5. **Validation & Rendering**: Pydantic validates the JSON structure, and Flask renders candidate match cards with skill badges and score bars.
6. **Cleanup**: Temporary files are automatically deleted at the conclusion of the request cycle.

## Learning Journey

This project evolved step-by-step through practical debugging and iteration:

1. **Terminal CLI Prototype**: Started as a basic Python script with a hard-coded job description, local resume files, and console print outputs.
2. **Modularization**: Refactored logic into clean, reusable Python functions and Pydantic schemas.
3. **Flask Integration**: Built a Flask backend with HTTP routes, file upload handling, and error handling.
4. **Frontend UI**: Created a recruiter-style web interface using HTML, CSS, and vanilla JavaScript.
5. **Cloud Deployment**: Configured project dependencies with `uv`, WSGI server settings with Gunicorn, and deployed to Render.

Building and converting the CLI prototype into a functional web application helped provide hands-on experience with full-stack Python development, API error handling, and cloud deployments.

## Current Limitations

This version is primarily designed for individual and small resume analysis for portfolio demonstration:

* **Synchronous Processing**: Each resume requires multiple LLM API calls executed synchronously during the HTTP request.
* **Rate Limits & Latency**: Processing several resumes in a single request increases response latency and can encounter API rate limits or server request timeouts on free-tier web hosting.
* **Scope**: An enterprise recruiter platform would typically use background job workers (e.g. Celery / Redis), asynchronous task queues, batch processing, and database storage. Those features are intentionally outside the scope of this learning project.

## AI Disclaimer

* AI-generated match scores and verdicts are provided as **advisory guidance only**.
* They should not be treated as automated hiring decisions.
* Large language model outputs may vary or contain inconsistencies, and human review remains essential in recruitment workflows.

## Privacy & Data Handling

* **Temporary Processing**: Uploaded resumes are processed in temporary memory/directories during request execution.
* **No Database Storage**: The application does not maintain a database or store uploaded resumes permanently.
* **External AI Provider**: Job descriptions and resume text are sent to the external Groq API for analysis. Users should avoid submitting sensitive or private personal documents when testing the public demo.

## Local Setup

### Prerequisites

* Python >= 3.13
* `uv` package manager (or standard `pip` / `venv`)
* A Groq API key (from [groq.com](https://groq.com))

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mokashkumar1/resume-analyzer
   cd resume-analyzer
   ```

2. Install dependencies with `uv`:
   ```bash
   uv sync
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. Run the application locally:
   ```bash
   uv run python app.py
   ```

5. Open your browser:
   * **Web App**: `http://127.0.0.1:5000`
   * **Health Check**: `http://127.0.0.1:5000/health`

## Deployment

This app is configured for single-service deployment on Render using `render.yaml`:

* **Runtime**: Python
* **Build Command**: `uv sync`
* **Start Command**: `uv run gunicorn app:app --bind 0.0.0.0:$PORT --timeout 180`
* **Health Check Path**: `/health`
* **Environment Variable**: `GROQ_API_KEY`
