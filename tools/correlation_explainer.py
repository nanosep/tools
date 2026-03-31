import streamlit as st

# Correlation types data - 8 complete types
CORRELATION_TYPES = {
    "Direct Causation": {
        "subtitle": "A actually causes B",
        "icon": "→",
        "color": "#22c55e",
        "probability": 15,
        "probability_label": "Uncommon",
        "danger_level": "low",
        "examples": [
            {"a": "Smoking", "b": "Lung Cancer", "explanation": "Cigarette smoke contains carcinogens that directly damage lung tissue and DNA, leading to cancer."},
            {"a": "Aspirin", "b": "Reduced Blood Clots", "explanation": "Aspirin inhibits cyclooxygenase enzymes, reducing thromboxane production and platelet aggregation."},
            {"a": "Seatbelt Use", "b": "Crash Survival", "explanation": "Seatbelts physically restrain occupants, distributing crash forces across stronger body parts."}
        ],
        "description": "Variable A directly causes changes in Variable B through a clear, identifiable mechanism. This is what most people assume when they see correlation, but it's actually the least common explanation.",
        "key_question": "Is there a plausible mechanism by which A could cause B?",
        "how_to_test": [
            "Randomized Controlled Trial (Gold standard)",
            "Dose-Response Relationship (More A = proportionally more B?)",
            "Temporal Sequence (Does A consistently precede B?)",
            "Mechanism Identification (Can you explain HOW A causes B?)"
        ],
        "common_mistakes": [
            "Assuming correlation implies causation",
            "Ignoring alternative explanations",
            "Confusing temporal sequence with causation"
        ],
        "historical_example": {
            "title": "Semmelweis & Handwashing (1847)",
            "story": "Ignaz Semmelweis noticed doctors who performed autopsies had higher patient death rates. He hypothesized 'cadaverous particles' caused infections. Handwashing reduced maternal mortality from 18% to 2%. Despite clear evidence, doctors rejected his theory for decades because the mechanism (germs) wasn't yet understood."
        }
    },
    "Reverse Causation": {
        "subtitle": "B actually causes A",
        "icon": "←",
        "color": "#f59e0b",
        "probability": 20,
        "probability_label": "Common",
        "danger_level": "high",
        "examples": [
            {"a": "Hospital Visits", "b": "Death Rate", "explanation": "People don't die because they visit hospitals—they visit hospitals because they're already sick."},
            {"a": "Antidepressant Use", "b": "Suicide Risk", "explanation": "Severely depressed people (higher suicide risk) are more likely to be prescribed antidepressants."},
            {"a": "Low Cholesterol", "b": "Cancer", "explanation": "Cancer itself can lower cholesterol levels, not the reverse."}
        ],
        "description": "We naturally assume A causes B, but the causal arrow actually points backward. B causes A. This is especially common in health research where illness drives behavior.",
        "key_question": "Could B be causing A instead of the other way around?",
        "how_to_test": [
            "Temporal Analysis (Which variable actually changes first?)",
            "Prospective Studies (Measure A before B can occur)",
            "Mechanism Plausibility (Is reverse causation mechanistically possible?)"
        ],
        "common_mistakes": [
            "Assuming the 'obvious' direction is correct",
            "Ignoring that sick people behave differently",
            "Not considering bidirectional relationships"
        ],
        "historical_example": {
            "title": "Hormone Replacement Therapy (2002)",
            "story": "Observational studies showed HRT reduced heart disease in women. Doctors widely prescribed it. Then randomized trials showed HRT actually INCREASED heart disease risk. The original correlation existed because healthier, wealthier women were more likely to take HRT—and more likely to have good heart health anyway."
        }
    },
    "Confounding Variable": {
        "subtitle": "C causes both A and B",
        "icon": "↔",
        "color": "#ef4444",
        "probability": 35,
        "probability_label": "Very Common",
        "danger_level": "high",
        "examples": [
            {"a": "Ice Cream Sales", "b": "Drowning Deaths", "explanation": "Summer weather (confounder) causes both. Hot days → more ice cream AND more swimming → more drownings."},
            {"a": "Shoe Size", "b": "Reading Ability", "explanation": "Age is the confounder. Older children have bigger feet AND read better. Shoes don't teach reading."},
            {"a": "Yellow Fingers", "b": "Lung Cancer", "explanation": "Smoking causes both yellow fingers (tar stains) and lung cancer. Cleaning your fingers won't prevent cancer."}
        ],
        "description": "A hidden third variable causes both A and B, creating a spurious correlation between them. This is the MOST common explanation for correlations that aren't causal.",
        "key_question": "What third variable could be driving both A and B?",
        "how_to_test": [
            "Statistical Control (Control for suspected confounders)",
            "Stratification (Analyze relationship within subgroups)",
            "Randomization (Random assignment eliminates confounding)",
            "DAG Analysis (Draw causal diagrams)"
        ],
        "common_mistakes": [
            "Failing to consider unmeasured confounders",
            "Assuming statistical control is sufficient",
            "Not drawing causal diagrams before analysis"
        ],
        "historical_example": {
            "title": "Coffee & Lung Cancer",
            "story": "Early studies found coffee drinkers had higher lung cancer rates. Panic ensued. But researchers failed to control for smoking—and coffee drinkers were much more likely to smoke. Once smoking was controlled for, the coffee-cancer link disappeared. Smoking was the confounder."
        }
    },
    "Mediated Causation": {
        "subtitle": "A → M → B (chain reaction)",
        "icon": "⇢",
        "color": "#8b5cf6",
        "probability": 25,
        "probability_label": "Common",
        "danger_level": "low",
        "examples": [
            {"a": "Education", "b": "Income", "explanation": "Education → Job Opportunities → Income. Education doesn't directly pay you; it creates opportunities."},
            {"a": "Exercise", "b": "Longevity", "explanation": "Exercise → Cardiovascular Health → Longevity. The mechanism is improved heart function."},
            {"a": "Sleep Deprivation", "b": "Weight Gain", "explanation": "Sleep Deprivation → Hormonal Changes (ghrelin/leptin) → Increased Appetite → Weight Gain."}
        ],
        "description": "A causes B, but only through one or more intermediate variables (mediators). Understanding the chain reveals the mechanism and identifies intervention points.",
        "key_question": "What's the mechanism connecting A to B?",
        "how_to_test": [
            "Mediation Analysis (Statistical test for intermediate variables)",
            "Path Analysis (Model the causal chain)",
            "Intervention Studies (Block the mediator, does A→B relationship disappear?)",
            "Mechanistic Studies (Measure intermediate steps)"
        ],
        "common_mistakes": [
            "Assuming A directly causes B when mechanism is complex",
            "Failing to identify intervention points",
            "Ignoring multiple parallel pathways"
        ],
        "historical_example": {
            "title": "Smoking → DNA Damage → Cancer",
            "story": "Early smoking research showed correlation with cancer, but skeptics demanded mechanism. Scientists discovered smoking → tar/carcinogens → DNA mutations → uncontrolled cell growth → cancer. Understanding the mediated pathway enabled targeted interventions and silenced tobacco industry denialism."
        }
    },
    "Bidirectional Causation": {
        "subtitle": "A ⇄ B (feedback loop)",
        "icon": "⇄",
        "color": "#06b6d4",
        "probability": 15,
        "probability_label": "Uncommon",
        "danger_level": "medium",
        "examples": [
            {"a": "Exercise", "b": "Mental Health", "explanation": "Exercise improves mental health AND good mental health makes you more likely to exercise. Virtuous cycle."},
            {"a": "Economic Growth", "b": "Education Investment", "explanation": "Growth funds education AND education drives growth. Positive feedback loop."},
            {"a": "Depression", "b": "Social Isolation", "explanation": "Depression causes withdrawal AND isolation worsens depression. Vicious cycle."}
        ],
        "description": "A causes B AND B causes A simultaneously, creating a feedback loop. Can be virtuous (reinforcing positive outcomes) or vicious (reinforcing negative outcomes).",
        "key_question": "Do they reinforce each other?",
        "how_to_test": [
            "Longitudinal Analysis (Track changes over time)",
            "Cross-Lagged Panel Models (Which change predicts future change?)",
            "Intervention Studies (Break one part of loop, does system stabilize?)",
            "Dynamic Systems Modeling"
        ],
        "common_mistakes": [
            "Trying to identify 'the' cause when both matter",
            "Ignoring feedback amplification over time",
            "Missing opportunities to break negative cycles"
        ],
        "historical_example": {
            "title": "Poverty ⇄ Poor Health",
            "story": "Public health research revealed poverty causes poor health (stress, malnutrition, lack of care) AND poor health causes poverty (medical debt, lost work, reduced productivity). Breaking the cycle requires intervening on BOTH sides—economic support AND healthcare access."
        }
    },
    "Spurious Correlation": {
        "subtitle": "Pure chance / coincidence",
        "icon": "?",
        "color": "#eab308",
        "probability": 10,
        "probability_label": "Rare",
        "danger_level": "medium",
        "examples": [
            {"a": "Nicolas Cage Films", "b": "Pool Drownings", "explanation": "r=0.67 correlation! Pure coincidence. No plausible mechanism."},
            {"a": "US Cheese Consumption", "b": "Deaths by Bedsheet Tangling", "explanation": "Statistically significant (p<0.05) but meaningless. Random noise."},
            {"a": "Maine Divorce Rate", "b": "Margarine Consumption", "explanation": "r=0.99! Tyler Vigen's spurious correlations website classic."}
        ],
        "description": "Two variables correlate purely by chance, especially with small samples or data dredging. With enough variables, some WILL correlate randomly.",
        "key_question": "Could this be random?",
        "how_to_test": [
            "Replication Studies (Does correlation hold in new data?)",
            "Theoretical Plausibility (Is there ANY reason these should relate?)",
            "Correction for Multiple Comparisons (Bonferroni, FDR)",
            "Pre-registration (Did you predict this correlation in advance?)"
        ],
        "common_mistakes": [
            "Data dredging (testing hundreds of correlations, reporting the 'significant' ones)",
            "Publication bias (only publishing 'interesting' correlations)",
            "Ignoring prior probability (extraordinary claims need extraordinary evidence)"
        ],
        "historical_example": {
            "title": "The Replication Crisis (2015)",
            "story": "Psychology researchers began systematically replicating famous studies. Only ~40% replicated. Many 'discoveries' were spurious correlations from small samples, p-hacking, and file-drawer effect (unpublished negative results). The crisis revolutionized scientific publishing standards."
        }
    },
    "Selection Bias": {
        "subtitle": "Biased sample creates illusion",
        "icon": "⊂",
        "color": "#ec4899",
        "probability": 25,
        "probability_label": "Common",
        "danger_level": "high",
        "examples": [
            {"a": "WWII Bomber Armor", "b": "Damage Patterns", "explanation": "Planes showed damage on wings/tail. Navy wanted to armor these areas. Abraham Wald realized: planes hit in engines DIDN'T RETURN. Survivorship bias."},
            {"a": "Successful Entrepreneurs", "b": "Risk-Taking", "explanation": "We interview successful risk-takers, not failed ones. Survival bias makes risk seem safer than it is."},
            {"a": "Hospital Quality", "b": "Death Rate", "explanation": "Best hospitals treat sickest patients, showing higher death rates. Selection bias makes them look worse."}
        ],
        "description": "The sample you observe is not representative of the full population. You only see survivors/winners/successes, creating false correlations.",
        "key_question": "Who's missing from this data?",
        "how_to_test": [
            "Identify Selection Mechanism (How did observations enter the sample?)",
            "Compare to Full Population (Census data, administrative records)",
            "Sensitivity Analysis (How much unmeasured selection needed to explain correlation?)",
            "Inverse Probability Weighting (Reweight sample to match population)"
        ],
        "common_mistakes": [
            "Survivorship bias (only studying successes)",
            "Self-selection bias (volunteers differ from non-volunteers)",
            "Attrition bias (dropouts differ from completers)"
        ],
        "historical_example": {
            "title": "Abraham Wald's Armor Analysis",
            "story": "WWII: Navy showed Wald bullet holes in returned bombers. Damage concentrated on wings and tail. They planned to add armor there. Wald said: 'Armor the engines.' Why? Planes hit in engines never came back. He was looking at SURVIVORS. This insight saved thousands of lives."
        }
    },
    "Ecological Fallacy": {
        "subtitle": "Group patterns ≠ Individual patterns",
        "icon": "≠",
        "color": "#14b8a6",
        "probability": 20,
        "probability_label": "Common",
        "danger_level": "medium",
        "examples": [
            {"a": "Country Chocolate Consumption", "b": "Nobel Prizes", "explanation": "Countries with higher chocolate consumption have more Nobel laureates. But individual chocolate eaters don't win Nobel prizes. Wealth confounds at country level."},
            {"a": "State Education Spending", "b": "Test Scores", "explanation": "States spending more may have LOWER scores because they have more disadvantaged students needing resources. Aggregate masks individual benefit."},
            {"a": "Neighborhood Income", "b": "Crime", "explanation": "Poor neighborhoods have more crime, but most poor individuals don't commit crimes. Group-level correlation ≠ individual risk."}
        ],
        "description": "Correlations observed at group level (countries, states, neighborhoods) don't necessarily apply to individuals. Aggregation can reverse or create correlations (Simpson's Paradox).",
        "key_question": "Am I assuming group data applies to individuals?",
        "how_to_test": [
            "Multi-Level Modeling (Separate group and individual effects)",
            "Individual-Level Data (Get person-level data if possible)",
            "Simpson's Paradox Check (Does relationship reverse within groups?)",
            "Contextual Effects Analysis"
        ],
        "common_mistakes": [
            "Inferring individual behavior from aggregate data",
            "Ignoring within-group variation",
            "Policy decisions based on ecological correlations"
        ],
        "historical_example": {
            "title": "UC Berkeley Admissions (Simpson's Paradox)",
            "story": "Berkeley sued for gender discrimination (1973). Overall admission: 44% men, 35% women. Discrimination? No. When examined by department, most departments slightly favored women. Women applied to more competitive departments. Aggregate data showed bias, but individual departments didn't discriminate. Simpson's Paradox."
        }
    }
}


def create_diagram(correlation_type):
    """Create text-based visual diagram showing relationship structure"""
    diagrams = {
        "Direct Causation": """
        A ────→ B
        (A causes B directly)
        """,
        "Reverse Causation": """
        A ←──── B
        (B actually causes A)
        """,
        "Confounding Variable": """
            C
           ╱ ╲
          ↓   ↓
        A     B
        (C causes both A and B)
        """,
        "Mediated Causation": """
        A ────→ M ────→ B
        (A causes B through M)
        """,
        "Bidirectional Causation": """
        A ⇄ B
        (Feedback loop)
        """,
        "Spurious Correlation": """
        A ? ? ? B
        (No real connection)
        """,
        "Selection Bias": """
        Sample(A, B) ≠ Population(A, B)
        (Biased sample)
        """,
        "Ecological Fallacy": """
        Group(A→B) ≠ Individual(A→B)
        (Aggregate ≠ Individual)
        """
    }
    return diagrams.get(correlation_type, "")


def render_correlation_explainer():
    """Render the Correlation Explainer educational tool"""

    st.title("🔬 Correlation ≠ Causation Explainer")
    st.write("Interactive guide to the 8 types of correlations and why most are NOT causation")

    # Landing page or type selection
    if 'ce_selected_type' not in st.session_state:
        # Landing page
        st.markdown("""
        ## Why "Correlation ≠ Causation"

        When two variables move together (correlate), most people assume one causes the other.
        **This is almost always wrong.** There are 8 different explanations for correlation,
        and direct causation is the LEAST common.

        ### The Problem

        - Media headlines: "Coffee linked to cancer!" (Later: "Coffee prevents cancer!")
        - Business decisions based on spurious correlations
        - Policy failures from misunderstanding causation
        - Pseudoscience exploiting correlation=causation confusion

        ### The 8 Types (by frequency)

        1. **Confounding Variable (35%)** - Hidden third variable causes both
        2. **Mediated Causation (25%)** - A causes B through intermediate steps
        3. **Selection Bias (25%)** - Biased sample creates illusion
        4. **Reverse Causation (20%)** - B actually causes A
        5. **Ecological Fallacy (20%)** - Group patterns ≠ individual patterns
        6. **Direct Causation (15%)** - A actually causes B ✓
        7. **Bidirectional (15%)** - Feedback loop
        8. **Spurious/Chance (10%)** - Pure coincidence

        **Only 15% of correlations are direct causation!**

        ---

        ### 🎯 Start Here: Common Misconceptions

        These famous examples demonstrate how easy it is to mistake correlation for causation:
        """)

        # Quick link examples
        quick_examples = {
            "Ice Cream & Drowning": {
                "type": "Confounding Variable",
                "explanation": "Both increase in summer (temperature is the confounding variable)",
                "icon": "🍦"
            },
            "Hospital Visits & Deaths": {
                "type": "Reverse Causation",
                "explanation": "People don't die because they visit hospitals—they visit because they're sick",
                "icon": "🏥"
            },
            "HRT & Heart Disease": {
                "type": "Selection Bias",
                "explanation": "Wealthy women (better health) more likely to afford HRT, creating biased sample",
                "icon": "💊"
            }
        }

        quick_cols = st.columns(3)
        for idx, (example_name, example_data) in enumerate(quick_examples.items()):
            with quick_cols[idx % 3]:
                if st.button(
                    f"{example_data['icon']} {example_name}",
                    key=f"ce_quick_{idx}",
                    use_container_width=True,
                    help=example_data['explanation']
                ):
                    st.session_state.ce_selected_type = example_data['type']
                    st.rerun()

        st.markdown("---")
        st.markdown("### 📚 Or Browse All 8 Types:")
        st.caption("Click any type below to see detailed explanation, examples, and testing methods")

        # Type selector grid

        # Sort by probability (most common first)
        sorted_types = sorted(
            CORRELATION_TYPES.items(),
            key=lambda x: x[1]['probability'],
            reverse=True
        )

        cols = st.columns(4)
        for idx, (type_name, type_data) in enumerate(sorted_types):
            with cols[idx % 4]:
                # Create button with styled label
                button_label = f"{type_data['icon']} **{type_name}**\n{type_data['probability']}% - {type_data['probability_label']}"

                if st.button(
                    button_label,
                    key=f"ce_type_{type_name}",
                    use_container_width=True,
                    help=type_data['subtitle']
                ):
                    st.session_state.ce_selected_type = type_name
                    st.rerun()

        # Footer tips
        st.markdown("---")
        st.info("""
        **💡 Pro Tip**: Before concluding causation from a correlation, systematically work through each of these 8 alternatives.
        Ask: "Could this be confounding? Reverse causation? Selection bias?" Most correlations in media are NOT direct causation.
        """)

    else:
        # Type detail view
        selected_type = st.session_state.ce_selected_type
        type_data = CORRELATION_TYPES[selected_type]

        # Back button
        if st.button("← Back to All Types"):
            del st.session_state.ce_selected_type
            st.rerun()

        # Header with color-coded background
        st.markdown(f"""
        <div style="background-color: {type_data['color']}20; padding: 20px; border-radius: 10px; border-left: 5px solid {type_data['color']};">
            <h2>{type_data['icon']} {selected_type}</h2>
            <p style="font-size: 1.2em;"><strong>{type_data['subtitle']}</strong></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        # Visual diagram
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### 📊 Visual Relationship")
            st.code(create_diagram(selected_type), language=None)

        with col2:
            # Probability meter
            st.markdown("### 📈 Frequency")
            st.progress(type_data['probability'] / 100)
            st.caption(f"**{type_data['probability']}%** of correlations\n({type_data['probability_label']})")

            # Danger level
            st.markdown("### ⚠️ Danger Level")
            danger_colors = {"low": "🟢 LOW", "medium": "🟡 MEDIUM", "high": "🔴 HIGH"}
            danger_label = danger_colors.get(type_data['danger_level'], "⚪ UNKNOWN")
            st.markdown(f"**{danger_label}**")
            st.caption("Risk of mistaking for causation")

        st.markdown("---")

        # Description
        st.markdown("### What Is This?")
        st.info(type_data['description'])

        # Key question
        st.markdown("### 🎯 The Critical Question")
        st.success(f"**{type_data['key_question']}**")

        st.markdown("---")

        # Real examples
        st.markdown("### 🌍 Real-World Examples")
        for i, example in enumerate(type_data['examples'], 1):
            with st.expander(f"Example {i}: {example['a']} ↔ {example['b']}", expanded=(i == 1)):
                st.markdown(f"**Variables**: {example['a']} & {example['b']}")
                st.markdown(f"**Explanation**: {example['explanation']}")

        st.markdown("---")

        # How to test
        st.markdown("### 🔬 How to Test for This Type")
        for method in type_data['how_to_test']:
            st.markdown(f"✓ {method}")

        # Common mistakes
        st.markdown("### ⚠️ Common Mistakes")
        for mistake in type_data['common_mistakes']:
            st.warning(f"❌ {mistake}")

        st.markdown("---")

        # Historical example
        st.markdown("### 📚 Historical Case Study")
        with st.expander(f"📖 {type_data['historical_example']['title']}", expanded=True):
            st.markdown(type_data['historical_example']['story'])

        # Comparison with other types
        st.markdown("---")
        st.markdown("### 📊 All Types Comparison")

        # Create comparison data
        comparison_data = {
            name: data['probability']
            for name, data in sorted(
                CORRELATION_TYPES.items(),
                key=lambda x: x[1]['probability'],
                reverse=True
            )
        }

        # Display as bar chart using st.bar_chart
        import pandas as pd
        df = pd.DataFrame({
            'Probability %': list(comparison_data.values())
        }, index=list(comparison_data.keys()))

        st.bar_chart(df)

        # Highlight current type
        st.caption(f"Currently viewing: **{selected_type}** ({type_data['probability']}%)")

        # Footer navigation
        st.markdown("---")
        st.info("""
        **Next Steps**: Explore other types using the "Back to All Types" button above, or apply this framework
        to correlations you see in news, research, or business decisions.
        """)
