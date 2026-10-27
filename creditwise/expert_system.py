def calculate_dti(monthly_debt, monthly_income):
    """Calculates the Debt-to-Income (DTI) ratio."""
    if monthly_income <= 0:
        return 100.0  # Handle zero or negative income as 100% debt burden
    return (monthly_debt / monthly_income) * 100

def evaluate_applicant(facts):
    """
    Evaluates applicant facts against explicit IF-THEN rules.
    Returns the risk classification, eligibility recommendation, and the rules that fired.
    """
    rules_fired = []
    positive_indicators = []
    negative_indicators = []
    neutral_indicators = []

    # Facts extraction
    age = facts.get('age', 0)
    monthly_income = facts.get('monthly_income', 0)
    monthly_debt = facts.get('monthly_debt', 0)
    credit_score = facts.get('credit_score', 0)
    employment_duration = facts.get('employment_duration', 0)
    previous_default = facts.get('previous_default', False)
    loan_amount = facts.get('loan_amount', 0)

    # Calculated Ratios
    dti = calculate_dti(monthly_debt, monthly_income)
    annual_income = monthly_income * 12
    loan_to_income = (loan_amount / annual_income) if annual_income > 0 else float('inf')

    # RULE 1: Age Eligibility
    if age >= 21 and age <= 60:
        rules_fired.append("RULE_AGE_1: Applicant is within the eligible age range (21-60).")
        positive_indicators.append("Age is within favorable limits.")
    else:
        rules_fired.append("RULE_AGE_2: Applicant is outside the standard eligible age range (21-60).")
        negative_indicators.append("Age is outside standard lending limits.")

    # RULE 2: Credit Score Evaluation
    if credit_score >= 750:
        rules_fired.append("RULE_CREDIT_1: Credit score >= 750. Indicates excellent credit history.")
        positive_indicators.append("Excellent Credit Score.")
    elif 650 <= credit_score <= 749:
        rules_fired.append("RULE_CREDIT_2: Credit score between 650 and 749. Indicates moderate credit history.")
        neutral_indicators.append("Moderate Credit Score.")
    else:
        rules_fired.append("RULE_CREDIT_3: Credit score < 650. Indicates adverse credit history.")
        negative_indicators.append("Adverse Credit Score.")

    # RULE 3: Debt-to-Income (DTI) Evaluation
    if dti <= 30.0:
        rules_fired.append(f"RULE_DTI_1: DTI ({dti:.2f}%) <= 30%. Indicates favorable affordability.")
        positive_indicators.append("Favorable Debt-to-Income Ratio.")
    elif 30.0 < dti <= 45.0:
        rules_fired.append(f"RULE_DTI_2: DTI ({dti:.2f}%) between 30% and 45%. Indicates moderate affordability.")
        neutral_indicators.append("Moderate Debt-to-Income Ratio.")
    else:
        rules_fired.append(f"RULE_DTI_3: DTI ({dti:.2f}%) > 45%. Indicates adverse affordability.")
        negative_indicators.append("Adverse Debt-to-Income Ratio.")

    # RULE 4: Previous Defaults
    if previous_default:
        rules_fired.append("RULE_DEFAULT_1: Applicant has a reported previous loan default. High risk indicator.")
        negative_indicators.append("Previous Loan Default Reported.")
    else:
        rules_fired.append("RULE_DEFAULT_2: No reported previous defaults. Positive indicator.")
        positive_indicators.append("Clean Repayment History.")

    # RULE 5: Employment Stability
    if employment_duration >= 24:
        rules_fired.append("RULE_EMP_1: Employment duration >= 24 months. Indicates favorable job stability.")
        positive_indicators.append("Stable Employment History.")
    elif employment_duration < 6:
        rules_fired.append("RULE_EMP_2: Employment duration < 6 months. Indicates caution for job stability.")
        negative_indicators.append("Short Employment Duration.")
    else:
        rules_fired.append("RULE_EMP_3: Employment duration between 6 and 24 months. Neutral stability indicator.")
        neutral_indicators.append("Moderate Employment Stability.")

    # Inference Aggregation and Risk Classification
    # Deterministic logic based on indicators
    if previous_default or credit_score < 650 or dti > 45.0:
        risk_category = "High Risk"
    elif len(negative_indicators) > 0 or len(neutral_indicators) >= 2:
        risk_category = "Medium Risk"
    else:
        risk_category = "Low Risk"

    # Eligibility Recommendation
    if risk_category == "Low Risk" and age >= 21 and age <= 60:
        eligibility = "Eligible for Further Review"
    elif risk_category == "Medium Risk" and age >= 21 and age <= 60:
        eligibility = "Conditional Review"
    else:
        eligibility = "Not Eligible Under Demonstration Rules"
        rules_fired.append("RULE_DECISION: Mandatory eligibility conditions not met or risk is too high.")

    return {
        "eligibility": eligibility,
        "risk_category": risk_category,
        "dti": dti,
        "loan_to_income": loan_to_income,
        "rules_fired": rules_fired,
        "positive_indicators": positive_indicators,
        "neutral_indicators": neutral_indicators,
        "negative_indicators": negative_indicators
    }
