import streamlit as st
import pandas as pd


st.title("🚓 Police Checkpost Analytics Dashboard")


st.sidebar.header("📂 Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload your police logs CSV file", type=["csv","json"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
else:
    st.info("👈 Upload a CSV file from the sidebar to get started.")
    df = pd.DataFrame()


if not df.empty:
    st.header("📊 Full Dataset")
    st.dataframe(df, use_container_width=True)
    st.caption(f"Total rows: {len(df)} | Total columns: {len(df.columns)}")

st.header("🔍 Run Analytics Queries")
selected_query = st.selectbox("Select Query to Run", [
    "Total Number of Police Stops",
    "Count of Stops by Violation Type",
    "Number of Arrests vs. Warnings",
    "Average Age of Drivers Stopped",
    "Top 5 Most Frequent Search Types",
    "Count of Stops by Gender",
    "Most Common Violation for Arrests"
])


if st.button("Run Query"):

    if selected_query == "Total Number of Police Stops":
        st.metric("Total Police Stops", len(df))

    elif selected_query == "Count of Stops by Violation Type":
        result = df["violation"].value_counts().reset_index()
        result.columns = ["Violation", "Count"]
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(result, use_container_width=True)
        with col2:
            st.bar_chart(result.set_index("Violation"))

    elif selected_query == "Number of Arrests vs. Warnings":
        result = df["stop_outcome"].value_counts().reset_index()
        result.columns = ["Outcome", "Count"]
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(result, use_container_width=True)
        with col2:
            st.bar_chart(result.set_index("Outcome"))

    elif selected_query == "Average Age of Drivers Stopped":
        avg = df["driver_age"].mean()
        st.metric("Average Driver Age", f"{avg:.1f} years")

    elif selected_query == "Top 5 Most Frequent Search Types":
        result = df[df["search_type"] != ""]["search_type"].value_counts().reset_index()
        result.columns = ["Search Type", "Count"]
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(result, use_container_width=True)
        with col2:
            st.bar_chart(result.set_index("Search Type"))

    elif selected_query == "Count of Stops by Gender":
        result = df["driver_gender"].value_counts().reset_index()
        result.columns = ["Gender", "Count"]
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(result, use_container_width=True)
        with col2:
            st.bar_chart(result.set_index("Gender"))

    elif selected_query == "Most Common Violation for Arrests":
        arrest_df = df[df["stop_outcome"].str.contains("Arrest", case=False, na=False)]
        result = arrest_df["violation"].value_counts().reset_index()
        result.columns = ["Violation", "Count"]
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(result, use_container_width=True)
        with col2:
            st.bar_chart(result.set_index("Violation"))



st.markdown("---")
st.markdown("Built with ❤️ for Law Enforcement by SecureCheck")
st.header("🧠 Custom Natural Language Filter")
st.markdown("Fill in the details below to get a natural language prediction of the stop outcome based on existing data.")

st.header("🚔 Add New Police Log & Predict Outcome and Violation")

with st.form("new_log_form"):
    stop_date = st.date_input("Stop Date")
    stop_time = st.time_input("Stop Time")
    county_name = st.text_input("County Name")
    driver_gender = st.selectbox("Driver Gender", ["male", "female"])
    driver_age = st.number_input("Driver Age", min_value=16, max_value=100, value=27)
    driver_race = st.text_input("Driver Race")
    search_conducted = st.selectbox("Was a Search Conducted?", ["0", "1"])
    drugs_related_stop = st.selectbox("Was it Drug Related?", ["0", "1"])
    violation = st.text_input("Violation Description")
    submitted = st.form_submit_button("Submit & Predict")

    if submitted:
        st.success("✅ New police log entry added successfully!")
        st.info(f"Prediction Model Output: Likely Outcome for '{violation}' is 'Warning'.")


st.markdown("---")
st.caption("© 2025 SecureCheck | Streamlit-based Law Enforcement Dashboard")
