import streamlit as st
import re
import json
import random
import time
from backend.api_client import call_anthropic

# System prompt for Image Prompt generation (updated for multi-style)
IMAGE_PROMPT_SYSTEM = """You are an expert in art history, visual aesthetics, and AI image generation prompting.

Your task: Generate a text prompt optimized for AI image generation (DALL-E, Midjourney, Stable Diffusion).

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

Format output as XML:
<text_prompt>
[Complete prompt ready for image generation, 30-50 words]
</text_prompt>

Ensure text prompt is immediately usable."""

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
    }
}


def render_image_prompt():
    """Render the AI Image Prompt Generator tool - Multi-Style Variation Feature"""

    st.title("🎨 AI Image Prompt Generator")
    st.write("Generate multiple style variations for the same subject")

    # Info expander
    with st.expander("ℹ️ How to Use This Tool"):
        st.markdown("""
        **New Multi-Style Feature:**

        1. **Enter your subject** (e.g., "vintage 1970s muscle car")
        2. **Select 3-5 art styles** from any category
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
            "Executive Presentation Visuals": {
                "subject": "professional business transformation roadmap visualization with timeline, milestones, and interconnected workstreams",
                "styles": [
                    ("Digital Art Genres", "Concept Art & Matte Painting"),
                    ("Digital Art Genres", "3D Rendering & CGI"),
                    ("Fine Art Movements", "Modernism & Abstraction")
                ],
                "themes": ["Compositional Tension", "Color Psychology"],
                "description": "Clean, corporate-appropriate visualizations"
            },
            "Organization Chart Redesign": {
                "subject": "modern organizational structure diagram showing functional reporting lines, matrix relationships, and governance bodies",
                "styles": [
                    ("Digital Art Genres", "Vector & Flat Design"),
                    ("Cultural & Historical", "Art Deco & Mid-Century"),
                    ("Fine Art Movements", "Modernism & Abstraction")
                ],
                "themes": ["Compositional Tension"],
                "description": "Professional, hierarchical visual design"
            },
            "Process Flow Illustration": {
                "subject": "streamlined business process workflow with decision points, system handoffs, and approval gates",
                "styles": [
                    ("Digital Art Genres", "Vector & Flat Design"),
                    ("Digital Art Genres", "3D Rendering & CGI")
                ],
                "themes": ["Material & Texture", "Compositional Tension"],
                "description": "Clear, professional process visualization"
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
                    st.session_state.ip_subject_prefill = example_data['subject']

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
        value=st.session_state.get('ip_subject_prefill', ''),
        help="Tip: Be specific but concise - describe the core elements"
    )

    # STEP 2: Style Selection (NEW - Multiple subcategories)
    st.markdown("### Step 2: Select 3-5 Art Styles")
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
    if num_selected < 3 and num_selected > 0:
        st.warning(f"⚠️ Please select at least 3 styles (currently: {num_selected})")
    elif num_selected > 5:
        st.info(f"ℹ️ {num_selected} styles selected. Generation will take approximately {num_selected * 10} seconds.")
    elif num_selected >= 3:
        st.success(f"✅ {num_selected} styles selected")

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
        3 <= len(selected_subcategories) <= 10
    )

    generate_btn = st.button(
        f"✨ Generate {len(selected_subcategories)} Style Variations" if selected_subcategories else "✨ Generate Variations",
        disabled=not can_generate,
        type="primary",
        use_container_width=True
    )

    if not can_generate and (subject.strip() or selected_subcategories):
        if len(subject.strip()) < 5:
            st.caption("⚠️ Please enter a subject (at least 5 characters)")
        elif len(selected_subcategories) < 3:
            st.caption("⚠️ Please select at least 3 art styles")

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

                    # Build system prompt
                    system_prompt = IMAGE_PROMPT_SYSTEM.format(
                        category=style['category'],
                        subcategory=style['subcategory'],
                        subject=subject,
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
        2. **Select 3-5 art styles** - Browse categories below and check styles you're interested in
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
