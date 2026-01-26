import streamlit as st
from backend.api_client import call_anthropic
from tools.decision_storm import render_decision_storm
from tools.chain_bundle_inception import render_chain_bundle_inception
from tools.advance_techs import render_advance_techs
from tools.creative_thinking import render_creative_thinking
from tools.image_prompt import render_image_prompt
# from tools.correlation_explainer import render_correlation_explainer  # Removed for enterprise focus

# Page configuration
st.set_page_config(
    page_title="ClarityCrew Tools",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional white theme styling
st.markdown("""
    <style>
    /* Main content area */
    .main {
        background-color: #FFFFFF;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #F8F9FA;
        border-right: 1px solid #E1E4E8;
    }

    /* Headers */
    h1, h2, h3 {
        color: #1A1A1A;
        font-weight: 600;
    }

    /* Buttons */
    .stButton>button {
        background-color: #0066CC;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }

    .stButton>button:hover {
        background-color: #0052A3;
    }

    /* Input fields */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        background-color: #FFFFFF;
        border: 1px solid #D1D5DB;
        border-radius: 6px;
    }

    /* Code blocks */
    .stCodeBlock {
        background-color: #F8F9FA;
        border: 1px solid #E1E4E8;
        border-radius: 6px;
    }

    /* Info/success/warning boxes - lighter versions */
    .stAlert {
        background-color: #F0F4F8;
        border-left: 4px solid #0066CC;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #F8F9FA;
        border-radius: 6px;
    }

    /* Cards/containers */
    [data-testid="stHorizontalBlock"] {
        gap: 1rem;
    }

    /* Remove dark backgrounds from all elements */
    .element-container {
        background-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)


def render_home():
    """Render the home page with API test"""
    st.title("🛠️ ClarityCrew Tools")
    st.markdown("### Welcome to AI-Powered Prompt Generation")

    st.markdown("""
    ClarityCrew Tools hosts 5 AI-powered prompt generation tools optimized for enterprise consulting,
    M&A advisory, and strategic transformation engagements.

    **Status:** ✅ **COMPLETE** - All 5 tools active! 🎉

    **Target Users:** Strategy consultants, M&A advisors, corporate development teams, transformation PMOs
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
        #### ✅ Active Tools (5/5) 🎉
        1. **Chain, Bundle & Inception** - TSA strategies, integration planning
        2. **Advanced Techniques** - ERP separation, tax structures, synergy analysis
        3. **Creative Thinking** - Talent retention, synergy identification, communication plans
        """)

    with col2:
        st.markdown("""
        #### ✅ More Tools
        4. **Decision Storm** - Build vs buy, divestiture options, timeline decisions
        5. **Image Prompt Generator** - Executive presentations, org charts, process flows
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
        options=["🏠 Home", "🔗 Chain, Bundle & Inception", "🚀 Advanced Techniques", "🎨 Creative Thinking", "🌪️ Decision Storm", "🖼️ Image Prompt"],
        index=0
    )

    st.sidebar.markdown("---")

    # About section with expander
    with st.sidebar.expander("ℹ️ About ClarityCrew Tools"):
        st.markdown("""
        **5 AI-Powered Tools** for enterprise consulting and M&A advisory:

        - Chain/Bundle/Inception: TSA strategies, integration planning
        - Advanced Techniques: ERP separation, tax optimization
        - Creative Thinking: Synergy identification, talent retention
        - Decision Storm: Build vs buy, divestiture analysis
        - Image Prompts: Executive presentations, org charts

        **Powered by:** Claude Sonnet 4.5
        **Model:** `claude-sonnet-4-20250514`

        **Status:** ✅ All 5 tools complete
        **Focus:** M&A, carve-outs, transformation
        """)

    # Route to selected tool
    if tool == "🏠 Home":
        render_home()
    elif tool == "🔗 Chain, Bundle & Inception":
        render_chain_bundle_inception()
    elif tool == "🚀 Advanced Techniques":
        render_advance_techs()
    elif tool == "🎨 Creative Thinking":
        render_creative_thinking()
    elif tool == "🌪️ Decision Storm":
        render_decision_storm()
    elif tool == "🖼️ Image Prompt":
        render_image_prompt()


if __name__ == "__main__":
    main()
