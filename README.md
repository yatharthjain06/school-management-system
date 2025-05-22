# 🏫 School Management System (AI-Enabled Demo)

This project is a full-stack school management demo that uses:

- ✅ **MySQL** for structured student/subject/grade data
- ✅ **Node.js (Express)** backend to serve data
- ✅ **Python (Gradio + OpenRouter)** frontend to handle natural language questions
- ✅ **MCP Protocol** for AI tool integration

It allows querying relationships between students and subjects using:

- 🔢 Student ID (e.g. `1`)
- 🧍 Student name (e.g. `Alice`)
- 📘 Subject-based reverse lookup (e.g. `Who is taking Science?`)

---

## 🚀 Quick Start

### 1. 📦 Set Up the Database

#### ✅ Start MySQL and load schema + data

```bash
mysql -u root -p

1. In the MySQL shell:
CREATE DATABASE school;
EXIT;

Then run:
mysql -u root -p school < database/schema.sql
mysql -u root -p school < database/seed_data.sql

There are already some data entries entered in for you, if you run SELECT * FROM Student;
+------------+---------------+---------------+
| student_id | student_name  | date_of_birth |
+------------+---------------+---------------+
|          1 | Alice Johnson | 2010-05-01    |
|          2 | Bob Smith     | 2011-07-12    |
|          3 | Charlie Brown | 2010-09-30    |
+------------+---------------+---------------+

2. Now start the backend (Node.js API):
cd backend
npm install
node server.js
The API should run at http://localhost:3001

3. Now start the frontend (Gradio + MCP UI):
cd frontend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Make sure your .env file contains:
API_BASE=http://localhost:3001
OPENROUTER_API_KEY=org-xxxxxxxx
LLM_MODEL=openai/gpt-3.5-turbo

Then run the app:
python app.py

And go to http://127.0.0.1:7860

Here are some test case screenshots that you can run as well:

![ID 1](screenshots/ss1.png)
![Science](screenshots/ss2.png)
![Alice](screenshots/ss3.png)
![Error](screenshots/ss4.png)
