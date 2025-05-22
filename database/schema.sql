CREATE TABLE Grade (
    grade_id INT AUTO_INCREMENT PRIMARY KEY,
    grade_name VARCHAR(50) NOT NULL
);
CREATE TABLE Subject (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL
);
CREATE TABLE Student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    date_of_birth DATE
);
CREATE TABLE StudentGradeSubject (
    sgs_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    grade_id INT,
    subject_id INT,
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (grade_id) REFERENCES Grade(grade_id),
    FOREIGN KEY (subject_id) REFERENCES Subject(subject_id)
);
