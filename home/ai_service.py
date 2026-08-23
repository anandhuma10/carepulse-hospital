import os

from google import genai

from .models import Department, Doctor


def recommend_department(symptom, departments):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY")
    )

    department_list = ", ".join(departments)

    prompt = f"""
You are a hospital department recommendation assistant.

The patient will describe their symptoms in English, Malayalam,
Manglish, or another language.

Your job is ONLY to recommend the most relevant hospital department
from the allowed list.

Allowed departments:
{department_list}

Patient description:
{symptom}

Rules:
- Do NOT diagnose a disease.
- Do NOT invent a department.
- Choose exactly ONE department from the allowed list.
- Understand Malayalam and Manglish.
- Return the department name on the first line.
- Return a short reason on the second line.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text.strip()

    lines = text.splitlines()

    department = lines[0].strip()
    reason = " ".join(lines[1:]).strip()

    if department not in departments:
        raise ValueError(
            f"AI returned an invalid department: {department}"
        )

    return {
        "department": department,
        "reason": reason
    }


def get_recommended_doctors(symptom):
    departments = list(
        Department.objects.values_list("name", flat=True)
    )

    ai_result = recommend_department(
        symptom,
        departments
    )

    department_name = ai_result["department"]

    department = Department.objects.filter(
        name__iexact=department_name
    ).first()

    if not department:
        return {
            "department": None,
            "reason": ai_result["reason"],
            "doctors": []
        }

    doctors = Doctor.objects.filter(
        department=department
    )

    return {
        "department": department.name,
        "reason": ai_result["reason"],
        "doctors": doctors
    }