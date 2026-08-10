import requests
import streamlit as st


API_URL = "http://loan-default-api:8000"


st.set_page_config(
    page_title="Loan Default Prediction",
    page_icon="🏦",
    layout="wide",
)


st.title("🏦 Loan Default Prediction")
st.write(
    "Enter the applicant information below to predict "
    "the probability of loan default."
)


st.divider()


# -----------------------------
# Applicant Financial Details
# -----------------------------

st.subheader("Financial Information")

col1, col2 = st.columns(2)

with col1:
    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0.0,
        value=300000.0,
    )

    property_value = st.number_input(
        "Property Value",
        min_value=0.0,
        value=400000.0,
    )

    income = st.number_input(
        "Income",
        min_value=0.0,
        value=7500.0,
    )

    term = st.number_input(
        "Loan Term",
        min_value=1,
        value=360,
    )

with col2:
    dtir1 = st.number_input(
        "DTIR1",
        min_value=0.0,
        value=42.0,
    )

    ltv = st.number_input(
        "LTV",
        min_value=0.0,
        value=75.0,
    )

    age = st.selectbox(
        "Age",
        [
            "25-34",
            "35-44",
            "45-54",
            "55-64",
            "65-74",
            "75-84",
        ],
        index=1,
    )

    total_units = st.selectbox(
        "Total Units",
        ["1U", "2U", "3U", "4U"],
    )


# -----------------------------
# Loan Information
# -----------------------------

st.subheader("Loan Information")

col1, col2 = st.columns(2)

with col1:
    loan_type = st.selectbox(
        "Loan Type",
        ["type1", "type2", "type3"],
    )

    loan_purpose = st.selectbox(
        "Loan Purpose",
        ["p1", "p2", "p3"],
    )

    occupancy_type = st.selectbox(
        "Occupancy Type",
        ["pr", "sr", "ir"],
    )

    submission_of_application = st.selectbox(
        "Submission of Application",
        ["to_inst", "not_inst"],
    )

with col2:
    neg_ammortization = st.selectbox(
        "Negative Amortization",
        ["not_neg", "neg_amm"],
    )

    lump_sum_payment = st.selectbox(
        "Lump Sum Payment",
        ["not_lpsm", "lpsm"],
    )

    co_applicant_credit_type = st.selectbox(
        "Co-Applicant Credit Type",
        ["CIB", "EXP"],
    )


st.divider()


# -----------------------------
# Prediction
# -----------------------------

if st.button(
    "🔍 Predict Loan Default",
    type="primary",
    use_container_width=True,
):

    payload = {
        "loan_amount": loan_amount,
        "property_value": property_value,
        "income": income,
        "term": term,
        "dtir1": dtir1,
        "LTV": ltv,
        "loan_type": loan_type,
        "loan_purpose": loan_purpose,
        "occupancy_type": occupancy_type,
        "submission_of_application": submission_of_application,
        "Neg_ammortization": neg_ammortization,
        "lump_sum_payment": lump_sum_payment,
        "co-applicant_credit_type": co_applicant_credit_type,
        "age": age,
        "total_units": total_units,
    }

    try:

        with st.spinner("Running prediction..."):

            response = requests.post(
                f"{API_URL}/predict",
                json=payload,
                timeout=30,
            )

        if response.status_code == 200:

            result = response.json()

            st.success("Prediction completed successfully!")

            st.subheader("Prediction Result")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Default Probability",
                    f"{result['default_probability'] * 100:.2f}%",
                )

            with col2:
                st.metric(
                    "Risk Score",
                    result["risk_score"],
                )

            with col3:
                st.metric(
                    "Recommendation",
                    result["underwriting_recommendation"],
                )

            probability = result["default_probability"]

            st.progress(probability)

            if probability >= 0.50:
                st.error(
                    "⚠️ High Risk: Loan application should be rejected."
                )
            else:
                st.success(
                    "✅ Low Risk: Loan application can be approved."
                )

        else:

            st.error(
                f"API returned error {response.status_code}"
            )

            st.code(response.text)

    except requests.exceptions.RequestException as exc:

        st.error(
            "Unable to connect to the Loan Prediction API."
        )

        st.code(str(exc))