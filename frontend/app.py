import os
import requests
import json
import gradio as gr
from dotenv import load_dotenv
from tools.student_tool import query_student_info

load_dotenv()

def ask_ai(user_input):
    model = os.getenv("LLM_MODEL", "openai/gpt-3.5-turbo")
    api_key = os.getenv("OPENROUTER_API_KEY")
    base_url = os.getenv("API_BASE", "http://localhost:3001")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost:7860",
        "X-Title": "School Management MCP",
        "Content-Type": "application/json"
    }

    # ✅ 1. Try to interpret input as a student ID
    try:
        student_id = int(user_input)
        data = query_student_info(student_id)
        if not data:
            return "No data found for this student."
        name = data[0]['student_name']
        grade = data[0]['grade_name']
        subjects = [row['subject_name'] for row in data]
        return f"{name} is in {grade} and is taking: {', '.join(subjects)}."
    except ValueError:
        pass  # Not a number, try parsing with OpenRouter

    # ✅ 2. Check if question is about a subject ("Who is taking Science?")
    if "who" in user_input.lower() and "taking" in user_input.lower():
        subject_prompt = f"""Extract the subject from this question: \"{user_input}\".
Only reply with the subject name like 'Math', 'Science', etc., or say 'invalid'."""

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": subject_prompt}],
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            return "OpenRouter error: " + response.text

        subject = response.json()["choices"][0]["message"]["content"].strip()
        if subject.lower() == "invalid":
            return "Could not determine the subject from your question."

        r = requests.get(f"{base_url}/student/subject/{subject}/students")
        if r.status_code != 200 or not r.json():
            return f"No students found taking {subject}."

        data = r.json()
        names = [f"{row['student_name']} ({row['grade_name']})" for row in data]
        return f"The following students are taking {subject}: {', '.join(names)}."

    # ✅ 3. Try extracting student ID from natural language
    id_prompt = f"""Extract the student ID from this question: \"{user_input}\".
If none is found, reply ONLY with the word: 'invalid'."""

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": id_prompt}],
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return "OpenRouter error: " + response.text

    content = response.json()["choices"][0]["message"]["content"].strip()
    if content.lower() == "invalid":
        return "Could not extract a valid student ID from your question."

    try:
        student_id = int(content)
        data = query_student_info(student_id)
    except:
        return "Model response wasn't a valid number or student not found."

    if not data:
        return "No data found for this student."

    name = data[0]['student_name']
    grade = data[0]['grade_name']
    subjects = [row['subject_name'] for row in data]
    return f"{name} is in {grade} and is taking: {', '.join(subjects)}."

# ✅ Gradio Interface
demo = gr.Interface(
    fn=ask_ai,
    inputs=gr.Textbox(label="Ask a question or enter a student ID"),
    outputs="text",
    title="Student Subject Lookup (OpenRouter + Gradio)"
)

if __name__ == "__main__":
    print("Launching Gradio...")
    demo.launch(mcp_server=True)
