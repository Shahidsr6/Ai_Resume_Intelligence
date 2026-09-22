from flask import Flask, render_template, request
from src.resume.analyzer import analyze_resume
import os
import re
import requests
from src.job_api import search_jobs
import time


app = Flask(__name__)

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

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        resume = request.files["resume"]

        if resume:

            print("Resume Received:", resume.filename)

            save_path = os.path.join("resumes", resume.filename)
            os.makedirs("resumes" , exist_ok=True)
            resume.save(save_path)

            print("Resume saved:", save_path)
            print("========== EXTRACTED RESUME TEXT ==========")
            print(resume)
            print("============================================")


            # =========================
            # RESUME ANALYSIS
            # =========================

            result = analyze_resume(save_path)

            resume_skills = result["resume_skills"]

            # Remove duplicate skills
            resume_skills = list(set(resume_skills))

            print("Resume Skills:", resume_skills)


            # =========================
            # MULTIPLE JOB SEARCH
            # =========================

        
            search_keywords = ["web developer"]


            # Remove duplicate search keywords
            search_keywords = list(
                dict.fromkeys(search_keywords)
            )


            print(
                "Job Search Keywords:",
                search_keywords
            )


            # =========================
            # SEARCH ALL JOBS
            # =========================

            all_jobs = []

            start_time = time.time()
            for keyword in search_keywords:
                print("Searching:", keyword)

                try:
                    job_data = search_jobs(keyword, "Pakistan")

                    all_jobs.extend(
                        job_data.get(
                             "data",
                               {}
                             ).get(
                            "jobs",
                                []
                            )
                             )

                except requests.exceptions.HTTPError as e:
                    print("Job API Error:", e)
                    continue

  
            print(
                "Total Jobs Found:",
                len(all_jobs)
            )


            # =========================
            # REMOVE DUPLICATE JOBS
            # =========================


            unique_jobs = {}

            for job in all_jobs:

                title = job.get("job_title", "").strip().lower()
                company = job.get("employer_name", ""
                ).strip().lower()

                # Create unique key using title + company
                job_key = title + "|" + company

                if job_key not in unique_jobs:

                    unique_jobs[job_key] = job


            jobs = {
                "results": list(
                    unique_jobs.values()
                )
            }

            # =========================
# FALLBACK JOBS
# =========================

            if len(jobs["results"]) == 0:

                jobs["results"] = [

            {
            "job_title": "Junior Web Developer",
            "employer_name": "Local Software Company",
            "job_city": "Pakistan",
            "job_country": "Pakistan",
            "job_apply_link": "https://www.rozee.pk/job/jsearch/q/junior%20Web%20Developer/",
            "job_description": "HTML CSS JavaScript PHP Web Development"
            },

            {
            "job_title": "Python Developer",
            "employer_name": "Software Company",
            "job_city": "Pakistan",
            "job_country": "Pakistan",
            "job_apply_link": "https://www.rozee.pk/job/jsearch/q/Python/",
            "job_description": "Python Web Development Flask Django"
            },

            {
            "job_title": "Frontend Developer",
            "employer_name": "Web Development Company",
            "job_city": "Pakistan",
            "job_country": "Pakistan",
            "job_apply_link": "https://www.rozee.pk/job/jsearch/q/Frontend/",
            "job_description": "HTML CSS JavaScript Bootstrap"
            },

            {
            "job_title": "PHP Developer",
            "employer_name": "Web Solutions Company",
            "job_city": "Pakistan",
            "job_country": "Pakistan",
            "job_apply_link": "https://www.rozee.pk/job/jsearch/q/PHP/",
            "job_description": "PHP HTML CSS JavaScript MySQL"
            },

            {
            "job_title": "Web Developer",
            "employer_name": "IT Company",
            "job_city": "Pakistan",
            "job_country": "Pakistan",
            "job_apply_link": "https://www.rozee.pk/job/jsearch/q/Web/",
            "job_description": "HTML CSS JavaScript PHP MySQL"
            }

             ]

            print(
            "Using fallback jobs:",
                len(jobs["results"])
                  )
            print(
                "Total Unique Jobs:",
                len(jobs["results"])
            )


            # =========================
            # JOB MATCHING
            # =========================

            recommended_jobs = []
            all_skills = ["python","javascript", "html","css","php","mysql","web development", "web designing", "graphics designing","social media marketing","java","c++","react","django","flask","node.js","mongodb","sql","bootstrap"
            ]

            for job in jobs.get(
                "results",
                []
            ):

                job_text = (
                    job.get("job_title", "")
                    + " "
                    + job.get("job_description", "")
                ).lower()


                job_required_skills = []


                for skill in all_skills:

                    if skill_exists(skill ,job_text):

                        job_required_skills.append(
                            skill
                        )

                # Remove duplicates
                matched = []
                for skill in resume_skills:
                    if skill.lower() in [s.lower() for s in job_required_skills]:
                        matched.append(skill)

                matched = list(set(matched))
                job_required_skills = list(set(job_required_skills))


                # =========================
                # MATCH PERCENTAGE
                # =========================
                print(" job required skills:", job_required_skills)
                print("Matched skills", matched)

                if resume_skills:

                    match_percentage = (
                        len(matched) * 100
                    ) / len(resume_skills)

                else:

                    match_percentage = 0


                job["match_percentage"] = round(
                    match_percentage,
                    1
                )

                job["matched_skills"] = matched


                recommended_jobs.append(
                    job
                )


            # =========================
            # SORT BY MATCH
            # =========================

            recommended_jobs.sort(
                key=lambda job:
                job.get(
                    "match_percentage",
                    0
                ),
                reverse=True
            )


            # =========================
            # TOP 5 JOBS
            # =========================

            recommended_jobs = (
                recommended_jobs[:5]
            )


            # =========================
            # PRINT RESULTS
            # =========================

            print(
                "\nRecommended Jobs:"
            )


            for job in recommended_jobs:

                print(
                    job.get("title"),
                    "-",
                    job.get(
                        "match_percentage"
                    ),
                    "%"
                )


            print(
                "Resume Skills:",
                resume_skills
            )


            # =========================
            # SEND TO HTML
            # =========================

            return render_template(
                "result.html",
                result=result,
                jobs=recommended_jobs
            )


    return render_template(
        "index.html"
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )