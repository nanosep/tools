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

    # Info expander
    with st.expander("ℹ️ How Decision Storm Works"):
        st.markdown("""
        This tool analyzes your scenario through **6 different analytical lenses**:

        - ⚠️ **Risk-First** - Threats, failure modes, what could go wrong
        - 📈 **Opportunity-First** - Upside potential, breakthrough possibilities
        - 💰 **Resource-First** - Costs, ROI, resource allocation
        - ⏰ **Timeline-First** - Timing, sequencing, velocity
        - 👥 **Stakeholder-First** - People, organizational dynamics
        - 🎯 **Strategic-First** - Competitive advantage, long-term impact

        **How to use:** Enter your scenario, choose 2-6 perspectives, and generate.
        Each perspective will provide a unique strategic analysis through its specific lens.
        """)

    # Examples section
    with st.expander("💡 Try These Examples", expanded=False):
        st.markdown("Click any example to auto-fill the form:")

        examples = {
            "Build vs Buy vs Partner (Systems)": {
                "scenario": "NewCo needs standalone ERP system post-carve-out. Options: 1) Build custom SAP instance (€40M, 18 months), 2) Buy Oracle Cloud ERP (€25M, 12 months), 3) Partner with managed services provider (€8M/year, 6 months). Each has different risk profiles for Day 1 readiness.",
                "count": 5,
                "description": "Risk, Opportunity, Resource, Timeline, Stakeholder perspectives"
            },
            "Divestiture vs IPO vs Shut Down": {
                "scenario": "Parent company evaluating exit options for underperforming €800M division. Divestiture offers €500M (60% of book value), IPO could achieve €700M but risky market conditions, orderly wind-down costs €200M but eliminates ongoing losses. 2,500 employees affected.",
                "count": 6,
                "description": "Strategic, Financial, Risk, Stakeholder, Timeline, Reputational lenses"
            },
            "Aggressive vs Phased Separation Timeline": {
                "scenario": "Carve-out separation can be completed in 12 months (aggressive, high risk, saves €15M in TSA costs) or 24 months (phased, lower risk, higher transition costs). Regulatory approval timing uncertain. Parent wants quick exit, NewCo management prefers caution.",
                "count": 4,
                "description": "Risk-First, Opportunity-First, Resource-First, Stakeholder-First"
            },
            "Offshore vs Nearshore vs Onshore Shared Services": {
                "scenario": "NewCo must establish standalone finance and HR shared services center. Offshore India (€8M/year, 40% cost savings, timezone challenges), Nearshore Poland (€12M/year, 25% savings, EU compliance), Onshore expansion of existing UK center (€15M/year, 10% savings, low risk). 180 FTE scope.",
                "count": 4,
                "description": "Cost, Risk, Quality, Timeline perspectives"
            },
            "🍷 Organic Certification Decision": {
                "scenario": "80-hectare Châteauneuf-du-Pape estate considering organic certification. Conversion costs €400K over 3 years, potential 15% price premium, but risk of 30% yield reduction in transition years. Established customer base may not value organic label, but younger demographic increasingly demands it.",
                "count": 5,
                "description": "Risk, Opportunity, Resource, Timeline, Stakeholder perspectives"
            },
            "🍷 Winery Sale vs. Next-Gen Transition": {
                "scenario": "Founder (68) of iconic Willamette Valley Pinot Noir producer evaluating options: 1) Sell to private equity at $25M, 2) Transition to daughter (passionate but needs $8M financing), 3) Sell majority to strategic partner while retaining 30% and winemaker role. 45 employees, family legacy, loyal customer base at stake.",
                "count": 6,
                "description": "Strategic, Financial, Risk, Stakeholder, Timeline, Emotional lenses"
            },
            "🍷 Vineyard Expansion vs. Brand Acquisition": {
                "scenario": "Successful Paso Robles winery ($12M revenue) considering: 1) Purchase adjacent 40-acre vineyard for $6M (vertical integration), 2) Acquire complementary brand with 35-state distribution for $8M (faster scale), 3) Invest in tasting room expansion and DTC infrastructure. Each path has different risk/return profile.",
                "count": 4,
                "description": "Risk-First, Opportunity-First, Resource-First, Strategic-First"
            },
            "🍷 Climate-Driven Relocation Decision": {
                "scenario": "Napa Valley estate facing heat stress on Cabernet vines. Options: 1) Invest $2M in climate mitigation (shade, irrigation), 2) Transition to heat-tolerant varietals (lose AVA prestige), 3) Acquire Oregon/Washington vineyard as hedge ($10M+), 4) Exit premium production, pivot to consulting/licensing. 25 employees at stake.",
                "count": 5,
                "description": "Risk, Timeline, Resource, Stakeholder, Strategic perspectives"
            }
        }

        cols = st.columns(2)
        for idx, (example_name, example_data) in enumerate(examples.items()):
            with cols[idx % 2]:
                if st.button(
                    f"📋 {example_name}",
                    key=f"ds_example_{idx}",
                    use_container_width=True,
                    help=example_data['description']
                ):
                    st.session_state.ds_scenario = example_data['scenario']
                    st.session_state.ds_count = example_data['count']
                    st.rerun()

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

        try:
            # Generate storms sequentially
            for i, lens_name in enumerate(selected_lens_names):
                lens = LENSES[lens_name]

                # Show progress
                st.caption(f"⏳ Generating perspective {i+1}/{num_perspectives}: {lens['icon']} **{lens_name}**...")

                # Build interpretive system prompt
                system_prompt = """You are a strategic analyst providing multi-perspective decision analysis.

CRITICAL INTERPRETATION RULES:
1. DO NOT quote the scenario literally
2. INTERPRET the decision's implications through your assigned lens
3. Provide 150-200 words of specific, actionable analysis
4. Include concrete examples, data points, or metrics where relevant
5. Be decision-oriented for executive audiences

Your analysis should help decision-makers understand trade-offs and take action."""

                # Build the user message with interpretive instructions
                user_message = f"""{lens['prompt']}

DECISION SCENARIO (interpret the strategic implications):
{scenario}

YOUR TASK:
Interpret this decision through your lens and provide structured analysis:

Key Insight: (2-3 sentences capturing the core implication from your perspective)

Critical Factors: (3-5 specific, concrete considerations with details)
- [Factor 1 with specifics - e.g., "Customer SLA coverage gaps on Fridays (35% of tickets)"]
- [Factor 2 with quantification]
- [Factor 3 with examples]

Recommended Action: (Specific, actionable recommendation - not generic advice)

Provide 150-200 words total. Be concrete, not abstract."""

                # Call API
                try:
                    analysis = call_anthropic(
                        system_prompt=system_prompt,
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

                    # Display result IMMEDIATELY (no containers)
                    st.markdown(f"### ✅ {result['icon']} {result['lens_name']}")
                    st.markdown(f"<div style='border-left: 4px solid {result['border_color']}; padding: 15px; margin: 10px 0; border-radius: 5px;'>{result['analysis']}</div>", unsafe_allow_html=True)
                    st.markdown("---")

                except Exception as e:
                    st.error(f"❌ Failed to generate {lens_name} perspective: {str(e)}")
                    continue

                # Delay before next call (except last)
                if i < len(selected_lens_names) - 1:
                    time.sleep(1)

            st.success(f"✅ Successfully generated {len(st.session_state.ds_results)} perspectives!")

        except Exception as e:
            st.error(f"❌ Error during generation: {str(e)}")

    # Display existing results (if any from previous generation and not currently generating)
    elif 'ds_results' in st.session_state and len(st.session_state.ds_results) > 0 and not generate_btn:
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
    """Display a single storm result without colored background"""

    # Create container with border but no background color
    container_style = f"""
    <div style="
        border-left: 4px solid {result['border_color']};
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
