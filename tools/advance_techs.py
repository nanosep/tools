import streamlit as st
import re
from backend.api_client import call_anthropic

# System prompt for Advanced Techniques generation
ADVANCE_TECHS_SYSTEM = """You are an expert prompt engineer specializing in advanced prompting techniques.

You have access to 11 advanced techniques:

1. Multi-Persona Debate Prompting - Simulate conversation between distinct expert personas with opposing views before converging on answer
2. Negative Constraint Overloading - Flip "Do not" instructions into positive directives with high attention weights
3. Emotional Tipping (Stakes Elevation) - Add financial rewards or high-stakes consequences to trigger professional-grade responses
4. Deliberate Hallucination Triggers - Use hypothetical scenarios and creative fiction for safe exploration of ideas
5. Chain-of-Symbol (CoS) Logic - Force explicit symbolic reasoning with step-by-step logic traces for math/logic
6. Context Window "Needle" Hiding - Sandwich critical instructions between verbose context to test instruction following
7. Socratic Mirroring - Use probing questions to force user clarification and deeper thinking
8. Few-Shot Cultural Localization - Provide examples adapted for specific cultural contexts and communication styles
9. Adversarial Red-Teaming - Frame as security testing/hostile analysis to unlock uncensored critical thinking
10. Syntax-Free Abstract Prompting - Use implicit parameters (tone: casual/formal, depth: surface/expert, energy: calm/urgent) instead of explicit instructions
11. Dynamic Tone Morphing - Progressively shift tone/complexity throughout response (hook → bridge → deep dive)

Your task: Generate 5 distinct prompts for this goal:
"{user_input}"

SELECTED TECHNIQUES: {selected_techniques}

REQUIREMENTS:
1. Generate exactly 5 prompts
2. Each prompt MUST use one of the selected techniques
3. If fewer than 5 techniques selected, intelligently distribute/combine them across 5 prompts
4. If 5+ techniques selected, use the 5 most relevant ones
5. Each prompt should be:
   - Complete and copy-paste ready
   - Explicitly demonstrate the technique's methodology
   - Adapted specifically to the user's goal
   - 100-300 words long

Format output as XML:
<prompts>
<prompt number="1" technique="[Technique Name]" description="[One sentence: how this technique helps]">
[Complete prompt text applying this technique to: {user_input}]
</prompt>
<prompt number="2" technique="[Different Technique]" description="[Description]">
[Complete prompt text]
</prompt>
... continue for all 5 prompts
</prompts>

Ensure each prompt clearly demonstrates its technique's unique approach."""

# Technique definitions with metadata
TECHNIQUES = {
    "Multi-Persona Debate": {
        "full_name": "Multi-Persona Debate Prompting",
        "description": "Simulate conversation between expert personas with opposing views",
        "icon": "🎭",
        "best_for": "Complex decisions, strategy, multi-stakeholder problems"
    },
    "Negative Constraint": {
        "full_name": "Negative Constraint Overloading (Positive Sandwich)",
        "description": "Convert 'Do not' instructions into positive directives",
        "icon": "🔄",
        "best_for": "Clear specifications, avoiding unwanted patterns"
    },
    "Emotional Tipping": {
        "full_name": "Emotional Tipping (Stakes Elevation)",
        "description": "Add high-stakes consequences to boost thoroughness",
        "icon": "💰",
        "best_for": "Critical tasks, coding, legal drafting, precision work"
    },
    "Deliberate Hallucination": {
        "full_name": "Deliberate Hallucination Triggers",
        "description": "Use hypothetical scenarios for creative exploration",
        "icon": "🌀",
        "best_for": "Creative work, brainstorming, fictional scenarios"
    },
    "Chain-of-Symbol": {
        "full_name": "Chain-of-Symbol (CoS) Logic",
        "description": "Force explicit symbolic reasoning for logic problems",
        "icon": "🔣",
        "best_for": "Math, logic puzzles, algorithmic thinking"
    },
    "Needle Hiding": {
        "full_name": "Context Window 'Needle' Hiding",
        "description": "Sandwich critical instructions in verbose context",
        "icon": "🎯",
        "best_for": "Testing instruction following, long-context tasks"
    },
    "Socratic Mirroring": {
        "full_name": "Socratic Mirroring",
        "description": "Use probing questions to force clarification",
        "icon": "❓",
        "best_for": "Unclear requirements, exploratory analysis"
    },
    "Cultural Localization": {
        "full_name": "Few-Shot Cultural Localization",
        "description": "Provide culturally-adapted examples",
        "icon": "🌍",
        "best_for": "International communication, diverse audiences"
    },
    "Adversarial Red-Team": {
        "full_name": "Adversarial Red-Teaming",
        "description": "Frame as security testing for critical analysis",
        "icon": "🛡️",
        "best_for": "Finding vulnerabilities, stress testing, critical review"
    },
    "Syntax-Free Abstract": {
        "full_name": "Syntax-Free Abstract Prompting",
        "description": "Use implicit parameters (tone/depth/energy)",
        "icon": "🎨",
        "best_for": "Flexible styling, voice matching, subtle control"
    },
    "Dynamic Tone Morphing": {
        "full_name": "Dynamic Tone Morphing",
        "description": "Progressively shift complexity throughout response",
        "icon": "🎢",
        "best_for": "Educational content, mixed audiences, narrative arcs"
    }
}


def parse_prompts_output(response):
    """Extract prompts from XML response with fallback"""
    prompts = []
    pattern = r'<prompt number="(\d+)" technique="([^"]*)" description="([^"]*)">(.*?)</prompt>'
    matches = re.findall(pattern, response, re.DOTALL)

    for number, technique, description, prompt in matches:
        prompts.append({
            'number': int(number),
            'technique': technique.strip(),
            'description': description.strip(),
            'prompt': prompt.strip()
        })

    # Fallback if no XML found
    if not prompts:
        # Try to split by numbered patterns or double newlines
        chunks = []

        # Try pattern like "1." or "Prompt 1:"
        numbered_pattern = r'(?:^|\n)(?:Prompt\s*)?(\d+)[.:\s]+(.+?)(?=(?:^|\n)(?:Prompt\s*)?\d+[.:\s]|$)'
        numbered_matches = re.findall(numbered_pattern, response, re.DOTALL | re.MULTILINE)

        if numbered_matches:
            for num, content in numbered_matches[:5]:
                chunks.append(content.strip())
        else:
            # Split by double newlines
            chunks = [c.strip() for c in response.split('\n\n') if len(c.strip()) > 50]

        # Create prompts from chunks
        for i, chunk in enumerate(chunks[:5], 1):
            prompts.append({
                'number': i,
                'technique': 'Advanced Technique',
                'description': 'Generated specialized prompt',
                'prompt': chunk
            })

    # Ensure we have exactly 5 prompts
    if len(prompts) < 5:
        # Pad with simple prompts if needed
        for i in range(len(prompts) + 1, 6):
            prompts.append({
                'number': i,
                'technique': 'Standard Approach',
                'description': 'Alternative perspective',
                'prompt': f"Approach {i}: Consider this task from a different angle..."
            })

    return prompts[:5]  # Return exactly 5 prompts


def render_advance_techs():
    """Render the Advanced Techniques Generator tool"""

    st.title("🚀 Advanced Techniques Generator")
    st.write("Generate specialized prompts using 11 cutting-edge prompting techniques")

    # Info expander
    with st.expander("ℹ️ About Advanced Techniques"):
        st.markdown("""
        This tool uses **11 advanced prompt engineering techniques** from the expert playbook:

        - 🎭 **Multi-Persona Debate** - Expert personas with opposing views
        - 🔄 **Negative Constraint Overloading** - Positive directive framing
        - 💰 **Emotional Tipping** - High-stakes consequences for precision
        - 🌀 **Deliberate Hallucination** - Creative hypothetical exploration
        - 🔣 **Chain-of-Symbol Logic** - Explicit symbolic reasoning
        - 🎯 **Needle Hiding** - Critical instructions in verbose context
        - ❓ **Socratic Mirroring** - Probing questions for clarification
        - 🌍 **Cultural Localization** - Culturally-adapted examples
        - 🛡️ **Adversarial Red-Teaming** - Security testing framing
        - 🎨 **Syntax-Free Abstract** - Implicit parameter control
        - 🎢 **Dynamic Tone Morphing** - Progressive complexity shifts

        **How it works:** Select 3-5 techniques most relevant to your goal, and the system will generate **5 specialized prompts**.
        Each prompt demonstrates a different technique applied to your specific task.
        """)

    st.markdown("---")

    # Input
    user_input = st.text_area(
        "Enter Your Goal or Task",
        height=120,
        placeholder="Example: Design a database schema for a high-frequency trading application",
        key="at_input"
    )

    # Technique selector
    st.markdown("### Select Techniques (choose 3-5)")
    st.caption("Select the techniques most relevant to your task. The system will generate 5 prompts using your selections.")

    selected = []

    # Display as grid with checkboxes
    cols = st.columns(3)
    for idx, (key, tech) in enumerate(TECHNIQUES.items()):
        with cols[idx % 3]:
            if st.checkbox(
                f"{tech['icon']} {key}",
                key=f"at_tech_{key}",
                help=f"{tech['description']}\n\nBest for: {tech['best_for']}"
            ):
                selected.append(tech['full_name'])

    # Validation message
    if len(selected) < 3 and len(selected) > 0:
        st.warning("⚠️ Please select at least 3 techniques for best results")
    elif len(selected) > 7:
        st.info(f"ℹ️ {len(selected)} techniques selected. System will use the 5 most relevant.")
    elif len(selected) >= 3:
        st.success(f"✅ {len(selected)} techniques selected")

    # Generate button
    generate_btn = st.button(
        "🚀 Generate 5 Prompts",
        disabled=(len(user_input.strip()) < 10 or len(selected) < 3),
        type="primary",
        use_container_width=True
    )

    st.caption("💡 Generation takes 10-15 seconds")

    # Generation logic
    if generate_btn and user_input.strip() and len(selected) >= 3:
        with st.spinner("Generating advanced prompts..."):
            try:
                # Build system prompt
                system_prompt = ADVANCE_TECHS_SYSTEM.format(
                    user_input=user_input,
                    selected_techniques=", ".join(selected)
                )

                # Build user message
                user_message = f"""Goal: {user_input}

Selected Techniques: {", ".join(selected)}

Generate exactly 5 prompts using the selected techniques. Each prompt should clearly demonstrate its technique's methodology applied to this specific goal."""

                # Call API
                response = call_anthropic(
                    system_prompt=system_prompt,
                    user_message=user_message,
                    max_tokens=2500
                )

                # Parse response
                st.session_state.at_results = parse_prompts_output(response)
                st.success("✅ 5 prompts generated successfully!")

            except Exception as e:
                st.error(f"Error generating prompts: {str(e)}")

    # Display results
    if 'at_results' in st.session_state and st.session_state.at_results:
        st.markdown("---")
        st.subheader("📋 Generated Prompts")
        st.info("**How to use:** Each prompt applies a different advanced technique to your goal. Copy and use any prompt that fits your needs.")

        for prompt_data in st.session_state.at_results:
            # Find matching icon
            icon = "⚡"
            for key, tech in TECHNIQUES.items():
                if tech['full_name'] in prompt_data['technique'] or key in prompt_data['technique']:
                    icon = tech['icon']
                    break

            with st.container():
                st.markdown(f"### {icon} Prompt {prompt_data['number']}: {prompt_data['technique']}")
                st.caption(prompt_data['description'])
                st.code(prompt_data['prompt'], language=None)
                st.markdown("")

    else:
        # Empty state
        if not generate_btn or not user_input.strip():
            st.markdown("---")
            st.info("""
            ### 🌟 Quick Start

            1. **Enter your goal** - Describe the task you want to create prompts for
            2. **Select 3-5 techniques** - Choose from the 11 advanced techniques based on your needs
            3. **Generate prompts** - Get 5 specialized prompts, each using a different technique
            4. **Copy and use** - Pick the prompt that best fits your requirements

            ### 💡 Example Combinations

            **For Code Optimization:**
            - Chain-of-Symbol Logic + Emotional Tipping + Adversarial Red-Team

            **For Creative Writing:**
            - Dynamic Tone Morphing + Cultural Localization + Deliberate Hallucination

            **For Complex Decisions:**
            - Multi-Persona Debate + Socratic Mirroring + Negative Constraint

            **For Precision Work:**
            - Emotional Tipping + Chain-of-Symbol + Adversarial Red-Team
            """)

            # Show technique reference table
            st.markdown("### 📚 Technique Reference")

            for key, tech in TECHNIQUES.items():
                with st.expander(f"{tech['icon']} {key}"):
                    st.markdown(f"**{tech['full_name']}**")
                    st.markdown(f"*{tech['description']}*")
                    st.markdown(f"**Best for:** {tech['best_for']}")
