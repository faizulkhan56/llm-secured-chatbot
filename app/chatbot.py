import streamlit as st
from llm_guard_init import prompt_scanner, output_scanner
from utils import evaluate_challenges
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Streamlit config
st.set_page_config(page_title="LLM Secured Chatbot")

# Session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# UI Tabs
tab1, tab2 = st.tabs(["🤖 Chatbot", "🧪 Auto Vulnerability Scan"])

with tab1:
    st.title("🔐 LLM-Guarded Chatbot")
    user_input = st.text_input("Ask me anything:", key="user_input")

    if user_input:
        # Scan input using LLM Guard
        cleaned_prompt, prompt_issues = prompt_scanner(user_input)

        if prompt_issues:
            st.error("❌ Prompt blocked due to possible injection or unsafe patterns.")
            st.session_state.history.append((user_input, "Blocked by input scanner"))
        else:
            try:
                # Call OpenAI using new SDK
                completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": cleaned_prompt}]
                )
                raw_response = completion.choices[0].message.content

                # Sanitize output
                safe_response, output_issues = output_scanner(raw_response)

                if output_issues:
                    st.warning("⚠️ Output sanitized due to potential sensitive data.")
                    response = safe_response
                else:
                    response = raw_response

                st.session_state.history.append((user_input, response))

            except Exception as e:
                st.error(f"OpenAI API Error: {str(e)}")

    # Show chat history
    for user, bot in st.session_state.history:
        st.markdown(f"**🧑 You:** {user}")
        st.markdown(f"**🤖 Bot:** {bot}")

with tab2:
    st.title("🧪 Auto Vulnerability Scan")
    if st.button("Run Scan Now"):
        results = evaluate_challenges()
        for item in results:
            emoji = "✅" if item["status"] == "Passed" else "❌"
            st.markdown(f"{emoji} [{item['challenge']}] `{item['prompt']}` → {item['status']}")

