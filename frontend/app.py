import os
import requests
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
from tools.student_tool import query_student_info, get_student_id_by_name

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ConversationalBot:
    def __init__(self):
        self.conversation_history = []
        self.current_context = {}

    def get_completion(self, messages):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=[
                {
                    "name": "query_student_info",
                    "description": "Get information about a student by their ID",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "student_id": {
                                "type": "integer",
                                "description": "The ID of the student"
                            }
                        },
                        "required": ["student_id"]
                    }
                },
                {
                    "name": "get_student_by_subject",
                    "description": "Find students taking a specific subject",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "subject": {
                                "type": "string",
                                "description": "The name of the subject"
                            }
                        },
                        "required": ["subject"]
                    }
                },
                {
                    "name": "get_student_id_by_name",
                    "description": "Get a student ID based on full name",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The full name of the student"
                            }
                        },
                        "required": ["name"]
                    }
                }
            ],
            function_call="auto"
        )
        return response.choices[0].message

    def format_response(self, data, query_type="student"):
        if not data or len(data) == 0:
            return "No data found."
        if query_type == "student":
            name = data[0]['student_name']
            grade = data[0]['grade_name']
            subjects = [row['subject_name'] for row in data]
            return f"{name} is in {grade} and is taking: {', '.join(subjects)}."
        return data

    def process_query(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})

        MAX_HISTORY = 10
        messages = [
            {"role": "system", "content": """You are a helpful school assistant. 
            You can retrieve student data by name, ID, or subject. 
            Call a function when needed to get real data."""},
            *self.conversation_history[-MAX_HISTORY:]
        ]

        response = self.get_completion(messages)

        if response.function_call:
            function_name = response.function_call.name
            function_args = eval(response.function_call.arguments)

            if function_name == "query_student_info":
                data = query_student_info(function_args["student_id"])
                result = self.format_response(data, "student")

            elif function_name == "get_student_by_subject":
                base_url = os.getenv("API_BASE", "http://localhost:3001")
                r = requests.get(f"{base_url}/student/subject/{function_args['subject']}/students")
                data = r.json()
                result = f"Students taking {function_args['subject']}: " + ", ".join(
                    [f"{s['student_name']} ({s['grade_name']})" for s in data])

            elif function_name == "get_student_id_by_name":
                student_id = get_student_id_by_name(function_args["name"])
                if student_id:
                    data = query_student_info(student_id)
                    result = self.format_response(data, "student")
                else:
                    result = f"No student found with the name {function_args['name']}."

            self.conversation_history.append({
                "role": "function",
                "name": function_name,
                "content": result or ""
            })

            messages.append({
                "role": "function",
                "name": function_name,
                "content": result or ""
            })

            response = self.get_completion(messages)

        self.conversation_history.append({
            "role": "assistant",
            "content": response.content or ""
        })

        return response.content

bot = ConversationalBot()

def chat_interface(user_input):
    return bot.process_query(user_input)

demo = gr.Interface(
    fn=chat_interface,
    inputs=gr.Textbox(
        label="Ask about students, subjects, or grades",
        placeholder="e.g., 'What subjects is Karina White taking?'"
    ),
    outputs=gr.Textbox(label="Response"),
    title="School Management Assistant",
    description="Ask about students and their academic data."
)

if __name__ == "__main__":
    print("Launching Gradio...")
    demo.launch(share=True)

def get_student_id_by_name(name_query):
    base_url = os.getenv("API_BASE", "http://localhost:3001")
    response = requests.get(f"{base_url}/student/all")
    if response.status_code != 200:
        return None
    name_query = name_query.strip().lower()
    students = response.json()
    for student in students:
        full_name = student['student_name'].strip().lower()
        name_parts = full_name.split()
        # Match full name or any part of the name
        if (
            name_query == full_name or
            name_query in name_parts
        ):
            return student['student_id']
    return None
