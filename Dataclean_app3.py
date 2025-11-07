import streamlit as st
import pandas as pd
import io
import csv

# --- PAGE CONFIG ---
st.set_page_config(page_title="🧹 Data Cleaning App", layout="wide", page_icon="🧼")

# --- CUSTOM HTML / CSS STYLING ---
st.markdown("""
<style>
    body {
        background-color: #f5f7fa;
    }
    .main {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0px 2px 15px rgba(0, 0, 0, 0.05);
    }
    h1, h2, h3 {
        color: #2b6cb0;
        font-family: 'Segoe UI', sans-serif;
    }
    .stApp {
        background: linear-gradient(120deg, #dbeafe 0%, #f0fdf4 100%);
    }
    .stButton>button {
        background-color: #4c6ef5;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
        font-size: 15px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #364fc7;
        color: #f8f9fa;
    }
    .signature {
        text-align: center;
        font-size: 15px;
        color: #718096;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.title("🧹 Data Cleaning Application")
st.markdown(
    "<p style='text-align:center; font-size:18px; color:#4A5568; font-weight:bold;'>"
    "Upload any dataset, view it neatly, and clean it easily!"
    "</p>",
    unsafe_allow_html=True
)

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader(
    "📂 Upload your file", 
    type=["csv", "xlsx", "xls", "txt", "json", "xml"]
)

if uploaded_file is not None:
    try:
        file_name = uploaded_file.name.lower()

        # --- Detect File Type Automatically ---
        if file_name.endswith((".csv", ".txt")):
            sample = uploaded_file.read(2048).decode("utf-8", errors="ignore")
            uploaded_file.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample)
                sep = dialect.delimiter
            except csv.Error:
                sep = ","
            df = pd.read_csv(uploaded_file, sep=sep)
            st.success(f"✅ File uploaded successfully! (Detected separator: '{sep}')")

        elif file_name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
            st.success("✅ Excel file uploaded successfully!")

        elif file_name.endswith(".json"):
            df = pd.read_json(uploaded_file)
            st.success("✅ JSON file uploaded successfully!")

        elif file_name.endswith(".xml"):
            df = pd.read_xml(uploaded_file)
            st.success("✅ XML file uploaded successfully!")

        else:
            st.error("❌ Unsupported file format. Please upload a CSV, Excel, TXT, JSON, XML, or HTML file.")
            st.stop()

        # --- DATASET OVERVIEW ---
        st.subheader("📊 Dataset Overview")
        st.markdown(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")

        col_summary = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str),
            "Missing Values": df.isnull().sum(),
            "Unique Values": df.nunique()
        })
        st.dataframe(col_summary, use_container_width=True)

        # --- DATA PREVIEW ---
        st.subheader("👀 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # --- INFO SUMMARY ---
        st.subheader("🧾 Info Summary")
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())

        # --- QUICK STATS ---
        st.write("**Total Missing Values:**", df.isnull().sum().sum())
        st.write("**Total Duplicate Records:**", df.duplicated().sum())
        st.markdown("---")

        # --- CLEANING OPTIONS ---
        st.subheader("🧰 Data Cleaning Options")
        col1, col2, col3, col4 = st.columns(4)

        # 1️⃣ Remove Missing Values
        with col1:
            if st.button("🚮 Remove Missing Values"):
                cleaned_df = df.dropna()
                csv_bytes = cleaned_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇️ Download CSV (No Missing Values)",
                    csv_bytes,
                    "cleaned_no_missing.csv",
                    "text/csv"
                )
                st.success("✅ Missing values removed successfully!")
                st.snow()

        # 2️⃣ Handle Missing Values
        with col2:
            if st.button("🧩 Handle Missing Values"):
                cleaned_df = df.copy()
                for col in cleaned_df.select_dtypes(include=["object"]).columns:
                    cleaned_df[col].fillna(cleaned_df[col].mode()[0], inplace=True)
                for col in cleaned_df.select_dtypes(include=["number"]).columns:
                    cleaned_df[col].interpolate(inplace=True)
                csv_bytes = cleaned_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇️ Download CSV (Handled Missing Values)",
                    csv_bytes,
                    "cleaned_handled_missing.csv",
                    "text/csv"
                )
                st.success("✅ Missing values handled successfully!")
                st.snow()

        # 3️⃣ Remove Duplicates
        with col3:
            if st.button("🧽 Remove Duplicate Records"):
                cleaned_df = df.drop_duplicates()
                csv_bytes = cleaned_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇️ Download CSV (No Duplicates)",
                    csv_bytes,
                    "cleaned_no_duplicates.csv",
                    "text/csv"
                )
                st.success("✅ Duplicate records removed successfully!")
                st.snow()

        # 4️⃣ Handle Missing + Duplicates
        with col4:
            if st.button("🔧 Handle Missing + Remove Duplicates"):
                cleaned_df = df.copy()
                for col in cleaned_df.select_dtypes(include=["object"]).columns:
                    cleaned_df[col].fillna(cleaned_df[col].mode()[0], inplace=True)
                for col in cleaned_df.select_dtypes(include=["number"]).columns:
                    cleaned_df[col].interpolate(inplace=True)
                cleaned_df.drop_duplicates(inplace=True)
                csv_bytes = cleaned_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇️ Download CSV (Handled Missing + No Duplicates)",
                    csv_bytes,
                    "cleaned_handled_no_duplicates.csv",
                    "text/csv"
                )
                st.success("✅ Cleaned successfully (missing handled + duplicates removed)!")
                st.balloons()

    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")

else:
    st.info("📁 Please upload a dataset to begin cleaning.")

# --- FOOTER ---
st.markdown('<p class="signature">Made with 🧠 by <b>IZZAHTAJUL 😎</b> using Streamlit | 2025 📊 Data Cleaning Dashboard</p>', unsafe_allow_html=True)
