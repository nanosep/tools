import streamlit as st
import re
from backend.api_client import call_anthropic

# System prompt for Creative Thinking generation
CREATIVE_THINKING_SYSTEM = """You are an expert in creative thinking methodologies and facilitation.

You have access to 24 creative thinking methods across 6 categories:

DIVERGENT THINKING (Generate ideas):
- Brainstorming: Rapid idea generation without judgment
- SCAMPER: Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, Reverse
- Mind Mapping: Visual branching of connected concepts
- Random Word Association: Force connections between unrelated concepts

CONVERGENT THINKING (Focus and refine):
- Six Thinking Hats: Evaluate from White (facts), Red (emotions), Black (risks), Yellow (benefits), Green (creative), Blue (process)
- Impact-Effort Matrix: Plot by impact vs effort to prioritize
- Pros-Cons-Fixes: List positives, negatives, then mitigation solutions
- Devil's Advocate: Systematically challenge assumptions

LATERAL THINKING (Unexpected angles):
- Provocation Technique: Start with deliberately impossible statements
- Reverse Thinking: Solve for opposite of goal, then reverse
- Analogies from Other Domains: Apply patterns from different fields
- Constraint Removal: Imagine constraints don't exist, work backward

COLLABORATIVE METHODS (Collective intelligence):
- Brainwriting: Silent parallel idea generation
- Round Robin: Structured turn-taking for equal input
- Nominal Group Technique: Individual work + anonymous voting
- Role Storming: Brainstorm from another persona's perspective

REFRAMING TECHNIQUES (Change perspective):
- Five Whys: Dig deeper by asking why repeatedly
- Perspective Shifting: View through different stakeholder lenses
- Time Travel: Project to past/future for insight
- Question Assumptions: Challenge fundamental beliefs

STRUCTURED IDEATION (Systematic creativity):
- TRIZ Principles: Use 40 inventive principles
- Morphological Analysis: Break into dimensions, combine variations
- Forced Connections: Combine random elements
- Attribute Listing: List attributes, modify systematically

Your task: Generate prompts for this challenge:
"{user_input}"

SELECTED METHODS: {selected_methods}
TARGET DEPARTMENT: {department}

REQUIREMENTS:
1. Generate one prompt for EACH selected method
2. Each prompt must:
   - Apply the method's specific technique
   - Be adapted for the {department} department's context
   - Be 100-200 words
   - Be immediately actionable and copy-paste ready
   - Include specific instructions on HOW to use the method
3. Use department-relevant terminology and examples
4. Make prompts practical, not theoretical

Format output as XML:
<prompts>
<prompt method="[Method Name]" category="[Category Name]">
[Complete prompt applying this method to the challenge, specifically adapted for {department}]
</prompt>
<prompt method="[Different Method]" category="[Category Name]">
[Complete prompt]
</prompt>
... continue for all selected methods
</prompts>

Ensure each prompt clearly demonstrates the method and is department-specific."""

# Categories and methods with metadata
CATEGORIES = {
    "Divergent Thinking": {
        "description": "Generate multiple ideas and possibilities",
        "icon": "💡",
        "color": "#f59e0b",
        "methods": [
            {"name": "Brainstorming", "when": "Need volume of ideas quickly", "tip": "Quantity breeds quality - aim for 50+ ideas"},
            {"name": "SCAMPER", "when": "Improving existing solutions", "tip": "Work through each letter methodically"},
            {"name": "Mind Mapping", "when": "Exploring concept relationships", "tip": "Let it grow organically, don't organize initially"},
            {"name": "Random Word Association", "when": "Breaking mental patterns", "tip": "More absurd connections = more creative insights"}
        ]
    },
    "Convergent Thinking": {
        "description": "Focus and refine ideas to find solutions",
        "icon": "🎯",
        "color": "#3b82f6",
        "methods": [
            {"name": "Six Thinking Hats", "when": "Need thorough evaluation", "tip": "Separate the hats - wear each fully before switching"},
            {"name": "Impact-Effort Matrix", "when": "Prioritizing multiple options", "tip": "Be honest about effort - overconfidence kills execution"},
            {"name": "Pros-Cons-Fixes", "when": "Balancing trade-offs", "tip": "The fixes column often reveals the path forward"},
            {"name": "Devil's Advocate", "when": "Testing idea robustness", "tip": "Get someone else to play devil's advocate"}
        ]
    },
    "Lateral Thinking": {
        "description": "Approach problems from unexpected angles",
        "icon": "🔀",
        "color": "#a855f7",
        "methods": [
            {"name": "Provocation Technique", "when": "Stuck in conventional thinking", "tip": "Example: What if customers paid us to NOT use our product?"},
            {"name": "Reverse Thinking", "when": "No progress on direct solutions", "tip": "Often reveals hidden assumptions blocking solution"},
            {"name": "Analogies from Other Domains", "when": "Need fresh mental models", "tip": "Biology and military strategy are goldmines"},
            {"name": "Constraint Removal", "when": "Feeling limited by resources", "tip": "The impossible solution reveals creative compromise"}
        ]
    },
    "Collaborative Methods": {
        "description": "Harness collective intelligence",
        "icon": "👥",
        "color": "#10b981",
        "methods": [
            {"name": "Brainwriting", "when": "Avoiding groupthink", "tip": "Introverts often contribute more with this"},
            {"name": "Round Robin", "when": "Ensuring equal participation", "tip": "Don't allow skipping - pass counts as turn"},
            {"name": "Nominal Group Technique", "when": "Need creativity and consensus", "tip": "Anonymity in voting reveals true preferences"},
            {"name": "Role Storming", "when": "Breaking team mental patterns", "tip": "Choose personas who see problem differently"}
        ]
    },
    "Reframing Techniques": {
        "description": "Change perspective to unlock insights",
        "icon": "🧠",
        "color": "#ef4444",
        "methods": [
            {"name": "Five Whys", "when": "Surface problem masks root", "tip": "Done when answer becomes organizational/human nature"},
            {"name": "Perspective Shifting", "when": "Stuck in your viewpoint", "tip": "Physically move to different locations when shifting"},
            {"name": "Time Travel", "when": "Need hindsight or foresight", "tip": "Pre-mortem: imagine failed, what went wrong?"},
            {"name": "Question Assumptions", "when": "Challenging status quo", "tip": "Ask: What if the opposite were true?"}
        ]
    },
    "Structured Ideation": {
        "description": "Systematic approaches to creativity",
        "icon": "⚡",
        "color": "#6366f1",
        "methods": [
            {"name": "TRIZ Principles", "when": "Technical problem-solving", "tip": "40 principles cover most engineering problems"},
            {"name": "Morphological Analysis", "when": "Complex multi-variable problems", "tip": "Systematically explore all combinations"},
            {"name": "Forced Connections", "when": "Creating novel combinations", "tip": "Randomly combine unrelated elements"},
            {"name": "Attribute Listing", "when": "Improving products/processes", "tip": "Modify one attribute at a time"}
        ]
    }
}

# Department options
DEPARTMENTS = [
    "Sales", "Marketing", "Finance", "Operations", "Product", "HR",
    "Strategy", "Customer Success", "IT", "Legal", "R&D", "Supply Chain",
    "Business Development", "Communications", "Data Analytics", "Procurement",
    "Quality Assurance", "Training"
]


def parse_prompts_output(response):
    """Extract prompts from XML response with fallback"""
    prompts = []
    pattern = r'<prompt method="([^"]*)" category="([^"]*)">(.*?)</prompt>'
    matches = re.findall(pattern, response, re.DOTALL)

    for method, category, prompt in matches:
        prompts.append({
            'method': method.strip(),
            'category': category.strip(),
            'prompt': prompt.strip()
        })

    # Fallback if no XML found
    if not prompts:
        # Try splitting by numbered patterns or double newlines
        chunks = [c.strip() for c in response.split('\n\n') if len(c.strip()) > 50]
        for i, chunk in enumerate(chunks, 1):
            prompts.append({
                'method': f'Method {i}',
                'category': 'Creative Thinking',
                'prompt': chunk
            })

    return prompts


def render_creative_thinking():
    """Render the Creative Thinking Prompt Generator tool"""

    st.title("🎨 Creative Thinking Prompt Generator")
    st.write("Generate facilitation prompts using 24 proven creative thinking methods")

    # Info expander
    with st.expander("ℹ️ About Creative Thinking Methods"):
        st.markdown("""
        This tool provides **24 creative thinking methods** across **6 categories**:

        - 💡 **Divergent Thinking** - Generate multiple ideas (Brainstorming, SCAMPER, Mind Mapping, Random Association)
        - 🎯 **Convergent Thinking** - Focus and refine (Six Hats, Impact-Effort Matrix, Pros-Cons-Fixes, Devil's Advocate)
        - 🔀 **Lateral Thinking** - Unexpected angles (Provocation, Reverse Thinking, Analogies, Constraint Removal)
        - 👥 **Collaborative Methods** - Collective intelligence (Brainwriting, Round Robin, Nominal Group, Role Storming)
        - 🧠 **Reframing Techniques** - Change perspective (Five Whys, Perspective Shifting, Time Travel, Question Assumptions)
        - ⚡ **Structured Ideation** - Systematic creativity (TRIZ, Morphological Analysis, Forced Connections, Attribute Listing)

        **How it works:** Select 1-5 methods most relevant to your challenge and department. The system generates
        department-specific prompts for each method you can use in workshops or brainstorming sessions.
        """)

    st.markdown("---")

    # Input
    user_input = st.text_area(
        "Enter Your Challenge or Goal",
        height=100,
        placeholder="Example: How can we reduce customer churn in our SaaS product?",
        key="ct_input"
    )

    # Department selector
    st.markdown("### Select Department")
    department = st.selectbox(
        "Which department is this for?",
        options=DEPARTMENTS,
        key="ct_department",
        help="Prompts will be adapted with terminology and examples specific to this department"
    )

    # Method selector by category
    st.markdown("### Select Creative Thinking Methods (choose 1-5)")
    st.caption("Browse methods by category and select the ones most relevant to your challenge")

    selected_methods = []

    for cat_name, cat_data in CATEGORIES.items():
        with st.expander(f"{cat_data['icon']} {cat_name} - {cat_data['description']}", expanded=False):
            for method in cat_data['methods']:
                col1, col2 = st.columns([3, 1])
                with col1:
                    is_selected = st.checkbox(
                        f"**{method['name']}**",
                        key=f"ct_method_{method['name']}",
                        help=f"When to use: {method['when']}\n\nPro tip: {method['tip']}"
                    )
                    if is_selected:
                        selected_methods.append({
                            'name': method['name'],
                            'category': cat_name
                        })
                with col2:
                    st.caption(f"💡 {method['when'][:30]}...")

    # Selection validation
    if len(selected_methods) == 0:
        st.warning("⚠️ Please select at least 1 method")
    elif len(selected_methods) > 5:
        st.warning(f"⚠️ You've selected {len(selected_methods)} methods. Consider focusing on 1-5 for best results.")
    else:
        st.success(f"✅ {len(selected_methods)} method(s) selected")

    # Generate button
    generate_btn = st.button(
        f"🚀 Generate {len(selected_methods) if selected_methods else 0} Prompt(s)",
        disabled=(len(user_input.strip()) < 10 or len(selected_methods) == 0),
        type="primary",
        use_container_width=True
    )

    st.caption("💡 Generation takes 10-20 seconds depending on number of methods")

    # Generation logic
    if generate_btn and user_input.strip() and len(selected_methods) > 0:
        with st.spinner(f"Generating {len(selected_methods)} creative thinking prompts for {department}..."):
            try:
                # Build method list
                method_names = [m['name'] for m in selected_methods]

                # Build system prompt
                system_prompt = CREATIVE_THINKING_SYSTEM.format(
                    user_input=user_input,
                    selected_methods=", ".join(method_names),
                    department=department
                )

                # Build user message
                user_message = f"""Challenge: {user_input}

Department: {department}
Selected Methods: {", ".join(method_names)}

Generate one prompt for EACH selected method, adapted specifically for the {department} department. Each prompt should clearly apply the method's technique to this challenge."""

                # Call API
                response = call_anthropic(
                    system_prompt=system_prompt,
                    user_message=user_message,
                    max_tokens=2500
                )

                # Parse response
                st.session_state.ct_results = parse_prompts_output(response)
                st.session_state.ct_department = department
                st.success(f"✅ {len(st.session_state.ct_results)} prompts generated!")

            except Exception as e:
                st.error(f"Error generating prompts: {str(e)}")

    # Display results
    if 'ct_results' in st.session_state and st.session_state.ct_results:
        st.markdown("---")
        st.subheader("📋 Generated Prompts")

        dept = st.session_state.get('ct_department', 'your department')
        st.info(f"**Department Context:** {dept} | **How to use:** Each prompt applies a specific creative thinking method to your challenge. Use them in workshops or solo sessions.")

        for prompt_data in st.session_state.ct_results:
            # Find category icon
            icon = "⚡"
            for cat_name, cat_data in CATEGORIES.items():
                if cat_name == prompt_data['category']:
                    icon = cat_data['icon']
                    break

            with st.container():
                st.markdown(f"### {icon} {prompt_data['method']}")
                st.caption(f"Category: {prompt_data['category']}")
                st.code(prompt_data['prompt'], language=None)
                st.markdown("")

    else:
        # Empty state
        if not generate_btn or not user_input.strip():
            st.markdown("---")
            st.info("""
            ### 🌟 Quick Start

            1. **Enter your challenge** - Describe the problem or goal
            2. **Select department** - Choose which team this is for
            3. **Choose 1-5 methods** - Browse by category and select relevant methods
            4. **Generate prompts** - Get department-specific facilitation prompts
            5. **Use in sessions** - Copy prompts for workshops or brainstorming

            ### 💡 Example Combinations

            **For Sales (Lead Generation):**
            - Brainstorming + SCAMPER + Random Word Association

            **For Product (Feature Prioritization):**
            - Impact-Effort Matrix + Six Thinking Hats + Pros-Cons-Fixes

            **For Operations (Process Improvement):**
            - Five Whys + Reverse Thinking + Constraint Removal

            **For Strategy (Innovation):**
            - Provocation Technique + Analogies + TRIZ Principles
            """)

            # Show quick reference
            st.markdown("### 📚 Method Categories")
            cols = st.columns(3)

            categories_list = list(CATEGORIES.items())
            for idx, (cat_name, cat_data) in enumerate(categories_list):
                with cols[idx % 3]:
                    st.markdown(f"**{cat_data['icon']} {cat_name}**")
                    st.caption(cat_data['description'])
                    st.caption(f"Methods: {len(cat_data['methods'])}")
