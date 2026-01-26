import streamlit as st
import re
from backend.api_client import call_anthropic

# System prompt for Creative Thinking generation
CREATIVE_THINKING_SYSTEM = """You are an expert facilitator of creative thinking methodologies.

CRITICAL INTERPRETATION RULES:
1. DO NOT quote the user's challenge literally in generated prompts
2. INTERPRET their high-level challenge into specific, department-contextualized instructions
3. Each prompt must be COMPLETE and EXECUTABLE on its own
4. Include: role/context, department-specific background, specific tasks (3-5), facilitation guidance, output format
5. Each prompt should be 150-200 words with clear structure
6. Use department-appropriate terminology and examples

CHALLENGE (interpret and elaborate this, do not quote):
"{user_input}"

SELECTED METHODS: {selected_methods}
TARGET DEPARTMENT: {department}

AVAILABLE METHODS (24 across 6 categories):

DIVERGENT THINKING: Brainstorming, SCAMPER, Mind Mapping, Random Word Association
CONVERGENT THINKING: Six Thinking Hats, Impact-Effort Matrix, Pros-Cons-Fixes, Devil's Advocate
LATERAL THINKING: Provocation Technique, Reverse Thinking, Analogies from Other Domains, Constraint Removal
COLLABORATIVE METHODS: Brainwriting, Round Robin, Nominal Group Technique, Role Storming
REFRAMING TECHNIQUES: Five Whys, Perspective Shifting, Time Travel, Question Assumptions
STRUCTURED IDEATION: TRIZ Principles, Morphological Analysis, Forced Connections, Attribute Listing

YOUR TASK:
Generate prompts that interpret the challenge and apply creative thinking methods for the {department} department.

INTERPRETATION STRATEGY:
1. Understand what the user is REALLY trying to solve for {department}
2. Contextualize with department-specific scenarios, metrics, constraints
3. Generate ONE prompt per selected method that:
   - Interprets the challenge into department-specific context
   - Applies the creative method's framework explicitly
   - Provides relevant examples from {department}
   - Includes facilitation instructions (how to run the session)
   - Specifies expected outputs
   - Is 150-200 words

EXAMPLE OF GOOD INTERPRETATION:
Challenge: "improve customer retention"
Department: Sales
Method: Five Whys

You interpret and create:
"You are a sales operations analyst investigating customer churn root causes for our B2B SaaS business.

Context: Experiencing 15% annual churn (target: <8%). Average customer LTV: $125K. Churn is concentrated in year 2-3 customers. Sales team reports 'lack of adoption' as primary reason.

Apply Five Whys Method:
Layer 1: Why are year 2-3 customers churning?
→ Analyze: Low product adoption after initial deployment

Layer 2: Why is product adoption low?
→ Analyze: Gaps in onboarding and training

Layer 3: Why do onboarding gaps exist?
→ Analyze: Resource constraints in customer success team

Layer 4: Why are resources constrained?
→ Analyze: Hiring hasn't kept pace with growth

Layer 5: Why hasn't hiring kept pace?
→ Analyze: Budget allocated to sales, not post-sale support

Output: Root cause analysis document with recommended intervention point (likely: reallocate budget to customer success) and projected retention impact."

REQUIREMENTS:
1. Generate one prompt for EACH selected method
2. Each prompt must be 150-200 words
3. Fully contextualize for {department}
4. Include facilitation guidance
5. Be immediately actionable

Format output as XML:
<prompts>
<prompt method="[Method Name]" category="[Category Name]">
[Fully elaborated, department-contextualized 150-200 word prompt]
</prompt>
... continue for all selected methods
</prompts>

Ensure each prompt interprets the challenge and demonstrates the method's application in {department} context."""

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

    # Examples section
    with st.expander("💡 Try These Examples", expanded=False):
        st.markdown("Click any example to auto-fill the form:")

        examples = {
            "TSA Exit Acceleration (Operations)": {
                "challenge": "Accelerate TSA exit from 24 months to 12 months to reduce dependency costs and achieve operational independence faster",
                "department": "Operations",
                "methods": ["Reverse Thinking", "Constraint Removal", "SCAMPER", "Five Whys"],
                "description": "Explore unconventional paths to rapid independence"
            },
            "Synergy Value Creation (Strategy)": {
                "challenge": "Identify and quantify €50M in revenue synergies post-merger beyond the obvious cost synergies already captured in the model",
                "department": "Strategy",
                "methods": ["Brainstorming", "Forced Connections", "Analogies from Other Domains", "Provocation Technique"],
                "description": "Generate non-obvious value creation opportunities"
            },
            "Talent Retention Strategy (HR)": {
                "challenge": "Retain 95% of critical talent during 18-month separation uncertainty. Current attrition trending at 22% for key roles.",
                "department": "HR",
                "methods": ["Six Thinking Hats", "Perspective Shifting", "Pros-Cons-Fixes", "Role Storming"],
                "description": "Multi-stakeholder approach to retention program design"
            },
            "Customer Communication Plan (Communications)": {
                "challenge": "Communicate business separation to enterprise customers without triggering contract renegotiations or churn. €400M revenue at risk.",
                "department": "Communications",
                "methods": ["Perspective Shifting", "Time Travel", "Devil's Advocate", "Scenario Planning"],
                "description": "Anticipate customer concerns and craft reassuring narrative"
            }
        }

        cols = st.columns(3)
        for idx, (example_name, example_data) in enumerate(examples.items()):
            with cols[idx % 3]:
                if st.button(
                    f"📋 {example_name}",
                    key=f"ct_example_{idx}",
                    use_container_width=True,
                    help=example_data['description']
                ):
                    # Store prefill data (separate from widget keys to avoid conflicts)
                    st.session_state.ct_input_prefill = example_data['challenge']
                    st.session_state.ct_department_prefill = example_data['department']
                    st.session_state.ct_methods_prefill = example_data['methods']
                    st.rerun()

    st.markdown("---")

    # Input (use prefill value if available)
    input_prefill = st.session_state.get('ct_input_prefill', '')
    user_input = st.text_area(
        "Enter Your Challenge or Goal",
        height=100,
        value=input_prefill,
        placeholder="Example: How can we reduce customer churn in our SaaS product?",
        key="ct_input_actual"
    )

    # Department selector (use prefill value if available)
    dept_prefill = st.session_state.get('ct_department_prefill', 'Sales')
    dept_index = DEPARTMENTS.index(dept_prefill) if dept_prefill in DEPARTMENTS else 0

    st.markdown("### Select Department")
    department = st.selectbox(
        "Which department is this for?",
        options=DEPARTMENTS,
        index=dept_index,
        key="ct_department_actual",
        help="Prompts will be adapted with terminology and examples specific to this department"
    )

    # Method selector by category
    st.markdown("### Select Creative Thinking Methods (choose 1-5)")
    st.caption("Browse methods by category and select the ones most relevant to your challenge")

    selected_methods = []

    # Get prefilled methods for pre-selection
    methods_prefill = st.session_state.get('ct_methods_prefill', [])

    for cat_name, cat_data in CATEGORIES.items():
        with st.expander(f"{cat_data['icon']} {cat_name} - {cat_data['description']}", expanded=False):
            for method in cat_data['methods']:
                col1, col2 = st.columns([3, 1])
                with col1:
                    # Pre-select if this method is in the prefill list
                    is_preselected = method['name'] in methods_prefill

                    is_selected = st.checkbox(
                        f"**{method['name']}**",
                        value=is_preselected,
                        key=f"ct_method_{method['name']}_actual",
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
                st.session_state.ct_department_display = department
                st.success(f"✅ {len(st.session_state.ct_results)} prompts generated!")

            except Exception as e:
                st.error(f"Error generating prompts: {str(e)}")

    # Display results
    if 'ct_results' in st.session_state and st.session_state.ct_results:
        st.markdown("---")
        st.subheader("📋 Generated Prompts")

        dept = st.session_state.get('ct_department_display', 'your department')
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
