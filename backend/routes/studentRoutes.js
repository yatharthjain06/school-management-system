const express = require('express');
const router = express.Router();
const db = require('../db');

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
      if (err) res.status(500).send(err);
      else res.send(result);
    });
  });
router.get('/all', (req, res) => {
    const query = `SELECT student_id, student_name FROM Student`;
    db.query(query, (err, result) => {
        if (err) res.status(500).send(err);
        else res.send(result);
    });
});
router.get('/subject/:name/students', (req, res) => {
    const subjectName = req.params.name;
    const query = `
        SELECT s.student_name, g.grade_name
        FROM Student s
        JOIN StudentGradeSubject sgs ON s.student_id = sgs.student_id
        JOIN Grade g ON sgs.grade_id = g.grade_id
        JOIN Subject sub ON sgs.subject_id = sub.subject_id
        WHERE sub.subject_name = ?
    `;
    db.query(query, [subjectName], (err, result) => {
        if (err) res.status(500).send(err);
        else res.send(result);
    });
});
router.get('/:id/subjects', (req, res) => {
  const studentId = req.params.id;
  const query = `
      SELECT s.student_name, g.grade_name, sub.subject_name
      FROM Student s
      JOIN StudentGradeSubject sgs ON s.student_id = sgs.student_id
      JOIN Grade g ON sgs.grade_id = g.grade_id
      JOIN Subject sub ON sgs.subject_id = sub.subject_id
      WHERE s.student_id = ?`;
  db.query(query, [studentId], (err, result) => {
      if (err) res.status(500).send(err);
      else res.send(result);
  });
});
module.exports = router;
