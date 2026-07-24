from __future__ import annotations

from .schemas import EducationItem, ProjectEvidence, SkillEvidence, StudentPreferences, StudentProfile


def _profiles() -> dict[str, StudentProfile]:
    class10 = StudentProfile(
        name="Aarav Sharma",
        stage="class10",
        current_class_or_program="Class 10",
        marks={"Mathematics": 88, "Science": 82, "English": 72, "Social Science": 68},
        aptitude={"Numerical": 90, "Logical": 86, "Scientific": 80, "Practical": 76, "Creative": 48, "Verbal": 61},
        interests=["Technology", "Engineering", "Coding", "Automation"],
        career_goal="Explore engineering and software careers.",
        preferences=StudentPreferences(
            location="Jammu",
            budget="medium",
            language="Hindi",
            work_styles=["Problem Solving", "Building", "Analysis"],
        ),
    )
    class12 = StudentProfile(
        name="Zoya Khan",
        stage="class12",
        current_class_or_program="Class 12",
        stream="Science PCB",
        marks={"Physics": 79, "Chemistry": 84, "Biology": 91, "English": 82, "Overall": 84},
        aptitude={"Scientific": 92, "Memory": 84, "Social": 80, "Logical": 73, "Practical": 76},
        entrance_readiness={"NEET": 78},
        interests=["Healthcare", "Medicine", "Biology", "Research"],
        career_goal="Work in healthcare while keeping a research alternative.",
        preferences=StudentPreferences(
            location="Srinagar",
            budget="low",
            language="Urdu",
            preferred_course_type="Government college",
            work_styles=["Caregiving", "Research", "Analysis"],
        ),
    )
    class12_arts = StudentProfile(
        name="Meera Arts Profile",
        stage="class12",
        current_class_or_program="Class 12",
        stream="Humanities",
        marks={"English": 84, "Political Science": 79, "History": 81, "Overall": 80},
        aptitude={"Verbal": 88, "Creative": 82, "Social": 85, "Logical": 60},
        interests=["Psychology", "Law", "Social Sciences"],
        career_goal="Study psychology or law.",
        preferences=StudentPreferences(location="Pune", budget="medium", language="English"),
    )
    college_demo = StudentProfile(
        name="Demo College Student",
        stage="college",
        current_class_or_program="B.Sc Computer Science student",
        education=[
            EducationItem(
                qualification="B.Sc",
                field="Computer Science",
                institution="Demo University",
                status="Second-year student",
                evidence="Coursework includes programming, databases, statistics, and introductory data science.",
            )
        ],
        skills=[
            SkillEvidence(
                name="Python",
                level="intermediate",
                evidence="Used Python and Pandas to clean and analyse student-placement data.",
                contexts=["data analysis", "automation", "machine learning"],
            ),
            SkillEvidence(
                name="SQL",
                level="intermediate",
                evidence="Wrote SQL queries for a placement and internship database.",
                contexts=["database", "data analysis", "reporting"],
            ),
            SkillEvidence(
                name="Statistics",
                level="beginner",
                evidence="Applied descriptive statistics and correlation analysis in coursework.",
                contexts=["statistics", "analysis"],
            ),
            SkillEvidence(
                name="Data Visualization",
                level="intermediate",
                evidence="Built a Power BI dashboard for placement trends.",
                contexts=["dashboard", "reporting", "business insights"],
            ),
            SkillEvidence(
                name="Machine Learning",
                level="beginner",
                evidence="Trained and evaluated a basic classification model for internship eligibility.",
                contexts=["model evaluation", "prediction", "data cleaning"],
            ),
            SkillEvidence(
                name="Excel/Power BI",
                level="intermediate",
                evidence="Used spreadsheets and Power BI to gather reporting requirements and map a placement-analysis process.",
                contexts=["requirement gathering", "process mapping", "dashboard", "business analysis"],
            ),
        ],
        projects=[
            ProjectEvidence(
                name="Campus Placement Insights Dashboard",
                summary="A Python, SQL, and Power BI project analysing placement patterns and student skill trends.",
                technologies=["Python", "Pandas", "SQL", "Power BI"],
                capabilities=["data analysis", "dashboard", "reporting", "business insights", "data visualization", "requirement gathering", "process mapping"],
                status="Completed",
            ),
            ProjectEvidence(
                name="Internship Eligibility Classifier",
                summary="A beginner machine-learning model with documented evaluation and limitations.",
                technologies=["Python", "scikit-learn", "Pandas"],
                capabilities=["machine learning", "prediction", "model evaluation", "data cleaning"],
                status="Completed",
            ),
        ],
        certifications=["Python fundamentals course"],
        interests=["Data & Analytics", "Artificial Intelligence", "Business", "Analytics", "Technology"],
        career_goal="Choose between data science, AI/ML, and business analytics pathways.",
        preferences=StudentPreferences(
            location="India",
            budget="medium",
            language="English",
            work_styles=["Analysis", "Problem Solving", "Building"],
        ),
    )
    dashboard = StudentProfile(
        name="Dashboard Portfolio",
        stage="college",
        current_class_or_program="B.Com Business Analytics graduate",
        education=[EducationItem(qualification="B.Com", field="Business Analytics", institution="Demo University", status="Graduate", evidence="Studied business statistics and analytics.")],
        skills=[
            SkillEvidence(name="SQL", level="intermediate", evidence="Queried sales and customer data.", contexts=["analysis", "business insights"]),
            SkillEvidence(name="Power BI", level="intermediate", evidence="Created interactive sales dashboards.", contexts=["dashboard", "reporting", "data visualization"]),
            SkillEvidence(name="Excel", level="advanced", evidence="Built financial models and reports.", contexts=["analysis", "reporting"]),
            SkillEvidence(name="Python", level="beginner", evidence="Used Pandas for data cleaning.", contexts=["data cleaning", "analysis"]),
        ],
        projects=[ProjectEvidence(name="Retail Sales Dashboard", summary="Analysed sales trends and customer segments for management reporting.", technologies=["Power BI", "SQL", "Excel", "Pandas"], capabilities=["dashboard", "business insights", "reporting", "data analysis"], status="Completed")],
        interests=["Data & Analytics", "Business", "Finance"],
        career_goal="Start in business or data analytics.",
        preferences=StudentPreferences(location="Mumbai", budget="low", language="English"),
    )
    ux = StudentProfile(
        name="UX Portfolio",
        stage="college",
        current_class_or_program="B.Des Interaction Design student",
        education=[EducationItem(qualification="B.Des", field="Interaction Design", institution="Demo Design School", status="Student", evidence="Studying interaction and visual design.")],
        skills=[
            SkillEvidence(name="Figma", level="advanced", evidence="Designed mobile and web prototypes.", contexts=["prototype", "design system"]),
            SkillEvidence(name="User Research", level="intermediate", evidence="Conducted interviews and usability tests.", contexts=["usability testing", "user research"]),
            SkillEvidence(name="Wireframing", level="advanced", evidence="Created low and high fidelity flows.", contexts=["wireframing", "prototype"]),
            SkillEvidence(name="Visual Design", level="intermediate", evidence="Built reusable design systems.", contexts=["design system", "visual design"]),
        ],
        projects=[ProjectEvidence(name="Public Transport App Redesign", summary="Redesigned ticket booking based on interviews and usability tests.", technologies=["Figma"], capabilities=["ux redesign", "prototype", "usability testing", "design system"], status="Completed")],
        interests=["Product Design", "Design", "User Research"],
        career_goal="Become a product designer or UX researcher.",
        preferences=StudentPreferences(location="Bengaluru", budget="medium", language="English"),
    )
    return {
        "class10": class10,
        "class12": class12,
        "class12_arts": class12_arts,
        "college_demo": college_demo,
        "dashboard": dashboard,
        "ux": ux,
    }


def parse_known_demo(profile_name: str) -> StudentProfile:
    """Return stable sample profiles for offline orchestration and tests."""

    profiles = _profiles()
    try:
        return profiles[profile_name]
    except KeyError as exc:
        raise ValueError(f"Unknown profile: {profile_name}") from exc
