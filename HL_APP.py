import streamlit as st
from PIL import Image
import numpy as np

# Page Config
st.set_page_config(page_title="HealthLens", page_icon="🩺", layout="wide")

# ---------------------------
# 🌈 Custom Styling (Aesthetic UI)
# ---------------------------
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
        }
        .main {
            background-color: #0e1117;
        }
        h1, h2, h3 {
            color: #00d4ff;
        }
        .stButton>button {
            background-color: #00d4ff;
            color: black;
            border-radius: 10px;
            height: 3em;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# 🩺 HEADER
# ---------------------------
st.title("🩺 HealthLens")
st.subheader("AI-powered Multimodal Medical Diagnosis")

st.markdown("---")

# ---------------------------
# 📊 DASHBOARD LAYOUT
# ---------------------------
col1, col2 = st.columns([1, 1])

# ---------------------------
# 📤 IMAGE INPUT
# ---------------------------
with col1:
    st.markdown("### 📤 Upload X-ray")
    uploaded_image = st.file_uploader("", type=["jpg", "png", "jpeg"])

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded X-ray", use_column_width=True)

# ---------------------------
# 🧾 SYMPTOMS INPUT
# ---------------------------
with col2:
    st.markdown("### 🧾 Enter Symptoms")

    symptoms = st.multiselect(
        "Select Symptoms",
        ["Cough", "Fever", "Chest Pain", "Breathlessness", "Fatigue", "Weight Loss"]
    )

    additional = st.text_input("Other symptoms")

# ---------------------------
# 🔍 ANALYZE BUTTON
# ---------------------------
st.markdown("---")
analyze = st.button("🔍 Analyze Patient Data")

# ---------------------------
# 📈 RESULTS SECTION
# ---------------------------
if analyze:
    if uploaded_image:
        st.markdown("## 🧠 Diagnosis Results")

        # Fake predictions (prototype)
        diseases = ["Pneumonia", "Tuberculosis"]
        confidence = np.random.uniform(60, 95, size=2)

        # Layout for results
        r1, r2 = st.columns(2)

        with r1:
            st.metric(label=diseases[0], value=f"{confidence[0]:.2f}%")

        with r2:
            st.metric(label=diseases[1], value=f"{confidence[1]:.2f}%")

        # Confidence bars
        st.markdown("### 📊 Confidence Levels")
        st.progress(int(confidence[0]))
        st.progress(int(confidence[1]))

        # Risk interpretation
        st.markdown("### ⚠️ Risk Insight")
        if max(confidence) > 80:
            st.error("High risk detected. Immediate medical consultation recommended.")
        else:
            st.warning("Moderate risk. Further tests advised.")

        # Footer note
        st.info("This is an AI-based prediction. Not a medical diagnosis.")

    else:
        st.warning("Please upload an X-ray image.")

# ---------------------------
# 📌 SIDEBAR (Extra Feature)
# ---------------------------
st.sidebar.title("📌 Dashboard Info")
st.sidebar.info("""
- Upload chest X-ray  
- Select symptoms  
- Get AI-based predictions  
""")

st.sidebar.markdown("### 🧬 Model Info")
st.sidebar.write("Multimodal CNN + Symptom Encoder (Prototype)")
