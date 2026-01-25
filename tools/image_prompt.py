import streamlit as st
import re
import json
import random
from backend.api_client import call_anthropic

# System prompt for Image Prompt generation
IMAGE_PROMPT_SYSTEM = """You are an expert in art history, visual aesthetics, and AI image generation prompting.

Your task: Generate TWO outputs for AI image generation:
1. A text prompt (optimized for tools like DALL-E, Midjourney, Stable Diffusion)
2. A structured JSON object with detailed metadata

SELECTED CATEGORY: {category}
SELECTED SUBCATEGORY: {subcategory}
SUBJECT: {subject}
THEMATIC ELEMENTS: {thematic_elements}

CATEGORY CONTEXT:
{subcategory_data}

REQUIREMENTS FOR TEXT PROMPT:
1. Start with the subject
2. Include 2-3 style descriptors from the subcategory
3. Reference 1-2 artists from the subcategory
4. If thematic elements selected, weave in their variations naturally
5. Include aesthetic qualities from subcategory
6. Keep prompt 30-50 words, comma-separated
7. Optimize for AI image generator parsing

REQUIREMENTS FOR JSON:
1. Generate unique ID
2. Include all selected categories and elements
3. Extract 4-6 key visual elements from subject
4. Define mood (2-3 adjectives)
5. Suggest color palette based on category + themes
6. Provide composition guidance
7. Include technical parameters (style reference, lighting, aesthetic approach)

Format output as XML:
<output>
<text_prompt>
[Complete prompt ready for image generation, 30-50 words]
</text_prompt>
<json_output>
{{
  "id": "img_prompt_[random_number]",
  "category": "{category}",
  "subcategory": "{subcategory}",
  "subject": "{subject}",
  "thematic_elements": ["list", "of", "selected", "theme", "names"],
  "prompt_text": "[same as text_prompt]",
  "metadata": {{
    "key_elements": ["element1", "element2", "element3", "element4"],
    "mood": "adjective1, adjective2, adjective3",
    "color_palette": "color description here",
    "composition": "composition style here",
    "technical_params": {{
      "style_reference": "artist or movement name",
      "lighting": "lighting approach description",
      "aesthetic": "aesthetic quality description"
    }}
  }}
}}
</json_output>
</output>

Ensure text prompt is immediately usable and JSON is properly formatted."""

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
    }
}


def parse_output(response):
    """Extract text prompt and JSON from XML response"""
    text_match = re.search(r'<text_prompt>(.*?)</text_prompt>', response, re.DOTALL)
    json_match = re.search(r'<json_output>(.*?)</json_output>', response, re.DOTALL)

    text_prompt = text_match.group(1).strip() if text_match else ""
    json_output = None

    if json_match:
        try:
            json_str = json_match.group(1).strip()
            # Try to parse JSON
            json_output = json.loads(json_str)
        except:
            # If parsing fails, store raw string
            json_output = {"error": "Failed to parse JSON", "raw": json_str}

    # Fallback if no text prompt found
    if not text_prompt:
        # Use first 200 chars of response as fallback
        text_prompt = response[:200] if len(response) > 200 else response

    return text_prompt, json_output


def render_image_prompt():
    """Render the AI Image Prompt Generator tool"""

    st.title("🎨 AI Image Prompt Generator")
    st.write("Generate optimized prompts for DALL-E, Midjourney, Stable Diffusion, and other AI image generators")

    # Info expander
    with st.expander("ℹ️ How to Use This Tool"):
        st.markdown("""
        This tool generates **two types of outputs**:

        **📝 Text Prompt** - Copy-paste ready for image generation tools
        - Optimized for AI parsing
        - Includes style, artists, mood, aesthetics
        - 30-50 words, comma-separated

        **📊 JSON Format** - Structured metadata for databases and batch processing
        - Unique ID for cataloging
        - Detailed visual elements breakdown
        - Mood, color palette, composition guidance
        - Technical parameters for consistency

        **Workflow**: Category → Subcategory → Optional Themes (max 3) → Subject → Generate
        """)

    # Examples section
    with st.expander("💡 Try These Examples", expanded=False):
        st.markdown("Click any example to auto-fill the form:")

        examples = {
            "Classical Portrait": {
                "category": "Fine Art Movements",
                "subcategory": "Classical & Academic",
                "themes": ["Light & Atmosphere"],
                "subject": "portrait of a Renaissance scholar in his study, surrounded by ancient manuscripts and scientific instruments",
                "description": "Fine art portrait with classical composition"
            },
            "Cyberpunk Street": {
                "category": "Fantasy & Sci-Fi",
                "subcategory": "Cyberpunk & Neon Aesthetics",
                "themes": ["Scale & Perspective", "Color Psychology"],
                "subject": "rain-soaked street market at night with holographic advertisements and neon signs reflecting in puddles",
                "description": "Sci-fi scene with dramatic lighting and scale"
            },
            "Nature Photography": {
                "category": "Photography Styles",
                "subcategory": "Landscape & Nature",
                "themes": ["Temporal Quality", "Material & Texture"],
                "subject": "misty forest at dawn with rays of sunlight filtering through ancient moss-covered trees",
                "description": "Natural landscape with atmospheric elements"
            }
        }

        cols = st.columns(3)
        for idx, (example_name, example_data) in enumerate(examples.items()):
            with cols[idx % 3]:
                if st.button(
                    f"📋 {example_name}",
                    key=f"ip_example_{idx}",
                    use_container_width=True,
                    help=example_data['description']
                ):
                    # Clear all theme checkboxes first
                    for theme_name in THEMATIC_ELEMENTS.keys():
                        st.session_state[f"theme_{theme_name}"] = False

                    # Set category and subcategory
                    st.session_state.ip_category = example_data['category']
                    st.session_state.ip_subcategory = example_data['subcategory']

                    # Set selected themes
                    for theme in example_data['themes']:
                        st.session_state[f"theme_{theme}"] = True

                    # Set subject
                    st.session_state.ip_subject = example_data['subject']

                    st.rerun()

    st.markdown("---")

    # Step 1: Category selection
    st.markdown("### Step 1: Select Art Category")

    category_cols = st.columns(4)

    for idx, (cat_name, cat_data) in enumerate(TAXONOMY.items()):
        with category_cols[idx % 4]:
            if st.button(
                f"{cat_data['icon']} {cat_name}",
                key=f"cat_{cat_name}",
                use_container_width=True
            ):
                st.session_state.ip_category = cat_name

    if 'ip_category' in st.session_state:
        selected_category = st.session_state.ip_category
        st.success(f"✅ Selected: {TAXONOMY[selected_category]['icon']} {selected_category}")

        # Step 2: Subcategory selection
        st.markdown("### Step 2: Select Subcategory")

        subcategory = st.selectbox(
            "Choose specific style",
            options=TAXONOMY[selected_category]["subcategories"],
            key="ip_subcategory"
        )

        # Step 3: Thematic elements (optional)
        st.markdown("### Step 3: Add Thematic Elements (optional, max 3)")
        st.caption("These modify mood, lighting, composition across any category")

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

        if len(selected_themes) > 3:
            st.warning("⚠️ Please select maximum 3 thematic elements for best results")
            selected_themes = selected_themes[:3]

        # Step 4: Subject input
        st.markdown("### Step 4: Enter Subject")
        subject = st.text_area(
            "Describe what you want to generate",
            height=100,
            placeholder="Examples:\n- ancient library filled with mystical tomes\n- cyberpunk street market at night\n- portrait of a stoic warrior\n- abstract representation of time",
            key="ip_subject",
            help="Tip: Press Ctrl+Enter to quickly finish editing"
        )

        # Generate button
        generate_btn = st.button(
            "✨ Generate Image Prompts",
            disabled=(len(subject.strip()) < 5),
            type="primary",
            use_container_width=True
        )

        st.caption("💡 Generation takes 10-15 seconds")

        if generate_btn and subject.strip():
            with st.spinner("Generating optimized prompts..."):
                try:
                    # Get subcategory details
                    subcat_data = SUBCATEGORY_DETAILS.get(
                        subcategory,
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

                    # Build system prompt
                    random_id = random.randint(1000, 9999)
                    system_prompt = IMAGE_PROMPT_SYSTEM.format(
                        category=selected_category,
                        subcategory=subcategory,
                        subject=subject,
                        thematic_elements=", ".join(selected_themes) if selected_themes else "None",
                        subcategory_data=subcat_context,
                        random_id=random_id
                    )

                    # Build user message
                    user_message = f"""Category: {selected_category}
Subcategory: {subcategory}
Subject: {subject}
Thematic Elements: {", ".join(selected_themes) if selected_themes else "None"}

Generate both text prompt and JSON output now."""

                    # Call API
                    response = call_anthropic(
                        system_prompt=system_prompt,
                        user_message=user_message,
                        max_tokens=1500
                    )

                    # Parse response
                    text_prompt, json_output = parse_output(response)

                    st.session_state.ip_text = text_prompt
                    st.session_state.ip_json = json_output
                    st.session_state.ip_category_display = selected_category
                    st.session_state.ip_subcategory_display = subcategory

                    st.success("✅ Prompts generated successfully!")

                except Exception as e:
                    st.error(f"Error generating prompts: {str(e)}")

    else:
        st.info("👆 Click a category button above to get started")

    # Display results
    if 'ip_text' in st.session_state and 'ip_json' in st.session_state:
        st.markdown("---")
        st.subheader("📋 Generated Outputs")

        # Show context
        if 'ip_category_display' in st.session_state:
            cat = st.session_state.ip_category_display
            subcat = st.session_state.ip_subcategory_display
            st.caption(f"**Context:** {TAXONOMY.get(cat, {}).get('icon', '🎨')} {cat} → {subcat}")

        # Text Prompt
        st.markdown("#### 📝 Text Prompt (Copy-Paste Ready)")
        st.info("Use this directly in DALL-E, Midjourney, Stable Diffusion, or any AI image generator")
        st.code(st.session_state.ip_text, language=None)

        st.markdown("---")

        # JSON Output
        st.markdown("#### 📊 JSON Format (Structured Metadata)")
        st.info("Use this for prompt libraries, databases, or batch processing workflows")

        if st.session_state.ip_json and 'error' not in st.session_state.ip_json:
            # Display formatted JSON
            st.json(st.session_state.ip_json)

            # Also provide code block for copying
            with st.expander("📋 Copy JSON"):
                st.code(json.dumps(st.session_state.ip_json, indent=2), language="json")
        else:
            st.warning("JSON parsing encountered an issue, showing raw output:")
            if isinstance(st.session_state.ip_json, dict) and 'raw' in st.session_state.ip_json:
                st.code(st.session_state.ip_json['raw'], language=None)
            else:
                st.code(str(st.session_state.ip_json), language=None)

    elif 'ip_category' not in st.session_state:
        # Empty state - show examples
        st.markdown("---")
        st.info("""
        ### 🌟 Quick Start

        1. **Select a category** from the buttons above (Fine Art, Photography, Digital Art, etc.)
        2. **Choose a subcategory** for specific style guidance
        3. **Optionally add themes** to modify mood, lighting, or composition (max 3)
        4. **Enter your subject** - what you want to see in the image
        5. **Generate** and get both text prompt and JSON format

        ### 💡 Example Workflows

        **Classic Art Portrait:**
        - Category: Fine Art Movements → Classical & Academic
        - Themes: Light & Atmosphere
        - Subject: "elderly scholar reading ancient texts"

        **Cyberpunk Scene:**
        - Category: Fantasy & Sci-Fi → Cyberpunk & Neon Aesthetics
        - Themes: Scale & Perspective, Color Psychology
        - Subject: "street market vendor at night"

        **Nature Photography:**
        - Category: Photography Styles → Landscape & Nature
        - Themes: Temporal Quality, Compositional Tension
        - Subject: "misty mountain sunrise"
        """)

        # Show category grid
        st.markdown("### 📚 Available Categories")
        cols = st.columns(4)

        for idx, (cat_name, cat_data) in enumerate(TAXONOMY.items()):
            with cols[idx % 4]:
                st.markdown(f"**{cat_data['icon']} {cat_name}**")
                st.caption(f"{len(cat_data['subcategories'])} subcategories")
