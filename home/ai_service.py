import os

from google import genai

from .models import Department, Doctor


def recommend_department(symptom, body_area, departments):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY")
    )

    department_list = ", ".join(departments)

    prompt = f"""
You are a hospital department recommendation assistant.

The patient may describe symptoms in English, Malayalam,
Manglish, or another language.

Your job is ONLY to recommend the most relevant hospital department
from the allowed list.

Allowed departments:
{department_list}

Patient's body area:
{body_area}

Patient's symptom description:
{symptom}

Rules:
- Do NOT diagnose a disease.
- Do NOT invent a department.
- Choose exactly ONE department from the allowed list.
- Use BOTH the body area and symptom description.
- Understand Malayalam and Manglish.
- Return ONLY valid JSON.
- Do not use Markdown.
- The JSON must contain exactly these two fields:
  "department"
  "reason"
- "department" must exactly match one department from the allowed list.
- "reason" must be short and explain why that department is relevant.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    import json

    try:
        result = json.loads(response.text)
    except (json.JSONDecodeError, TypeError):
        raise ValueError("AI returned an invalid response format.")

    department = result.get("department", "").strip()
    reason = result.get("reason", "").strip()

    if department not in departments:
        raise ValueError(
            f"AI returned an invalid department: {department}"
        )

    return {
        "department": department,
        "reason": reason
    }

def get_recommended_doctors(symptom, body_area):
    departments = list(
        Department.objects.values_list("name", flat=True)
    )

    ai_result = recommend_department(
        symptom,
        body_area,
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