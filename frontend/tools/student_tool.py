import mysql.connector
import os
import requests

def query_student_info(student_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Reader369!",
        database="school"
    )
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT s.student_name, g.grade_name, sub.subject_name
    FROM student s
    JOIN studentgradesubject sgs ON s.student_id = sgs.student_id
    JOIN grade g ON sgs.grade_id = g.grade_id
    JOIN subject sub ON sgs.subject_id = sub.subject_id
    WHERE s.student_id = %s
    """
    cursor.execute(query, (student_id,))
    result = cursor.fetchall()
    conn.close()
    return result

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
        # Match full name, first name, or last name
        if (
            name_query == full_name or
            (name_parts and name_query == name_parts[0]) or
            (len(name_parts) > 1 and name_query == name_parts[-1])
        ):
            return student['student_id']
    return None
