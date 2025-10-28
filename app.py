import streamlit as st
import openai
import os
from PyPDF2 import PdfReader

st.title("🧾 RCM Applicability Checker (Simple Demo)")

# Get API key from environment (we'll add later in Streamlit Secrets)
openai.api_key = os.getenv("OPENAI_API_KEY")

st.write("Upload your RCM notification PDFs and describe the transaction.")

uploaded_files = st.file_uploader("Upload one or more Notification PDFs", type="pdf", accept_multiple_files=True)

transaction = st.text_area("Describe the transaction",
                           placeholder="e.g. GTA service to a registered company on 12-06-2024")

if st.button("Check RCM Applicability"):
    if not transaction:
        st.error("Please describe the transaction first.")
    else:
        st.info("AI analysing…")

        # extract text from uploaded pdfs
        combined_text = ""
        for f in uploaded_files:
            reader = PdfReader(f)
            for p in reader.pages:
                combined_text += p.extract_text() or ""

        prompt = f"""
        You are a GST expert. Based on these Notification extracts:
        {combined_text[:8000]}

        and this transaction:
        {transaction}

        Say clearly whether RCM applies or not and cite the notification number if applicable.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":prompt}],
                temperature=0,
                max_tokens=500
            )
            answer = response.choices[0].message.content
            st.success("AI Decision:")
            st.write(answer)
        except Exception as e:
            st.error(f"OpenAI error: {e}")
