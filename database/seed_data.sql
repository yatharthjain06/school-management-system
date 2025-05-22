-- Insert grades
INSERT INTO Grade (grade_id, grade_name)
VALUES (1, 'Grade 1'), (2, 'Grade 2'), (3, 'Grade 3');

-- Insert subjects
INSERT INTO Subject (subject_id, subject_name)
VALUES (1, 'Math'), (2, 'English'), (3, 'Science'), (4, 'History');

-- Insert students
INSERT INTO Student (student_id, student_name, date_of_birth)
VALUES 
  (1, 'Alice Johnson', '2010-05-01'),
  (2, 'Bob Smith', '2011-07-12'),
  (3, 'Charlie Brown', '2010-09-30'),
  (4, 'Alice Evans', '2011-03-15');

-- Link students to grades and subjects
INSERT INTO StudentGradeSubject (student_id, grade_id, subject_id)
VALUES
  -- Alice Johnson (Grade 1: Math, English)
  (1, 1, 1),
  (1, 1, 2),

  -- Bob Smith (Grade 2: English, Science)
  (2, 2, 2),
  (2, 2, 3),

  -- Charlie Brown (Grade 1: Math, Science, History)
  (3, 1, 1),
  (3, 1, 3),
  (3, 1, 4),

  -- Alice Evans (Grade 2: English, History)
  (4, 2, 2),
  (4, 2, 4);