# URL Shortener – Flask CI/CD Project

## 📌 Project Overview
This project is a simple URL shortening web application built using Flask.
It allows users to convert long URLs into short links and automatically redirects them to the original URL.

The project was designed to demonstrate practical usage of CI/CD concepts in a real application.

---

## ⚙️ Features
- Shorten long URLs into short links
- Automatic redirection to original URLs
- URL normalization (handles missing http/https)
- Frontend served directly by Flask
- Automated testing using PyTest
- CI pipeline using GitHub Actions

---

## 🛠️ Technology Stack
- Backend: Python (Flask)
- Frontend: HTML, JavaScript
- Testing: PyTest
- CI/CD: GitHub Actions

---

## 🔄 CI/CD Pipeline
Every push or pull request to the `main` branch triggers an automated CI pipeline that:
1. Sets up a Python environment
2. Installs dependencies
3. Runs automated tests using PyTest

If any test fails, the pipeline stops and reports the error.

---

## ▶️ How to Run Locally

```bash
python app.py
