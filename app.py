import streamlit as st
import os
import json
from scripts.pipeline_demo import run_demo_pipeline
from scripts.pipeline_onboarding import run_onboarding_pipeline

st.set_page_config(page_title="Clara Automation Dashboard", layout="wide")

st.title("Clara Voice Agent Automation Dashboard")

st.markdown("Demo → v1 | Onboarding → v2 | Version Controlled")

# Upload Demo Transcript
st.header("1️⃣ Upload Demo Transcript")
demo_file = st.file_uploader("Upload Demo Transcript (.txt)", type=["txt"])

if demo_file:
    demo_path = os.path.join("dataset/demo", demo_file.name)
    with open(demo_path, "wb") as f:
        f.write(demo_file.read())

    st.success("Demo transcript saved.")
    run_demo_pipeline(demo_path)
    st.success("v1 generated successfully.")

# Upload Onboarding Transcript
st.header("2️⃣ Upload Onboarding Transcript")
account_id = st.text_input("Enter Account ID for onboarding update")

onboarding_file = st.file_uploader("Upload Onboarding Transcript (.txt)", type=["txt"])

if onboarding_file and account_id:
    onboarding_path = os.path.join("dataset/onboarding", onboarding_file.name)
    with open(onboarding_path, "wb") as f:
        f.write(onboarding_file.read())

    st.success("Onboarding transcript saved.")
    run_onboarding_pipeline(account_id, onboarding_path)
    st.success("v2 processed.")

# View Account Data
st.header("3️⃣ View Account Data")

view_id = st.text_input("Enter Account ID to View Outputs")

if view_id:
    v1_path = f"outputs/accounts/{view_id}/v1/account_memo.json"
    v2_path = f"outputs/accounts/{view_id}/v2/account_memo.json"

    if os.path.exists(v1_path):
        st.subheader("v1 Account Memo")
        with open(v1_path) as f:
            st.json(json.load(f))

    if os.path.exists(v2_path):
        st.subheader("v2 Account Memo")
        with open(v2_path) as f:
            st.json(json.load(f))

        changelog_path = f"outputs/accounts/{view_id}/v2/changelog.json"
        if os.path.exists(changelog_path):
            st.subheader("Changelog")
            with open(changelog_path) as f:
                st.json(json.load(f))