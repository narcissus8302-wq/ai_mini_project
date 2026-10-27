import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from expert_system import evaluate_applicant
from chatbot import get_chatbot_response

# Configure the Streamlit page
st.set_page_config(
    page_title="CREDITWISE - Loan Eligibility Expert System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark fintech theme styles
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        background-color: #0e1117;
        color: #e0e6ed;
    }
    .metric-card {
        background-color: #1e2530;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .metric-label {
        font-size: 14px;
        color: #94a3b8;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #f1f5f9;
    }
    .badge-favorable {
        background-color: rgba(16, 185, 129, 0.2);
        color: #34d399;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    .badge-caution {
        background-color: rgba(245, 158, 11, 0.2);
        color: #fbbf24;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    .badge-adverse {
        background-color: rgba(239, 68, 68, 0.2);
        color: #f87171;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    hr {
        border-color: #334155;
    }
</style>
""", unsafe_allow_html=True)

# Format currency in INR
def format_currency(amount):
    if amount >= 100000:
        return f"₹{amount / 100000:.2f} Lakh"
    return f"₹{amount:,.0f}"

# Session State Initialization
if 'assessment' not in st.session_state:
    st.session_state.assessment = None
if 'applicant_data' not in st.session_state:
    st.session_state.applicant_data = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar Navigation
st.sidebar.title("🏦 CREDITWISE")
st.sidebar.markdown("Financial Loan Eligibility Expert System")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["Dashboard", "Evaluate Applicant", "AI Assistant & How It Works"])

# --- DASHBOARD PAGE ---
if page == "Dashboard":
    st.title("Credit Assessment Dashboard")

    if st.session_state.assessment is None:
        st.info("No assessment data available. Please go to 'Evaluate Applicant' to run a new assessment.")
        st.markdown("### Sample Applicant Data (Demonstration)")
        # Show sample data layout
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Monthly Income</div><div class='metric-value'>₹50,000</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Requested Loan</div><div class='metric-value'>₹5.00 Lakh</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>DTI Ratio</div><div class='metric-value'>20%</div></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Credit Score</div><div class='metric-value'>780</div></div>", unsafe_allow_html=True)
    else:
        # Display Actual Assessment
        a_data = st.session_state.applicant_data
        result = st.session_state.assessment

        st.markdown("### Applicant Financial Summary")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Monthly Income</div><div class='metric-value'>{format_currency(a_data['monthly_income'])}</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Requested Loan</div><div class='metric-value'>{format_currency(a_data['loan_amount'])}</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>DTI Ratio</div><div class='metric-value'>{result['dti']:.1f}%</div></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>Credit Score</div><div class='metric-value'>{a_data['credit_score']}</div></div>", unsafe_allow_html=True)

        # Optional 5th metric or row for loan-to-income
        st.markdown(f"**Loan-to-Annual-Income Ratio:** {result['loan_to_income']:.2f}")

        st.markdown("---")
        st.markdown("### Assessment Result")

        res_col1, res_col2 = st.columns([1, 1])

        with res_col1:
            # Risk and Eligibility Badges
            risk_color = "badge-favorable" if result['risk_category'] == "Low Risk" else "badge-caution" if result['risk_category'] == "Medium Risk" else "badge-adverse"
            st.markdown(f"**Credit Risk Category:** <span class='{risk_color}'>{result['risk_category']}</span>", unsafe_allow_html=True)

            elig_color = "badge-favorable" if "Eligible" in result['eligibility'] and "Not" not in result['eligibility'] else "badge-adverse" if "Not" in result['eligibility'] else "badge-caution"
            st.markdown(f"**Eligibility Recommendation:** <span class='{elig_color}'>{result['eligibility']}</span>", unsafe_allow_html=True)

            st.markdown("#### Positive Factors:")
            for p in result['positive_indicators']:
                st.markdown(f"✅ {p}")

            if result['neutral_indicators']:
                st.markdown("#### Neutral Factors:")
                for n in result['neutral_indicators']:
                    st.markdown(f"⚠️ {n}")

            if result['negative_indicators']:
                st.markdown("#### Risk Factors:")
                for neg in result['negative_indicators']:
                    st.markdown(f"❌ {neg}")

        with res_col2:
            # Visual Breakdown (Gauge Chart for Credit Score)
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = a_data['credit_score'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Credit Score"},
                gauge = {
                    'axis': {'range': [300, 900]},
                    'bar': {'color': "#3b82f6"},
                    'steps': [
                        {'range': [300, 649], 'color': "rgba(239, 68, 68, 0.4)"},
                        {'range': [650, 749], 'color': "rgba(245, 158, 11, 0.4)"},
                        {'range': [750, 900], 'color': "rgba(16, 185, 129, 0.4)"}
                    ]
                }
            ))
            fig.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor="rgba(0,0,0,0)", font={'color': "#e0e6ed"})
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.markdown("### Why Did CREDITWISE Reach This Decision?")
        st.markdown("*The expert system activated the following IF-THEN rules based on the applicant's facts:*")
        for rule in result['rules_fired']:
            st.markdown(f"- `{rule}`")

        st.caption("Disclaimer: This is an educational expert system and not a real credit assessment or loan approval service.")


# --- EVALUATE APPLICANT PAGE ---
elif page == "Evaluate Applicant":
    st.title("Evaluate Applicant")
    st.markdown("Enter the applicant's details below to run the expert system rules.")

    with st.form("evaluation_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Personal & Employment")
            age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1)
            emp_type = st.selectbox("Employment Type", ["Salaried", "Self-employed"])
            monthly_income = st.number_input("Monthly Net Income (₹)", min_value=0.0, value=50000.0, step=1000.0)
            emp_duration = st.number_input("Employment Duration (months)", min_value=0, value=36, step=1)

        with col2:
            st.subheader("Financial Details")
            credit_score = st.number_input("Credit Score", min_value=300, max_value=900, value=750, step=1)
            monthly_debt = st.number_input("Existing Monthly Debt Obligations (₹)", min_value=0.0, value=10000.0, step=1000.0)
            prev_default = st.radio("Previous Loan Default?", ["No", "Yes"])
            loan_amount = st.number_input("Requested Loan Amount (₹)", min_value=1000.0, value=500000.0, step=10000.0)
            loan_tenure = st.number_input("Loan Tenure (months)", min_value=1, value=60, step=1)

        submit_btn = st.form_submit_button("Run Expert System Assessment")

        if submit_btn:
            # Fact compilation
            facts = {
                "age": age,
                "monthly_income": monthly_income,
                "monthly_debt": monthly_debt,
                "credit_score": credit_score,
                "employment_duration": emp_duration,
                "previous_default": True if prev_default == "Yes" else False,
                "loan_amount": loan_amount
            }

            # Run inference engine
            result = evaluate_applicant(facts)

            # Save to session state
            st.session_state.applicant_data = facts
            st.session_state.assessment = result

            st.success("Assessment Complete! Navigate to the Dashboard to view the results.")

# --- AI ASSISTANT & HOW IT WORKS PAGE ---
elif page == "AI Assistant & How It Works":
    st.title("AI Assistant & System Architecture")

    tab1, tab2 = st.tabs(["AI Assistant (Chatbot)", "How It Works (Theory)"])

    with tab1:
        st.subheader("CREDITWISE Expert Assistant")
        st.markdown("Ask questions about credit scores, DTI, eligibility factors, or the system's reasoning.")

        # Display chat history
        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                st.markdown(f"**👤 You:** {msg['text']}")
            else:
                st.markdown(f"**🤖 AI:** {msg['text']}")

        # Chat input
        with st.form("chat_form", clear_on_submit=True):
            user_query = st.text_input("Type your question here...")
            submitted = st.form_submit_button("Send")

            if submitted and user_query:
                # Add user query to history
                st.session_state.chat_history.append({"role": "user", "text": user_query})
                # Get response
                response = get_chatbot_response(user_query, st.session_state.assessment)
                # Add bot response to history
                st.session_state.chat_history.append({"role": "bot", "text": response})
                st.rerun()

    with tab2:
        st.subheader("How CREDITWISE Works")
        st.markdown("""
        **CREDITWISE** is a deterministic rule-based expert system designed to evaluate loan eligibility and classify credit risk.

        ### Core Concepts:
        * **Knowledge Base:** Contains explicit financial rules (e.g., "IF Credit Score < 650 THEN Risk is High").
        * **Applicant Facts & Working Memory:** The data entered by the user (income, debt, age) is loaded into the system's working memory as facts.
        * **Inference Engine:** The component that matches the applicant's facts against the Knowledge Base rules. It evaluates conditions and fires applicable rules deterministically.
        * **Explanation Facility:** Because explicit rules are used, the system logs every rule that successfully "fires", allowing it to clearly explain *why* it reached a specific decision.
        * **Pattern Matching (Chatbot):** The AI Assistant uses predefined rules and regular expressions (Regex) to map user questions to scripted explanations. It also demonstrates context-awareness by checking the active assessment results to explain specific decisions about the current applicant.

        ### Example Rules:
        1. **IF** `debt_to_income_ratio > 45%` **THEN** `classify_as("High Risk")` and `add_negative_indicator("Adverse DTI")`
        2. **IF** `credit_score >= 750` **THEN** `add_positive_indicator("Excellent Credit Score")`

        *This project demonstrates a genuine rule-based approach fulfilling the Artificial Intelligence and Learning (AIL) syllabus requirements for pattern matching and rule-based systems.*
        """)
