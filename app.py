import streamlit as st
from backend.api_client import call_anthropic

# Page configuration
st.set_page_config(
    page_title="ClarityCrew Tools",
    page_icon="🛠️",
    layout="wide"
)

# Main app
def main():
    st.title("🛠️ ClarityCrew Tools")
    st.markdown("### Phase 1 Setup Complete")

    st.markdown("""
    Welcome to ClarityCrew Tools! This application hosts 6 AI-powered prompt generation tools.

    **Phase 1 Status:** ✅ Project structure and API connectivity established
    """)

    st.divider()

    # API Test Section
    st.subheader("🔌 API Connectivity Test")
    st.markdown("Click the button below to test the Anthropic API connection.")

    if st.button("Test API Connection", type="primary"):
        with st.spinner("Calling Anthropic API..."):
            try:
                system_prompt = "You are a helpful assistant. Respond concisely."
                user_message = "Say 'API connection successful!' and confirm you are Claude."

                response = call_anthropic(system_prompt, user_message, max_tokens=100)

                st.success("API call successful!")
                st.markdown("**Response:**")
                st.info(response)

            except Exception as e:
                st.error(f"API call failed: {str(e)}")
                st.markdown("**Troubleshooting:**")
                st.markdown("- Ensure your `.env` file exists with a valid `ANTHROPIC_API_KEY`")
                st.markdown("- Check that you've installed all dependencies: `pip install -r requirements.txt`")

    st.divider()

    # Project Information
    with st.expander("ℹ️ Project Information"):
        st.markdown("""
        **Tech Stack:**
        - Frontend: Streamlit
        - Backend: Python
        - AI Model: Claude Sonnet 4 (claude-sonnet-4-20250514)

        **Next Steps:**
        Phase 2 will add the 6 prompt generation tools from the artifacts.
        """)

if __name__ == "__main__":
    main()
