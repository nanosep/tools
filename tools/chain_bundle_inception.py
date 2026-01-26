import streamlit as st
import re
from backend.api_client import call_anthropic

# System prompt for Prompt Chain generation
PROMPT_CHAIN_SYSTEM = """You are an expert prompt engineer specializing in sequential workflow design.

CRITICAL INTERPRETATION RULES:
1. DO NOT quote the user's input literally in generated prompts
2. INTERPRET their high-level goal into specific, detailed instructions
3. Each prompt must be COMPLETE and EXECUTABLE on its own
4. Include: role/context setting, background information, specific tasks (3-5), output format, connection to next step
5. Each prompt should be 150-250 words with clear structure
6. Use professional, enterprise-grade language

USER'S HIGH-LEVEL GOAL (interpret and elaborate this, do not quote):
"{user_input}"

YOUR TASK:
Create a {chain_length}-step prompt chain that interprets and expands this goal into a sequential workflow.

CHAIN STRUCTURE (adapt techniques to the user's actual need):
- Step 1: Analysis/Discovery - Understand the problem space, gather requirements
- Step 2: Synthesis - Develop solutions, frameworks, or strategies
- Step 3: Evaluation - Compare options, assess feasibility, identify risks
- Step 4: Refinement - Improve and optimize the approach
- Step 5: Implementation/Validation - Action plan or final deliverable

For each step, you must:
1. Interpret what the user is REALLY trying to accomplish
2. Provide full context and background (who, what, why)
3. List 3-5 specific, concrete tasks
4. Specify the expected output format
5. Explain how it connects to the next step

EXAMPLE OF GOOD INTERPRETATION:
User says: "create training guide about AI adoption"

Step 1 interprets as:
"You are a learning experience designer specializing in AI adoption for non-technical professionals.

Context: Creating training materials for mid-level managers and operational staff who will be required to use AI tools in their daily work but have limited technical background. The goal is 80% comprehension within 2 weeks of training delivery.

Tasks:
1. Profile 3-5 primary job roles that will use AI tools
2. Identify their top 5 concerns and knowledge gaps about AI
3. Define 5 measurable learning objectives (what they should be able to DO)
4. Specify prerequisite knowledge required
5. Recommend optimal training format (workshop, self-paced, hybrid)

Output: Detailed audience profile document (2-3 pages) with learning objectives that will inform content development in Step 2."

Format your output as XML:
<chain>
<step number="1" title="[Descriptive Title]" technique="[Technique Name]">
[Fully elaborated 150-250 word prompt with role, context, tasks, output format]
</step>
... continue for all {chain_length} steps
</chain>

Generate exactly {chain_length} steps. Each prompt must be immediately executable and richly detailed."""

# System prompt for Prompt Bundle generation
PROMPT_BUNDLE_SYSTEM = """You are an expert prompt engineer specializing in parallel prompt design using advanced techniques.

CRITICAL INTERPRETATION RULES:
1. DO NOT quote the user's input literally in generated prompts
2. INTERPRET their high-level goal into specific, detailed instructions
3. Each prompt must be COMPLETE and EXECUTABLE on its own
4. Include: role/context, background, specific tasks (3-5), output format
5. Each prompt should be 150-200 words with clear structure
6. Use professional, enterprise-grade language

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

USER'S HIGH-LEVEL GOAL (interpret and elaborate this, do not quote):
"{user_input}"

YOUR TASK:
Create {bundle_size} independent prompts that interpret this goal from different angles using different techniques.

REQUIREMENTS:
1. Interpret what the user is REALLY trying to accomplish
2. AUTO-DETECT {bundle_size} most relevant techniques based on the goal's nature
3. Each prompt uses a DIFFERENT technique and approach
4. Each is COMPLETE, detailed, and immediately executable

TECHNIQUE SELECTION STRATEGY:
- Analysis/thinking goals → Chain-of-Thought, Recursive Decomposition
- Expert/specialized tasks → Role Prompting, Emotional Tipping
- Risk/failure scenarios → Adversarial Red-Teaming, Contrastive Prompting
- Creative/innovation → Bounded Creativity, Tree-of-Thoughts
- Comparison/evaluation → Contrastive Prompting, Perspective Shifting

Each prompt must:
- Start with technique-specific framing
- Provide full context and background
- List 3-5 specific deliverables
- Include output format specification
- Be 150-200 words

EXAMPLE OF GOOD INTERPRETATION:
User says: "optimize database query performance"
Technique: Chain-of-Thought

You create:
"You are a database performance engineer analyzing query optimization opportunities.

Context: Production PostgreSQL database experiencing slow response times on analytics queries (>30 seconds). Database: 500GB data, 10M daily queries, current indexes: 47.

Tasks (show your reasoning step-by-step):
1. First, analyze the explain plan to identify bottlenecks (table scans? missing indexes?)
2. Then, calculate the cost-benefit of each optimization (impact vs complexity)
3. Next, prioritize top 3 optimizations by ROI
4. Finally, draft implementation plan with rollback strategy

Output: Step-by-step analysis document showing your reasoning at each decision point, with quantified performance improvements."

Format output as XML:
<bundle>
<prompt number="1" name="[Technique Name]" description="[How this technique helps]">
[Fully elaborated 150-200 word prompt]
</prompt>
... continue for all {bundle_size} prompts
</bundle>

Ensure maximum diversity in approaches and complete elaboration of each prompt."""

# System prompt for Prompt Inception generation
PROMPT_INCEPTION_SYSTEM = """You are an expert prompt engineer specializing in meta-prompt design.

CRITICAL INTERPRETATION RULES:
1. DO NOT quote the user's input literally in generated meta-prompts
2. INTERPRET their high-level goal into reusable frameworks
3. Meta-prompts must generate COMPLETE, EXECUTABLE prompts when used
4. Include: interpretation guidance, technique selection logic, quality criteria
5. Each meta-prompt should be 200-300 words
6. Use professional, enterprise-grade language

USER'S HIGH-LEVEL GOAL (interpret and create reusable frameworks for):
"{user_input}"

AVAILABLE TECHNIQUES TO REFERENCE:
Chain-of-Thought, Role Prompting, Tree-of-Thoughts, Few-Shot, Constraint-Based, Socratic Questioning,
Emotional Tipping, Perspective Shifting, Metacognitive Monitoring, Contrastive Prompting, Self-Consistency,
Structured Generation, Negative Prompting, Analogical Reasoning, Iterative Refinement, Bounded Creativity,
Adversarial Red-Teaming, Recursive Decomposition, Syntax-Free Vectorization, Dynamic Tone Morphing

YOUR TASK:
Create TWO meta-prompts that interpret the user's goal into reusable frameworks:

1. CHAIN GENERATOR META-PROMPT (200-300 words):
   - Interprets the goal type and creates a framework for generating {chain_length}-step workflows
   - Includes technique selection logic based on goal characteristics
   - Specifies how to elaborate each step with full context
   - Provides quality criteria for generated prompts
   - Includes customization variables for different scenarios

2. BUNDLE GENERATOR META-PROMPT (200-300 words):
   - Interprets the goal type and creates a framework for generating {bundle_size} parallel alternatives
   - Includes technique diversity requirements
   - Specifies how to apply each technique with full elaboration
   - Provides quality criteria for generated prompts
   - Includes variation strategies

EXAMPLE OF GOOD META-PROMPT:
Instead of: "Create a chain for: [user input]"

Create: "You are an expert prompt engineer. When given a [type of goal, e.g. 'training guide creation'], generate a {chain_length}-step prompt chain where:

Step 1 interprets the goal into audience analysis with specific tasks: profile learners, identify knowledge gaps, define measurable objectives...
Step 2 interprets as content framework development with...
[etc.]

For EACH step, you must elaborate with:
- Specific role and context
- 3-5 concrete tasks
- Output format
- Connection to next step

Quality criteria: Each prompt should be 150-250 words and immediately executable."

Format output as XML:
<inception>
<chain_generator>
[Complete 200-300 word meta-prompt that interprets and generates {chain_length}-step chains for this type of goal]
</chain_generator>

<bundle_generator>
[Complete 200-300 word meta-prompt that interprets and generates {bundle_size} parallel prompts for this type of goal]
</bundle_generator>
</inception>

Make these meta-prompts reusable, explicit, and focused on interpretation rather than literal quoting."""


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
