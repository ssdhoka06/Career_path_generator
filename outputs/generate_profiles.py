import json
import random
from datetime import datetime, timedelta

random.seed(42)

CITIES = ["Bangalore", "Mumbai", "Pune", "Hyderabad", "Chennai", "Delhi", "Gurgaon", "Noida", "Kolkata", "Ahmedabad"]
STATES = {"Bangalore": "Karnataka", "Mumbai": "Maharashtra", "Pune": "Maharashtra",
          "Hyderabad": "Telangana", "Chennai": "Tamil Nadu", "Delhi": "Delhi",
          "Gurgaon": "Haryana", "Noida": "Uttar Pradesh", "Kolkata": "West Bengal", "Ahmedabad": "Gujarat"}

FIRST_NAMES = ["Rahul", "Priya", "Arjun", "Meera", "Karan", "Nisha", "Vikram", "Ananya", "Rohan", "Sneha",
               "Aditya", "Pooja", "Nikhil", "Kavya", "Siddharth", "Divya", "Amit", "Riya", "Suresh", "Anjali",
               "Rajesh", "Shruti", "Vivek", "Neha", "Akash", "Simran", "Deepak", "Kritika", "Manish", "Swati",
               "Varun", "Pallavi", "Santosh", "Madhuri", "Harish", "Lakshmi", "Sanjay", "Tanvi", "Ravi", "Preeti",
               "Gaurav", "Shweta", "Vishal", "Aarti", "Sachin", "Nidhi", "Dinesh", "Monisha", "Punit", "Rekha"]

LAST_NAMES = ["Sharma", "Patel", "Kumar", "Singh", "Reddy", "Nair", "Gupta", "Joshi", "Verma", "Shah",
              "Mehta", "Iyer", "Pillai", "Rao", "Khanna", "Malhotra", "Bhatia", "Chopra", "Shetty", "Patil",
              "Desai", "Thakur", "Chandra", "Mishra", "Banerjee", "Das", "Chatterjee", "Bose", "Ghosh", "Roy"]

DEGREES = ["B.Tech", "B.Sc", "MBA", "M.Tech", "BCA", "MCA", "B.Com", "B.E", "Diploma", "PhD", "B.Arch"]
FIELDS = ["Computer Science", "Electronics & Communication", "Mechanical Engineering", "Civil Engineering",
          "Information Technology", "Commerce", "Mathematics", "Physics", "MBA Finance", "MBA Marketing",
          "Electrical Engineering", "Chemical Engineering", "Biotechnology", "Data Science", "Arts"]

TIERS = ["Tier 1", "Tier 2", "Tier 3"]

IT_ROLES = ["Software Engineer", "Senior Software Engineer", "Full Stack Developer", "Backend Developer",
            "Frontend Developer", "DevOps Engineer", "Data Engineer", "Data Analyst", "ML Engineer",
            "QA Engineer", "Technical Lead", "Software Architect"]
FINANCE_ROLES = ["Financial Analyst", "Investment Analyst", "Credit Analyst", "Risk Analyst", "CA", "Accountant"]
ENGINEERING_ROLES = ["Mechanical Engineer", "Civil Engineer", "Electrical Engineer", "Production Engineer", "Design Engineer"]
EDUCATION_ROLES = ["Teacher", "Lecturer", "Tutor", "Training Manager", "Academic Coordinator"]
HEALTHCARE_ROLES = ["Clinical Data Analyst", "Health IT Consultant", "Biomedical Engineer", "Pharmacist"]

INDUSTRIES = {"IT": 0.60, "Finance": 0.15, "Engineering": 0.10, "Education": 0.10, "Healthcare": 0.05}

TECH_SKILLS_POOL = ["Python", "Java", "JavaScript", "React", "Node.js", "SQL", "C++", "C#", "Go",
                    "TypeScript", "AWS", "Docker", "Kubernetes", "TensorFlow", "PyTorch", "Machine Learning",
                    "Deep Learning", "NLP", "Computer Vision", "Data Analysis", "Excel", "Tableau",
                    "Power BI", "Spark", "Kafka", "Redis", "PostgreSQL", "MongoDB", "REST APIs",
                    "GraphQL", "Git", "Linux", "Terraform", "Ansible", "CI/CD", "Figma", "AutoCAD",
                    "MATLAB", "R", "Scala", "Flutter", "Android", "iOS", "Swift", "Kotlin"]

SOFT_SKILLS_POOL = ["Team Leadership", "Communication", "Problem Solving", "Critical Thinking",
                    "Public Speaking", "Time Management", "Mentoring", "Collaboration", "Adaptability",
                    "Negotiation", "Stakeholder Management", "Agile", "Project Management", "Presentation Skills"]

CERTIFICATIONS_POOL = ["AWS SAA", "AWS DevOps", "GCP Professional", "Azure Fundamentals", "CKA",
                       "PMP", "CEH", "CISSP", "Google Analytics", "Scrum Master", "ITIL", "CFA Level 1",
                       "Data Science Certificate", "TensorFlow Developer", "CompTIA Security+"]

INTEREST_DOMAINS = ["AI/ML", "Cybersecurity", "Product Management", "EdTech", "Cloud & DevOps",
                    "FinTech", "Healthcare IT", "Digital Marketing", "UI/UX Design", "Data Engineering",
                    "Full Stack Development", "Entrepreneurship", "Research & Academia", "Consulting"]

CAREER_GOALS = [
    "Transition into AI/ML engineering", "Become a data scientist", "Move into product management",
    "Start my own company", "Transition to teaching and education", "Build a career in cybersecurity",
    "Become a cloud architect", "Work in EdTech", "Move into FinTech", "Get into research",
    "Transition to UX design", "Become an engineering manager", "Work remotely for an international company",
    "Build expertise in GenAI", "Move from services to product company"
]

LIFE_EVENTS = ["None", "None", "None", "None", "New Parent", "Relocation", "Layoff", "Health Issue", "Divorce"]
WORK_PRIORITIES = ["Career Growth", "Work-Life Balance", "Financial Stability", "Purpose & Impact"]
WORK_STYLES = ["Remote", "Hybrid", "On-Site"]
EMPLOYMENT_STATUS = ["Employed Full-Time", "Employed Full-Time", "Employed Full-Time",
                     "Freelance", "Unemployed", "Student", "Part-Time"]
LIFE_STAGES = ["Early Career", "Mid Career", "Late Career", "Career Break", "Re-entering Workforce"]


def get_industry():
    r = random.random()
    cumulative = 0
    for industry, prob in INDUSTRIES.items():
        cumulative += prob
        if r <= cumulative:
            return industry
    return "IT"


def get_roles_for_industry(industry):
    mapping = {
        "IT": IT_ROLES, "Finance": FINANCE_ROLES,
        "Engineering": ENGINEERING_ROLES, "Education": EDUCATION_ROLES, "Healthcare": HEALTHCARE_ROLES
    }
    return random.choice(mapping[industry])


def get_salary(industry, experience, role):
    base_ranges = {
        "IT": {"entry": (4, 10), "mid": (12, 28), "senior": (28, 60)},
        "Finance": {"entry": (4, 8), "mid": (10, 20), "senior": (20, 40)},
        "Engineering": {"entry": (3, 6), "mid": (7, 15), "senior": (15, 28)},
        "Education": {"entry": (3, 5), "mid": (6, 12), "senior": (12, 22)},
        "Healthcare": {"entry": (4, 8), "mid": (9, 18), "senior": (18, 35)}
    }
    if experience < 3:
        level = "entry"
    elif experience < 8:
        level = "mid"
    else:
        level = "senior"
    low, high = base_ranges[industry][level]
    return round(random.uniform(low, high), 1)


def get_life_stage(age, employment_status):
    if employment_status == "Student":
        return "Early Career"
    if age < 27:
        return "Early Career"
    elif age < 35:
        return random.choice(["Early Career", "Mid Career"])
    elif age < 45:
        return random.choice(["Mid Career", "Mid Career", "Late Career"])
    else:
        return random.choice(["Mid Career", "Late Career"])


def get_burnout(age, experience, life_event):
    base = random.randint(1, 5)
    if experience > 5:
        base += random.randint(0, 2)
    if life_event in ["Layoff", "Divorce", "Health Issue"]:
        base += random.randint(2, 4)
    if age > 30 and experience > 6:
        base += random.randint(0, 2)
    return min(base, 10)


def compute_leadership_score(experience, certifications, soft_skills, role):
    score = 3.0
    score += min(experience * 0.3, 4.0)
    score += len(certifications) * 0.3
    score += len(soft_skills) * 0.2
    if any(word in role.lower() for word in ["lead", "senior", "manager", "architect", "director"]):
        score += 1.5
    return min(round(score, 1), 10.0)


def compute_alignment(skills, interest_domains):
    domain_skill_map = {
        "AI/ML": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "Deep Learning", "NLP"],
        "Cybersecurity": ["Linux", "CompTIA Security+", "CEH", "CISSP", "Python"],
        "Cloud & DevOps": ["AWS", "Docker", "Kubernetes", "Terraform", "CI/CD", "Linux"],
        "Full Stack Development": ["JavaScript", "React", "Node.js", "SQL", "REST APIs"],
        "Data Engineering": ["Python", "SQL", "Spark", "Kafka", "AWS", "PostgreSQL"],
        "FinTech": ["Python", "Java", "SQL", "REST APIs"],
        "UI/UX Design": ["Figma"],
        "Product Management": ["Agile", "Stakeholder Management", "SQL"],
    }
    if not interest_domains:
        return "Low"
    best_match = 0
    for domain in interest_domains:
        required = domain_skill_map.get(domain, [])
        if not required:
            best_match = max(best_match, 50)
            continue
        matches = len([s for s in skills if s in required])
        pct = matches / len(required) * 100
        best_match = max(best_match, pct)
    if best_match >= 70:
        return "High"
    elif best_match >= 40:
        return "Moderate"
    return "Low"


profiles = []
for i in range(1, 1001):
    user_id = f"user_{str(i).zfill(4)}"
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    
    # Age distribution peaking 24-32
    age_weights = list(range(22, 45))
    age_probs = []
    for a in age_weights:
        if 24 <= a <= 32:
            age_probs.append(4)
        elif 33 <= a <= 38:
            age_probs.append(2)
        else:
            age_probs.append(1)
    age = random.choices(age_weights, weights=age_probs, k=1)[0]
    
    gender_r = random.random()
    if gender_r < 0.62:
        gender = "Male"
    elif gender_r < 0.92:
        gender = "Female"
    else:
        gender = random.choice(["Non-Binary", "Prefer Not To Say"])
    
    city = random.choice(CITIES)
    state = STATES[city]
    
    # Institution tier weighted
    tier = random.choices(TIERS, weights=[15, 45, 40], k=1)[0]
    
    # Degree distribution
    industry = get_industry()
    if industry == "IT":
        degree = random.choices(DEGREES, weights=[40, 10, 5, 15, 10, 10, 0, 5, 2, 1, 2], k=1)[0]
        field = random.choice(["Computer Science", "Information Technology", "Electronics & Communication", "Mathematics"])
    elif industry == "Finance":
        degree = random.choices(["B.Com", "MBA", "B.Tech", "BCA"], weights=[35, 35, 20, 10], k=1)[0]
        field = random.choice(["Commerce", "MBA Finance", "Computer Science"])
    elif industry == "Engineering":
        degree = random.choices(["B.Tech", "B.E", "M.Tech", "Diploma"], weights=[50, 25, 15, 10], k=1)[0]
        field = random.choice(["Mechanical Engineering", "Civil Engineering", "Electrical Engineering"])
    elif industry == "Education":
        degree = random.choices(["B.Tech", "M.Tech", "B.Sc", "MBA"], weights=[35, 25, 25, 15], k=1)[0]
        field = random.choice(["Computer Science", "Mathematics", "Physics"])
    else:
        degree = random.choices(["B.Tech", "B.Sc", "MBA", "MCA"], weights=[30, 30, 20, 20], k=1)[0]
        field = random.choice(["Biotechnology", "Computer Science", "Information Technology"])
    
    current_role = get_roles_for_industry(industry)
    
    # Experience based on age
    max_exp = max(0.5, age - 22)
    experience = round(random.uniform(0.5, min(max_exp, age - 21)), 1)
    
    employment_status = random.choices(
        EMPLOYMENT_STATUS,
        weights=[60, 60, 60, 8, 5, 10, 7], k=1
    )[0]
    
    salary = get_salary(industry, experience, current_role)
    
    # Skills based on industry
    if industry == "IT":
        num_tech = random.randint(3, 8)
        tech_skills = random.sample(TECH_SKILLS_POOL[:25], min(num_tech, 25))
    else:
        num_tech = random.randint(2, 5)
        tech_skills = random.sample(TECH_SKILLS_POOL, min(num_tech, len(TECH_SKILLS_POOL)))
    
    num_soft = random.randint(2, 5)
    soft_skills = random.sample(SOFT_SKILLS_POOL, num_soft)
    
    num_certs = random.choices([0, 1, 2, 3], weights=[40, 35, 18, 7], k=1)[0]
    certifications = random.sample(CERTIFICATIONS_POOL, num_certs)
    
    interest_domains = random.sample(INTEREST_DOMAINS, random.randint(1, 3))
    career_goal = random.choice(CAREER_GOALS)
    work_style = random.choice(WORK_STYLES)
    willing_to_relocate = random.choice([True, False])
    target_timeline = random.choice([1, 2, 3, 5])
    
    life_stage = get_life_stage(age, employment_status)
    
    # Life event - new parent more likely 28-40
    if 28 <= age <= 40:
        life_event = random.choices(LIFE_EVENTS + ["New Parent"], weights=[1]*9 + [3], k=1)[0]
    else:
        life_event = random.choice(LIFE_EVENTS)
    
    burnout = get_burnout(age, experience, life_event)
    stress_tolerance = random.randint(max(1, 8 - burnout), min(10, 10 - burnout + 3))
    
    # Has dependents more likely 28+
    if age >= 28:
        has_dependents = random.choices([True, False], weights=[45, 55], k=1)[0]
    else:
        has_dependents = random.choices([True, False], weights=[10, 90], k=1)[0]
    
    # Work priority based on life stage
    if life_stage == "Early Career":
        work_priority = random.choices(WORK_PRIORITIES, weights=[50, 15, 25, 10], k=1)[0]
    elif life_stage == "Mid Career":
        work_priority = random.choices(WORK_PRIORITIES, weights=[25, 30, 25, 20], k=1)[0]
    else:
        work_priority = random.choices(WORK_PRIORITIES, weights=[15, 35, 25, 25], k=1)[0]
    
    leadership_score = compute_leadership_score(experience, certifications, soft_skills, current_role)
    alignment_category = compute_alignment(tech_skills, interest_domains)
    
    created_at = datetime.now() - timedelta(days=random.randint(0, 365))
    
    profile = {
        "user_id": user_id,
        "full_name": name,
        "age": age,
        "gender": gender,
        "location_city": city,
        "location_state": state,
        "highest_degree": degree,
        "field_of_study": field,
        "institution_tier": tier,
        "current_role": current_role,
        "current_industry": industry,
        "years_of_experience": experience,
        "employment_status": employment_status,
        "current_salary_lpa": salary,
        "technical_skills": tech_skills,
        "soft_skills": soft_skills,
        "certifications": certifications,
        "interest_domains": interest_domains,
        "career_goal": career_goal,
        "preferred_work_style": work_style,
        "willing_to_relocate": willing_to_relocate,
        "target_timeline_years": target_timeline,
        "life_stage": life_stage,
        "burnout_level": burnout,
        "stress_tolerance": stress_tolerance,
        "has_dependents": has_dependents,
        "recent_life_event": life_event,
        "work_life_priority": work_priority,
        "leadership_score": leadership_score,
        "alignment_category": alignment_category,
        "created_at": created_at.isoformat() + "Z",
        "updated_at": created_at.isoformat() + "Z"
    }
    profiles.append(profile)

with open("outputs/user_profiles.json", "w") as f:
    json.dump(profiles, f, indent=2)

print(f"Generated {len(profiles)} profiles")

# Print distribution stats
industries = [p["current_industry"] for p in profiles]
for ind in set(industries):
    print(f"{ind}: {industries.count(ind)} ({industries.count(ind)/len(profiles)*100:.1f}%)")

alignments = [p["alignment_category"] for p in profiles]
for a in ["High", "Moderate", "Low"]:
    print(f"Alignment {a}: {alignments.count(a)}")
