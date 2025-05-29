const express = require('express');
const router = express.Router();
const db = require('../db');

// 🔍 Get all students in a grade by grade *name*
router.get('/grade/:name', (req, res) => {
  const gradeName = req.params.name;
  const query = `
    SELECT s.student_name, g.grade_name
    FROM Student s
    JOIN StudentGradeSubject sgs ON s.student_id = sgs.student_id
    JOIN Grade g ON sgs.grade_id = g.grade_id
    WHERE g.grade_name = ?
    GROUP BY s.student_id, s.student_name, g.grade_name
  `;
  db.query(query, [gradeName], (err, result) => {
    if (err) return res.status(500).json({ error: 'Database error', details: err });
    res.json(result);
  });
});

// ✅ NEW: Get all students in a grade by grade *ID*
router.get('/grades/:id/students', (req, res) => {
  const gradeId = req.params.id;
  const query = `
    SELECT s.student_name, g.grade_name
    FROM Student s
    JOIN StudentGradeSubject sgs ON s.student_id = sgs.student_id
    JOIN Grade g ON sgs.grade_id = g.grade_id
    WHERE g.grade_id = ?
    GROUP BY s.student_id, s.student_name, g.grade_name
  `;
  db.query(query, [gradeId], (err, result) => {
    if (err) return res.status(500).json({ error: 'Database error', details: err });
    res.json(result);
  });
});

// 📋 Get all students (basic list)
router.get('/all', (req, res) => {
  const query = `SELECT student_id, student_name FROM Student`;
  db.query(query, (err, result) => {
    if (err) return res.status(500).json({ error: 'Database error', details: err });
    res.json(result);
  });
});

// 📚 Get students by subject name
router.get('/subject/:name/students', (req, res) => {
  const subjectName = req.params.name;
  const query = `
    SELECT s.student_name, g.grade_name
    FROM Student s
    JOIN StudentGradeSubject sgs ON s.student_id = sgs.student_id
    JOIN Grade g ON sgs.grade_id = g.grade_id
    JOIN Subject sub ON sgs.subject_id = sub.subject_id
    WHERE sub.subject_name = ?
    GROUP BY s.student_name, g.grade_name
  `;
  db.query(query, [subjectName], (err, result) => {
    if (err) return res.status(500).json({ error: 'Database error', details: err });
    res.json(result);
  });
});

// 🎯 Get a student’s subjects by their student ID
router.get('/:id/subjects', (req, res) => {
  const studentId = req.params.id;
  const query = `
    SELECT s.student_name, g.grade_name, sub.subject_name
    FROM Student s
    JOIN StudentGradeSubject sgs ON s.student_id = sgs.student_id
    JOIN Grade g ON sgs.grade_id = g.grade_id
    JOIN Subject sub ON sgs.subject_id = sub.subject_id
    WHERE s.student_id = ?
  `;
  db.query(query, [studentId], (err, result) => {
    if (err) return res.status(500).json({ error: 'Database error', details: err });
    res.json(result);
  });
});

// 🔍 Get subjects by partial student name match
router.get('/student/subjects/by-name', (req, res) => {
  const { name } = req.query;
  const query = `
    SELECT DISTINCT sub.subject_name
    FROM Student s
    JOIN StudentGradeSubject sgs ON s.student_id = sgs.student_id
    JOIN Subject sub ON sgs.subject_id = sub.subject_id
    WHERE s.student_name LIKE ?
  `;
  const likeName = `%${name}%`;
  db.query(query, [likeName], (err, results) => {
    if (err) return res.status(500).json({ error: 'Database error', details: err });
    res.json(results);
  });
});

module.exports = router;
