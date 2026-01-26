import streamlit as st
import re
from backend.api_client import call_anthropic

# System prompt for Advanced Techniques generation
ADVANCE_TECHS_SYSTEM = """You are an expert prompt engineer specializing in advanced prompting techniques.

CRITICAL INTERPRETATION RULES:
1. DO NOT quote the user's challenge literally in generated prompts
2. INTERPRET their high-level challenge into specific, detailed instructions
3. Each prompt must be COMPLETE and EXECUTABLE on its own
4. Include: role/context, background information, specific tasks (3-5), output format
5. Each prompt should be 150-250 words with clear structure
6. Use professional, enterprise-grade language

USER'S CHALLENGE (interpret and elaborate this, do not quote):
"{user_input}"

SELECTED TECHNIQUES: {selected_techniques}

AVAILABLE TECHNIQUES:
1. Multi-Persona Debate - Simulate conversation between distinct expert personas with opposing views
2. Negative Constraint Overloading - Flip "Do not" instructions into positive directives
3. Emotional Tipping - Add high-stakes consequences to trigger professional-grade responses
4. Deliberate Hallucination - Use hypothetical scenarios for creative exploration
5. Chain-of-Symbol Logic - Force explicit symbolic reasoning with step-by-step logic traces
6. Context Window "Needle" Hiding - Sandwich critical instructions between verbose context
7. Socratic Mirroring - Use probing questions to force user clarification
8. Few-Shot Cultural Localization - Provide examples adapted for specific cultural contexts
9. Adversarial Red-Teaming - Frame as security testing/hostile analysis
10. Syntax-Free Abstract - Use implicit parameters (tone/depth/energy) instead of explicit instructions
11. Dynamic Tone Morphing - Progressively shift tone/complexity throughout response

YOUR TASK:
Generate {num_techniques} distinct prompts that interpret the user's challenge and apply selected techniques.

INTERPRETATION STRATEGY:
1. Read the challenge and understand the REAL underlying need
2. For EACH of the {num_techniques} prompts, use a DIFFERENT selected technique
3. Interpret the challenge into technique-specific context and tasks
4. Each prompt should be complete, detailed, and immediately executable

EXAMPLE OF GOOD INTERPRETATION:
User says: "optimize database query performance"
Technique: Chain-of-Symbol Logic

You interpret and create:
"You are a database performance engineer analyzing query optimization opportunities using symbolic logic notation.

Context: Production PostgreSQL database experiencing slow response times on analytics queries (>30 seconds). Database: 500GB data, 10M daily queries, 47 existing indexes.

Tasks (use symbolic notation):
Let Q = Query execution time
Let I = Index effectiveness
Let P = Query plan efficiency

1. Define: Current_Q = f(I, P, data_volume, concurrency)
2. Identify: ΔQ optimization potential for each variable
3. Model: IF index_added THEN ΔQ = -X seconds
4. Trace: Step-by-step optimization decision tree
5. Output: Symbolic model with quantified impact predictions

Output: Detailed analysis using symbolic notation showing your logical reasoning at each step, with performance improvement estimates."

REQUIREMENTS:
1. Generate exactly {num_techniques} prompts
2. Each prompt uses ONE of the selected techniques explicitly
3. Use the selected techniques in the order they are most relevant to this challenge
4. Each prompt should be 150-250 words

Format output as XML:
<prompts>
<prompt number="1" technique="[Technique Name]" description="[How this technique helps this challenge]">
[Fully elaborated 150-250 word prompt applying this technique]
</prompt>
... continue for all {num_techniques} prompts
</prompts>

Ensure each prompt interprets the challenge and demonstrates the technique's unique methodology."""

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


def parse_prompts_output(response, expected_count):
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
            for num, content in numbered_matches[:expected_count]:
                chunks.append(content.strip())
        else:
            # Split by double newlines
            chunks = [c.strip() for c in response.split('\n\n') if len(c.strip()) > 50]

        # Create prompts from chunks
        for i, chunk in enumerate(chunks[:expected_count], 1):
            prompts.append({
                'number': i,
                'technique': 'Advanced Technique',
                'description': 'Generated specialized prompt',
                'prompt': chunk
            })

    return prompts[:expected_count]  # Return exactly the expected count


def render_advance_techs():
    """Render the Advanced Techniques Generator tool"""

    st.title("🚀 Advanced Techniques Generator")
    st.write("Generate specialized prompts using expert-level prompting techniques with comprehensive documentation")

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
            "ERP System Separation (Technical)": {
                "input": "Design SAP carve-out strategy for separating NewCo from parent's global ERP instance. 47 legal entities, 23 countries, 12-month timeline to standalone system.",
                "techniques": ["chain_of_symbol", "adversarial_redteam", "emotional_tipping"],
                "note": "Symbolic logic for dependencies + red-team for risks + high stakes framing"
            },
            "Working Capital Optimization (Financial)": {
                "input": "Optimize working capital structure for NewCo post-separation. Currently €150M tied up in parent cash pooling arrangements. Target: 30% reduction in NWC.",
                "techniques": ["multi_persona", "chain_of_symbol", "socratic_mirroring"],
                "note": "CFO/Treasury/Controller personas + quantitative analysis + clarifying questions"
            },
            "Shared Services Migration (Strategic)": {
                "input": "Transition from parent's shared services center to NewCo standalone or third-party provider. Scope: Finance, HR, IT, Procurement. 800 FTEs affected.",
                "techniques": ["multi_persona", "negative_constraint", "adversarial_redteam"],
                "note": "Stakeholder perspectives + positive constraints + failure mode analysis"
            },
            "Cross-Border Tax Structure (Complex)": {
                "input": "Design optimal post-separation tax structure for NewCo operating in 15 jurisdictions. Balance tax efficiency with transfer pricing compliance and operational complexity.",
                "techniques": ["deliberate_hallucination", "chain_of_symbol", "cultural_localization"],
                "note": "Scenario exploration + quantitative modeling + jurisdiction-specific considerations"
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
    st.caption("Select the techniques most relevant to your task. The system will generate one prompt for each selected technique.")

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
        st.info(f"ℹ️ {len(selected)} techniques selected. This will generate {len(selected)} prompts.")
    elif len(selected) >= 3:
        st.success(f"✅ {len(selected)} techniques selected")

    # Generate button
    num_techniques = len(selected)
    generate_btn = st.button(
        f"🚀 Generate {num_techniques} Prompts",
        disabled=(len(user_input.strip()) < 10 or num_techniques < 3),
        type="primary",
        use_container_width=True
    )

    st.caption("💡 Generation takes 10-15 seconds")

    # Generation logic
    if generate_btn and user_input.strip() and num_techniques >= 3:
        import time

        # Initialize results storage
        st.session_state.at_results = []

        # Create placeholders for progress and results
        progress_placeholder = st.empty()
        results_container = st.container()

        try:
            # Generate prompts sequentially, one per technique
            for i, (tech_key, tech_name) in enumerate(zip(selected_keys, selected)):
                tech_info = TECHNIQUES[tech_key]

                # Show progress
                with progress_placeholder.container():
                    st.info(f"⚡ Generating prompt {i+1}/{num_techniques}: {tech_info['icon']} **{tech_info['name']}**...")

                # Build system prompt for single technique
                single_system_prompt = f"""You are an expert prompt engineer specializing in advanced prompting techniques.

CRITICAL INTERPRETATION RULES:
1. DO NOT quote the user's challenge literally in the generated prompt
2. INTERPRET their high-level challenge into specific, detailed instructions
3. The prompt must be COMPLETE and EXECUTABLE on its own
4. Include: role/context, background information, specific tasks (3-5), output format
5. The prompt should be 150-250 words with clear structure
6. Use professional, enterprise-grade language

USER'S CHALLENGE (interpret and elaborate this, do not quote):
"{user_input}"

TECHNIQUE TO APPLY: {tech_name}

TECHNIQUE DETAILS:
{tech_info['definition']}

Mechanism: {tech_info['mechanism']}

YOUR TASK:
Create ONE detailed prompt that interprets the user's challenge and applies the {tech_name} technique. The prompt should be complete, detailed, and immediately executable. Demonstrate the technique's unique methodology clearly."""

                # Build user message
                user_message = f"""Challenge: {user_input}

Technique: {tech_name}

Generate a single 150-250 word prompt that interprets this challenge and applies the {tech_name} technique. The prompt should clearly demonstrate how this technique's methodology applies to this specific challenge."""

                # Call API
                try:
                    response = call_anthropic(
                        system_prompt=single_system_prompt,
                        user_message=user_message,
                        max_tokens=800
                    )

                    # Store result
                    prompt_data = {
                        'number': i + 1,
                        'technique': tech_name,
                        'description': f"Applies {tech_info['name']} to your challenge",
                        'prompt': response.strip(),
                        'icon': tech_info['icon']
                    }
                    st.session_state.at_results.append(prompt_data)

                    # Display result immediately
                    with results_container:
                        st.markdown(f"### {prompt_data['icon']} Prompt {prompt_data['number']}: {prompt_data['technique']}")
                        st.caption(prompt_data['description'])
                        st.code(prompt_data['prompt'], language=None)
                        st.markdown("")

                except Exception as e:
                    st.error(f"❌ Failed to generate prompt for {tech_info['name']}: {str(e)}")
                    continue

                # Delay before next call (except last)
                if i < len(selected_keys) - 1:
                    time.sleep(1)

            # Clear progress indicator
            progress_placeholder.empty()
            progress_placeholder.success(f"✅ Successfully generated {len(st.session_state.at_results)} prompts!")

        except Exception as e:
            st.error(f"Error generating prompts: {str(e)}")

    # Display results (if not currently generating)
    if 'at_results' in st.session_state and st.session_state.at_results and not generate_btn:
        st.markdown("---")
        st.subheader("📋 Generated Prompts")
        st.info("**How to use:** Each prompt applies a different advanced technique to your goal. Copy and use any prompt that fits your needs.")

        for prompt_data in st.session_state.at_results:
            # Get icon from data or find matching icon
            icon = prompt_data.get('icon', '⚡')
            if icon == '⚡':
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
            4. **Generate prompts** - Get one specialized prompt for each selected technique
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
