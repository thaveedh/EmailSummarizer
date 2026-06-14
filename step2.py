import json
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.1-flash-lite")



email = """


Submit the client proposal by 5 PM today.

Extract any deadline if present.
If no deadline exists return empty string.
"""
response = model.generate_content(
    f"""
You are an intelligent email assistant.

Analyze the email and return ONLY valid JSON.

{{
    "summary":"",
    "priority":"",
    "action_items":[],
    "timeline":""
}}

Rules:
- Summary should be 2-3 lines maximum.
- Priority must be HIGH, MEDIUM, or LOW.
- Extract action items.
- Extract any deadline, meeting time, due date, or timeline into the deadline field.
- If none exists, return empty string.

Email:
{email}
"""
)
result = json.loads(response.text)

print("Summary:", result["summary"])
print("Priority:", result["priority"])
print("Actions:", result["action_items"])    
print("Deadline:", result["deadline"])