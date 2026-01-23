import streamlit as st
import time
import random
from backend.api_client import call_anthropic

# Lens definitions extracted from Decision_Storm.jsx
LENSES = {
    "Risk-First": {
        "prompt": "Analyze this scenario focusing primarily on risks, threats, and what could go wrong. What are the failure modes?",
        "color": "#fee2e2",  # red-50
        "border_color": "#fecaca",  # red-200
        "icon": "⚠️"
    },
    "Opportunity-First": {
        "prompt": "Analyze this scenario focusing primarily on opportunities, upside potential, and what could go right. What are the breakthrough possibilities?",
        "color": "#dcfce7",  # green-50
        "border_color": "#bbf7d0",  # green-200
        "icon": "📈"
    },
    "Resource-First": {
        "prompt": "Analyze this scenario focusing primarily on resource allocation, costs, and ROI. What does this require and what does it return?",
        "color": "#dbeafe",  # blue-50
        "border_color": "#bfdbfe",  # blue-200
        "icon": "💰"
    },
    "Timeline-First": {
        "prompt": "Analyze this scenario focusing primarily on timing, sequencing, and velocity. What should happen when, and how fast can we move?",
        "color": "#f3e8ff",  # purple-50
        "border_color": "#e9d5ff",  # purple-200
        "icon": "⏰"
    },
    "Stakeholder-First": {
        "prompt": "Analyze this scenario focusing primarily on people, stakeholders, and organizational dynamics. Who cares about this and how will they react?",
        "color": "#ffedd5",  # orange-50
        "border_color": "#fed7aa",  # orange-200
        "icon": "👥"
    },
    "Strategic-First": {
        "prompt": "Analyze this scenario focusing primarily on strategic positioning, competitive advantage, and long-term implications. How does this change the game?",
        "color": "#e0e7ff",  # indigo-50
        "border_color": "#c7d2fe",  # indigo-200
        "icon": "🎯"
    }
}


def render_decision_storm():
    """Render the Decision Storm Generator tool"""

    st.title("🔀 Decision Storm Generator")
    st.write("Transform one scenario into multiple strategic perspectives")

    # Input section
    st.markdown("---")
    scenario = st.text_area(
        "Enter Your Scenario or Decision",
        height=150,
        placeholder="Example: We're considering launching a new B2B SaaS product targeting mid-market companies. Initial development would take 6 months and $500K. Early customer interviews show strong interest but we'd be entering a crowded market...",
        key="ds_scenario"
    )

    # Controls
    col1, col2 = st.columns([1, 3])

    with col1:
        num_perspectives = st.selectbox(
            "Number of Perspectives",
            options=[2, 3, 4, 5, 6],
            index=1,  # default 3
            key="ds_count"
        )

    with col2:
        generate_btn = st.button(
            "⚡ Generate Decision Storms",
            disabled=(len(scenario.strip()) < 10),
            type="primary",
            use_container_width=True
        )

    st.caption("💡 Perspectives are generated one at a time to avoid rate limits. Each takes ~10 seconds.")

    # Generation logic
    if generate_btn and scenario.strip():
        # Clear previous results
        if 'ds_results' in st.session_state:
            del st.session_state.ds_results

        st.session_state.ds_results = []

        # Select random lenses
        selected_lens_names = random.sample(list(LENSES.keys()), num_perspectives)

        # Create a placeholder for progress
        progress_placeholder = st.empty()
        results_container = st.container()

        try:
            # Generate storms sequentially
            for i, lens_name in enumerate(selected_lens_names):
                lens = LENSES[lens_name]

                # Show progress
                with progress_placeholder.container():
                    st.info(f"⚡ Generating perspective {i+1}/{num_perspectives}: {lens['icon']} **{lens_name}**...")

                # Build the user message with explicit structure
                user_message = f"""{lens['prompt']}

SCENARIO:
{scenario}

Provide a focused analysis from this perspective. Be specific and actionable. Structure your response as:
1. Key Insight (one sentence)
2. Critical Factors (3-4 bullet points)
3. Recommended Action (one clear next step)

Keep it concise and decision-oriented."""

                # Call API
                try:
                    analysis = call_anthropic(
                        system_prompt="You are a strategic analyst. Provide structured analysis following the format exactly.",
                        user_message=user_message,
                        max_tokens=1000
                    )

                    # Store result
                    result = {
                        "lens_name": lens_name,
                        "icon": lens["icon"],
                        "color": lens["color"],
                        "border_color": lens["border_color"],
                        "analysis": analysis
                    }
                    st.session_state.ds_results.append(result)

                    # Display result immediately in colored container
                    with results_container:
                        display_storm_result(result)

                except Exception as e:
                    st.error(f"❌ Failed to generate {lens_name} perspective: {str(e)}")
                    continue

                # Delay before next call (except last)
                if i < len(selected_lens_names) - 1:
                    time.sleep(1)

            # Clear progress indicator
            progress_placeholder.empty()
            progress_placeholder.success(f"✅ Successfully generated {len(st.session_state.ds_results)} perspectives!")

        except Exception as e:
            st.error(f"❌ Error during generation: {str(e)}")

    # Display existing results (if any from previous generation)
    elif 'ds_results' in st.session_state and len(st.session_state.ds_results) > 0:
        st.markdown("---")
        st.subheader("Generated Perspectives")
        for result in st.session_state.ds_results:
            display_storm_result(result)

    else:
        # Empty state
        if not generate_btn:
            st.markdown("---")
            st.info("""
            ### 🌟 How It Works

            1. **Enter your scenario** - Describe a decision or situation you're facing
            2. **Choose perspectives** - Select how many different viewpoints you want (2-6)
            3. **Generate storms** - AI will analyze your scenario through multiple strategic lenses

            Each perspective provides:
            - A key insight
            - Critical factors to consider
            - A recommended next action
            """)

            # Show available lenses
            st.markdown("### 📋 Available Analytical Lenses")
            cols = st.columns(3)
            for idx, (lens_name, lens_data) in enumerate(LENSES.items()):
                with cols[idx % 3]:
                    st.markdown(f"{lens_data['icon']} **{lens_name}**")


def display_storm_result(result):
    """Display a single storm result in a colored container"""

    # Create colored container using markdown with custom HTML
    container_style = f"""
    <div style="
        background-color: {result['color']};
        border: 2px solid {result['border_color']};
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
    ">
        <h3 style="margin-top: 0;">{result['icon']} {result['lens_name']} Lens</h3>
    </div>
    """

    st.markdown(container_style, unsafe_allow_html=True)

    # Display analysis in an expander for better organization
    with st.expander("📄 View Analysis", expanded=True):
        st.markdown(result['analysis'])

        # Add copy button
        st.code(result['analysis'], language=None)

    st.markdown("")  # Add spacing
