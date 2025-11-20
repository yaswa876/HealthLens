import streamlit as st
import pandas as pd
import os
from PIL import Image
import torch
from torchvision import transforms

# ------------------ Setup ------------------
USER_DB = "users.csv"
HISTORY_DB = "history.csv"

def init_db():
    if not os.path.exists(USER_DB):
        pd.DataFrame(columns=["username", "password"]).to_csv(USER_DB, index=False)
    if not os.path.exists(HISTORY_DB):
        pd.DataFrame(columns=["username", "symptoms", "diagnosis"]).to_csv(HISTORY_DB, index=False)

init_db()
# ------------------ Auth ------------------
def register(username, password):
    df = pd.read_csv(USER_DB)
    if username in df["username"].values:
        return False
    df = pd.concat([df, pd.DataFrame([{"username": username, "password": password}])], ignore_index=True)
    df.to_csv(USER_DB, index=False)
    return True

def login(username, password):
    df = pd.read_csv(USER_DB)
    return ((df["username"] == username) & (df["password"] == password)).any()
# ------------------ History ------------------
def save_history(username, symptoms, diagnosis):
    df = pd.read_csv(HISTORY_DB)
    df = pd.concat([df, pd.DataFrame([{"username": username, "symptoms": symptoms, "diagnosis": diagnosis}])], ignore_index=True)
    df.to_csv(HISTORY_DB, index=False)

def get_history(username):
    df = pd.read_csv(HISTORY_DB)
    return df[df["username"] == username]
# ------------------ Model ------------------
def load_model():
    # Dummy model logic for illustration
    return lambda img_tensor, text: "TB Positive" if "blood" in text.lower() else "Pneumonia Suspected"

def preprocess_image(image_file):
    image = Image.open(image_file).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])
    return transform(image).unsqueeze(0)

model = load_model()
# ------------------ Streamlit UI ------------------
st.set_page_config(page_title="HealthLens", layout="centered")
st.title("🩺 HealthLens: TB & Pneumonia Diagnosis")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
# Auth Panel
with st.expander(" Login / Register"):
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        username = st.text_input("Username", key="login_user")
…        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Register"):
            if register(new_user, new_pass):
                st.success("Registered successfully!")
            else:
                st.error("Username already exists")
# Diagnosis Panel
if st.session_state.logged_in:
    st.subheader("📋 Enter Symptoms and Upload Chest X-ray")
    symptoms = st.text_area("Describe symptoms (e.g. cough, fever, fatigue, blood in sputum)")
    image_file = st.file_uploader("Upload Chest X-ray", type=["jpg", "jpeg", "png"])

    if st.button("Diagnose"):
        if image_file and symptoms:
            img_tensor = preprocess_image(image_file)
            diagnosis = model(img_tensor, symptoms)
            st.success(f" Diagnosis: {diagnosis}")
            save_history(st.session_state.username, symptoms, diagnosis)
        else:
            st.warning("Please provide both image and symptoms")
# History Panel
    st.subheader(" Diagnosis History")
    history_df = get_history(st.session_state.username)
    st.dataframe(history_df)

else:
    st.info("Please login to access diagnosis and history.")
