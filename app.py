import streamlit as st
from backend.api_client import call_anthropic
from tools.decision_storm import render_decision_storm
from tools.chain_bundle_inception import render_chain_bundle_inception
from tools.advance_techs import render_advance_techs
from tools.creative_thinking import render_creative_thinking
from tools.image_prompt import render_image_prompt
from tools.prompt_templates import render_prompt_templates
from tools.creative_content import render_creative_content
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


def main():
    """Main application with navigation"""

    # Sidebar navigation
    st.sidebar.title("🛠️ ClarityCrew Tools")
    st.sidebar.markdown("---")

    # Tool selection
    tool = st.sidebar.radio(
        "Select Tool",
        options=[
            "🔗 Chain, Bundle & Inception",
            "🚀 Advanced Techniques",
            "🎨 Creative Thinking",
            "🌪️ Decision Storm",
            "🖼️ Image Prompt Generator",
            "📚 Prompt Templates",
            "🎬 Creative Content for Business"
        ],
        index=0,
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")

    # About section with expander
    with st.sidebar.expander("ℹ️ About ClarityCrew Tools"):
        st.markdown("""
        **7 AI-Powered Tools** for enterprise consulting and M&A advisory:

        - Chain/Bundle/Inception: TSA strategies, integration planning
        - Advanced Techniques: ERP separation, tax optimization
        - Creative Thinking: Synergy identification, talent retention
        - Decision Storm: Build vs buy, divestiture analysis
        - Image Prompt Generator: Executive presentations, org charts
        - Prompt Templates: Ready-to-use enterprise prompts
        - Creative Content for Business: AI media use case catalog

        **Powered by:** Claude Sonnet 4.5
        **Model:** `claude-sonnet-4-20250514`

        **Status:** ✅ All 7 tools complete
        **Focus:** M&A, carve-outs, transformation
        """)

    # Route to selected tool
    if tool == "🔗 Chain, Bundle & Inception":
        render_chain_bundle_inception()
    elif tool == "🚀 Advanced Techniques":
        render_advance_techs()
    elif tool == "🎨 Creative Thinking":
        render_creative_thinking()
    elif tool == "🌪️ Decision Storm":
        render_decision_storm()
    elif tool == "🖼️ Image Prompt Generator":
        render_image_prompt()
    elif tool == "📚 Prompt Templates":
        render_prompt_templates()
    elif tool == "🎬 Creative Content for Business":
        render_creative_content()


if __name__ == "__main__":
    main()
