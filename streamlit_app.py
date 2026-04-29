import streamlit as st
from app import pipeline
import json

st.set_page_config(page_title="AI Support Agent", layout="centered")

st.title("🤖 Mumzworld AI Support Assistant")
st.write("Multilingual (English + Arabic) customer support triage system")

# Input box
user_input = st.text_area("Enter customer message:")

if st.button("Analyze"):
    if not user_input.strip():
        st.warning("Please enter a message.")
    else:
        with st.spinner("Processing..."):
            result = pipeline(user_input)

        st.subheader("📊 Result")

        # Pretty JSON display
        st.json(result)

        # Highlight key fields
        if "intent" in result:
            st.success(f"Intent: {result['intent']}")
            st.info(f"Urgency: {result['urgency']}")
            st.write(f"Confidence: {result['confidence']}")

            st.subheader("💬 Response")

            st.markdown("**English:**")
            st.write(result["reply"]["en"])

            st.markdown("**Arabic:**")
            st.write(result["reply"]["ar"])

        if result.get("requires_human"):
            st.error("⚠️ Requires human attention")