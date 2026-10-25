"""
Advanced Job Matching Module
Combines TF-IDF text similarity and required-skill overlap.
Returns ranked jobs with matched and missing skills.
"""

import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


ALIASES = {
    "ml": "machine learning",
    "sklearn": "scikit learn",
    "scikit learn library": "scikit learn",
    "js": "javascript",
    "nodejs": "node.js",
    "node js": "node.js",
    "powerbi": "power bi",
    "ms excel": "excel",
    "microsoft excel": "excel",
}


def normalize_skill(skill):
    """Normalize skill names for comparison."""
    skill = str(skill).lower().strip()
    return re.sub(r"[\s_-]+", " ", skill)


def canonical_skill(skill):
    """Standardize common skill aliases."""
    normalized = normalize_skill(skill)
    return ALIASES.get(normalized, normalized)


def split_skills(value):
    """Split comma-, semicolon-, pipe-, or newline-separated skills."""
    if value is None or pd.isna(value):
        return []

    return [
        item.strip()
        for item in re.split(r"[,;\n|]+", str(value))
        if item.strip()
    ]


def load_jobs(csv_path="datasets/jobs.csv"):
    """Load and validate the jobs dataset."""
    jobs = pd.read_csv(csv_path)

    required_columns = [
        "job_id", "title", "company", "skills_required"
    ]

    missing = [
        column for column in required_columns
        if column not in jobs.columns
    ]

    if missing:
        raise ValueError(
            f"Jobs dataset is missing columns: {', '.join(missing)}"
        )

    if "description" not in jobs.columns:
        jobs["description"] = ""

    return jobs


def recommend_jobs(resume_text, resume_skills, jobs_df, top_n=5):
    """
    Rank jobs using:
    65% TF-IDF text similarity
    35% required-skill overlap.

    If none of a job's required skills match, its final score
    is capped at 65% of its text-similarity score.
    """

    if jobs_df is None or jobs_df.empty:
        return []

    jobs = jobs_df.copy()

    required_columns = [
        "job_id", "title", "company", "skills_required"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in jobs.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(missing_columns)}"
        )

    if "description" not in jobs.columns:
        jobs["description"] = ""

    for column in [
        "title", "company", "description", "skills_required"
    ]:
        jobs[column] = jobs[column].fillna("").astype(str)

    resume_text = str(resume_text or "")

    resume_skill_set = {
        canonical_skill(skill)
        for skill in (resume_skills or [])
        if normalize_skill(skill)
    }

    job_texts = (
        jobs["title"] + " " +
        jobs["description"] + " " +
        jobs["skills_required"]
    ).tolist()

    resume_query = (
        resume_text + " " +
        " ".join(sorted(resume_skill_set))
    ).strip()

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True,
        )

        matrix = vectorizer.fit_transform(
            job_texts + [resume_query]
        )

        text_scores = cosine_similarity(
            matrix[-1], matrix[:-1]
        ).flatten().tolist()

    except ValueError:
        text_scores = [0.0] * len(jobs)

    skill_scores = []
    matched_lists = []
    missing_lists = []

    for required_text in jobs["skills_required"]:
        required_display = split_skills(required_text)

        matched = []
        missing = []
        unique_required = set()
        seen = set()

        for display_name in required_display:
            canonical = canonical_skill(display_name)

            if not canonical or canonical in seen:
                continue

            seen.add(canonical)
            unique_required.add(canonical)

            if canonical in resume_skill_set:
                matched.append(display_name)
            else:
                missing.append(display_name)

        matched_lists.append(matched)
        missing_lists.append(missing)

        if unique_required:
            overlap = unique_required.intersection(resume_skill_set)
            skill_score = len(overlap) / len(unique_required)
        else:
            skill_score = 0.0

        skill_scores.append(skill_score)

    final_scores = []

    for text_score, skill_score in zip(text_scores, skill_scores):
        score = (0.65 * text_score) + (0.35 * skill_score)

        # Penalize jobs when none of the required skills match.
        if skill_score == 0:
            score = 0.25 * text_score

        final_scores.append(score)

    jobs["match_score"] = [
        round(score * 100, 2)
        for score in final_scores
    ]

    jobs["matched_skills"] = matched_lists
    jobs["missing_skills"] = missing_lists

    jobs = jobs.sort_values(
        by="match_score",
        ascending=False,
        kind="stable",
    ).head(max(0, int(top_n)))

    return jobs[
        [
            "job_id",
            "title",
            "company",
            "skills_required",
            "match_score",
            "matched_skills",
            "missing_skills",
        ]
    ].to_dict(orient="records")