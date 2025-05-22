INSERT INTO Grade (grade_name) VALUES ('Grade 1'), ('Grade 2'), ('Grade 3');
INSERT INTO Subject (subject_name) VALUES ('Math'), ('English'), ('Science'), ('History');
INSERT INTO Student (student_name, date_of_birth) VALUES 
('Alice Johnson', '2010-05-01'),
('Bob Smith', '2011-07-12'),
('Charlie Brown', '2010-09-30');
INSERT INTO StudentGradeSubject (student_id, grade_id, subject_id) VALUES 
(1, 1, 1), (1, 1, 2),
(2, 2, 1), (2, 2, 3),
(3, 1, 2), (3, 1, 4);
