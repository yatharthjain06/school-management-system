const express = require('express');
const cors = require('cors');
const studentRoutes = require('./routes/studentRoutes');

const app = express();
app.use(cors());
app.use('/student', studentRoutes);

app.listen(3001, () => console.log('API running on port 3001'));