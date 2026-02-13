import streamlit as st
import re
import json
import random
import time
from backend.api_client import call_anthropic

# System prompt for Image Prompt generation (updated for multi-style)
IMAGE_PROMPT_SYSTEM = """You are an expert in art history, visual aesthetics, and AI image generation prompting.

CRITICAL INTERPRETATION RULES:
1. DO NOT simply repeat the user's subject description
2. INTERPRET the visual intent and ELABORATE with artistic details
3. Add specific details: composition, lighting, mood, textures, atmosphere
4. Integrate style characteristics naturally
5. Create a vivid, concrete visual description
6. Optimize for AI image generator parsing

SELECTED CATEGORY: {category}
SELECTED SUBCATEGORY: {subcategory}
USER'S SUBJECT (interpret and elaborate this, do not quote): {subject}
THEMATIC ELEMENTS: {thematic_elements}

CATEGORY CONTEXT:
{subcategory_data}

YOUR TASK:
Interpret the user's subject and create an optimized image generation prompt by:

1. INTERPRETING the visual intent behind the subject
2. ELABORATING with specific artistic details:
   - Composition choices (foreground/background, framing, perspective)
   - Lighting characteristics (time of day, light quality, shadows)
   - Mood and atmosphere
   - Material textures and finishes
   - Color palette specifics
3. INTEGRATING style characteristics from the subcategory
4. APPLYING thematic element variations naturally
5. REFERENCING 1-2 relevant artists from the subcategory

INTERPRETATION STRATEGY:
- Generic subject → Add specific visual details
- "vintage car" → Interpret as: specific era, condition, setting, lighting mood
- "professional portrait" → Interpret as: attire specifics, background, lighting style, expression
- "business concept" → Interpret into concrete visual metaphors

CATEGORY-SPECIFIC GUIDANCE:

For "Information Architecture & Data Viz":
- Focus on clarity, hierarchy, and information structure
- Include specific layout elements (grids, nodes, connectors, callouts)
- Mention aspect ratio recommendations (16:9 for workflows, square for infographics)
- Specify label density and text placement
- Include technical elements (arrows, decision points, data callouts)
- Balance information density with scanability

EXAMPLE OF GOOD INTERPRETATION:
User says: "vintage car in desert"

You interpret and elaborate:
"Weathered 1967 Mustang fastback, faded red paint with rust patina, parked on cracked desert highway at golden hour. Long shadows across wind-swept sand dunes, distant Arizona mesas. Warm amber and terracotta color palette, cinematic composition. Nostalgic Americana aesthetic, fine art photography style."

REQUIREMENTS:
1. Create a 30-50 word, comma-separated prompt
2. Start with the interpreted/elaborated subject
3. Include specific visual details (not generic descriptions)
4. Reference subcategory aesthetics and artists
5. Weave in thematic elements naturally
6. Optimize for AI parsing (descriptive, concrete language)

Format output as XML:
<text_prompt>
[Fully elaborated 30-50 word prompt with specific artistic details, comma-separated]
</text_prompt>

Ensure the prompt interprets and elaborates on the subject with vivid visual details."""

# Taxonomy structure - 7 categories with subcategories
TAXONOMY = {
    "Fine Art Movements": {
        "icon": "🎨",
        "subcategories": [
            "Classical & Academic",
            "Impressionism & Post-Impressionism",
            "Modernism & Abstraction",
            "Surrealism & Symbolism",
            "Expressionism & Fauvism",
            "Art Nouveau & Deco"
        ]
    },
    "Photography Styles": {
        "icon": "📸",
        "subcategories": [
            "Documentary & Photojournalism",
            "Portrait & Fashion",
            "Landscape & Nature",
            "Architectural & Urban",
            "Still Life & Product",
            "Abstract & Experimental"
        ]
    },
    "Digital Art Genres": {
        "icon": "💻",
        "subcategories": [
            "Concept Art & Matte Painting",
            "Character Design & Illustration",
            "Pixel Art & Voxel",
            "3D Rendering & CGI",
            "Vector & Flat Design"
        ]
    },
    "Fantasy & Sci-Fi": {
        "icon": "🚀",
        "subcategories": [
            "High Fantasy & Tolkienesque",
            "Cyberpunk & Neon Aesthetics",
            "Space Opera & Cosmic",
            "Steampunk & Dieselpunk",
            "Solarpunk & Eco-Futurism",
            "Horror & Dark Fantasy"
        ]
    },
    "Cultural & Historical": {
        "icon": "🏛️",
        "subcategories": [
            "Ancient Civilizations",
            "Medieval & Renaissance",
            "Asian Art Traditions",
            "Indigenous & Tribal",
            "Art Deco & Mid-Century",
            "Contemporary Urban"
        ]
    },
    "Animation & Comics": {
        "icon": "🎬",
        "subcategories": [
            "Anime & Manga",
            "Western Comics",
            "Cartoon & Children's Book",
            "Stop Motion & Claymation"
        ]
    },
    "Emerging Styles": {
        "icon": "✨",
        "subcategories": [
            "Vaporwave & Retrowave",
            "Glitch Art & Digital Decay",
            "Bio Art & Organic Tech",
            "Maximalism & Baroque Revival"
        ]
    },
    "Information Architecture & Data Viz": {
        "icon": "📊",
        "description": "Visualizing complex data, workflows, and textual summaries through structured design",
        "subcategories": [
            "Infographic & Data Storytelling",
            "Whiteboard & Visual Synthesis",
            "Workflow & Logic Flowcharts",
            "Technical Cheat Sheet"
        ]
    }
}

# Thematic elements that apply across all categories
THEMATIC_ELEMENTS = {
    "Light & Atmosphere": {
        "icon": "☀️",
        "description": "Illumination, weather, and atmospheric conditions"
    },
    "Scale & Perspective": {
        "icon": "🔭",
        "description": "Subject size, viewer position, spatial hierarchy"
    },
    "Temporal Quality": {
        "icon": "⏳",
        "description": "Time relation - frozen moment, decay, progression"
    },
    "Color Psychology": {
        "icon": "🎨",
        "description": "Palette selection driving emotional meaning"
    },
    "Compositional Tension": {
        "icon": "⚖️",
        "description": "Balance, asymmetry, visual weight distribution"
    },
    "Material & Texture": {
        "icon": "🧱",
        "description": "Surface qualities and tactile dimension"
    },
    "Narrative Density": {
        "icon": "📖",
        "description": "Amount of storytelling information in frame"
    }
}

# Detailed subcategory data for LLM context
SUBCATEGORY_DETAILS = {
    "Classical & Academic": {
        "themes": "Idealized beauty, mythological narratives, technical mastery",
        "styles": "Precise draftsmanship, balanced composition, naturalistic rendering",
        "artists": "Caravaggio, Rembrandt, Vermeer, Bouguereau",
        "aesthetics": "Chiaroscuro lighting, sfumato blending, golden ratio composition"
    },
    "Cyberpunk & Neon Aesthetics": {
        "themes": "Tech dystopia, corporate dominance, human-machine fusion, urban decay",
        "styles": "High contrast, neon color palettes, reflective wet surfaces, dense cityscapes",
        "artists": "Syd Mead, Simon Stålenhag, Beeple, Maciej Kuciara",
        "aesthetics": "Neon lighting, rain-slicked streets, holographic displays, industrial grit"
    },
    "Impressionism & Post-Impressionism": {
        "themes": "Light perception, fleeting moments, emotional color",
        "styles": "Visible brushstrokes, pure color application, outdoor scenes",
        "artists": "Monet, Renoir, Van Gogh, Cézanne",
        "aesthetics": "Dappled light, vibrant palettes, atmospheric effects"
    },
    "Anime & Manga": {
        "themes": "Expressive emotions, dynamic action, fantastical elements",
        "styles": "Large eyes, stylized hair, speed lines, dramatic angles",
        "artists": "Hayao Miyazaki, Makoto Shinkai, CLAMP, Akira Toriyama",
        "aesthetics": "Cel-shaded look, dramatic lighting, detailed backgrounds"
    },
    "Concept Art & Matte Painting": {
        "themes": "World-building, cinematic environments, narrative spaces",
        "styles": "Atmospheric perspective, detailed foregrounds, expansive vistas",
        "artists": "Ralph McQuarrie, Craig Mullins, Feng Zhu, Sparth",
        "aesthetics": "Cinematic composition, dramatic lighting, epic scale"
    },
    "Portrait & Fashion": {
        "themes": "Human character, style expression, cultural identity",
        "styles": "Sharp focus on subject, controlled lighting, minimal backgrounds",
        "artists": "Annie Leibovitz, Richard Avedon, Irving Penn, Mario Testino",
        "aesthetics": "Dramatic lighting, shallow depth of field, bold fashion statements"
    },
    "3D Rendering & CGI": {
        "themes": "Photorealism, technical precision, digital craftsmanship",
        "styles": "Ray tracing, subsurface scattering, physically-based rendering",
        "artists": "Ian Hubert, Beeple, Peter Tarka, Ash Thorp",
        "aesthetics": "Hyperrealistic materials, perfect lighting, clean geometry"
    },
    "Landscape & Nature": {
        "themes": "Natural beauty, environmental storytelling, seasonal moods",
        "styles": "Wide vistas, foreground-background layering, natural light",
        "artists": "Ansel Adams, Sebastião Salgado, Art Wolfe, Galen Rowell",
        "aesthetics": "Golden hour lighting, atmospheric depth, dramatic skies"
    },
    "Infographic & Data Storytelling": {
        "themes": "Hierarchy, clarity, data-driven, scannable layout, visual data storytelling",
        "styles": "Bento box grid, modular callouts, flat vector icons, high-contrast typography, color-coded sections",
        "subjects": "Statistical overviews, historical timelines, comparison charts, how-to guides, annual reports, market analysis",
        "artists": "Edward Tufte, Otl Aicher, Gerd Arntz, David McCandless",
        "aesthetics": "Clean margins, quantitative color coding, legend/key inclusion, sans-serif dominance, data hierarchy"
    },
    "Whiteboard & Visual Synthesis": {
        "themes": "Collaborative, spontaneous, brain-dump, conceptual mapping, visual thinking",
        "styles": "Hand-drawn marker strokes, felt-tip pen texture, Post-it note clusters, rough sketches, organic flow",
        "subjects": "Meeting summaries, ideation sessions, mind maps, concept deconstruction, workshop outputs, strategy sessions",
        "artists": "Dan Roam, Sunni Brown, David Sibbet",
        "aesthetics": "Ink bleeds, whiteboard sheen, varied line weights, scribble connectors, highlighter accents, spontaneous annotations"
    },
    "Workflow & Logic Flowcharts": {
        "themes": "Sequential logic, decision trees, process optimization, structural clarity, systematic thinking",
        "styles": "Node-and-edge diagrams, standard BPMN symbols, directional arrows, swimlane layouts, structured hierarchies",
        "subjects": "Software logic, business operations, user journeys, biological processes, organizational workflows, decision frameworks",
        "artists": "ISO standard aesthetics, Lombardy layout, engineering blueprints, technical documentation standards",
        "aesthetics": "Connecting lines with arrowheads, decision diamonds, terminal capsules, geometric consistency, clear entry/exit points"
    },
    "Technical Cheat Sheet": {
        "themes": "Information density, reference utility, exploded views, comprehensive labeling, quick reference",
        "styles": "Swiss International Style, technical illustration, blueprint drafting, grid-heavy layouts, modular organization",
        "subjects": "Programming syntax, mechanical assemblies, keyboard shortcuts, field guides, command references, specification sheets",
        "artists": "Josef Müller-Brockmann, Wim Crouwel, Massimo Vignelli, Swiss design school",
        "aesthetics": "Fine-line technical drawing, numbered callouts, high-density text blocks, micro-grids, systematic typography"
    }
}


def interpret_info_architecture_subject(subject, subcategory):
    """
    Intelligently expand generic subjects into structured descriptions
    for Information Architecture & Data Viz category.

    Args:
        subject: User's input subject
        subcategory: Selected subcategory

    Returns:
        Expanded, structured subject description
    """
    subject_lower = subject.lower()

    # Keyword detection patterns
    flowchart_keywords = ['flow', 'process', 'workflow', 'procedure', 'sequence', 'pipeline']
    infographic_keywords = ['data', 'summary', 'report', 'statistics', 'analysis', 'comparison', 'versus', 'vs']
    whiteboard_keywords = ['whiteboard', 'brainstorm', 'meeting', 'workshop', 'ideation', 'planning']
    cheatsheet_keywords = ['cheat sheet', 'reference', 'guide', 'commands', 'syntax', 'shortcuts']
    timeline_keywords = ['timeline', 'roadmap', 'schedule', 'phases', 'milestones']
    funnel_keywords = ['funnel', 'conversion', 'journey', 'pipeline']

    # Check for keyword matches
    is_flowchart = any(kw in subject_lower for kw in flowchart_keywords)
    is_infographic = any(kw in subject_lower for kw in infographic_keywords)
    is_whiteboard = any(kw in subject_lower for kw in whiteboard_keywords)
    is_cheatsheet = any(kw in subject_lower for kw in cheatsheet_keywords)
    is_timeline = any(kw in subject_lower for kw in timeline_keywords)
    is_funnel = any(kw in subject_lower for kw in funnel_keywords)

    # Subcategory-specific expansions
    if subcategory == "Workflow & Logic Flowcharts":
        if is_flowchart or is_timeline:
            return f"A comprehensive {subject} diagram showing sequential logic, featuring interconnected nodes, decision paths, and directional flow within a structured hierarchy. Clear entry and exit points with labeled transitions."
        elif is_funnel:
            return f"A {subject} visualization with distinct stages arranged vertically, showing progression and conversion metrics at each level with connecting flow indicators."
        else:
            return f"A logical process map for {subject} with geometric nodes connected by directional arrows, decision diamonds for branching logic, and terminal capsules for endpoints."

    elif subcategory == "Infographic & Data Storytelling":
        if is_infographic or is_timeline:
            return f"A visual synthesis of {subject} structured as an information-rich layout with hierarchical headers, illustrative icons, data callouts, and clean typographic organization. Modular grid with color-coded sections."
        elif 'comparison' in subject_lower or 'vs' in subject_lower or 'versus' in subject_lower:
            return f"A comparative visualization of {subject} using side-by-side layouts, contrasting data points, and clear visual differentiation between compared elements."
        else:
            return f"An infographic representation of {subject} with scannable data hierarchy, flat vector icons, bold numerical headers, and distinct thematic blocks flowing from top to bottom."

    elif subcategory == "Whiteboard & Visual Synthesis":
        if is_whiteboard:
            return f"A collaborative whiteboard canvas capturing {subject} with rough sketches, hand-drawn diagrams, colorful sticky note clusters, marker-drawn arrows, and circled key concepts. Spontaneous visual thinking style."
        else:
            return f"A visual brainstorming session output for {subject} featuring organic marker strokes, conceptual connections, rough annotations, and mind-map style organization with varied line weights."

    elif subcategory == "Technical Cheat Sheet":
        if is_cheatsheet:
            return f"A high-density reference guide for {subject} with multi-column grid layout, labeled diagrams, condensed typography, numbered callouts, and icon-based shortcuts for quick scanning."
        else:
            return f"A comprehensive technical reference for {subject} organized in systematic grid structure with exploded view diagrams, fine-line illustrations, and dense informational blocks with precise labeling."

    # Default expansion if no keywords match
    return f"A structured visual representation of {subject} optimized for information clarity and professional presentation."


def render_image_prompt():
    """Render the AI Image Prompt Generator tool - Multi-Style Variation Feature"""

    st.title("🎨 AI Image Prompt Generator")
    st.write("Generate multiple style variations for the same subject")

    # Info expander
    with st.expander("ℹ️ How to Use This Tool"):
        st.markdown("""
        **New Multi-Style Feature:**

        1. **Enter your subject** (e.g., "vintage 1970s muscle car")
        2. **Select 1-5 art styles** from any category
        3. **Optionally add 1-2 thematic elements** (applied to all variations)
        4. **Generate variations** - get one optimized prompt per style

        **Use Cases:**
        - Explore how the same subject looks across different art movements
        - Generate variety for creative projects
        - A/B test different styles before committing to one
        - Build a style library for consistent brand imagery

        **Output:** Each variation is a 30-50 word text prompt ready to use in DALL-E, Midjourney, or Stable Diffusion.
        """)

    # Examples section
    with st.expander("💡 Try These Examples", expanded=False):
        st.markdown("Click any example to auto-fill:")

        examples = {
            "📊 Executive M&A Strategy Board Deck": {
                "subject": "Three-year post-merger integration roadmap showing Phase 1 systems consolidation (months 1-12), Phase 2 organizational restructuring (months 13-24), and Phase 3 synergy realization (months 25-36). Include milestones for IT cutover, headcount optimization, and EBITDA improvement targets with decision gates at each phase transition.",
                "styles": [
                    ("Information Architecture & Data Viz", "Infographic & Data Storytelling")
                ],
                "themes": ["Compositional Tension", "Temporal Quality"],
                "description": "Detailed timeline infographic for executive presentation"
            },
            "📊 Post-Acquisition Org Chart": {
                "subject": "Corporate organizational structure post-acquisition showing dual reporting lines between functional teams (Finance, HR, IT, Operations) and business unit leaders. Highlight matrix reporting relationships, shared service dependencies, and governance bodies (Steering Committee, Integration PMO). Show 3 organizational layers: C-suite, functional leaders, and business unit heads.",
                "styles": [
                    ("Information Architecture & Data Viz", "Workflow & Logic Flowcharts")
                ],
                "themes": ["Compositional Tension"],
                "description": "Hierarchical org structure with matrix relationships"
            },
            "📊 Enterprise Procurement Process": {
                "subject": "End-to-end procurement workflow from requisition to payment. Show decision points for approval thresholds ($10K, $50K, $250K), parallel paths for goods vs services, integration touchpoints with ERP and finance systems, and exception handling for rush orders. Include 12 process steps with role assignments (Requestor, Manager, Procurement, Finance, Vendor).",
                "styles": [
                    ("Information Architecture & Data Viz", "Workflow & Logic Flowcharts")
                ],
                "themes": ["Compositional Tension", "Material & Texture"],
                "description": "Detailed process flowchart with decision logic"
            },
            "📊 Q4 Financial Performance Summary": {
                "subject": "Quarterly business review dashboard showing revenue by segment (North America 45%, EMEA 30%, APAC 25%), gross margin trend over 4 quarters (improving from 38% to 42%), top 10 customers by revenue contribution, and variance analysis against plan (Revenue +8%, EBITDA +12%, headcount -3%). Include YoY comparison callouts and forecast indicators for Q1.",
                "styles": [
                    ("Information Architecture & Data Viz", "Infographic & Data Storytelling")
                ],
                "themes": ["Color Psychology", "Compositional Tension"],
                "description": "Data-rich performance infographic with metrics"
            },
            "📊 Product Strategy Workshop Canvas": {
                "subject": "Strategic planning whiteboard output showing product vision 2025-2027, competitive positioning matrix (price vs features) with 8 competitors plotted, SWOT analysis with 5 items per quadrant, prioritized initiative backlog using 2x2 matrix (impact vs effort), and resource allocation across 4 product lines. Include Post-it clusters for customer feedback themes and hand-drawn arrows showing strategic dependencies.",
                "styles": [
                    ("Information Architecture & Data Viz", "Whiteboard & Visual Synthesis")
                ],
                "themes": ["Narrative Density", "Compositional Tension"],
                "description": "Collaborative strategy session visual output"
            },
            "🛒 Dashboard Operativo de Tiendas": {
                "subject": "Panel de control mensual mostrando rendimiento de 18 supermercados Alimerka: ventas por categoría (pescadería, panadería, frescos), margen bruto por tienda, comparativa vs. objetivo, indicadores de merma y rotación de stock. Incluir gráficos de barras para ranking de tiendas y mapa de Asturias con iconos por ubicación.",
                "styles": [
                    ("Information Architecture & Data Viz", "Infographic & Data Storytelling")
                ],
                "themes": ["Color Psychology", "Compositional Tension"],
                "description": "Operational KPI infographic with quantitative data"
            },
            "🛒 Flujo de Reparto a Domicilio": {
                "subject": "Diagrama de flujo del proceso de entrega a domicilio mostrando 8 pasos desde recepción de pedido online hasta entrega en casa del cliente. Incluir puntos de decisión para validación de stock, asignación de ruta, ventanas de entrega y gestión de incidencias. Mostrar touchpoints con sistemas IT (app, ERP, GPS) y roles responsables (almacén, repartidor, atención cliente).",
                "styles": [
                    ("Information Architecture & Data Viz", "Workflow & Logic Flowcharts")
                ],
                "themes": ["Compositional Tension", "Material & Texture"],
                "description": "Operational flowchart with department swimlanes"
            },
            "🛒 Análisis de Contribución por Categoría": {
                "subject": "Matriz de análisis de portfolio de productos mostrando 12 categorías (frescos, panadería, bebidas, limpieza, etc.) posicionadas según dos ejes: margen bruto (eje Y) vs. volumen de ventas (eje X). Incluir burbujas proporcionales a la contribución total, códigos de color por familia de producto, y anotaciones para categorías estratégicas y oportunidades de mejora.",
                "styles": [
                    ("Information Architecture & Data Viz", "Infographic & Data Storytelling")
                ],
                "themes": ["Color Psychology", "Compositional Tension", "Scale & Perspective"],
                "description": "Strategic consulting-style scatter plot matrix"
            },
            "🛒 Mapa de Expansión Regional": {
                "subject": "Mapa de Asturias mostrando 18 tiendas Alimerka actuales (iconos verdes) y 4 ubicaciones potenciales evaluadas para expansión (iconos naranjas con scoring). Incluir zonas de influencia por radio de 5km, datos demográficos por área (población, renta media), indicadores de competencia (Mercadona, Carrefour, DIA) y análisis de tráfico peatonal. Leyenda con criterios de selección de ubicación.",
                "styles": [
                    ("Information Architecture & Data Viz", "Infographic & Data Storytelling")
                ],
                "themes": ["Scale & Perspective", "Color Psychology"],
                "description": "Geomarketing with multi-criteria analysis"
            },
            "🛒 Workshop de Estrategia Comercial": {
                "subject": "Output de sesión de planificación whiteboard mostrando análisis DAFO con 5 items por cuadrante (fortalezas: proximidad local, productos frescos; debilidades: escala menor vs. nacionales; oportunidades: comercio electrónico, productos locales; amenazas: guerra de precios, grandes superficies). Incluir matriz de priorización impacto-esfuerzo con 8 iniciativas estratégicas, clusters de Post-its por temática (operaciones, marketing, digital) y flechas dibujadas conectando dependencias entre proyectos.",
                "styles": [
                    ("Information Architecture & Data Viz", "Whiteboard & Visual Synthesis")
                ],
                "themes": ["Narrative Density", "Compositional Tension"],
                "description": "Collaborative strategy workshop visualization"
            }
        }

        cols = st.columns(3)
        for idx, (example_name, example_data) in enumerate(examples.items()):
            with cols[idx % 3]:
                if st.button(
                    f"📋 {example_name}",
                    key=f"ip_ex_{idx}",
                    use_container_width=True,
                    help=example_data['description']
                ):
                    # Clear all checkboxes first
                    for cat_name, cat_data in TAXONOMY.items():
                        for subcategory in cat_data['subcategories']:
                            checkbox_key = f"ip_subcat_{cat_name}_{subcategory}"
                            st.session_state[checkbox_key] = False

                    for theme_name in THEMATIC_ELEMENTS.keys():
                        st.session_state[f"theme_{theme_name}"] = False

                    # Set subject
                    st.session_state.ip_subject = example_data['subject']

                    # Set styles
                    for cat, subcat in example_data['styles']:
                        checkbox_key = f"ip_subcat_{cat}_{subcat}"
                        st.session_state[checkbox_key] = True

                    # Set themes
                    for theme in example_data['themes']:
                        st.session_state[f"theme_{theme}"] = True

                    st.rerun()

    st.markdown("---")

    # STEP 1: Subject Input (MOVED TO TOP)
    st.markdown("### Step 1: Enter Your Subject")
    subject = st.text_area(
        "Describe what you want to generate",
        height=100,
        placeholder="Examples:\n- vintage 1970s muscle car in desert\n- medieval knight in ornate armor\n- cozy coffee shop interior\n- abstract representation of music",
        key="ip_subject",
        help="Tip: Be specific but concise - describe the core elements"
    )

    # STEP 2: Style Selection (NEW - Multiple subcategories)
    st.markdown("### Step 2: Select 1-5 Art Styles")
    st.caption("Choose subcategories from any category. Each will generate a unique prompt for your subject.")

    selected_subcategories = []

    # Organize by category with checkboxes
    for cat_name, cat_data in TAXONOMY.items():
        with st.expander(f"{cat_data['icon']} {cat_name}", expanded=False):
            cols = st.columns(2)
            for idx, subcategory in enumerate(cat_data['subcategories']):
                with cols[idx % 2]:
                    # Create unique key for checkbox
                    checkbox_key = f"ip_subcat_{cat_name}_{subcategory}"

                    is_selected = st.checkbox(
                        subcategory,
                        key=checkbox_key,
                        help=f"Generate variation in {subcategory} style"
                    )

                    if is_selected:
                        selected_subcategories.append({
                            'category': cat_name,
                            'subcategory': subcategory,
                            'icon': cat_data['icon']
                        })

    # Validation message
    num_selected = len(selected_subcategories)
    if num_selected == 0:
        pass  # No message when nothing selected
    elif 1 <= num_selected <= 5:
        st.success(f"✅ {num_selected} style{'s' if num_selected > 1 else ''} selected")
    elif num_selected > 5:
        st.warning(f"⚠️ {num_selected} styles selected. Maximum 5 styles recommended for best results.")

    # Show selected styles summary
    if selected_subcategories:
        st.markdown("**Selected Styles:**")
        selected_text = ", ".join([f"{s['icon']} {s['subcategory']}" for s in selected_subcategories])
        st.info(selected_text)

    # STEP 3: Thematic Elements (OPTIONAL - applied to all)
    st.markdown("### Step 3: Add Thematic Elements (Optional)")
    st.caption("These will be applied to ALL selected styles. Maximum 2 recommended.")

    selected_themes = []
    theme_cols = st.columns(4)

    for idx, (theme_name, theme_data) in enumerate(THEMATIC_ELEMENTS.items()):
        with theme_cols[idx % 4]:
            if st.checkbox(
                f"{theme_data['icon']} {theme_name}",
                key=f"theme_{theme_name}",
                help=theme_data['description']
            ):
                selected_themes.append(theme_name)

    if len(selected_themes) > 2:
        st.warning("⚠️ More than 2 thematic elements may create overly complex prompts")

    # Generate button
    st.markdown("---")

    can_generate = (
        len(subject.strip()) >= 5 and
        1 <= len(selected_subcategories) <= 5
    )

    # Build button text with singular/plural handling
    num_styles = len(selected_subcategories)
    if num_styles == 0:
        button_text = "✨ Generate Variations"
    elif num_styles == 1:
        button_text = "✨ Generate 1 Style Variation"
    else:
        button_text = f"✨ Generate {num_styles} Style Variations"

    generate_btn = st.button(
        button_text,
        disabled=not can_generate,
        type="primary",
        use_container_width=True
    )

    if not can_generate and (subject.strip() or selected_subcategories):
        if len(subject.strip()) < 5:
            st.caption("⚠️ Please enter a subject (at least 5 characters)")
        elif len(selected_subcategories) < 1:
            st.caption("⚠️ Please select at least 1 art style")
        elif len(selected_subcategories) > 5:
            st.caption("⚠️ Please select at most 5 styles for best results")

    # Generation logic
    if generate_btn and can_generate:
        with st.spinner(f"Generating {len(selected_subcategories)} style variations..."):
            st.session_state.ip_variations = []
            st.session_state.ip_subject_display = subject

            progress_container = st.container()

            for idx, style in enumerate(selected_subcategories, 1):
                try:
                    # Progress indicator
                    with progress_container:
                        st.caption(f"⚡ Generating variation {idx}/{len(selected_subcategories)}: {style['icon']} **{style['subcategory']}**")

                    # Get subcategory details
                    subcat_data = SUBCATEGORY_DETAILS.get(
                        style['subcategory'],
                        {
                            "themes": "Visual storytelling and aesthetic exploration",
                            "styles": "Characteristic visual approach",
                            "artists": "Representative creators in this style",
                            "aesthetics": "Key visual qualities"
                        }
                    )

                    # Format subcategory context
                    subcat_context = f"""Themes: {subcat_data['themes']}
Styles: {subcat_data['styles']}
Reference Artists: {subcat_data['artists']}
Aesthetic Qualities: {subcat_data['aesthetics']}"""

                    # Apply intelligent subject interpretation for Information Architecture category
                    if style['category'] == "Information Architecture & Data Viz":
                        interpreted_subject = interpret_info_architecture_subject(subject, style['subcategory'])
                    else:
                        # Use subject as-is for artistic categories
                        interpreted_subject = subject

                    # Build system prompt
                    system_prompt = IMAGE_PROMPT_SYSTEM.format(
                        category=style['category'],
                        subcategory=style['subcategory'],
                        subject=interpreted_subject,
                        thematic_elements=", ".join(selected_themes) if selected_themes else "None",
                        subcategory_data=subcat_context
                    )

                    # Build user message
                    user_message = f"""Category: {style['category']}
Subcategory: {style['subcategory']}
Subject: {subject}
Thematic Elements: {", ".join(selected_themes) if selected_themes else "None"}

Generate a text prompt optimized for AI image generation."""

                    # Call API
                    response = call_anthropic(
                        system_prompt=system_prompt,
                        user_message=user_message,
                        max_tokens=800
                    )

                    # Parse response (text only)
                    text_match = re.search(r'<text_prompt>(.*?)</text_prompt>', response, re.DOTALL)
                    text_prompt = text_match.group(1).strip() if text_match else response[:200]

                    # Store variation
                    st.session_state.ip_variations.append({
                        'category': style['category'],
                        'subcategory': style['subcategory'],
                        'icon': style['icon'],
                        'prompt': text_prompt
                    })

                    # Small delay to avoid rate limiting (already included in api_client)
                    # Additional delay if needed
                    if idx < len(selected_subcategories):
                        time.sleep(0.5)

                except Exception as e:
                    st.error(f"Error generating {style['subcategory']}: {str(e)}")

            progress_container.empty()
            st.success(f"✅ Generated {len(st.session_state.ip_variations)} variations!")

    # Display results
    if 'ip_variations' in st.session_state and st.session_state.ip_variations:
        st.markdown("---")

        subject_display = st.session_state.get('ip_subject_display', 'your subject')
        st.markdown(f"## 🎨 Generated Variations")
        st.markdown(f"**Subject:** \"{subject_display}\"")

        st.info(f"**{len(st.session_state.ip_variations)} style variations** • Copy any prompt to use in DALL-E, Midjourney, Stable Diffusion, or other AI image generators")

        # Display each variation
        for idx, variation in enumerate(st.session_state.ip_variations, 1):
            st.markdown(f"### {variation['icon']} Variation {idx}: {variation['subcategory']}")
            st.caption(f"Category: {variation['category']}")

            # Prompt in copyable code block
            st.code(variation['prompt'], language=None)

            if idx < len(st.session_state.ip_variations):
                st.markdown("---")

        # Action buttons
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Generate Different Styles", use_container_width=True):
                # Clear results to start fresh
                if 'ip_variations' in st.session_state:
                    del st.session_state.ip_variations
                if 'ip_subject_display' in st.session_state:
                    del st.session_state.ip_subject_display
                st.rerun()

        with col2:
            # Export all prompts as text file
            all_prompts_text = f"Subject: {subject_display}\n\n"
            all_prompts_text += "=" * 60 + "\n\n"

            for idx, v in enumerate(st.session_state.ip_variations, 1):
                all_prompts_text += f"VARIATION {idx}: {v['subcategory']}\n"
                all_prompts_text += f"Category: {v['category']}\n\n"
                all_prompts_text += f"{v['prompt']}\n\n"
                all_prompts_text += "=" * 60 + "\n\n"

            # Clean filename
            filename_subject = "".join(c for c in subject_display if c.isalnum() or c in (' ', '-', '_'))[:30]
            filename = f"image_prompts_{filename_subject}.txt"

            st.download_button(
                "💾 Download All Prompts",
                data=all_prompts_text,
                file_name=filename,
                mime="text/plain",
                use_container_width=True
            )

    elif not generate_btn:
        # Empty state - show guidance
        st.markdown("---")
        st.info("""
        ### 🌟 Quick Start

        1. **Enter your subject** - What do you want to see? (e.g., "vintage car", "fantasy castle")
        2. **Select 1-5 art styles** - Browse categories below and check styles you're interested in
        3. **Optionally add 1-2 themes** - Modify lighting, mood, or composition across all variations
        4. **Generate** - Get one optimized prompt per style in ~10 seconds per variation

        ### 💡 Pro Tips

        - **Mix categories**: Combine Photography + Fine Art + Digital for diverse results
        - **Keep subject consistent**: The same subject across styles shows artistic range
        - **Limit themes**: 1-2 themes keep prompts focused and effective
        - **Download all**: Use the download button to save your entire prompt library
        """)

        # Show category overview
        st.markdown("### 📚 Available Art Styles")
        st.caption(f"Total: {sum(len(cat['subcategories']) for cat in TAXONOMY.values())} subcategories across 7 categories")

        overview_cols = st.columns(4)
        for idx, (cat_name, cat_data) in enumerate(TAXONOMY.items()):
            with overview_cols[idx % 4]:
                st.markdown(f"**{cat_data['icon']} {cat_name}**")
                st.caption(f"{len(cat_data['subcategories'])} styles")
