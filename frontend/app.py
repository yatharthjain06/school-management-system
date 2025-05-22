import os
import requests
import gradio as gr
from dotenv import load_dotenv
from tools.student_tool import query_student_info, get_student_id_by_name

load_dotenv()

def ask_ai(user_input):
    base_url = os.getenv("API_BASE", "http://localhost:3001")

    # Try student ID
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
        pass

    # Reverse subject question (e.g. "Who is taking Science?")
    if "who" in user_input.lower() and "taking" in user_input.lower():
        subject = None
        for sub in ["Math", "Science", "English", "History"]:
            if sub.lower() in user_input.lower():
                subject = sub
                break
        if not subject:
            return "Could not determine the subject from your question."

        r = requests.get(f"{base_url}/student/subject/{subject}/students")
        if r.status_code != 200 or not r.json():
            return f"No students found taking {subject}."

        data = r.json()
        names = [f"{row['student_name']} ({row['grade_name']})" for row in data]
        return f"The following students are taking {subject}: {', '.join(names)}."

    # Try matching by name
    words = user_input.split()
    for word in words:
        student_id = get_student_id_by_name(word)
        if student_id:
            data = query_student_info(student_id)
            if not data:
                return f"No data found for {word}."
            name = data[0]['student_name']
            grade = data[0]['grade_name']
            subjects = [row['subject_name'] for row in data]
            return f"{name} is in {grade} and is taking: {', '.join(subjects)}."

    return "Could not extract a student ID or name from your question."

# Gradio interface
demo = gr.Interface(
    fn=ask_ai,
    inputs=gr.Textbox(label="Ask a question or enter a student ID or name"),
    outputs="text",
    title="Student Subject Lookup (ID, Name, or Subject)"
)

if __name__ == "__main__":
    print("Launching Gradio...")
    demo.launch(mcp_server=True)
