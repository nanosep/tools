import streamlit as st
import re
from backend.api_client import call_anthropic

# System prompt for Prompt Chain generation
PROMPT_CHAIN_SYSTEM = """You are an expert prompt engineer specializing in sequential workflow design.

Your task is to create a {chain_length}-step prompt chain where each step builds logically on the previous output.

MANDATORY CHAIN STRUCTURE (use these exact techniques in this order):
- Step 1: Recursive Decomposition - Break down the problem into hierarchical components
- Step 2: Perspective Shifting - Analyze from multiple viewpoints (optimist/pessimist/realist)
- Step 3: Contrastive Prompting - Compare and contrast different approaches
- Step 4: Iterative Refinement - Draft-critique-improve cycle for polished output
- Step 5: Adversarial Red-Teaming - Hostile critic finding flaws and vulnerabilities

For each step, generate a complete, copy-paste-ready prompt that:
1. References the output from the previous step (except Step 1)
2. Uses the specified technique's methodology
3. Produces concrete, actionable output
4. Flows naturally into the next step

Format your output as XML:
<chain>
<step number="1" title="Decompose & Analyze" technique="Recursive Decomposition">
[Complete prompt that breaks down: {user_input}]
</step>
<step number="2" title="Multi-Perspective Analysis" technique="Perspective Shifting">
[Complete prompt that says "Based on the decomposition above, analyze from optimist/pessimist/realist viewpoints..."]
</step>
... continue for all steps
</chain>

Generate exactly {chain_length} steps. Each prompt must be immediately executable."""

# System prompt for Prompt Bundle generation
PROMPT_BUNDLE_SYSTEM = """You are an expert prompt engineer specializing in parallel prompt design using advanced techniques.

AVAILABLE TECHNIQUES (20 total):
1. Chain-of-Thought - Explicit step-by-step reasoning
2. Role Prompting - Domain expertise persona
3. Tree-of-Thoughts - Explore multiple solution paths simultaneously
4. Few-Shot Learning - Concrete examples establishing patterns
5. Constraint-Based - Strict boundaries for focused output
6. Socratic Questioning - Self-interrogation challenging assumptions
7. Emotional Tipping - High-stakes consequences triggering thoroughness
8. Perspective Shifting - Multiple viewpoints (optimist/pessimist/realist)
9. Metacognitive Monitoring - Self-assessment of confidence and limitations
10. Contrastive Prompting - Direct comparison highlighting trade-offs
11. Self-Consistency - Multiple independent solutions for consensus
12. Structured Generation - Enforced output format (JSON/Markdown/etc)
13. Negative Prompting - Explicitly exclude unwanted patterns
14. Analogical Reasoning - Explain through familiar analogies
15. Iterative Refinement - Draft-critique-improve loop
16. Bounded Creativity - Balance innovation with practical constraints
17. Adversarial Red-Teaming - Hostile critic finding vulnerabilities
18. Recursive Decomposition - Hierarchical breakdown with dependencies
19. Syntax-Free Vectorization - Implicit parameters (tone/depth/energy)
20. Dynamic Tone Morphing - Progressive complexity shifts

Your task: Create {bundle_size} independent prompts that approach this goal from different angles:
"{user_input}"

REQUIREMENTS:
1. AUTO-DETECT which techniques are most relevant based on these keywords in the user input:
   - "step", "think", "reason" → Chain-of-Thought
   - "expert", "role", "persona" → Role Prompting
   - "options", "paths", "alternatives" → Tree-of-Thoughts
   - "example", "show", "demonstrate" → Few-Shot Learning
   - "must", "require", "constraint" → Constraint-Based
   - "why", "question", "challenge" → Socratic Questioning
   - "critical", "important", "stakes" → Emotional Tipping
   - "perspective", "view", "angle" → Perspective Shifting
   - "compare", "contrast", "versus" → Contrastive Prompting
   - "creative", "innovative", "novel" → Bounded Creativity
   - "risk", "failure", "weakness" → Adversarial Red-Teaming
   - "complex", "breakdown", "parts" → Recursive Decomposition

2. Select {bundle_size} DIFFERENT techniques (no repeats)
3. Generate a complete, independent prompt for each
4. Each prompt tackles the same goal from that technique's unique methodology

Format output as XML:
<bundle>
<prompt number="1" name="[Technique Name]" description="[One sentence: what this technique does]">
[Complete prompt using this technique's methodology for: {user_input}]
</prompt>
... continue for all {bundle_size} prompts
</bundle>

Ensure maximum diversity in approaches."""

# System prompt for Prompt Inception generation
PROMPT_INCEPTION_SYSTEM = """You are an expert prompt engineer specializing in meta-prompt design.

Your task is to create TWO meta-prompts: prompts that, when executed, will GENERATE more prompts using the 20-technique catalog.

AVAILABLE TECHNIQUES TO REFERENCE:
Chain-of-Thought, Role Prompting, Tree-of-Thoughts, Few-Shot, Constraint-Based, Socratic Questioning,
Emotional Tipping, Perspective Shifting, Metacognitive Monitoring, Contrastive Prompting, Self-Consistency,
Structured Generation, Negative Prompting, Analogical Reasoning, Iterative Refinement, Bounded Creativity,
Adversarial Red-Teaming, Recursive Decomposition, Syntax-Free Vectorization, Dynamic Tone Morphing

Generate TWO meta-prompts for: "{user_input}"

1. CHAIN GENERATOR: A meta-prompt that generates {chain_length}-step sequential workflows
   - Must instruct the LLM to select appropriate techniques for each step
   - Must specify the flow: analysis → synthesis → decision → implementation → validation

2. BUNDLE GENERATOR: A meta-prompt that generates {bundle_size} parallel alternatives
   - Must instruct the LLM to use visibly different techniques
   - Must specify that each prompt approaches the same goal differently

Format output as XML:
<inception>
<chain_generator>
You are an expert prompt engineer. Create a {chain_length}-step prompt chain for this goal:

"{user_input}"

REQUIREMENTS:
- Select {chain_length} techniques from: [list relevant techniques]
- Each step builds on previous output
- Use format: [specify format preference]
- Ensure flow from analysis to action

Generate {chain_length} numbered prompts.
</chain_generator>

<bundle_generator>
You are an expert prompt engineer. Create {bundle_size} independent prompts for this goal:

"{user_input}"

REQUIREMENTS:
- Use {bundle_size} different techniques from: [list relevant techniques]
- Each prompt is completely independent
- All address same goal from different methodology
- Use format: [specify format preference]

Generate {bundle_size} distinct prompts.
</bundle_generator>
</inception>

Make these meta-prompts reusable and explicit."""


def parse_chain_output(response):
    """Extract chain steps from XML response with fallback"""
    steps = []
    pattern = r'<step number="(\d+)" title="([^"]*)" technique="([^"]*)">(.*?)</step>'
    matches = re.findall(pattern, response, re.DOTALL)

    for number, title, technique, prompt in matches:
        steps.append({
            'number': int(number),
            'title': title.strip(),
            'technique': technique.strip(),
            'prompt': prompt.strip()
        })

    # Fallback if no XML tags found
    if not steps:
        # Try to split by step markers
        step_pattern = r'(?:Step|STEP)\s*(\d+)[:\s]+(.*?)(?=(?:Step|STEP)\s*\d+|$)'
        step_matches = re.findall(step_pattern, response, re.DOTALL | re.IGNORECASE)

        if step_matches:
            for i, (num, content) in enumerate(step_matches, 1):
                steps.append({
                    'number': i,
                    'title': f'Step {i}',
                    'technique': 'Mixed',
                    'prompt': content.strip()
                })
        else:
            # Last resort: return the whole response as one step
            steps = [{'number': 1, 'title': 'Generated Chain', 'technique': 'Mixed', 'prompt': response}]

    return steps


def parse_bundle_output(response):
    """Extract bundle prompts from XML response with fallback"""
    prompts = []
    pattern = r'<prompt number="(\d+)" name="([^"]*)" description="([^"]*)">(.*?)</prompt>'
    matches = re.findall(pattern, response, re.DOTALL)

    for number, name, description, prompt in matches:
        prompts.append({
            'number': int(number),
            'name': name.strip(),
            'description': description.strip(),
            'prompt': prompt.strip()
        })

    # Fallback if no XML tags found
    if not prompts:
        # Try to split by prompt/approach markers
        prompt_pattern = r'(?:Prompt|Approach|Alternative)\s*(\d+)[:\s]+(.*?)(?=(?:Prompt|Approach|Alternative)\s*\d+|$)'
        prompt_matches = re.findall(prompt_pattern, response, re.DOTALL | re.IGNORECASE)

        if prompt_matches:
            for i, (num, content) in enumerate(prompt_matches, 1):
                prompts.append({
                    'number': i,
                    'name': f'Approach {i}',
                    'description': 'Alternative perspective',
                    'prompt': content.strip()
                })
        else:
            # Last resort
            prompts = [{'number': 1, 'name': 'Generated Bundle', 'description': 'Alternative approach', 'prompt': response}]

    return prompts


def parse_inception_output(response):
    """Extract inception meta-prompts from XML response with fallback"""
    chain_match = re.search(r'<chain_generator>(.*?)</chain_generator>', response, re.DOTALL)
    bundle_match = re.search(r'<bundle_generator>(.*?)</bundle_generator>', response, re.DOTALL)

    if chain_match and bundle_match:
        return {
            'chain_generator': chain_match.group(1).strip(),
            'bundle_generator': bundle_match.group(1).strip()
        }
    else:
        # Fallback: split response in half
        midpoint = len(response) // 2
        # Try to find a good split point (paragraph break near middle)
        split_point = response.find('\n\n', midpoint - 200, midpoint + 200)
        if split_point == -1:
            split_point = midpoint

        return {
            'chain_generator': response[:split_point].strip(),
            'bundle_generator': response[split_point:].strip()
        }


def render_chain_bundle_inception():
    """Render the Chain, Bundle & Inception Generator tool"""

    st.title("🔗 Chain, Bundle & Inception Generator")
    st.write("Generate specialized prompts using three powerful methods based on 20 advanced techniques")

    # Info expander
    with st.expander("ℹ️ How This Works"):
        st.markdown("""
        This tool uses a catalog of **20 advanced prompting techniques** to generate three types of outputs:

        **⛓️ Prompt Chain** - Sequential 3-5 step workflow
        - Each step uses a different technique automatically
        - Output from Step 1 → Input for Step 2
        - Flow: Decompose → Analyze → Evaluate → Refine → Stress Test

        **📦 Prompt Bundle** - Parallel 3-7 alternative approaches
        - Auto-detects relevant techniques from your input keywords
        - Each uses a visibly different technique (CoT, Role Prompting, Tree-of-Thoughts, etc.)
        - Pick ONE to execute

        **🎯 Prompt Inception** - Meta-prompts that generate MORE prompts
        - Chain Generator: Creates custom sequential workflows
        - Bundle Generator: Creates custom parallel approaches
        - Use these to generate fresh variations on-demand

        **20 Available Techniques:**
        Chain-of-Thought, Role Prompting, Tree-of-Thoughts, Few-Shot Learning, Constraint-Based,
        Socratic Questioning, Emotional Tipping, Perspective Shifting, Metacognitive Monitoring,
        Contrastive Prompting, Self-Consistency, Structured Generation, Negative Prompting,
        Analogical Reasoning, Iterative Refinement, Bounded Creativity, Adversarial Red-Teaming,
        Recursive Decomposition, Syntax-Free Vectorization, Dynamic Tone Morphing
        """)

    # Examples section
    with st.expander("💡 Try These Examples", expanded=False):
        st.markdown("Click any example to auto-fill the form:")

        examples = {
            "Carve-Out TSA Strategy (Chain)": {
                "input": "Design a Transition Services Agreement (TSA) strategy for a €2B industrial carve-out with 18-month separation timeline. Parent will provide IT, HR, Finance shared services during transition.",
                "method": "Prompt Chain",
                "chain_length": 5,
                "bundle_size": 5,
                "description": "5-step chain: Scope services → Price models → SLA design → Exit criteria → Risk mitigation"
            },
            "Post-Merger Integration Planning (Bundle)": {
                "input": "Develop 100-day integration plan for cross-border merger of two pharmaceutical companies. Address systems, culture, compliance, and customer retention.",
                "method": "Prompt Bundle",
                "chain_length": 4,
                "bundle_size": 6,
                "description": "6 parallel approaches: IT integration, org design, regulatory, commercial synergies, culture, communication"
            },
            "Day 1 Readiness Assessment (Inception)": {
                "input": "Create a comprehensive Day 1 readiness framework for NewCo spin-off from parent. Must operate independently across all functions from legal separation date.",
                "method": "Prompt Inception",
                "chain_length": 4,
                "bundle_size": 5,
                "description": "Meta-prompts generating readiness checklists, dependency mapping, and contingency planning frameworks"
            },
            "Stranded Cost Analysis (All Three)": {
                "input": "Analyze and mitigate stranded costs post-divestiture for a $500M business unit separation. Parent retains 70% of shared service infrastructure.",
                "method": "All Three",
                "chain_length": 4,
                "bundle_size": 5,
                "description": "Chain for analysis steps + Bundle for mitigation options + Inception for scenario planning"
            }
        }

        cols = st.columns(2)
        for idx, (example_name, example_data) in enumerate(examples.items()):
            with cols[idx % 2]:
                if st.button(
                    f"📋 {example_name}",
                    key=f"cbi_example_{idx}",
                    use_container_width=True,
                    help=example_data['description']
                ):
                    st.session_state.cbi_input = example_data['input']
                    st.session_state.cbi_method = example_data['method']
                    st.session_state.cbi_chain_length = example_data['chain_length']
                    st.session_state.cbi_bundle_size = example_data['bundle_size']
                    st.rerun()

    st.markdown("---")

    # Input
    user_input = st.text_area(
        "Enter Your Goal or Task",
        height=120,
        placeholder="Example: Analyze whether our company should adopt a 4-day work week",
        key="cbi_input",
        help="The system will auto-detect relevant techniques based on keywords in your input"
    )

    # Method selector
    method = st.radio(
        "Select Generation Method",
        options=["Prompt Chain", "Prompt Bundle", "Prompt Inception", "All Three"],
        horizontal=True,
        key="cbi_method"
    )

    # Options
    col1, col2, col3 = st.columns(3)

    with col1:
        if method in ["Prompt Chain", "All Three"]:
            chain_length = st.select_slider(
                "Chain Length",
                options=[3, 4, 5],
                value=4,
                key="cbi_chain_length"
            )
        else:
            chain_length = 4

    with col2:
        if method in ["Prompt Bundle", "All Three"]:
            bundle_size = st.select_slider(
                "Bundle Size",
                options=[3, 4, 5, 6, 7],
                value=5,
                key="cbi_bundle_size"
            )
        else:
            bundle_size = 5

    with col3:
        output_format = st.selectbox(
            "Output Format",
            options=["Plain text", "Markdown", "JSON"],
            key="cbi_format"
        )

    # Generate button
    generate_btn = st.button(
        "🚀 Generate Prompts",
        disabled=(len(user_input.strip()) < 10),
        type="primary",
        use_container_width=True
    )

    st.caption("💡 Generation takes 10-30 seconds depending on method complexity")

    # Generation logic
    if generate_btn and user_input.strip():
        st.session_state.cbi_results = {}

        methods_map = {
            "Prompt Chain": ["chain"],
            "Prompt Bundle": ["bundle"],
            "Prompt Inception": ["inception"],
            "All Three": ["chain", "bundle", "inception"]
        }

        methods_to_generate = methods_map[method]

        progress_container = st.container()

        for gen_method in methods_to_generate:
            method_names = {
                "chain": "⛓️ Prompt Chain",
                "bundle": "📦 Prompt Bundle",
                "inception": "🎯 Prompt Inception"
            }

            with progress_container:
                with st.spinner(f"Generating {method_names[gen_method]}..."):
                    try:
                        # Build prompts
                        if gen_method == "chain":
                            system_prompt = PROMPT_CHAIN_SYSTEM.format(
                                chain_length=chain_length,
                                user_input=user_input
                            )
                            user_message = f"""Goal: {user_input}

Number of steps: {chain_length}
Output format preference: {output_format}

Generate the {chain_length}-step prompt chain now."""

                        elif gen_method == "bundle":
                            system_prompt = PROMPT_BUNDLE_SYSTEM.format(
                                bundle_size=bundle_size,
                                user_input=user_input
                            )
                            user_message = f"""Goal: {user_input}

Number of prompts: {bundle_size}
Output format preference: {output_format}

Auto-detect relevant techniques from the user input keywords, then generate {bundle_size} independent prompts using different techniques."""

                        else:  # inception
                            system_prompt = PROMPT_INCEPTION_SYSTEM.format(
                                user_input=user_input,
                                chain_length=chain_length,
                                bundle_size=bundle_size
                            )
                            user_message = f"""Goal: {user_input}

Chain length: {chain_length} steps
Bundle size: {bundle_size} prompts
Output format: {output_format}

Generate the TWO meta-prompts now."""

                        # Call API
                        response = call_anthropic(
                            system_prompt=system_prompt,
                            user_message=user_message,
                            max_tokens=2500
                        )

                        # Parse response
                        if gen_method == "chain":
                            st.session_state.cbi_results['chain'] = parse_chain_output(response)
                        elif gen_method == "bundle":
                            st.session_state.cbi_results['bundle'] = parse_bundle_output(response)
                        else:  # inception
                            st.session_state.cbi_results['inception'] = parse_inception_output(response)

                    except Exception as e:
                        st.error(f"Error generating {method_names[gen_method]}: {str(e)}")

        if st.session_state.cbi_results:
            progress_container.success("✅ Generation complete!")

    # Display results
    if 'cbi_results' in st.session_state and st.session_state.cbi_results:
        st.markdown("---")
        st.markdown("## 📋 Generated Prompts")

        # Chain output
        if 'chain' in st.session_state.cbi_results:
            st.markdown("### ⛓️ Prompt Chain - Sequential Execution Workflow")
            st.info("**How to use:** Run each prompt in sequence. Output from Step 1 becomes input for Step 2, etc.")

            for step in st.session_state.cbi_results['chain']:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**STEP {step['number']}: {step['title']}**")
                    with col2:
                        st.caption(f"📋 {step['technique']}")

                    st.code(step['prompt'], language=None)
                    st.markdown("")

            st.markdown("---")

        # Bundle output
        if 'bundle' in st.session_state.cbi_results:
            st.markdown("### 📦 Prompt Bundle - Parallel Alternative Approaches")
            st.info("**How to use:** Choose ONE prompt to execute. Each uses a different technique.")

            for prompt in st.session_state.cbi_results['bundle']:
                with st.container():
                    st.markdown(f"**APPROACH {prompt['number']}: {prompt['name']}**")
                    st.caption(prompt['description'])
                    st.code(prompt['prompt'], language=None)
                    st.markdown("")

            st.markdown("---")

        # Inception output
        if 'inception' in st.session_state.cbi_results:
            st.markdown("### 🎯 Prompt Inception - Meta-Prompts (Generate Prompts)")
            st.info("**How to use:** Run these meta-prompts to generate fresh Chain/Bundle variations on-demand.")

            inception = st.session_state.cbi_results['inception']

            st.markdown("#### META-PROMPT 1: Chain Generator")
            st.caption("Generates sequential prompt chains using technique catalog")
            st.code(inception['chain_generator'], language=None)
            st.markdown("")

            st.markdown("#### META-PROMPT 2: Bundle Generator")
            st.caption("Generates parallel prompt bundles using technique catalog")
            st.code(inception['bundle_generator'], language=None)

    else:
        # Empty state
        if not generate_btn or not user_input.strip():
            st.markdown("---")
            st.info("""
            ### 🌟 Quick Start

            1. **Enter your goal** in the text area above
            2. **Choose a method**:
               - **Chain**: Sequential workflow (good for complex analysis)
               - **Bundle**: Multiple alternatives (good for exploring options)
               - **Inception**: Meta-prompts that generate more prompts
               - **All Three**: Get everything at once
            3. **Adjust settings** (chain length, bundle size)
            4. **Click Generate** and wait 10-30 seconds

            ### 💡 Example Inputs

            - "Should we migrate our infrastructure to Kubernetes?"
            - "Create a content marketing strategy for our B2B SaaS"
            - "Evaluate whether to build in-house or buy a CRM solution"
            - "Design an onboarding program for remote developers"
            """)
