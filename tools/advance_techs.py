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

# Comprehensive technique definitions with full documentation
TECHNIQUES = {
    "multi_persona": {
        "name": "Multi-Persona Debate",
        "icon": "🎭",
        "full_name": "Multi-Persona Debate Prompting",
        "definition": "A metacognitive technique that forces the AI to simulate a conversation between distinct expert personas with opposing views before converging on a final answer.",
        "what_it_does": [
            "Reduces 'average' or generic responses by forcing conflict",
            "Increases nuance and depth by exploring multiple angles",
            "Triggers self-correction and critique within the generation process"
        ],
        "mechanism": "It leverages the Dialectical Method (Thesis, Antithesis, Synthesis). By assigning specific roles (e.g., 'Skeptic'), you override the model's default 'people-pleasing' tendency to agree with the user's premise, activating internal error-checking.",
        "when_to_use": "Use for complex decision-making, strategy formulation, or when you suspect the 'obvious' answer is too simple.",
        "department_examples": [
            {
                "department": "HR",
                "scenario": "Designing a Hybrid Work Policy",
                "description": "Debate between CHRO (flexibility), CFO (costs), and Engineering Manager (collaboration) to create balanced policy"
            },
            {
                "department": "Content",
                "scenario": "Choosing Content Strategy Direction",
                "description": "SEO Specialist vs Video Producer vs Content Strategist deciding on $50K Q2 budget allocation"
            },
            {
                "department": "Project Management",
                "scenario": "Choosing Between Agile vs. Waterfall",
                "description": "Agile Coach vs Compliance Officer vs Product Owner for 9-month enterprise migration"
            },
            {
                "department": "UX Design",
                "scenario": "Resolving Navigation Architecture Conflict",
                "description": "Minimalist Designer vs Accessibility Advocate vs Product Analyst for mobile banking app"
            }
        ],
        "limitations": "Can be verbose and slow. If personas are not distinct enough, they may simply agree, defeating the purpose."
    },

    "negative_constraint": {
        "name": "Negative Constraint Overloading",
        "icon": "🔄",
        "full_name": "Negative Constraint Overloading (The 'Positive Sandwich' Fix)",
        "definition": "Addressing the phenomenon where piling on 'Do not' instructions degrades model performance, by refactoring these into positive, weighted instructions.",
        "what_it_does": [
            "Prevents 'instruction forgetting' in complex prompts",
            "Reduces anxiety/confusion in the model's attention mechanism",
            "Stabilizes output format"
        ],
        "mechanism": "LLMs have 'negation blindness' and struggle to navigate infinite negative paths ('Don't do X, Y, Z'). They perform better with high-attention positive paths ('Do A'). Positive tokens carry higher attention weights.",
        "when_to_use": "When you find yourself writing more than 3 'do not' instructions, or when outputs ignore your constraints.",
        "department_examples": [
            {
                "department": "Customer Service",
                "scenario": "Training AI Chatbot Response Templates",
                "description": "Converting negative overload into positive sandwich structure for customer responses"
            },
            {
                "department": "Content",
                "scenario": "Writing Email Newsletter",
                "description": "Transforming 'don't be salesy, don't use clickbait' into positive structure guidance"
            },
            {
                "department": "HR",
                "scenario": "Writing Rejection Emails",
                "description": "Reframing constraints into positive tone and structure guidelines"
            },
            {
                "department": "Project Management",
                "scenario": "Writing Sprint Retrospective Summary",
                "description": "Converting blameless constraints into positive action-focused structure"
            }
        ],
        "limitations": "Requires more upfront prompt design work. Some safety constraints genuinely need to be negative."
    },

    "emotional_tipping": {
        "name": "Emotional Tipping",
        "icon": "💰",
        "full_name": "Emotional Tipping (Stakes Elevation)",
        "definition": "Artificially raising the perceived stakes or emotional weight of a request to trigger more detailed, careful, or thorough responses from the model.",
        "what_it_does": [
            "Increases response length and detail density",
            "Triggers more careful reasoning and error-checking",
            "Activates 'high-stakes' behavior patterns in the model"
        ],
        "mechanism": "Models are trained on high-stakes contexts (medical, legal, financial) where carefulness matters. By framing your query as high-stakes, you activate those training patterns. It's essentially role-playing consequence.",
        "when_to_use": "When you need maximum effort, thorough analysis, or when default responses are too casual/shallow.",
        "department_examples": [
            {
                "department": "Finance",
                "scenario": "Financial Modeling for Board Deck",
                "description": "Framing analysis as board-critical to get thorough scenario modeling"
            },
            {
                "department": "Legal",
                "scenario": "Contract Risk Analysis",
                "description": "Elevating stakes to trigger careful clause-by-clause review"
            },
            {
                "department": "Engineering",
                "scenario": "Security Vulnerability Assessment",
                "description": "Framing as production-critical to get exhaustive threat modeling"
            },
            {
                "department": "Sales",
                "scenario": "Enterprise Proposal Review",
                "description": "Positioning as $1M deal to get meticulous proposal critique"
            }
        ],
        "limitations": "Can feel manipulative. Some models may detect and ignore obvious stake inflation. Overuse diminishes effectiveness."
    },

    "deliberate_hallucination": {
        "name": "Deliberate Hallucination",
        "icon": "🌀",
        "full_name": "Deliberate Hallucination (Controlled Creative Divergence)",
        "definition": "Explicitly requesting the model to speculate, invent, or imagine possibilities beyond its training data—while maintaining awareness of the fictional nature.",
        "what_it_does": [
            "Unlocks creative ideation and lateral thinking",
            "Generates novel combinations and 'what-if' scenarios",
            "Bypasses the model's conservative 'I don't know' reflexes"
        ],
        "mechanism": "By giving explicit permission to speculate, you override the model's safety rails that prevent uncertain claims. The key is framing it as 'hypothetical' or 'speculative', which triggers creative rather than factual generation patterns.",
        "when_to_use": "For brainstorming, scenario planning, creative writing, or exploring possibilities beyond known data. NOT for factual research.",
        "department_examples": [
            {
                "department": "Product",
                "scenario": "Future Product Vision (5-Year Horizon)",
                "description": "Speculating on technology trends and product evolution paths"
            },
            {
                "department": "Strategy",
                "scenario": "Scenario Planning for Emerging Markets",
                "description": "Imagining multiple future states for strategic planning"
            },
            {
                "department": "R&D",
                "scenario": "Breakthrough Innovation Ideation",
                "description": "Exploring 'impossible' solutions to technical constraints"
            },
            {
                "department": "Marketing",
                "scenario": "Brand Campaign Concepts (Blue Sky)",
                "description": "Generating unconventional campaign ideas without budget constraints"
            }
        ],
        "limitations": "Output is explicitly unreliable for facts. Must be clearly labeled as speculative. Can produce nonsense if not constrained."
    },

    "chain_of_symbol": {
        "name": "Chain-of-Symbol Logic",
        "icon": "🔣",
        "full_name": "Chain-of-Symbol Logic (Explicit Reasoning Traces)",
        "definition": "Forcing the model to show its reasoning using symbolic notation (variables, logic operators, step labels) before generating natural language output.",
        "what_it_does": [
            "Makes reasoning transparent and debuggable",
            "Reduces logical leaps and increases rigor",
            "Forces step-by-step decomposition of complex problems"
        ],
        "mechanism": "Symbolic reasoning activates different attention patterns than prose generation. By requiring explicit notation (IF-THEN, variables, numbered steps), you force the model into 'programmer mode' rather than 'writer mode', which is more precise.",
        "when_to_use": "For logical reasoning, math, debugging, decision trees, or any task where you need to verify the thinking process.",
        "department_examples": [
            {
                "department": "Engineering",
                "scenario": "Debugging Complex System Behavior",
                "description": "Using symbolic trace to map state transitions and identify failure point"
            },
            {
                "department": "Data Science",
                "scenario": "Feature Engineering Logic Documentation",
                "description": "Documenting transformation logic with explicit variable definitions"
            },
            {
                "department": "Operations",
                "scenario": "Process Flowchart Logic Validation",
                "description": "Verifying decision tree logic using symbolic IF-THEN notation"
            },
            {
                "department": "Finance",
                "scenario": "Financial Model Assumptions Audit",
                "description": "Tracing calculation logic with explicit variable dependencies"
            }
        ],
        "limitations": "Verbose. Can feel awkward for non-technical users. Not suitable for creative or persuasive writing."
    },

    "needle_hiding": {
        "name": "Needle Hiding",
        "icon": "🎯",
        "full_name": "Needle Hiding (Critical Instruction Burial)",
        "definition": "Deliberately burying the most important instruction within verbose context to test and improve the model's instruction-following and attention mechanisms.",
        "what_it_does": [
            "Tests if model actually reads full context vs. skimming",
            "Improves compliance with subtle or counter-intuitive instructions",
            "Useful for quality assurance and model testing"
        ],
        "mechanism": "Models have recency bias (pay more attention to start/end). By hiding critical instructions mid-context, you test whether attention mechanisms are truly global. If the model follows the hidden instruction, you know it's reading carefully.",
        "when_to_use": "For testing model attention, ensuring compliance with buried requirements, or when instructions must be subtle.",
        "department_examples": [
            {
                "department": "QA",
                "scenario": "Testing AI Model Compliance",
                "description": "Embedding test requirements in documentation to verify thorough reading"
            },
            {
                "department": "Legal",
                "scenario": "Contract Clause Attention Test",
                "description": "Verifying AI catches critical clauses buried in lengthy agreements"
            },
            {
                "department": "Training",
                "scenario": "Employee Manual Comprehension",
                "description": "Testing if AI-assisted learning catches important policy details"
            }
        ],
        "limitations": "Adversarial by nature. Can reduce clarity. Not suitable for production systems where clarity is paramount."
    },

    "socratic_mirroring": {
        "name": "Socratic Mirroring",
        "icon": "❓",
        "full_name": "Socratic Mirroring (Reflective Question Inversion)",
        "definition": "Instead of answering your question, instruct the model to ask YOU clarifying questions first, forcing you to think more deeply about what you actually need.",
        "what_it_does": [
            "Surfaces hidden assumptions in your query",
            "Improves problem definition before solving",
            "Forces user to articulate requirements more precisely"
        ],
        "mechanism": "By inverting the dialogue, the model acts as facilitator rather than oracle. This mimics Socratic method—using questions to reveal gaps in understanding. Often the process of answering the model's questions solves your problem before it generates an answer.",
        "when_to_use": "When you're stuck, when your problem is poorly defined, or when you suspect you're asking the wrong question.",
        "department_examples": [
            {
                "department": "Product",
                "scenario": "Vague Feature Request Refinement",
                "description": "Model asks about user needs, constraints, success metrics before suggesting solutions"
            },
            {
                "department": "Consulting",
                "scenario": "Client Problem Diagnosis",
                "description": "Using questions to uncover root issues vs. stated symptoms"
            },
            {
                "department": "UX Research",
                "scenario": "Research Question Formulation",
                "description": "Clarifying research objectives before designing study methodology"
            },
            {
                "department": "Strategy",
                "scenario": "Strategic Initiative Scoping",
                "description": "Probing assumptions about goals, constraints, and success criteria"
            }
        ],
        "limitations": "Adds interaction overhead. Not suitable for simple, well-defined queries. Can feel patronizing if overused."
    },

    "cultural_localization": {
        "name": "Cultural Localization",
        "icon": "🌍",
        "full_name": "Cultural Localization (Context-Aware Adaptation)",
        "definition": "Explicitly specifying cultural context, idioms, references, and norms to adapt output for specific audiences beyond simple translation.",
        "what_it_does": [
            "Adapts tone, examples, and references to cultural context",
            "Avoids cultural faux pas and misunderstandings",
            "Increases resonance and relatability for target audience"
        ],
        "mechanism": "Models are trained on predominantly Western content. By explicitly stating cultural context, you activate minority training data from specific regions and adjust for cultural differences in communication style, humor, formality, etc.",
        "when_to_use": "When writing for non-Western audiences, when cultural sensitivity matters, or when localizing content beyond translation.",
        "department_examples": [
            {
                "department": "Marketing",
                "scenario": "Global Campaign Localization",
                "description": "Adapting US campaign concepts for Asian markets with different cultural values"
            },
            {
                "department": "Customer Success",
                "scenario": "International Support Templates",
                "description": "Adjusting response style for high-context vs. low-context cultures"
            },
            {
                "department": "HR",
                "scenario": "Global Team Communication",
                "description": "Framing policies with culturally appropriate examples and tone"
            },
            {
                "department": "Sales",
                "scenario": "Region-Specific Pitch Adaptation",
                "description": "Adjusting value propositions and social proof for different markets"
            }
        ],
        "limitations": "Model's cultural knowledge is uneven. May still produce stereotypes. Best paired with human cultural experts."
    },

    "adversarial_redteam": {
        "name": "Adversarial Red-Teaming",
        "icon": "🛡️",
        "full_name": "Adversarial Red-Teaming (Deliberate Attack Simulation)",
        "definition": "Instructing the model to actively attack, critique, or find flaws in a plan, argument, or system—essentially making it your harshest critic.",
        "what_it_does": [
            "Exposes blind spots and vulnerabilities before they become problems",
            "Generates edge cases and failure scenarios",
            "Stress-tests assumptions and logic"
        ],
        "mechanism": "By explicitly framing the task as adversarial, you override the model's default 'helpful assistant' persona and activate critical/skeptical reasoning patterns. This is similar to hiring a devil's advocate or penetration tester.",
        "when_to_use": "Before launching products, presenting strategies, or making major decisions. Whenever you need someone to 'break' your thinking.",
        "department_examples": [
            {
                "department": "Security",
                "scenario": "Threat Modeling for New Feature",
                "description": "Model acts as attacker identifying potential vulnerabilities"
            },
            {
                "department": "Product",
                "scenario": "Pre-Launch Risk Assessment",
                "description": "Generating failure scenarios and edge cases before release"
            },
            {
                "department": "Strategy",
                "scenario": "Competitive Response Simulation",
                "description": "Model plays competitor planning counter-moves to your strategy"
            },
            {
                "department": "Legal",
                "scenario": "Contract Vulnerability Analysis",
                "description": "Identifying loopholes and ambiguities from adversary perspective"
            }
        ],
        "limitations": "Can be demoralizing if not framed properly. May over-index on worst-case scenarios. Balance with constructive feedback."
    },

    "syntax_free": {
        "name": "Syntax-Free Abstract",
        "icon": "🎨",
        "full_name": "Syntax-Free Abstract Vectorization",
        "definition": "Describing desired output characteristics using purely abstract, sensory, or conceptual language instead of explicit formatting instructions.",
        "what_it_does": [
            "Unlocks creative interpretations vs. rigid templates",
            "Allows model to choose optimal format for the concept",
            "Useful for design, aesthetics, and open-ended creation"
        ],
        "mechanism": "Rather than specifying 'write 3 bullet points', you specify 'make it feel compact and scannable'. This activates the model's associative understanding of concepts rather than template-following. It's more like directing a creative than programming a machine.",
        "when_to_use": "For creative work, design briefs, when you want the model to surprise you, or when rigid structure would limit quality.",
        "department_examples": [
            {
                "department": "Design",
                "scenario": "Brand Voice Development",
                "description": "Describing desired brand personality through metaphor and feeling"
            },
            {
                "department": "Content",
                "scenario": "Editorial Style Evolution",
                "description": "Guiding tone shifts using abstract descriptors vs. explicit rules"
            },
            {
                "department": "UX Writing",
                "scenario": "Microcopy Emotional Calibration",
                "description": "Specifying button/label feel without prescribing exact words"
            },
            {
                "department": "Marketing",
                "scenario": "Campaign Mood Board Translation",
                "description": "Converting visual/emotional references into copy guidelines"
            }
        ],
        "limitations": "Less predictable. Harder to replicate exactly. May require multiple iterations to hit the right 'feel'."
    },

    "dynamic_tone": {
        "name": "Dynamic Tone Morphing",
        "icon": "🎢",
        "full_name": "Dynamic Tone Morphing (Progressive Complexity Shifts)",
        "definition": "Instructing the model to deliberately shift tone, complexity, or style as the response progresses—creating a journey rather than a static output.",
        "what_it_does": [
            "Matches audience sophistication progression",
            "Creates engaging narrative arc in explanations",
            "Allows single response to serve multiple audience levels"
        ],
        "mechanism": "By explicitly mapping tone to sections or progression, you override the model's default of maintaining consistent tone. This is especially powerful for educational content where you want to 'meet them where they are' then elevate.",
        "when_to_use": "For educational content, layered explanations, when audience expertise is unknown, or to make complex topics accessible.",
        "department_examples": [
            {
                "department": "Training",
                "scenario": "Onboarding Documentation Layers",
                "description": "Starting simple for day 1, increasing depth for week 2, expert level for month 3"
            },
            {
                "department": "Sales",
                "scenario": "Technical Proposal Structure",
                "description": "Exec summary (business), technical deep-dive (engineers), ROI details (finance)"
            },
            {
                "department": "Product",
                "scenario": "Feature Documentation for Mixed Audiences",
                "description": "Starting with user benefits, moving to technical implementation details"
            },
            {
                "department": "Communications",
                "scenario": "Crisis Communication Scaling",
                "description": "Simple public message → detailed stakeholder brief → technical incident report"
            }
        ],
        "limitations": "Requires clear section demarcation. Can feel disjointed if transitions aren't smooth. Harder to edit for consistency."
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
    st.write("Generate 5 prompts using expert-level prompting techniques with comprehensive documentation")

    # Info expander
    with st.expander("ℹ️ About These Techniques"):
        st.markdown("""
        These 11 techniques represent advanced prompt engineering methods used by experts.
        Each technique has specific mechanisms and use cases.

        **Click "📚 Browse Technique Library" below** to see:
        - What each technique does
        - Why it works (mechanism)
        - When to use it
        - Department-specific examples
        """)

    # NEW: Technique Library Browser
    with st.expander("📚 Browse Technique Library", expanded=False):
        st.markdown("### Explore All 11 Techniques")
        st.caption("Select any technique to see full documentation with examples")

        # Dropdown selector
        selected_technique_key = st.selectbox(
            "Select a technique to learn about:",
            options=list(TECHNIQUES.keys()),
            format_func=lambda x: f"{TECHNIQUES[x]['icon']} {TECHNIQUES[x]['name']}",
            key="technique_browser"
        )

        if selected_technique_key:
            tech = TECHNIQUES[selected_technique_key]

            st.markdown(f"## {tech['icon']} {tech['full_name']}")
            st.info(tech['definition'])

            # Three columns for core info
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("#### 🎯 What It Does")
                for item in tech['what_it_does']:
                    st.markdown(f"• {item}")

            with col2:
                st.markdown("#### ⚙️ Mechanism")
                st.markdown(tech['mechanism'])

            with col3:
                st.markdown("#### 📅 When To Use")
                st.markdown(tech['when_to_use'])

            # Department examples
            st.markdown("---")
            st.markdown("#### 💼 Department-Specific Use Cases")

            example_cols = st.columns(2)
            for idx, example in enumerate(tech.get('department_examples', [])):
                with example_cols[idx % 2]:
                    st.markdown(f"**{example['department']}:** {example['scenario']}")
                    st.caption(example['description'])

            # Limitations
            if 'limitations' in tech:
                st.warning(f"⚠️ **Limitations**: {tech['limitations']}")

    # Examples section
    with st.expander("💡 Try These Examples", expanded=False):
        st.markdown("Click any example to auto-fill the form:")

        examples = {
            "Database Optimization (Technical)": {
                "input": "Optimize database query performance for our analytics dashboard with 10M+ daily queries and sub-second response requirements",
                "techniques": ["chain_of_symbol", "emotional_tipping", "adversarial_redteam"],
                "note": "Uses symbolic logic + stakes elevation + vulnerability testing"
            },
            "Hybrid Work Policy (Strategic)": {
                "input": "Design a fair hybrid work policy balancing employee flexibility, cost optimization, and team collaboration",
                "techniques": ["multi_persona", "negative_constraint", "socratic_mirroring"],
                "note": "Multi-perspective debate + positive framing + clarifying questions"
            },
            "Global Campaign (Creative)": {
                "input": "Adapt our US marketing campaign for Asian markets with different cultural values",
                "techniques": ["cultural_localization", "syntax_free", "dynamic_tone"],
                "note": "Cultural adaptation + abstract description + progressive complexity"
            },
            "Product Launch Risk (Critical)": {
                "input": "Identify potential failure modes for our new mobile payment feature before launch",
                "techniques": ["adversarial_redteam", "emotional_tipping", "deliberate_hallucination"],
                "note": "Attack simulation + high stakes + speculative scenarios"
            }
        }

        for name, data in examples.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(f"📋 {name}", key=f"ex_{name}", use_container_width=True):
                    # Clear all checkboxes
                    for tech_key in TECHNIQUES.keys():
                        st.session_state[f"at_tech_{tech_key}"] = False

                    # Set input and techniques
                    st.session_state.at_input = data['input']
                    for tech_key in data['techniques']:
                        st.session_state[f"at_tech_{tech_key}"] = True

                    st.rerun()
            with col2:
                st.caption(data['note'])

    st.markdown("---")

    # Input
    user_input = st.text_area(
        "Enter Your Goal or Task",
        height=120,
        placeholder="Example: Design a database schema for a high-frequency trading application",
        key="at_input"
    )

    # Technique selector
    st.markdown("### Select 3-5 Advanced Techniques")
    st.caption("Select the techniques most relevant to your task. The system will generate 5 prompts using your selections.")

    selected = []
    selected_keys = []

    # Display as grid with checkboxes
    cols = st.columns(3)
    for idx, (key, tech) in enumerate(TECHNIQUES.items()):
        with cols[idx % 3]:
            is_selected = st.checkbox(
                f"{tech['icon']} **{tech['name']}**",
                key=f"at_tech_{key}",
                help=tech['definition']
            )

            if is_selected:
                selected.append(tech['full_name'])
                selected_keys.append(key)

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
                if tech['full_name'] in prompt_data['technique'] or tech['name'] in prompt_data['technique']:
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
            2. **Browse techniques** - Click "📚 Browse Technique Library" to learn about each method
            3. **Select 3-5 techniques** - Choose techniques based on your specific needs
            4. **Generate prompts** - Get 5 specialized prompts, each using a different technique
            5. **Copy and use** - Pick the prompt that best fits your requirements

            ### 💡 Recommended Combinations

            **For Code/Technical Work:**
            - Chain-of-Symbol Logic + Emotional Tipping + Adversarial Red-Team

            **For Creative/Marketing:**
            - Dynamic Tone Morphing + Cultural Localization + Syntax-Free Abstract

            **For Strategy/Decisions:**
            - Multi-Persona Debate + Socratic Mirroring + Negative Constraint

            **For Risk Assessment:**
            - Adversarial Red-Team + Emotional Tipping + Deliberate Hallucination
            """)
