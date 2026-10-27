import re

def get_chatbot_response(user_input, current_assessment=None):
    """
    Evaluates the user input against predefined rules and pattern matching (regex/keywords).
    Context-aware if an assessment dictionary is provided.
    """
    input_lower = user_input.lower().strip()

    # RULE: Explain Credit Score
    if re.search(r"what is a? ?credit score", input_lower) or "credit score" in input_lower:
        response = (
            "A credit score is a numerical representation of a borrower's creditworthiness based on their repayment history. "
            "In CREDITWISE, a score of 750 or above is favorable, while a score below 650 indicates adverse risk."
        )
        if current_assessment:
            response += f" The current applicant's risk level is evaluated as: {current_assessment.get('risk_category')}."
        return response

    # RULE: Explain Debt-to-Income (DTI) Ratio
    if re.search(r"what is (a )?dti", input_lower) or re.search(r"debt[ \-]to[ \-]income", input_lower) or "dti" in input_lower:
        response = (
            "The Debt-to-Income (DTI) ratio compares an individual's monthly debt payments to their monthly gross income. "
            "It is calculated as: (Monthly Debt / Monthly Income) * 100. A lower DTI (<= 30%) means favorable affordability."
        )
        if current_assessment:
            dti = current_assessment.get('dti', 0)
            response += f" The current applicant's calculated DTI is {dti:.2f}%."
        return response

    # RULE: Loan Eligibility Factors
    if re.search(r"eligibility", input_lower) or re.search(r"factors", input_lower):
        return (
            "Loan eligibility in this system is influenced by several factors: "
            "Credit Score, Debt-to-Income (DTI) ratio, Previous Defaults, Employment Stability (months), and Age."
        )

    # RULE: Explain Risk Classification
    if re.search(r"why.*high risk", input_lower) or "high risk" in input_lower:
        if current_assessment and current_assessment.get('risk_category') == 'High Risk':
            negatives = ", ".join(current_assessment.get('negative_indicators', []))
            return f"The current applicant was classified as High Risk because of the following factors: {negatives}."
        return (
            "An applicant is classified as 'High Risk' if they have a previous loan default, a credit score below 650, "
            "or a DTI ratio greater than 45%."
        )

    # RULE: Conditional Review
    if "conditional review" in input_lower:
        return (
            "A 'Conditional Review' means the applicant has some neutral or negative indicators that require manual underwriter review, "
            "but they are not immediately rejected. This often happens if they fall into the 'Medium Risk' category but meet age rules."
        )

    # RULE: How the Expert System Works
    if re.search(r"how.*work", input_lower) or "expert system" in input_lower:
        return (
            "CREDITWISE works by using an Inference Engine that matches 'Applicant Facts' against a predefined 'Knowledge Base' "
            "of explicit IF-THEN rules. It determines a credit risk and eligibility recommendation deterministically."
        )

    # FALLBACK RULE
    return (
        "I am a simple rule-based assistant. I can answer questions about 'credit score', 'DTI', 'eligibility factors', "
        "'conditional review', 'high risk', and 'how the expert system works'. Please rephrase your question."
    )
