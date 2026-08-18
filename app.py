import logging
import os
from json import JSONDecodeError
from pathlib import Path
from tempfile import TemporaryDirectory

from flask import Flask, render_template, request
from pydantic import ValidationError
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from resume_analyser import (
    parse_job_description,
    parse_resume,
    final_score,
    read_resume
)


ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_CONTENT_LENGTH = 8 * 1024 * 1024

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
logging.basicConfig(level=logging.INFO)


@app.errorhandler(RequestEntityTooLarge)
def handle_large_upload(error):
    return render_template(
        "index.html",
        error="Upload is too large. Please upload smaller PDF or DOCX files."
    ), 413


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return {"status": "ok"}, 200


@app.route("/analyze", methods=["POST"])
def analyze():

    job_description = request.form.get("job_description", "").strip()

    uploaded_files = request.files.getlist("resumes")

    if not job_description:
        return render_template(
            "index.html",
            error="Please enter a job description."
        )

    if not uploaded_files or all(not file.filename for file in uploaded_files):
        return render_template(
            "index.html",
            error="Please upload at least one PDF or DOCX resume."
        )

    valid_files = []
    rejected_files = []

    for uploaded_file in uploaded_files:

        if not uploaded_file.filename:
            continue

        suffix = Path(uploaded_file.filename).suffix.lower()

        if suffix in ALLOWED_EXTENSIONS:
            valid_files.append(uploaded_file)
        else:
            rejected_files.append(uploaded_file.filename)

    if rejected_files:
        return render_template(
            "index.html",
            error="Only PDF and DOCX resumes are supported."
        )

    if not valid_files:
        return render_template(
            "index.html",
            error="Please upload at least one PDF or DOCX resume."
        )

    try:

        job = parse_job_description(job_description)

        all_results = []

        with TemporaryDirectory() as temp_folder:

            temp_folder = Path(temp_folder)

            for uploaded_file in valid_files:

                safe_filename = secure_filename(uploaded_file.filename)

                if not safe_filename:
                    continue

                file_path = temp_folder / safe_filename

                uploaded_file.save(file_path)

                resume_text = read_resume(file_path)

                if not resume_text or not resume_text.strip():
                    return render_template(
                        "index.html",
                        error=f"Could not extract readable text from {safe_filename}."
                    )

                parsed_resume = parse_resume(resume_text)

                result = final_score(
                    job,
                    parsed_resume
                )

                all_results.append({
                    "name": parsed_resume.name or safe_filename,
                    "filename": safe_filename,
                    "score": result.score,
                    "details": result.details
                })

        if not all_results:
            return render_template(
                "index.html",
                error="No readable resume content could be analyzed."
            )

        all_results.sort(
            key=lambda candidate: candidate["score"],
            reverse=True
        )

        return render_template(
            "index.html",
            results=all_results,
            job_role=job.role
        )

    except (JSONDecodeError, ValidationError) as error:

        app.logger.exception("Invalid AI response while analyzing resumes.")

        return render_template(
            "index.html",
            error="The AI response could not be processed. Please try again."
        )

    except ValueError as error:

        app.logger.exception("Resume analysis validation failed.")

        return render_template(
            "index.html",
            error=str(error)
        )

    except Exception as error:

        app.logger.exception("Unexpected error while analyzing resumes.")

        return render_template(
            "index.html",
            error="Something went wrong while analyzing the resumes. Please try again later."
        )


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
