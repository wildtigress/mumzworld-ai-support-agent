import streamlit as st
from app import pipeline

st.set_page_config(page_title="Mumzworld AI Support", layout="centered")

# ---------------------------
# Header
# ---------------------------
st.title("🤖 Mumzworld AI Support Assistant")
st.write("Multilingual (English + Arabic) customer support triage system")

# ---------------------------
# Input
# ---------------------------
user_input = st.text_area("Enter customer message:", height=120)

# ---------------------------
# Action
# ---------------------------
if st.button("Analyze"):

    if not user_input.strip():
        st.warning("Please enter a message.")
    else:
        with st.spinner("Processing..."):
            result = pipeline(user_input)

        st.divider()
        st.subheader("📊 Structured Output")

        # Always show raw JSON (important for credibility)
        st.json(result)

        # ---------------------------
        # Error / fallback handling
        # ---------------------------
        if "reply" not in result:
            st.error("⚠️ System could not process the request properly.")
            st.write(result)
            st.stop()

        # ---------------------------
        # Status (AI vs Human)
        # ---------------------------
        st.subheader("📌 Status")

        if result.get("requires_human"):
            st.error("⚠️ Escalated to Human Agent")
        else:
            st.success("✅ Handled by AI")

        # ---------------------------
        # Analysis
        # ---------------------------
        st.subheader("🧠 Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Intent", result.get("intent", "N/A"))

        with col2:
            st.metric("Confidence", result.get("confidence", "N/A"))

        # ---------------------------
        # Responses
        # ---------------------------
        st.subheader("💬 Response")

        st.markdown("### 🇬🇧 English")
        st.write(result["reply"].get("en", ""))

        st.markdown("### 🇸🇦 Arabic")
        st.write(result["reply"].get("ar", ""))