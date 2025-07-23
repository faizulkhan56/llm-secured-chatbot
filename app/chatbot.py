import streamlit as st
import openai
from dotenv import load_dotenv
import os

from app.llm_guard_init import prompt_scanner, output_scanner
from app.utils import evaluate_challenges  # NEW

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("🛡️ LLM-Secured Chatbot")

tab1, tab2 = st.tabs(["💬 Chatbot", "🧪 Auto Vulnerability Scan"])

# ---------------- Tab 1: Chatbot ----------------
with tab1:
    user_input = st.text_input("Ask me anything:", key="user_input")

    if "history" not in st.session_state:
        st.session_state.history = []

    if user_input:
        cleaned_prompt, prompt_issues = prompt_scanner.scan(user_input)

        if prompt_issues:
            response = "⚠️ Your prompt was blocked for security reasons."
        else:
            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": cleaned_prompt}]
                )
                raw_response = completion.choices[0].message["content"]
                safe_response, output_issues = output_scanner.scan(raw_response)

                response = safe_response if not output_issues else "⚠️ Output blocked due to sensitive content."

            except Exception as e:
                response = f"⚠️ Error: {e}"

        st.session_state.history.append((user_input, response))

    for user, bot in st.session_state.history:
        st.markdown(f"**🧑 You:** {user}")
        st.markdown(f"**🤖 Bot:** {bot}")

# ---------------- Tab 2: Auto Scan ----------------
with tab2:
    st.markdown("## 🔎 PromptMe Vulnerability Evaluation")
    if st.button("Run Scan Now"):
        with st.spinner("Running vulnerability scan..."):
            results = evaluate_challenges()
        st.success("✅ Scan Complete")

        for challenge, prompt, verdict in results:
            st.markdown(f"**{challenge}** → _{prompt}_  \n➡️ **{verdict}**")
