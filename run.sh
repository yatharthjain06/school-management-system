#!/bin/bash
cd backend && npm install && node server.js &
cd ../frontend && pip install -r requirements.txt && python app.py
