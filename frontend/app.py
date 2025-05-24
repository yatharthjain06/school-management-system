import os
import requests
import gradio as gr
from dotenv import load_dotenv
from tools.student_tool import query_student_info, get_student_id_by_name

load_dotenv()

def ask_school_assistant(question: str) -> dict:
    """
    Answer school-related questions using an LLM and the MySQL backend.

    Args:
        question (str): User's natural language input

    Returns:
        dict: A structured response with type and answer string
    """
    base_url = os.getenv("API_BASE", "http://localhost:3001")

    # Step 1: Directly check if input is an ID
    try:
        student_id = int(question)
        data = query_student_info(student_id)
        if data:
            name = data[0]["student_name"]
            grade = data[0]["grade_name"]
            subjects = [row["subject_name"] for row in data]
            return {
                "type": "id",
                "response": f"{name} is in {grade} and is taking: {', '.join(subjects)}"
            }
    except ValueError:
        pass

    # Step 2: Use LLM via OpenRouter to classify input
    prompt = f"""
You are an AI assistant for a school system. Given a natural language question, extract:
- type: one of id, name, subject, grade
- value: the actual content like student ID, name, subject name, or grade label

Respond ONLY in this format:
type: subject
value: English

Now analyze this question:
\"{question}\"
"""

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:7860",
        "X-Title": "School Assistant"
    }

    payload = {
        "model": os.getenv("LLM_MODEL", "openai/gpt-3.5-turbo"),
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        output = res.json()["choices"][0]["message"]["content"]
        lines = output.strip().splitlines()
        type_line = next((l for l in lines if l.lower().startswith("type:")), None)
        value_line = next((l for l in lines if l.lower().startswith("value:")), None)

        if not type_line or not value_line:
            raise ValueError("Missing expected format")

        qtype = type_line.split(":", 1)[1].strip().lower()
        value = value_line.split(":", 1)[1].strip()

    except Exception as e:
        return {
            "type": "error",
            "response": f"Malformed LLM response: {e}\n\nRaw output:\n{output if 'output' in locals() else ''}"
        }

    # Step 3: Use backend routes based on LLM-detected type
    if qtype == "name":
        student_id = get_student_id_by_name(value)
        if student_id:
            data = query_student_info(student_id)
            if data:
                name = data[0]["student_name"]
                grade = data[0]["grade_name"]
                subjects = [row["subject_name"] for row in data]
                return {"type": "name", "response": f"{name} is in {grade} and is taking: {', '.join(subjects)}"}
        return {"type": "name", "response": f"No data found for name: {value}"}

    elif qtype == "subject":
        r = requests.get(f"{base_url}/student/subject/{value}/students")
        if r.status_code != 200 or not r.json():
            return {"type": "subject", "response": f"No students found taking {value}."}
        students = r.json()
        names = [f"{s['student_name']} ({s['grade_name']})" for s in students]
        return {"type": "subject", "response": f"Students taking {value}: {', '.join(names)}"}

    elif qtype == "grade":
        r = requests.get(f"{base_url}/student/grade/{value}")
        if r.status_code != 200 or not r.json():
            return {"type": "grade", "response": f"No students found in {value}."}
        students = r.json()
        names = [f"{s['student_name']} ({s['grade_name']})" for s in students]
        return {"type": "grade", "response": f"Students in {value}: {', '.join(names)}"}

    elif qtype == "id":
        try:
            student_id = int(value)
            data = query_student_info(student_id)
            if data:
                name = data[0]["student_name"]
                grade = data[0]["grade_name"]
                subjects = [row["subject_name"] for row in data]
                return {"type": "id", "response": f"{name} is in {grade} and is taking: {', '.join(subjects)}"}
        except:
            pass
        return {"type": "id", "response": f"No data found for ID: {value}"}

    return {"type": "unknown", "response": "Sorry, I couldn't understand the question."}

# Gradio Interface
demo = gr.Interface(
    fn=ask_school_assistant,
    inputs=gr.Textbox(label="Ask about students, grades, or subjects"),
    outputs="json",
    title="📚 School Assistant (LLM-Powered)",
    description="Ask natural questions like 'What is Alice taking?' or 'Who is in Grade 2?'"
)

if __name__ == "__main__":
    print("Launching Gradio...")
    demo.launch(mcp_server=True)
