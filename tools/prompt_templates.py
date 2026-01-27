import streamlit as st

def display_prompt(title, description, when_to_use, prompt_text):
    """Display a single prompt template"""

    with st.expander(f"**{title}**", expanded=False):
        # Description
        st.markdown(f"**What it is:** {description}")
        st.markdown(f"**When to use:** {when_to_use}")

        st.markdown("---")

        # The actual prompt in a code block (gives automatic copy button)
        st.code(prompt_text, language=None)


def render_audience_prompts():
    st.markdown("### 👥 Audience Understanding")
    st.caption("5 prompts for understanding communication patterns, cognitive styles, and behavioral traits")

    # Mirror Chamber
    display_prompt(
        title="Mirror Chamber",
        description="Revealing how a person's motives, style, or biases show up in their words",
        when_to_use="When analyzing communication patterns or profiling decision-makers from their language",
        prompt_text="""Analyze the following text as if you were a behavioral profiler. Describe what it reveals about the author's priorities, emotional tone, and decision style — use evidence from phrasing, rhythm, and structure. Then list 3 hypotheses you'd test to confirm your reading."""
    )

    # Signature Mapping
    display_prompt(
        title="Signature Mapping",
        description="Detecting thinking patterns—analytical, intuitive, narrative, relational, or improvisational",
        when_to_use="When adapting communication to different cognitive styles or understanding how someone reasons",
        prompt_text="""Given this email or short passage, classify the author's reasoning mode: analytical, narrative, relational, or improvisational. List linguistic cues supporting each label. Then suggest how to adapt communication for highest resonance."""
    )

    # Dual Lens
    display_prompt(
        title="Dual Lens",
        description="Contrasting internal self-image with external perception to spot alignment gaps",
        when_to_use="When improving self-awareness or understanding how leadership style is received by others",
        prompt_text="""Describe how [persona: e.g., a cautious CFO] probably sees themselves. Then describe how others might see them under stress. Identify the 1 alignment and 1 misalignment that most affect performance."""
    )

    # Contextual Mask
    display_prompt(
        title="Contextual Mask",
        description="Showing how behavior shifts between contexts while identifying stable core traits",
        when_to_use="When preparing for different communication contexts or exploring behavioral adaptability",
        prompt_text="""Imagine this person in three contexts: team meeting, investor pitch, private reflection. Write a 3-sentence vignette for each showing subtle changes in tone, vocabulary, and confidence. Then summarize the stable core that remains underneath."""
    )

    # Relational Geometry
    display_prompt(
        title="Relational Geometry",
        description="Mapping interaction styles and compatibility across several behavioral dimensions",
        when_to_use="When building teams, predicting collaboration challenges, or optimizing communication across personality styles",
        prompt_text="""Map this person's relational geometry using four axes: Directive ↔ Supportive, Reserved ↔ Expressive, Analytical ↔ Intuitive, Pragmatic ↔ Idealistic. Place them on each axis (1–10) and justify the position with examples. Suggest which pairings create friction or flow."""
    )


def render_excel_prompts():
    st.markdown("### 📊 Excel Analysis & Insights")
    st.caption("4 prompts for data analysis, pattern recognition, and insights generation")

    # Find What Matters in Your Data
    display_prompt(
        title="Find What Matters in Your Data",
        description="Spot trends and outliers instantly – no manual number-crunching",
        when_to_use="When analyzing large datasets (sales, headcount, customer metrics, supply-chain data) to identify what deserves immediate attention",
        prompt_text="""You are an executive analyst helping me understand what really matters in this dataset.

DATA INPUT: [Paste an Excel table or describe columns]

STEP 1 — Quick Data Scan: Briefly describe the shape of the data. Flag any obvious data quality issues.

STEP 2 — Core Trends: Identify top 3–5 important patterns. For each, specify: METRIC, PATTERN, DRIVER HYPOTHESIS.

STEP 3 — Outliers & Anomalies: List 3–5 most notable anomalies and explain why they're suspicious or important.

STEP 4 — Variance Drivers: Tell me which 3 metrics appear to explain the most variance in performance. Suggest how to test these drivers.

STEP 5 — Executive "So What": Give me 3 strategic questions to investigate and 3 concrete actions this dataset hints at."""
    )

    # Check Spreadsheet Quality
    display_prompt(
        title="Check Spreadsheet Quality",
        description="Finding errors, duplicates, and inconsistencies before presenting to leadership",
        when_to_use="Before finalizing budgets, sending reports to leadership, or loading data into dashboards",
        prompt_text="""Act as a data-quality auditor reviewing a spreadsheet before it goes to leadership.

INPUT: [Paste an Excel table or describe key columns]

STEP 1 — Structural Checks: Identify duplicate rows or values. Highlight missing data in critical columns.

STEP 2 — Numeric & Logic Checks: Flag outliers. Detect logical errors (negative headcount, cost > revenue, impossible dates).

STEP 3 — Formatting & Consistency: List formatting inconsistencies that could break formulas or dashboards. Note inconsistent category naming.

STEP 4 — Risk Assessment: Give the sheet a Data Quality Score (0–10) with justification. Summarize the 3 biggest risks of using this data as-is.

STEP 5 — Prioritized Fix List: Provide High/Medium/Low fixes with WHAT, WHY, and HOW for each.

End with verdict: CLEAN ENOUGH FOR LEADERSHIP / NEEDS FIXES BEFORE USE."""
    )

    # Set Up Performance Comparisons
    display_prompt(
        title="Set Up Performance Comparisons",
        description="Building year-over-year, actual vs budget, or cross-department comparisons with variance formulas",
        when_to_use="When preparing monthly or quarterly reviews to explain performance gaps to leadership or the board",
        prompt_text="""You are designing a performance comparison pack in Excel for leadership.

COMPARISON NEEDED: [Describe, e.g., "2024 Actual vs 2024 Budget"]

STEP 1 — Layout Recommendation: Propose a clear worksheet structure. Specify exact column layout.

STEP 2 — Formulas & Flags: Provide exact Excel formulas for: $ variance, % variance, Favorable/Unfavorable flag.

STEP 3 — Variance Story Table: Define a summary table of top 5 largest variances with: Metric/Segment, Variance ($ and %), explanation, follow-up action.

STEP 4 — Visuals: Recommend 2–3 charts. For each, specify axes, series, and the insight it highlights.

STEP 5 — Executive Notes: Suggest a short "Performance Story" outline (3–5 bullets)."""
    )

    # Extract Business Insights from Tables
    display_prompt(
        title="Extract Business Insights from Tables",
        description="Turning raw numbers into actionable insights without staring at spreadsheets for hours",
        when_to_use="When preparing for strategy meetings, board updates, or investor discussions",
        prompt_text="""Here is a key table from my strategic plan [paste table]. Act as an executive analyst and turn it into board-level insights.

STEP 1 — Read & Classify: Briefly describe what the table is about. Note any obvious caveats.

STEP 2 — Core Insights: Give me the top 5 most important insights. For each: WHAT (pattern), WHERE (segment/metric), HOW BIG (magnitude).

STEP 3 — Business Implications: For each insight, state 1–2 business implications framed for executives.

STEP 4 — Recommended Actions: Propose 1–2 specific actions per insight. Label as NOW / NEXT QUARTER / LATER.

STEP 5 — The Surprise: Highlight one surprising finding and why it matters.

Keep everything in clear, non-technical language suitable for senior leadership."""
    )


def render_admin_prompts():
    st.markdown("### 📋 Admin & Productivity")
    st.caption("2 prompts for daily productivity, document management, and administrative tasks")

    # Meeting Debris Compressor
    display_prompt(
        title="Meeting Debris Compressor",
        description="Turning messy meeting notes into executive summaries, team minutes, and personal to-do lists",
        when_to_use="After every meeting where you need to track decisions, actions, and open questions",
        prompt_text="""ROLE: You are my Meeting Debris Compressor.

GOAL: Turn raw notes or transcripts into: Executive summary, Team-facing minutes, Personal to-do list.

INPUT FORMAT: Either raw bullet notes or a call transcript.

INSTRUCTIONS:
1) Extract and structure: Key decisions, Open questions, Action items with Owner/Description/Deadline.

2) Produce THREE outputs:

A) MANAGER SUMMARY: 5–7 bullets, max 150 words, focus on decisions and next milestones.

B) TEAM MINUTES (EMAIL-READY): Subject line with date. Short intro. Sections: Decisions, Action Items by Person, Open Questions. Copy-paste ready.

C) PERSONAL TO-DO LIST: Checklist of action items where you are owner. Each item: [ ] description — due [date].

3) Generate a MARKDOWN TABLE of all action items: ID, Owner, Action, Due Date, Priority, Dependencies.

STYLE: Clear, neutral, no drama. Use people's names exactly as stated."""
    )

    # Weekly Status Alchemist
    display_prompt(
        title="Weekly Status Alchemist",
        description="Turning weekly chaos into clean status updates for different audiences",
        when_to_use="For weekly reports to managers, teams, and executives",
        prompt_text="""ROLE: You are my Weekly Status Alchemist.

GOAL: Turn messy notes, calendar, emails, and thoughts into clean weekly updates for different audiences.

INPUT FORMAT: Fragments of tasks done, calendar appointments, draft notes, metrics or numbers.

INSTRUCTIONS:
1) Parse input and infer: What got done, What moved but isn't done, Blockers/risks, Measurable progress.

2) Build a Master Timeline Summary (5–10 bullets, chronological).

3) Generate THREE tailored statuses:

A) Manager Update: 200–300 words. Slightly candid on risks.

B) Team Update: 200–400 words. Collaborative tone.

C) Exec/Steering Update: Max 200 words. Ruthless prioritization.

Each uses: Highlights / Lowlights / Next Week / Dependencies structure.

4) Output in order: Master Timeline Summary, Manager Update, Team Update, Exec/Steering Update.

STYLE: Clear, non-dramatic. No fake numbers; label approximations."""
    )


def render_prompt_templates():
    """Render the Prompt Templates tool"""

    st.title("📚 Prompt Templates")
    st.write("Ready-to-use prompts for enterprise workflows - just copy and paste")

    # Info expander
    with st.expander("ℹ️ How to Use These Prompts"):
        st.markdown("""
        These are curated, battle-tested prompts ready for immediate use:

        1. **Browse prompts by category** - Choose from Audience Understanding, Excel Analysis, or Admin & Productivity
        2. **Read the description and use case** - Understand what the prompt does and when to use it
        3. **Click to expand and view the full prompt** - See the complete prompt text
        4. **Copy the prompt** - Use the copy button in the code block
        5. **Paste into your AI tool** - Use with Claude, ChatGPT, or any other AI assistant

        No generation needed - these prompts are ready to go!
        """)

    st.markdown("---")

    # Category selector
    category = st.radio(
        "Select Category",
        ["👥 Audience Understanding", "📊 Excel Analysis & Insights", "📋 Admin & Productivity"],
        horizontal=True
    )

    st.markdown("---")

    # Display prompts for selected category
    if category == "👥 Audience Understanding":
        render_audience_prompts()
    elif category == "📊 Excel Analysis & Insights":
        render_excel_prompts()
    else:
        render_admin_prompts()
