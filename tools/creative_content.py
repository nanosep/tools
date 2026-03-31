"""
Creative Content for Business - AI Media Use Cases Catalog
Displays 200+ business use cases for AI-generated media organized by department
"""

import streamlit as st


# Data extracted from freepik_examples.html
DEPARTMENTS_DATA = {
    "Marketing": {
        "icon": "📢",
        "color": "#FF6B6B",
        "useCases": [
            "Rapid campaign concepting (headline variants, visual directions, storyboards)",
            "Social content 'factory' (image sets, short-form video edits, captions, thumbnails)",
            "Product/content localization (language + cultural variants, region-specific creatives)",
            "Brand-consistent design production (banners, landing visuals, icons, simple motion)",
            "PR & thought leadership packs (quotes-to-visuals, podcast snippets, blog-to-video)",
            "Campaign content 'factory' (social variants, thumbnails, short-form video cuts)",
            "Brand storytelling (founder narrative videos, customer story reels)",
            "SEO content repurposing (blog → infographic → short video → audio snippet)",
            "Creative testing at scale (10 ad angles → 10 visual families)",
            "Event content (speaker clips, highlight reels, agenda visuals)"
        ]
    },
    "HR / People Ops": {
        "icon": "👥",
        "color": "#4ECDC4",
        "useCases": [
            "Recruitment content (role videos, 'day in the life,' team intros, office/location showcases)",
            "Employer brand storytelling (candidate FAQs as short videos, culture reels)",
            "Onboarding packs (welcome videos, role-specific explainers, policy summaries in visuals)",
            "Internal comms (CEO updates turned into short clips, visual explainers for policy changes)",
            "Performance enablement content (how to write goals, feedback examples as media)",
            "Culture content (values in action stories, internal spotlights)"
        ]
    },
    "Sales / Business Development": {
        "icon": "💼",
        "color": "#95E1D3",
        "useCases": [
            "Personalized outreach assets (industry-specific one-pagers, short explainer videos per segment)",
            "Proposal acceleration (deck visuals, case-study snippets, tailored demo scripts)",
            "Account-based marketing kits (custom microsites, product walkthrough clips, ROI visualizations)",
            "Objection-handling content (short clips answering top 20 objections, battlecards as visuals)",
            "Any-language video outreach (one pitch → multilingual versions with approved voiceovers)",
            "Personalized proposal videos (account context + tailored narrative in 60–120 seconds)",
            "RFP/RFI response packs (dense answers → clear diagrams + short explainer clips)",
            "Product demo 'snackables' (feature micro-demos, objection-handling clips)",
            "Industry-specific proof packs (case study → visuals → 30-sec story video)",
            "Competitive comparison visuals (feature grid + 'what matters' narrated explainer)",
            "Sales enablement media (battlecards as visuals, talk-tracks as audio rehearsals)"
        ]
    },
    "Operations / Supply Chain": {
        "icon": "⚙️",
        "color": "#F38181",
        "useCases": [
            "SOPs turned into visual guides (step-by-step images, short 'how to' videos)",
            "Incident reporting summaries (timeline visuals, root-cause explainer clips)",
            "Safety & compliance micro-content (refreshers, signage visuals, localized training snippets)",
            "Knowledge capture from experts (interviews → structured playbooks + short clips)",
            "Process explainers (handoffs, dependencies, 'who does what' visuals)",
            "Standard work visual guides (warehouse pick/pack, dispatch, returns)",
            "Incident retros (timeline visuals + 'root cause in plain English' clips)",
            "Vendor onboarding content (requirements → step-by-step video guides)",
            "Inventory / demand comms (forecast changes as simple explainers for non-analysts)"
        ]
    },
    "Customer Support": {
        "icon": "🎧",
        "color": "#AA96DA",
        "useCases": [
            "Self-serve help center upgrades (article → video, GIF walkthroughs, annotated screenshots)",
            "Multilingual support content (consistent translations + localized visuals)",
            "Agent assist content (instant 'how to respond' snippets, tone examples, macro libraries)",
            "Proactive customer comms (outage updates, feature releases, billing explainers in plain visuals)",
            "Help-center upgrades (article → short walkthrough video + annotated screenshots)",
            "Troubleshooting visual trees (symptom → fix as a simple flow graphic)",
            "Release/change comms (what changed + what to do, in 30 seconds)",
            "Agent macro libraries with tone examples (samples as mini audio/video references)",
            "Community content (top issues → weekly 'here's the fix' video post)"
        ]
    },
    "Learning & Development": {
        "icon": "📚",
        "color": "#FCBAD3",
        "useCases": [
            "Microlearning content pipeline (modules → quizzes → recap clips)",
            "Role-based simulations (scenario videos, branching role-plays, call practice)",
            "Internal academies (prompting basics, tool-specific how-tos, compliance refreshers)",
            "Train-the-trainer kits (slide visuals, facilitator scripts, exercises, rubrics)",
            "Microlearning modules (job tasks → short lessons with quizzes + recap videos)",
            "Role-play simulations (customer calls, negotiation, conflict scenarios as scripts + audio)",
            "Knowledge base 'academy' (internal wiki → structured course content)",
            "Compliance refreshers that don't feel like punishment (short, specific, visual)"
        ]
    },
    "Executive Leadership": {
        "icon": "👔",
        "color": "#A8D8EA",
        "useCases": [
            "Board-ready story packs (narrated slide videos, 'what changed this month' clips)",
            "Executive briefings from messy inputs (audio memo → clean summary + 60-sec update video)",
            "Strategy narratives (vision videos, internal alignment reels, OKR explainers)",
            "Crisis & change communication (rapid FAQ videos, calm-toned leadership messages)",
            "Investor-style storytelling for internal use (metric-to-story visuals, milestone timelines)",
            "'One decision, three options' content (short scenario videos for leadership alignment)"
        ]
    },
    "Strategy / Corporate Dev": {
        "icon": "🎯",
        "color": "#FFD93D",
        "useCases": [
            "Market landscape visuals (maps, competitor grids, 'who's buying whom' timelines)",
            "Deal narratives (acquisition rationale videos, synergy storyboards)",
            "PMI / separation comms content (what changes for whom, explained in plain visuals)",
            "Operating model explainers (org/role changes as short animated walkthroughs)",
            "Scenario planning as media (3 futures → 3 short videos your execs will actually watch)"
        ]
    },
    "Product Management": {
        "icon": "🚀",
        "color": "#6BCB77",
        "useCases": [
            "Feature announcement kits (demo videos, GIFs, screenshots, release notes visuals)",
            "Product education content (interactive tours, 'how it works' animations)",
            "Persona storytelling (customer interviews → persona cards + short persona videos)",
            "UX copy + micro-visuals (tooltips, empty states, onboarding visuals)",
            "Roadmap comms (quarterly roadmap as a 90-sec video + simple visuals)",
            "Beta feedback digestion (feedback dumps → themed reels for the product team)"
        ]
    },
    "R&D / Engineering": {
        "icon": "🔬",
        "color": "#C490E4",
        "useCases": [
            "Rapid concept visualization (sketch-to-render, variant exploration, moodboards)",
            "Prototype demo videos (screen recordings → polished walkthroughs with narration)",
            "Technical explainer animations (architecture in motion, 'why this works' clips)",
            "Lab/engineering SOP visuals (step-by-step image guides, short 'do/don't' clips)",
            "Synthetic user scenarios (use-case videos showing edge cases + expected behavior)",
            "Experiment documentation (results → visual abstract, poster-style summaries)",
            "Knowledge capture from experts (whiteboard talk → structured explainer video series)"
        ]
    },
    "Customer Success": {
        "icon": "🌟",
        "color": "#F7B731",
        "useCases": [
            "QBR kits (data → story slides + a narrated recap video)",
            "Adoption nudges (micro-tutorials, '1 feature per week' clips)",
            "Renewal value storytelling (impact reels showing wins and usage moments)",
            "Stakeholder alignment content (exec sponsor recap videos, success summaries)",
            "Onboarding journeys (role-based tutorials, 'first 7 days' video checklists)"
        ]
    },
    "Manufacturing / Quality": {
        "icon": "🏭",
        "color": "#FF5E57",
        "useCases": [
            "Safety micro-content (5-minute refreshers, hazard visuals, signage variants)",
            "Quality defect libraries (image examples of defects + what 'good' looks like)",
            "Training-by-station (short station videos, maintenance walkarounds)",
            "Audit readiness explainers (what auditors look for, visual checklists)",
            "Preventive maintenance content (procedure clips, common failure visuals)"
        ]
    },
    "Finance / FP&A": {
        "icon": "💰",
        "color": "#26C6DA",
        "useCases": [
            "Budget narratives (numbers → story visuals for non-finance stakeholders)",
            "Policy and process explainers (expenses, approvals, close calendar as media)",
            "KPI storytelling (monthly performance videos: 'what moved, why, what next')",
            "Investor-grade internal updates (quarterly recap reels for leadership)",
            "Collections/customer billing explainers (simple videos that reduce disputes)"
        ]
    },
    "Legal / Compliance": {
        "icon": "⚖️",
        "color": "#5F6F94",
        "useCases": [
            "Policy education content (what the policy means in practice, visual examples)",
            "Contract playbooks (clause libraries as simple visual guides)",
            "Privacy/security training snippets (phishing examples, do/don't visuals)",
            "Regulatory change comms (what changed + who must do what, in 60 seconds)",
            "Incident communications templates (approved messaging content packs)"
        ]
    },
    "IT / Security": {
        "icon": "🔒",
        "color": "#45B7D1",
        "useCases": [
            "How-to content at scale (VPN, access requests, tooling onboarding videos)",
            "Security awareness campaigns (phishing sims + short explainers)",
            "System change comms (downtime, migrations, new tools—clear visuals)",
            "Data literacy content (how dashboards work, how to interpret metrics)",
            "Internal tool demos (screen recordings → polished walkthroughs)"
        ]
    },
    "Procurement": {
        "icon": "📋",
        "color": "#96CEB4",
        "useCases": [
            "Supplier onboarding explainers (requirements, portals, timelines as media)",
            "Category strategy storytelling (why this sourcing move, with visuals)",
            "RFx content packs (how to respond, what 'good' looks like)",
            "Stakeholder comms (tradeoffs, constraints, and outcomes explained visually)"
        ]
    },
    "Facilities / Workplace": {
        "icon": "🏢",
        "color": "#DDA15E",
        "useCases": [
            "Workplace onboarding (how to book rooms, access rules, visitor policy videos)",
            "Safety & emergency content (evacuation, first-aid basics as visuals)",
            "Space change comms (renovations, relocations, 'what's changing' clips)",
            "Service request tutorials (how to log issues, what info to include)"
        ]
    },
    "PR / Corporate Comms": {
        "icon": "📰",
        "color": "#E63946",
        "useCases": [
            "Press kits as multimedia (key message videos, spokesperson briefing clips)",
            "Social proof content (customer quotes → visuals → short reels)",
            "Leadership comms (town halls, 'ask me anything' highlights)",
            "Event coverage (recap reels, session summaries, speaker clips)"
        ]
    },
    "Partnerships": {
        "icon": "🤝",
        "color": "#457B9D",
        "useCases": [
            "Partner enablement kits (co-sell decks, demo videos, positioning clips)",
            "Co-marketing content generation (joint case studies, launch videos)",
            "Training for partner reps (micro modules + objection-handling videos)",
            "Marketplace listing media (short explainer videos, visuals, screenshots)"
        ]
    },
    "Field Service": {
        "icon": "🔧",
        "color": "#F4A261",
        "useCases": [
            "On-site procedure videos (repair steps, safety checks, diagnostics)",
            "Visual troubleshooting guides (symptom → action → verification)",
            "Customer-facing 'what to expect' content (service visit prep videos)",
            "Technician knowledge capture (best tech explains once → everyone benefits)"
        ]
    }
}


def detect_media_types(use_case_text):
    """
    Detect media types from use case text using keyword matching.
    Returns list of media types: ['Image', 'Video', 'Audio']
    """
    text_lower = use_case_text.lower()
    media_types = []

    # Video keywords
    video_keywords = ['video', 'clip', 'reel', 'recording', 'footage', 'demo', 'walkthrough',
                      'animation', 'motion', 'story', 'highlight']
    if any(keyword in text_lower for keyword in video_keywords):
        media_types.append('Video')

    # Image keywords
    image_keywords = ['visual', 'image', 'graphic', 'infographic', 'photo', 'diagram',
                      'screenshot', 'banner', 'icon', 'thumbnail', 'signage', 'card']
    if any(keyword in text_lower for keyword in image_keywords):
        media_types.append('Image')

    # Audio keywords
    audio_keywords = ['audio', 'voice', 'narrat', 'podcast', 'sound', 'speech', 'voiceover']
    if any(keyword in text_lower for keyword in audio_keywords):
        media_types.append('Audio')

    # If no specific media type detected, assume it could be any
    if not media_types:
        media_types = ['Image', 'Video', 'Audio']

    return media_types


def filter_use_cases_by_media(use_cases, selected_media_types):
    """
    Filter use cases based on selected media types.
    If 'All Media Types' is selected, return all use cases.
    """
    if not selected_media_types or 'All Media Types' in selected_media_types:
        return use_cases

    filtered = []
    for use_case in use_cases:
        detected_types = detect_media_types(use_case)
        # Include if any selected media type is in detected types
        if any(media_type in detected_types for media_type in selected_media_types):
            filtered.append(use_case)

    return filtered


def render_creative_content():
    """Main render function for Creative Content for Business tool"""

    st.title("🎬 Creative Content for Business")
    st.write("**AI Media Use Cases Catalog** - 200+ use cases for AI-generated media across business functions")

    # Info expander
    with st.expander("ℹ️ About This Tool", expanded=False):
        st.markdown("""
        This catalog displays **200+ real-world use cases** for AI-generated media (images, videos, and audio)
        organized by business function.

        **How to use:**
        1. Select a department to view its use cases
        2. Filter by media type (Image, Video, Audio)
        3. Click on use cases to explore specific applications

        **Why this matters:**
        - Discover practical applications for AI-generated content
        - Identify opportunities in your organization
        - Understand how different departments use AI media
        - See examples of images, videos, and audio in business contexts

        **Source:** Curated from enterprise AI content use cases
        """)

    st.markdown("---")

    # Calculate total statistics
    total_departments = len(DEPARTMENTS_DATA)
    total_use_cases = sum(len(dept["useCases"]) for dept in DEPARTMENTS_DATA.values())

    # Display stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Departments", total_departments)
    with col2:
        st.metric("Total Use Cases", total_use_cases)
    with col3:
        # Count filtered use cases
        st.metric("Categories", "20")

    st.markdown("---")

    # Controls
    col1, col2 = st.columns([2, 1])

    with col1:
        # Department selector
        department_names = ["All Departments"] + list(DEPARTMENTS_DATA.keys())
        selected_department = st.selectbox(
            "📂 Select Department",
            options=department_names,
            index=0
        )

    with col2:
        # Media type filter
        media_types = ["All Media Types", "Image", "Video", "Audio"]
        selected_media = st.multiselect(
            "🎨 Filter by Media Type",
            options=media_types,
            default=["All Media Types"]
        )

    st.markdown("---")

    # Display use cases
    if selected_department == "All Departments":
        # Show all departments
        st.subheader("All Departments")

        for dept_name, dept_data in DEPARTMENTS_DATA.items():
            # Filter use cases by media type
            filtered_cases = filter_use_cases_by_media(dept_data["useCases"], selected_media)

            if filtered_cases:  # Only show if there are filtered results
                with st.expander(f"{dept_data['icon']} **{dept_name}** ({len(filtered_cases)} use cases)", expanded=False):
                    for i, use_case in enumerate(filtered_cases, 1):
                        detected_types = detect_media_types(use_case)
                        media_badges = " ".join([f"`{mt}`" for mt in detected_types])
                        st.markdown(f"{i}. {use_case}  \n   {media_badges}")
    else:
        # Show selected department
        dept_data = DEPARTMENTS_DATA[selected_department]

        # Department header with icon and color
        st.markdown(f"## {dept_data['icon']} {selected_department}")

        # Filter use cases by media type
        filtered_cases = filter_use_cases_by_media(dept_data["useCases"], selected_media)

        if filtered_cases:
            st.write(f"**{len(filtered_cases)} use cases** in this department")
            st.markdown("---")

            # Display use cases
            for i, use_case in enumerate(filtered_cases, 1):
                detected_types = detect_media_types(use_case)
                media_badges = " ".join([f"`{mt}`" for mt in detected_types])

                with st.expander(f"**Use Case {i}**", expanded=False):
                    st.markdown(f"**Media Types:** {media_badges}")
                    st.markdown(f"**Description:**  \n{use_case}")
        else:
            st.info(f"No use cases found for the selected media type(s) in {selected_department}.")

    st.markdown("---")

    # Footer
    st.caption("💡 This catalog is a reference tool. No AI generation is performed here - use other ClarityCrew tools for content creation.")
