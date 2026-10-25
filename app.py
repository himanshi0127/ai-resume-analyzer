"""
AI-Based Resume Analyzer and Job Recommendation System
Main Flask application
"""

import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

from utils.parser import parse_resume
from utils.matcher import load_jobs, recommend_jobs
from utils.scorer import score_resume

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx"}
JOBS_CSV = "datasets/jobs.csv"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": "Only PDF and DOCX files are supported"
        }), 400

    filename = secure_filename(file.filename)

    if not filename:
        return jsonify({"error": "Invalid filename"}), 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    try:
        file.save(file_path)

        # Step 1: Parse resume
        parsed_data = parse_resume(file_path)

        # Step 2: Calculate score, strengths and recommendations
        resume_score = score_resume(parsed_data)

        # Step 3: Recommend suitable jobs
        jobs_df = load_jobs(JOBS_CSV)

        recommendations = recommend_jobs(
            resume_text=parsed_data["raw_text"],
            resume_skills=parsed_data["skills"],
            jobs_df=jobs_df,
            top_n=5
        )

        # Step 4: Prepare response for the frontend
        response = {
            "name": parsed_data["name"],
            "email": parsed_data["email"],
            "phone": parsed_data["phone"],
            "skills": parsed_data["skills"],
            "education": parsed_data["education"],
            "score": resume_score["score"],
            "feedback": resume_score["feedback"],
            "strengths": resume_score["strengths"],
            "recommendations": resume_score["recommendations"],
            "score_breakdown": resume_score["score_breakdown"],
            "recommended_jobs": recommendations
        }

        return jsonify(response)

    except Exception:
        app.logger.exception("Resume analysis failed")
        return jsonify({
            "error": (
                "Resume analysis failed. Check that the resume file is valid "
                "and the project files are configured correctly."
            )
        }), 500

    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                app.logger.warning("Could not remove uploaded file.")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
