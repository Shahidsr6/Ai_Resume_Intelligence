from .reader import read_resume
import re

def skill_exists(skill,text):
    """Check whether a skil exsists as a 
    complete word/phrase.
    prevents:java-> javascript
    SQL ->MySQL
    """
    skill = skill.lower().strip()
    text = text.lower()
    pattern = r"(?<![a-z0-9+#.])" + re.escape(skill) + r"(?![a-z0-9+#.])"
    return bool(re.search(pattern,text))

def extract_skills_from_resume(resume_text):

    text = resume_text.lower()

    # Possible headings for different CVs
    skill_headings = [
        "technical skills",
        "technical skill",
        "skills",
        "skill",
        "key skills",
        "core skills",
        "professional skills",
        "programming skills",
        "computer skills"
    ]

    # Possible sections that come after Skills
    next_section_headings = [
        "education",
        "experience",
        "work experience",
        "professional experience",
        "projects",
        "project",
        "certifications",
        "certificate",
        "language",
        "languages",
        "career objective",
        "objective",
        "professional summary",
        "summary",
        "profile",
        "about me"
    ]

    skills_section = ""

    # Find a skills heading
    for heading in skill_headings:

        pattern = r"(?m)^\s*" + re.escape(heading) + r"\s*$"
        match = re.search(pattern, text)

        if match:

            start = match.end()

            # Find where next section starts
            end = len(text)

            for next_heading in next_section_headings:

                next_pattern = r"(?m)^\s*" + re.escape(next_heading) + r"\s*$"
                next_match = re.search(
                    next_pattern,
                    text[start:]
                )

                if next_match:

                    possible_end = start + next_match.start()

                    if possible_end < end:
                        end = possible_end

            skills_section = text[start:end]

            break

    print("========== SKILLS SECTION ==========")
    print(skills_section)
    print("====================================")

    # Our known skills vocabulary
    known_skills = [
        "python",
        "java",
        "c++",
        "c#",
        "javascript",
        "html",
        "css",
        "php",
        "mysql",
        "sql",
        "bootstrap",
        "django",
        "flask",
        "fastapi",
        "react",
        "node.js",
        "nodejs",
        "angular",
        "mongodb",
        "jupyterlab",
        "pandas",
        "numpy",
        "machine learning",
        "deep learning",
        "web development",
        "web designing",
        "graphics designing",
        "social media marketing"
    ]

    detected_skills = []

    for skill in known_skills:

        if skill_exists(skill , skills_section):

            detected_skills.append(skill)

            print("Skill found:", skill)

    return list(dict.fromkeys(detected_skills))


def analyze_resume(file_path):

    # IMPORTANT:
    # Use the uploaded file path
    resume = read_resume(file_path)

    print("========== EXTRACTED RESUME TEXT ==========")
    print(resume)
    print("============================================")

    # ==================================
    # EXTRACT ACTUAL RESUME SKILLS
    # ==================================

    resume_skills = extract_skills_from_resume(resume)

    print("Resume Skills:", resume_skills)

    # ==================================
    # JOB REQUIRED SKILLS
    # ==================================

    job_skills = [
        "html",
        "css",
        "javascript",
        "php",
        "mysql",
        "web development"
    ]

    job_skills = list(
        dict.fromkeys(
            skill.lower().strip()
            for skill in job_skills
        )
    )

    # ==================================
    # MATCH SKILLS
    # ==================================

    matched_skills = []
    missing_skills = []

    for skill in job_skills:

        if skill in resume_skills:

            matched_skills.append(skill)

        else:

            missing_skills.append(skill)

    # ==================================
    # JOB MATCH %
    # ==================================

    if job_skills:

        job_matched_percentage = round(
            len(matched_skills) * 100 / len(job_skills),
            1
        )

    else:

        job_matched_percentage = 0

    # ==================================
    # RESUME SCORE
    # ==================================

    skill_scores = {
    "python": 3.5,
    "javascript": 3.5,
    "php": 3.0,
    "html": 3.5,
    "css": 3.0,
    "mysql": 3.0,
    "django": 3.0,
    "flask": 2.5,
    "node.js": 3.0,
    "java": 2.0,
}

    skills_score = 0

    for skill, marks in skill_scores.items():

        if re.search(r"\b" + re.escape(skill.lower()) + r"\b" , resume.lower()):

            skills_score += marks

    skills_score = round(skills_score, 1)

    score = skills_score
    

    # ==================================
    # EDUCATION
    # ==================================

    education_keywords = [
        "matric",
        "intermediate",
        "bs",
        "bsc",
        "ms",
        "msc",
        "phd"
    ]

    education_found = []

    for edu in education_keywords:

        if edu.lower() in resume.lower():

            education_found.append(edu)

   # ==================================
    # EDUCATION SCORE
    # ==================================

    education_score = 0

    if "bs" in education_found or "bsc" in education_found:
        education_score = 3.5+4.5+5.5

    elif "ms" in education_found or "msc" in education_found:
        education_score = 3.5 + 4.5 + 5.5 + 6.5

    elif "phd" in education_found :
        education_score = 3.5 + 4.5+ 5.5 +6.5 + 6.5

    elif "intermediate" in education_found:
        education_score = 3.5 + 4.5

    elif "matric" in education_found:
        education_score = 3.5

    education_score = round(education_score, 1)
    # ==================================
    # EXPERIENCE
    # ==================================

    experience_text = resume.lower()
    experience_months = 0
    year_match = re.search(
    r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
    experience_text
)

    if year_match:
        years = float(year_match.group(1))
        experience_months = int(years*12)
    else:
        month_match = re.search(r"(\d+)\s*(?:months?)|mos?" ,experience_text)
        if month_match:
            months =month_match.group(1)
            if months is not None:
                experience_months = int(months)


    experience_score = 0
    if experience_months ==0:
        experience_score = 5

    elif experience_months < 12:
        experience_score = 12

    elif experience_months < 24:
        experience_score = 15

    elif experience_months < 36:
        experience_score = 18

    elif experience_months < 48:
        experience_score = 20

    elif experience_months < 60:
        experience_score = 23

    else:
        experience_score = 25

    experience_score = round(experience_score ,1)

    experience_found = []
    if experience_months > 0:
        experience_found.append(str(round(experience_months/12 , 1)))

    
    # ==================================
    # PROJECTS
    # ==================================

    projects_found = []
    project_count = 0
    project_score = 0
    projects_keywords = ["final year project", "project","projects", "github"]

    for project in projects_keywords:

        if project.lower() in resume.lower():

            projects_found.append(project)

    if "final year project" in projects_found:
        project_count += 1

    if "project" in projects_found:
        project_count += 1

    if "projects" in projects_found:
        project_count += 1

    if "github" in projects_found:
        project_count +=1

    if project_count == 0:
        project_score = 0

    elif project_count == 1:
        project_score = 7

    elif project_count == 2:
        project_score =13

    elif project_count == 3:
        project_score = 18

    else :
        project_score = 25 


    percentage = skills_score + project_score + education_score + experience_score    

    # ==================================
    # PRINT RESULTS
    # ==================================

    print("\n========== RESUME ANALYSIS ==========")
    print("Resume Skills:", resume_skills)
    print("Matched Skills:", matched_skills)
    print("Missing Skills:", missing_skills)
    print("Resume Percentage:", percentage)
    print("Job Match Percentage:", job_matched_percentage)
    print("Education:", education_found)
    print("Education score", education_score)
    print("Experience:", experience_found)
    print("experience Score", experience_score)
    print("Projects:", projects_found)
    print("Project count:", project_count)
    print("Project Score:", project_score)
    print("====================================")

    return {
        "resume_skills": resume_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "score": score,
        "resume_percentage": percentage,
        "job_match_percentage": job_matched_percentage,
        "education": education_found,
        "experience": experience_found,
        "experience score": experience_score,
        "projects": projects_found,
        "projects_count": project_count,
        "project_score": project_score,
        "job_skills": job_skills,
        "skills_score":skills_score,
        "education_score":education_score,
        "experience_score":experience_score,
        "project_score":project_score
    }