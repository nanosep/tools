import streamlit as st
from backend.api_client import call_anthropic
from tools.decision_storm import render_decision_storm
from tools.chain_bundle_inception import render_chain_bundle_inception
from tools.advance_techs import render_advance_techs
from tools.creative_thinking import render_creative_thinking
from tools.image_prompt import render_image_prompt
from tools.correlation_explainer import render_correlation_explainer

# Page configuration
st.set_page_config(
    page_title="ClarityCrew Tools",
    page_icon="🛠️",
    layout="wide"
)


def render_home():
    """Render the home page with API test"""
    st.title("🛠️ ClarityCrew Tools")
    st.markdown("### Welcome to AI-Powered Prompt Generation")

    st.markdown("""
    ClarityCrew Tools hosts 6 AI-powered prompt generation tools to help you analyze scenarios,
    generate creative ideas, and make better decisions.

    **Status:** ✅ **COMPLETE** - All 6 tools active! 🎉
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

    # Available Tools
    st.subheader("📦 Available Tools")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### ✅ Active Tools (6/6) 🎉
        - 🔀 **Decision Storm** - Multiple strategic perspectives
        - 🔗 **Chain, Bundle & Inception** - Sequential/parallel/meta-prompts
        - 🚀 **Advanced Techniques** - 11 cutting-edge techniques
        """)

    with col2:
        st.markdown("""
        #### ✅ More Tools
        - 🎨 **Creative Thinking** - 24 methods, department-adapted
        - 🖼️ **Image Prompt** - AI image generation prompts
        - 🔬 **Correlation Explainer** - Educational: 8 correlation types
        """)

    # Project Information
    with st.expander("ℹ️ Project Information"):
        st.markdown("""
        **Tech Stack:**
        - Frontend: Streamlit
        - Backend: Python
        - AI Model: Claude Sonnet 4 (claude-sonnet-4-20250514)

        **Repository:** https://github.com/nanosep/tools
        """)


def main():
    """Main application with navigation"""

    # Sidebar navigation
    st.sidebar.title("🛠️ ClarityCrew Tools")
    st.sidebar.markdown("---")

    # Tool selection
    tool = st.sidebar.radio(
        "Select Tool",
        options=["🏠 Home", "🔀 Decision Storm", "🔗 Chain, Bundle & Inception", "🚀 Advanced Techniques", "🎨 Creative Thinking", "🖼️ Image Prompt", "🔬 Correlation Explainer"],
        index=0
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### About
    AI-powered prompt generation tools using Claude Sonnet 4.

    **Phase 2 Active**
    """)

    # Route to selected tool
    if tool == "🏠 Home":
        render_home()
    elif tool == "🔀 Decision Storm":
        render_decision_storm()
    elif tool == "🔗 Chain, Bundle & Inception":
        render_chain_bundle_inception()
    elif tool == "🚀 Advanced Techniques":
        render_advance_techs()
    elif tool == "🎨 Creative Thinking":
        render_creative_thinking()
    elif tool == "🖼️ Image Prompt":
        render_image_prompt()
    elif tool == "🔬 Correlation Explainer":
        render_correlation_explainer()


if __name__ == "__main__":
    main()
