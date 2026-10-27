# CREDITWISE — Financial Loan Eligibility & Credit Risk Expert System

## Aim
To develop a complete, functional AI mini-project suitable for the Third-Year Engineering (T.E.) Artificial Intelligence and Learning (AIL) practical under Savitribai Phule Pune University (SPPU). The application demonstrates knowledge representation, rule evaluation, and conversational pattern matching as prescribed in the syllabus.

## Problem Statement
Build a Financial Loan Eligibility and Credit Risk Evaluation Expert System that accepts applicant information, evaluates it using predefined IF-THEN rules, classifies credit risk, and provides an explainable preliminary eligibility recommendation, accompanied by an interactive conversational assistant.

## Objectives
- Demonstrate knowledge representation using explicit IF-THEN rules in Python.
- Develop a deterministic inference engine to evaluate financial facts and recommend credit risk categories.
- Build a lightweight rule-based conversational chatbot to explain domain concepts and applicant assessment outputs using pattern matching.
- Provide a clean, dark-themed, fintech-style graphical user interface (GUI) using Streamlit.

## Theory & Architecture
This project utilizes a **Rule-Based Expert System** architecture:
- **Knowledge Base:** Consists of explicit IF-THEN financial rules (e.g., thresholding for Credit Score, Debt-to-Income (DTI), Employment Duration).
- **Working Memory:** The facts inputted by the user in the "Evaluate Applicant" form.
- **Inference Engine:** Iterates over the facts, matches them against the Knowledge Base, and fires all applicable rules.
- **Explanation Facility:** Exposes the explicitly fired rules to explain *why* a particular decision (Low, Medium, High Risk) was made.
- **Pattern Matching (Chatbot):** Satisfies Part B, Assignment 4 of the SPPU AIL syllabus by using regular expressions to interpret user queries and map them to predefined responses, avoiding generic static text loops.

## Technologies Used
- Python 3
- Streamlit (Web interface)
- Plotly (Data Visualization)
- Pandas

## Installation Instructions
For Windows/Linux/macOS:
1. Ensure Python 3.8+ is installed.
2. Clone or download this project.
3. Open a terminal or command prompt in the project directory (`creditwise/`).
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Execution Instructions
Launch the Streamlit server:
```bash
streamlit run app.py
```
This will open the CREDITWISE application in your default web browser (typically at http://localhost:8501).

## Limitations and Future Scope
- **Limitations:** This is an educational expert system and does not connect to actual banking APIs, external ML models, or live credit bureaus. Risk rules are simplified for demonstration purposes.
- **Future Scope:** Extend the system to utilize a formal rules engine library (like PyKE or Experta), integrate backward chaining for goal-driven evaluation, or upgrade the chatbot to hybrid architectures combining rules with small NLP models.
