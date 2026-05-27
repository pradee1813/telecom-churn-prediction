import streamlit as st
import joblib
import numpy as np

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Telecom Churn Prediction",
    page_icon="📱",
    layout="centered"
)


# ---------------- LOAD MODEL ---------------- #

model = joblib.load("churn_model.pkl")

# ---------------- SESSION STATES ---------------- #

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "input"

# ---------------- LOGIN PAGE ---------------- #

if not st.session_state.logged_in:

    st.title("🔐 Login Page")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username == "admin" and password == "1234":

            st.session_state.logged_in = True

            st.rerun()

        else:

            st.error("Invalid Username or Password")

# ---------------- INPUT PAGE ---------------- #

elif st.session_state.page == "input":

    st.title("📱 Telecom Churn Prediction")

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    SeniorCitizen = st.selectbox(
        "Senior Citizen",
        ["No", "Yes"]
    )

    Partner = st.selectbox(
        "Partner",
        ["No", "Yes"]
    )

    Dependents = st.selectbox(
        "Dependents",
        ["No", "Yes"]
    )

    tenure = st.number_input("Tenure")

    PhoneService = st.selectbox(
        "Phone Service",
        ["No", "Yes"]
    )

    MultipleLines = st.selectbox(
        "Multiple Lines",
        ["No", "Yes"]
    )

    InternetService = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"]
    )

    OnlineSecurity = st.selectbox(
        "Online Security",
        ["No", "Yes"]
    )

    OnlineBackup = st.selectbox(
        "Online Backup",
        ["No", "Yes"]
    )

    DeviceProtection = st.selectbox(
        "Device Protection",
        ["No", "Yes"]
    )

    TechSupport = st.selectbox(
        "Tech Support",
        ["No", "Yes"]
    )

    StreamingTV = st.selectbox(
        "Streaming TV",
        ["No", "Yes"]
    )

    StreamingMovies = st.selectbox(
        "Streaming Movies",
        ["No", "Yes"]
    )

    Contract = st.selectbox(
        "Contract",
        ["Month-to-month", "One year", "Two year"]
    )

    PaperlessBilling = st.selectbox(
        "Paperless Billing",
        ["No", "Yes"]
    )

    PaymentMethod = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer",
            "Credit card"
        ]
    )

    MonthlyCharges = st.number_input(
        "Monthly Charges"
    )

    EstimatedTotalCharges = st.number_input(
        "Estimated Total Charges"
    )

    # ---------------- ENCODING ---------------- #

    gender = 1 if gender == "Male" else 0
    SeniorCitizen = 1 if SeniorCitizen == "Yes" else 0
    Partner = 1 if Partner == "Yes" else 0
    Dependents = 1 if Dependents == "Yes" else 0
    PhoneService = 1 if PhoneService == "Yes" else 0
    MultipleLines = 1 if MultipleLines == "Yes" else 0
    OnlineSecurity = 1 if OnlineSecurity == "Yes" else 0
    OnlineBackup = 1 if OnlineBackup == "Yes" else 0
    DeviceProtection = 1 if DeviceProtection == "Yes" else 0
    TechSupport = 1 if TechSupport == "Yes" else 0
    StreamingTV = 1 if StreamingTV == "Yes" else 0
    StreamingMovies = 1 if StreamingMovies == "Yes" else 0
    PaperlessBilling = 1 if PaperlessBilling == "Yes" else 0

    InternetService = {
        "DSL": 0,
        "Fiber optic": 1,
        "No": 2
    }[InternetService]

    Contract = {
        "Month-to-month": 0,
        "One year": 1,
        "Two year": 2
    }[Contract]

    PaymentMethod = {
        "Electronic check": 0,
        "Mailed check": 1,
        "Bank transfer": 2,
        "Credit card": 3
    }[PaymentMethod]

    # ---------------- PREDICT BUTTON ---------------- #

    if st.button("Predict"):

        data = np.array([[
            gender,
            SeniorCitizen,
            Partner,
            Dependents,
            tenure,
            PhoneService,
            MultipleLines,
            InternetService,
            OnlineSecurity,
            OnlineBackup,
            DeviceProtection,
            TechSupport,
            StreamingTV,
            StreamingMovies,
            Contract,
            PaperlessBilling,
            PaymentMethod,
            MonthlyCharges,
            EstimatedTotalCharges
        ]])

        prediction = model.predict(data)

        probability = model.predict_proba(data)

        st.session_state.prediction = prediction[0]

        st.session_state.probability = (
            probability[0][1] * 100
        )

        st.session_state.page = "result"

        st.rerun()

# ---------------- RESULT PAGE ---------------- #

elif st.session_state.page == "result":

    st.title("📊 Prediction Result")

    if st.session_state.prediction == 1:

        st.error("⚠️ Customer Will Churn")

    else:

        st.success("✅ Customer Will Not Churn")

    st.info(
        f"Churn Probability: "
        f"{st.session_state.probability:.2f}%"
    )

    if st.button("Back"):

        st.session_state.page = "input"

        st.rerun()

    if st.button("Logout"):

        st.session_state.logged_in = False

        st.session_state.page = "input"

        st.rerun()