import requests
import os

def query_student_info(student_id):
    base_url = os.getenv("API_BASE", "http://localhost:3001")
    response = requests.get(f"{base_url}/student/{student_id}/subjects")

    if response.status_code != 200 or not response.json():
        return []

    return response.json()

def get_student_id_by_name(name_query):
    base_url = os.getenv("API_BASE", "http://localhost:3001")
    response = requests.get(f"{base_url}/student/all")
    if response.status_code != 200:
        return None
    name_query = name_query.strip().lower()
    students = response.json()
    for student in students:
        full_name = student['student_name'].strip().lower()
        if name_query == full_name:
            return student['student_id']
    return None

def get_subjects_by_student_name(name):
    base_url = os.getenv("API_BASE", "http://localhost:3001")
    response = requests.get(f"{base_url}/student/subjects/by-name", params={"name": name})
    if response.status_code != 200:
        return []
    return response.json()
