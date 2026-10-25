"""
Resume Scoring and Improvement Recommendation Module.
Calculates a resume score out of 100 and provides
personalized feedback and improvement recommendations.
"""


def score_resume(parsed_data):
    score = 0
    feedback = []
    strengths = []
    recommendations = []

    # 1. Contact Information: 20 points
    contact_score = 0

    if parsed_data.get("email"):
        contact_score += 10
        strengths.append("Email address detected.")
    else:
        feedback.append("Add a valid email address.")
        recommendations.append({
            "title": "Add your email address",
            "priority": "High",
            "reason": "Recruiters need a way to contact you.",
            "action": (
                "Add a professional email address near the top "
                "of your resume."
            )
        })

    if parsed_data.get("phone"):
        contact_score += 10
        strengths.append("Phone number detected.")
    else:
        feedback.append("Add a valid phone number.")
        recommendations.append({
            "title": "Add your phone number",
            "priority": "High",
            "reason": "Recruiters need your contact number.",
            "action": (
                "Add your correct phone number in the contact section."
            )
        })

    score += contact_score

    # 2. Skills: 30 points
    skills = parsed_data.get("skills", [])
    skill_count = len(set(skills))

    if skill_count >= 8:
        skills_score = 30
        strengths.append("Good range of recognizable skills.")
    elif skill_count >= 5:
        skills_score = 22
        feedback.append("Consider adding more relevant skills.")
    elif skill_count >= 1:
        skills_score = 12
        feedback.append(
            "Add a dedicated Skills section with relevant skills."
        )
    else:
        skills_score = 0
        feedback.append(
            "No recognizable skills found. Add relevant skills."
        )

    score += skills_score

    if skill_count < 8:
        recommendations.append({
            "title": "Improve your Skills section",
            "priority": "High" if skill_count < 5 else "Medium",
            "reason": (
                f"The analyzer recognized {skill_count} skills."
            ),
            "action": (
                "List relevant technical and soft skills you genuinely "
                "possess. Include suitable programming languages, "
                "tools, and technologies."
            )
        })

    # 3. Education: 15 points
    education = parsed_data.get("education", [])

    if education:
        education_score = 15
        strengths.append("Education information detected.")
    else:
        education_score = 0
        feedback.append(
            "Mention your degree and qualification clearly."
        )
        recommendations.append({
            "title": "Complete your Education section",
            "priority": "High",
            "reason": (
                "Education helps recruiters understand your qualifications."
            ),
            "action": (
                "Mention your degree, institution, expected graduation "
                "year, and relevant coursework where appropriate."
            )
        })

    score += education_score

    # 4. Resume Sections: 20 points
    sections = {
        str(section).strip().lower()
        for section in parsed_data.get("sections", [])
    }

    section_points = {
        "projects": 8,
        "experience": 5,
        "certifications": 3,
        "achievements": 2,
        "summary": 2
    }

    section_score = min(
        sum(
            points
            for section, points in section_points.items()
            if section in sections
        ),
        20
    )

    score += section_score

    # Project recommendation
    if "projects" not in sections:
        feedback.append(
            "No Projects section was detected. Relevant projects "
            "can demonstrate practical skills."
        )
        recommendations.append({
            "title": "Add a Projects section",
            "priority": "High",
            "reason": (
                "Projects help recruiters understand how you apply "
                "your knowledge and solve practical problems."
            ),
            "action": (
                "Add genuine academic or personal projects. Mention "
                "the project name, objective, technologies used, "
                "your contribution, main features, and outcome. "
                "Include a GitHub link if available. Never list "
                "a project you have not actually worked on."
            )
        })

    # Summary recommendation
    if "summary" not in sections:
        feedback.append(
            "Consider adding a short career objective or summary."
        )
        recommendations.append({
            "title": "Write a professional summary",
            "priority": "Medium",
            "reason": (
                "A short introduction helps recruiters understand "
                "your background and career goals."
            ),
            "action": (
                "Write 2-3 sentences about your education, key skills, "
                "career interests, and target role."
            )
        })

    # Experience recommendation
    if "experience" not in sections:
        feedback.append(
            "No internship or work experience section was detected. "
            "Students can highlight practical learning instead."
        )
        recommendations.append({
            "title": "Highlight practical learning",
            "priority": "Medium",
            "reason": (
                "Practical experience can demonstrate your abilities, "
                "but formal work experience is not compulsory for students."
            ),
            "action": (
                "If applicable, mention internships, training, "
                "volunteering, or practical work. If you have no formal "
                "experience, focus on genuine academic projects and "
                "coursework instead."
            )
        })

    # Certifications recommendation
    if "certifications" not in sections:
        recommendations.append({
            "title": "Add relevant certifications",
            "priority": "Low",
            "reason": (
                "Relevant certifications can support your skills."
            ),
            "action": (
                "List genuine completed courses or certifications, "
                "including the provider when appropriate."
            )
        })

    # Achievements recommendation
    if "achievements" not in sections:
        recommendations.append({
            "title": "Highlight achievements",
            "priority": "Low",
            "reason": (
                "Relevant achievements can show your progress "
                "and accomplishments."
            ),
            "action": (
                "Mention genuine awards, competition results, "
                "academic accomplishments, or measurable project "
                "outcomes if applicable."
            )
        })

    # 5. Resume Content Depth: 15 points
    raw_text = parsed_data.get("raw_text", "")
    word_count = len(raw_text.split())

    if word_count >= 300:
        content_score = 15
        strengths.append(
            "Resume contains a reasonable amount of detail."
        )
    elif word_count >= 150:
        content_score = 10
        feedback.append(
            "Add useful details about projects and achievements."
        )
    elif word_count >= 75:
        content_score = 5
        feedback.append(
            "Resume content appears brief; add relevant details."
        )
    else:
        content_score = 0
        feedback.append(
            "Very little text was extracted. Check the resume file."
        )

    score += content_score

    if word_count < 300:
        recommendations.append({
            "title": "Add meaningful details",
            "priority": "Medium",
            "reason": (
                f"The analyzer extracted approximately {word_count} words."
            ),
            "action": (
                "Describe relevant projects, responsibilities, tools, "
                "and outcomes. Keep the information clear and avoid "
                "unnecessary repetition."
            )
        })

    # Default feedback and strengths
    if not feedback:
        feedback.append(
            "Good work! The main resume checks passed."
        )

    if not strengths:
        strengths.append(
            "Your resume has been analyzed. Review the recommendations "
            "to identify areas for improvement."
        )

    # 6. Score Breakdown
    score_breakdown = [
        {
            "category": "Contact Information",
            "earned": contact_score,
            "maximum": 20
        },
        {
            "category": "Skills",
            "earned": skills_score,
            "maximum": 30
        },
        {
            "category": "Education",
            "earned": education_score,
            "maximum": 15
        },
        {
            "category": "Resume Sections",
            "earned": section_score,
            "maximum": 20
        },
        {
            "category": "Content Depth",
            "earned": content_score,
            "maximum": 15
        }
    ]

    return {
        "score": min(score, 100),
        "feedback": feedback,
        "strengths": strengths,
        "recommendations": recommendations,
        "score_breakdown": score_breakdown,
        "word_count": word_count,
        "skill_count": skill_count
    }