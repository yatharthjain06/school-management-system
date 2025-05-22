import requests
import os

def query_student_info(student_id):
    base_url = os.getenv("API_BASE", "http://localhost:3001")
    response = requests.get(f"{base_url}/student/{student_id}/subjects")

    if response.status_code != 200 or not response.json():
        return []

    return response.json()

