import json
import os
import re
import google.generativeai as genai

# ----------------------------
# Configure Gemini
# ----------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

model = None

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
    except Exception:
        model = None

# ----------------------------
# Load SHL Catalog
# ----------------------------

try:
    with open("catalog.json", "r", encoding="utf-8") as f:
        catalog = json.load(f)
except Exception:
    catalog = []


# ----------------------------
# Extract Keywords
# ----------------------------

def extract_keywords(text):
    words = re.findall(r"[a-zA-Z0-9+#.]+", text.lower())

    stop_words = {
        "i","need","an","a","the","for","with","and",
        "of","to","hire","hiring","looking","developer",
        "experience","years","year","role","assessment",
        "test","candidate","want"
    }

    return [w for w in words if w not in stop_words]


# ----------------------------
# Search Catalog
# ----------------------------

def search_catalog(query):

    keywords = extract_keywords(query)

    matches = []

    for item in catalog:

        searchable = " ".join([
            str(item.get("name","")),
            str(item.get("description","")),
            " ".join(item.get("keys",[])),
            " ".join(item.get("job_levels",[])),
            " ".join(item.get("languages",[])),
            str(item.get("duration",""))
        ]).lower()

        score = 0

        for word in keywords:
            if word in searchable:
                score += 1

        if score > 0:
            matches.append((score,item))

    matches.sort(key=lambda x:x[0], reverse=True)

    recommendations = []

    for score,item in matches[:5]:

        recommendations.append({
            "name": item.get("name",""),
            "url": item.get("link",""),
            "description": item.get("description",""),
            "duration": item.get("duration",""),
            "remote": item.get("remote",""),
            "adaptive": item.get("adaptive",""),
            "job_levels": item.get("job_levels",[])
        })

    return recommendations


# ----------------------------
# Main Chat Function
# ----------------------------

def chat_with_bot(messages):

    user_message = messages[-1].content

    lower = user_message.lower()

    # ----------------------------
    # Out of Scope
    # ----------------------------

    out_of_scope = [
        "weather",
        "movie",
        "cricket",
        "football",
        "politics",
        "legal",
        "salary",
        "stock",
        "bitcoin"
    ]

    if any(word in lower for word in out_of_scope):

        return (
            "I'm designed to answer only SHL assessment recommendation questions.",
            [],
            False
        )

    # ----------------------------
    # Clarification
    # ----------------------------

    if len(user_message.split()) < 3:

        return (
            "Please describe the role you're hiring for. Example: Hiring a Java developer with 3 years of experience.",
            [],
            False
        )

    # ----------------------------
    # Gemini Understanding
    # ----------------------------

    search_text = user_message

    if model:

        prompt = f"""
Extract the important hiring skills, technologies and role.

Sentence:
{user_message}

Return only keywords separated by commas.

Example:
Java, Spring Boot, Backend, Software Engineer
"""

        try:

            response = model.generate_content(prompt)

            if response.text:
                search_text = response.text.strip()

        except Exception:
            pass

    # ----------------------------
    # Search SHL Catalog
    # ----------------------------

    recommendations = search_catalog(search_text)

    if recommendations:

        return (
            f"I found {len(recommendations)} matching SHL assessments.",
            recommendations,
            True
        )

    return (
        "I couldn't find an exact match. Could you mention the programming language, technology, or job role?",
        [],
        False
    )