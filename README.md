# AI-Based Resume Analyzer and Job Recommendation System

An AI-powered web app that parses a resume (PDF/DOCX), extracts key
details (name, email, phone, skills, education), gives it an ATS-style
score, and recommends the top matching jobs using TF-IDF + Cosine
Similarity.

## Features
- Resume upload (PDF / DOCX)
- Automatic extraction of name, email, phone, skills, education
- ATS-friendliness scoring (out of 100) with improvement feedback
- Job recommendation engine (TF-IDF + Cosine Similarity)
- Simple web UI (HTML/CSS/JS + Flask backend)

## Project Structure
```
resume_analyzer/
├── app.py                 # Flask app (routes + orchestration)
├── requirements.txt
├── utils/
│   ├── parser.py           # Resume text extraction + info parsing
│   ├── matcher.py           # TF-IDF job matching
│   └── scorer.py            # ATS scoring logic
├── datasets/
│   └── jobs.csv             # Sample job postings (replace with real data)
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── uploads/                 # Temporary resume storage (auto-cleared)
```

## Setup Instructions

1. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://127.0.0.1:5000
   ```

5. Upload a `.pdf` or `.docx` resume and click **Analyze Resume**.

## How It Works
1. **Parsing** (`utils/parser.py`): Extracts raw text using `pdfplumber`
   (PDF) or `python-docx` (DOCX). Uses regex for email/phone and a
   predefined skill dictionary for skill matching.
2. **Scoring** (`utils/scorer.py`): Awards points for contact info,
   number of detected skills, education mention, and resume length —
   giving a score out of 100 with actionable feedback.
3. **Matching** (`utils/matcher.py`): Combines resume text + extracted
   skills into a query, vectorizes it alongside all job descriptions
   using TF-IDF, and ranks jobs by cosine similarity.

## Next Steps / Improvements
- Replace `datasets/jobs.csv` with a real job dataset (Kaggle, Adzuna
  API, LinkedIn Jobs API) or connect to a live jobs API.
- Use `spaCy` NER for more robust name/entity extraction.
- Use `sentence-transformers` (Sentence-BERT) instead of TF-IDF for
  better semantic matching.
- Add a database (MySQL/MongoDB) to store user resumes and job history.
- Add user authentication and a dashboard to track applications.
- Deploy on Render/Heroku/AWS.

## Notes
- Expand `SKILL_DB` in `utils/parser.py` with more skills relevant to
  your target job domains.
- The name extraction is a simple heuristic (first line of resume);
  for production use, consider spaCy's Named Entity Recognition (NER).
