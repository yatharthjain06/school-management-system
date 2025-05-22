import os
import requests
import gradio as gr
from dotenv import load_dotenv
from tools.student_tool import query_student_info, get_student_id_by_name

load_dotenv()

def ask_ai(user_input):
    base_url = os.getenv("API_BASE", "http://localhost:3001")

    # ✅ Try student ID
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

    # ✅ Grade-based lookup (e.g., "Who is in Grade 1?")
    if "grade" in user_input.lower():
        words = user_input.lower().split()
        try:
            grade_number = next(word for word in words if word.isdigit())
            grade_name = f"Grade {grade_number}"
            r = requests.get(f"{base_url}/student/grade/{grade_name}")
            if r.status_code != 200 or not r.json():
                return f"No students found in {grade_name}."
            data = r.json()
            names = [f"{row['student_name']} ({row['grade_name']})" for row in data]
            return f"Students in {grade_name}: {', '.join(names)}"
        except StopIteration:
            return "Could not determine which grade you meant."

    # ✅ Subject-based query
    if any(word in user_input.lower() for word in ["who", "taking", "doing", "studying", "enrolled in", "students taking"]):
        subjects = ["Math", "Science", "English", "History"]
        subject = next((sub for sub in subjects if sub.lower() in user_input.lower()), None)
        
        if not subject:
            return "Could not determine the subject from your question."

        r = requests.get(f"{base_url}/student/subject/{subject}/students")
        if r.status_code != 200 or not r.json():
            return f"No students found taking {subject}."

        data = r.json()
        names = [f"{row['student_name']} ({row['grade_name']})" for row in data]
        return f"The following students are taking {subject}: {', '.join(names)}."

    # ✅ Name-based query (supports multiple matches)
    name_matches = []
    words = user_input.split()
    for word in words:
        name_matches = get_student_ids_by_name(word)
        if name_matches:
            break

    if len(name_matches) == 1:
        student_id, name = name_matches[0]
        data = query_student_info(student_id)
        if not data:
            return f"No data found for {name}."
        grade = data[0]['grade_name']
        subjects = [row['subject_name'] for row in data]
        return f"{name} is in {grade} and is taking: {', '.join(subjects)}."
    elif len(name_matches) > 1:
        results = []
        for student_id, name in name_matches:
            data = query_student_info(student_id)
            if not data:
                continue
            grade = data[0]['grade_name']
            subjects = [row['subject_name'] for row in data]
            results.append(f"{name} is in {grade} and is taking: {', '.join(subjects)}.")
        return "\n\n".join(results)


    # ❌ Fallback
    return "Could not extract a student ID, name, or grade from your question."

# Gradio interface
demo = gr.Interface(
    fn=ask_ai,
    inputs=gr.Textbox(label="Ask a question or enter a student ID or name"),
    outputs="text",
    title="Student Subject Lookup (ID, Name, Subject, or Grade)"
)

if __name__ == "__main__":
    print("Launching Gradio...")
    demo.launch(mcp_server=True)
