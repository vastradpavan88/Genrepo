
 # Automated Email Report Generator

## Project Title

Automated Email Report Generator Using Python

---

## Project Description

The Automated Email Report Generator is a Python-based web application
that reads data from CSV and Excel files, processes the data, performs
basic statistical analysis, creates visualizations, displays the results
on a dashboard, generates a PDF report, and sends the report through email.

The dashboard is generated from the uploaded file and is not a
real-time dashboard.

---

## Objectives

1. Upload CSV and Excel files.
2. Process the uploaded data.
3. Calculate basic statistics.
4. Generate charts.
5. Display the results in a dashboard.
6. Generate a PDF report.
7. Send the PDF report through email.
8. Reduce repetitive manual reporting work.

---

## Technologies

- Python
- Flask
- Pandas
- OpenPyXL
- Matplotlib
- ReportLab
- HTML
- CSS
- JavaScript
- SMTP
- Gmail

---

## Workflow

Excel / CSV
    ↓
Upload
    ↓
Data Processing
    ↓
Statistical Analysis
    ↓
Dashboard
    ↓
Charts
    ↓
PDF Report
    ↓
Email

---

## Features

### File Upload

Supports:

- CSV
- XLSX

### Data Analysis

The system calculates:

- Total records
- Total columns
- Sum
- Average
- Maximum
- Minimum

### Dashboard

The dashboard displays:

- File information
- Summary cards
- Statistical analysis
- Charts
- Data preview

### PDF Report

The PDF contains:

- Report title
- Source file
- Data summary
- Statistical analysis
- Charts

### Email

The generated PDF can be sent to an email recipient.

---

## Installation

Create virtual environment:

python -m venv venv

Activate virtual environment:

.\venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

---

## Environment Variables

Create a `.env` file:

FLASK_SECRET_KEY=your_secret_key

EMAIL_ADDRESS=yourgmail@gmail.com

EMAIL_PASSWORD=your_gmail_app_password

---

## Run

Run the application:

python app.py

Open the browser:

http://127.0.0.1:5000

---

## Project Structure

Automated-Email-Report-Generator/

├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── uploads/
├── reports/
│
├── templates/
│   ├── index.html
│   └── dashboard.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── services/
    ├── __init__.py
    ├── data_processor.py
    ├── report_generator.py
    └── email_sender.py