document.getElementById("upload-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const fileInput = document.getElementById("resume");
    const errorDiv = document.getElementById("error");
    const loadingDiv = document.getElementById("loading");
    const resultsDiv = document.getElementById("results");
    const jobsBody = document.getElementById("jobs-body");

    const skillGapSection = document.getElementById("skill-gap-section");
    const skillGapContainer = document.getElementById("skill-gap-container");

    const strengthsList = document.getElementById("r-strengths");
    const recommendationsContainer =
        document.getElementById("recommendations-container");

    errorDiv.textContent = "";
    resultsDiv.style.display = "none";
    loadingDiv.style.display = "none";

    if (skillGapSection) skillGapSection.style.display = "none";

    if (!fileInput.files.length) {
        errorDiv.textContent = "Please select a resume file.";
        return;
    }

    const formData = new FormData();
    formData.append("resume", fileInput.files[0]);

    loadingDiv.style.display = "block";

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        loadingDiv.style.display = "none";

        if (!response.ok) {
            errorDiv.textContent = data.error || "Something went wrong.";
            return;
        }

        // 1. Extracted Information
        document.getElementById("r-name").textContent = data.name || "N/A";
        document.getElementById("r-email").textContent = data.email || "N/A";
        document.getElementById("r-phone").textContent = data.phone || "N/A";

        document.getElementById("r-education").textContent =
            Array.isArray(data.education) && data.education.length
                ? data.education.join(", ")
                : "N/A";

        document.getElementById("r-skills").textContent =
            Array.isArray(data.skills) && data.skills.length
                ? data.skills.join(", ")
                : "N/A";

        // 2. Resume Score
        const scoreValue = Number(data.score);
const scoreElement = document.getElementById("r-score");
const scoreRing = document.getElementById("score-ring");

if (Number.isFinite(scoreValue) && scoreValue >= 0 && scoreValue <= 100) {
    scoreElement.textContent = scoreValue;

    if (scoreRing) {
        const circumference = 2 * Math.PI * 62;
        const offset = circumference * (1 - scoreValue / 100);

        scoreRing.style.strokeDasharray = `${circumference}`;
        scoreRing.style.strokeDashoffset = `${offset}`;
    }
} else {
    scoreElement.textContent = "N/A";

    if (scoreRing) {
        scoreRing.style.strokeDashoffset = `${2 * Math.PI * 62}`;
    }
}

            // Resume Score Breakdown
        const breakdownContainer =
            document.getElementById("score-breakdown-container");

        if (breakdownContainer) {
            breakdownContainer.replaceChildren();

            (data.score_breakdown || []).forEach(item => {
                const card = document.createElement("div");
                card.style.margin = "12px 0";

                const label = document.createElement("p");
                label.textContent =
                    `${item.category}: ${item.earned}/${item.maximum}`;
                label.style.fontWeight = "bold";
                card.appendChild(label);

                const bar = document.createElement("div");
                bar.style.width = "100%";
                bar.style.height = "10px";
                bar.style.background = "#e1e7ef";
                bar.style.borderRadius = "8px";
                bar.style.overflow = "hidden";

                const fill = document.createElement("div");
                fill.style.height = "100%";
                fill.style.background = "#27845c";
                fill.style.borderRadius = "8px";

                const maximum = Number(item.maximum) || 0;
                const earned = Number(item.earned) || 0;
                const percentage = maximum > 0
                    ? Math.min(100, Math.max(0, earned / maximum * 100))
                    : 0;

                fill.style.width = percentage + "%";

                bar.appendChild(fill);
                card.appendChild(bar);
                breakdownContainer.appendChild(card);
            });
        }
        
        // 3. Resume Feedback
        const feedbackList = document.getElementById("r-feedback");
        feedbackList.replaceChildren();

        (data.feedback || []).forEach(message => {
            const li = document.createElement("li");
            li.textContent = message;
            feedbackList.appendChild(li);
        });

        // 4. Resume Strengths
        if (strengthsList) {
            strengthsList.replaceChildren();

            (data.strengths || []).forEach(strength => {
                const li = document.createElement("li");
                li.textContent = strength;
                strengthsList.appendChild(li);
            });
        }

        // 5. Resume Improvement Recommendations
        if (recommendationsContainer) {
            recommendationsContainer.replaceChildren();

            const recommendations = Array.isArray(data.recommendations)
                ? data.recommendations
                : [];

            if (recommendations.length > 0) {
                recommendations.forEach(rec => {
                    const card = document.createElement("div");

                    card.style.border = "1px solid #d9e1ec";
                    card.style.borderLeft = "4px solid #24569b";
                    card.style.borderRadius = "8px";
                    card.style.padding = "14px";
                    card.style.marginBottom = "12px";
                    card.style.background = "#f8faff";

                    const title = document.createElement("h3");
                    title.textContent = rec.title || "Improvement suggestion";
                    title.style.marginTop = "0";
                    title.style.color = "#173b70";
                    card.appendChild(title);

                    const priority = document.createElement("p");
                    priority.textContent =
                        "Priority: " + (rec.priority || "Medium");
                    priority.style.fontWeight = "bold";
                    card.appendChild(priority);

                    const reason = document.createElement("p");
                    reason.textContent =
                        "Why it matters: " + (rec.reason || "");
                    card.appendChild(reason);

                    const action = document.createElement("p");
                    action.textContent =
                        "What to do: " + (rec.action || "");
                    card.appendChild(action);

                    recommendationsContainer.appendChild(card);
                });
            } else {
                const message = document.createElement("p");
                message.textContent =
                    "No specific recommendations available. Your resume passed the main checks.";
                recommendationsContainer.appendChild(message);
            }
        }

        // 6. Recommended Jobs - Modern Job Cards
        jobsBody.replaceChildren();

        const recommendedJobs = Array.isArray(data.recommended_jobs)
            ? data.recommended_jobs
            : [];

        jobsBody.className = "jobs-grid";

        function formatSkills(skills) {
            if (Array.isArray(skills)) {
                return skills.length ? skills : [];
            }
            return skills ? String(skills).split(",").map(s => s.trim()) : [];
        }

        function createSkillTags(skills, type) {
            const wrapper = document.createElement("div");
            wrapper.className = "skill-tags";

            const items = formatSkills(skills);

            if (!items.length) {
                const empty = document.createElement("span");
                empty.textContent = "None";
                empty.className = "skill-tag neutral";
                wrapper.appendChild(empty);
                return wrapper;
            }

            items.forEach(skill => {
                const tag = document.createElement("span");
                tag.className = `skill-tag ${type}`;
                tag.textContent = skill;
                wrapper.appendChild(tag);
            });

            return wrapper;
        }

        if (recommendedJobs.length === 0) {
            const empty = document.createElement("p");
            empty.textContent = "No job recommendations available for this resume.";
            jobsBody.appendChild(empty);
        }

        recommendedJobs.forEach((job, index) => {
            const card = document.createElement("article");
            card.className = "job-card";

            const top = document.createElement("div");
            top.className = "job-card-top";

            const number = document.createElement("span");
            number.className = "job-number";
            number.textContent = `JOB ${String(index + 1).padStart(2, "0")}`;

            const match = document.createElement("span");
            match.className = "job-match";
            match.textContent = `${job.match_score ?? 0}% match`;

            top.append(number, match);
            card.appendChild(top);

            const title = document.createElement("h3");
            title.className = "job-title";
            title.textContent = job.title || "Recommended Role";
            card.appendChild(title);

            const company = document.createElement("p");
            company.className = "job-company";
            company.textContent = `▣  ${job.company || "Company not specified"}`;
            card.appendChild(company);

            const requiredHeading = document.createElement("h4");
            requiredHeading.textContent = "Required Skills";
            card.appendChild(requiredHeading);
            card.appendChild(createSkillTags(job.skills_required, "required"));

            const matchedHeading = document.createElement("h4");
            matchedHeading.textContent = "Your Matching Skills";
            card.appendChild(matchedHeading);
            card.appendChild(createSkillTags(job.matched_skills, "matched"));

            const missingHeading = document.createElement("h4");
            missingHeading.textContent = "Skills to Develop";
            card.appendChild(missingHeading);
            card.appendChild(createSkillTags(job.missing_skills, "missing"));

            jobsBody.appendChild(card);
        });

        // 7. Job-wise Skill Gap Analysis
        if (skillGapSection && skillGapContainer) {
            skillGapContainer.replaceChildren();

            const learningSuggestions = {
                "machine learning":
                    "Learn supervised and unsupervised learning. Practise with a small prediction project.",
                "statistics":
                    "Practise mean, median, standard deviation, probability, and data interpretation.",
                "javascript":
                    "Learn variables, functions, DOM manipulation, and events.",
                "react":
                    "Practise components, props, state, and hooks.",
                "excel":
                    "Practise formulas, sorting, filtering, and pivot tables.",
                "power bi":
                    "Learn dashboards, data visualization, and basic DAX.",
                "django":
                    "Learn Django models, views, URLs, and templates.",
                "rest api":
                    "Learn HTTP methods, JSON, API requests, and responses.",
                "tensorflow":
                    "Study neural network basics and build a beginner project.",
                "deep learning":
                    "Learn neural networks, backpropagation, and basic models."
            };

            const jobsWithGaps = recommendedJobs.filter(job =>
                Array.isArray(job.missing_skills) &&
                job.missing_skills.length > 0
            );

            if (jobsWithGaps.length > 0) {
                skillGapSection.style.display = "block";

                jobsWithGaps.forEach(job => {
                    const card = document.createElement("div");
                    card.className = "skill-card";

                    const title = document.createElement("h3");
                    title.textContent = job.title || "Recommended Job";
                    card.appendChild(title);

                    const company = document.createElement("p");
                    company.textContent = "Company: " + (job.company || "N/A");
                    card.appendChild(company);

                    const match = document.createElement("p");
                    match.textContent =
                        "Job Match: " + (job.match_score ?? 0) + "%";
                    card.appendChild(match);

                    const missingHeading = document.createElement("h4");
                    missingHeading.textContent = "Missing Skills";
                    card.appendChild(missingHeading);

                    const missingList = document.createElement("ul");

                    job.missing_skills.forEach(skill => {
                        const li = document.createElement("li");
                        li.textContent = skill;
                        missingList.appendChild(li);
                    });

                    card.appendChild(missingList);

                    const suggestionHeading = document.createElement("h4");
                    suggestionHeading.textContent = "Learning Suggestions";
                    card.appendChild(suggestionHeading);

                    const suggestionList = document.createElement("ul");

                    job.missing_skills.forEach(skill => {
                        const li = document.createElement("li");
                        const normalizedSkill = skill.toLowerCase().trim();

                        li.textContent =
                            skill + ": " +
                            (learningSuggestions[normalizedSkill] ||
                                `Learn the fundamentals of ${skill} and practise with a small project.`);

                        suggestionList.appendChild(li);
                    });

                    card.appendChild(suggestionList);
                    skillGapContainer.appendChild(card);
                });
            } else {
                skillGapSection.style.display = "none";
            }
        }

        // 8. Show Results
        resultsDiv.style.display = "block";

    } catch (err) {
        loadingDiv.style.display = "none";
        errorDiv.textContent =
            "Error connecting to server. Please try again.";

        console.error("Resume analysis error:", err);
    }
});