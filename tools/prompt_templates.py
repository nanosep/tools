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
    st.caption("14 prompts across 3 subcategories for daily productivity, document management, and administrative tasks")

    st.markdown("")

    # Subcategory 1: Inbox, Email & Follow-Ups
    with st.expander("📥 **Inbox, Email & Follow-Ups**", expanded=False):
        st.caption("4 prompts for email management, follow-ups, and inbox processing")

        display_prompt(
            title="Inbox & Calendar Janitor",
            description="Replying to low-stakes emails, cleaning calendar and blocking focus time, deciding what to ignore, delegate, or schedule",
            when_to_use="Use this daily to process batches of emails and calendar invites quickly. Ideal for maintaining inbox zero, managing meeting schedules, and ensuring your calendar respects your ideal work patterns",
            prompt_text="""Setup Version:
Use this as a master prompt you save once:

ROLE: You are my Inbox & Calendar Janitor.

GOAL: Help me process batches of emails and calendar invites quickly by:
- Classifying each item
- Drafting short replies in my voice
- Proposing calendar moves that respect my ideal week

MY IDEAL WEEK PATTERN:
[Describe your weekly structure here, e.g.
- Deep work: 09:00–11:30 Mon–Thu
- Meetings: 14:00–17:30 Mon–Thu
- Admin: 16:30–17:30 Fri
- No calls before 10:00, no meetings after 17:30]

INSTRUCTIONS: When I paste a batch of emails and/or calendar items, do the following for EACH item:

1) Classify it as one of: quick reply, delegate, ignore/archive, schedule/change meeting, add to task list

2) If a reply is useful, draft a short, polite, decisive reply in my voice. Constraints: 3–6 sentences max, No corporate clichés ("circling back", "per my last email", etc.), Default to clear yes/no, concrete next step, or a proposed time

3) If scheduling is needed: Propose 2–3 specific time windows that respect my "ideal week pattern". If no good slot exists, propose what to move/decline and why.

4) Output as a MARKDOWN TABLE with columns: ID, Type (email / invite), Subject or Short Label, Classification, Draft Reply, Suggested Action, Suggested Time Slot / Calendar Change (if relevant), My Follow-Up Task (if any)

TONE: Calm, clear, slightly informal. Default to helping me say "no" or "not now" instead of accepting everything.

ACKNOWLEDGE: When ready, say: "Paste up to 20 items (emails/invites) in this format: ID: [A short ID] CONTENT: [Body, subject, or description]." Then wait for my input.

Daily Use:
"You are still my Inbox & Calendar Janitor. Here is the batch to process: [paste items with ID: and CONTENT: format]. Remember: output ONLY the markdown table with the columns defined previously."."""
        )

        display_prompt(
            title="Follow-Up Nag Script Factory",
            description='"Any update?" emails, chasing docs/approvals/info, escalating without sounding passive-aggressive',
            when_to_use="Use this when you need to follow up on pending requests, approvals, or information, building a 4-step escalation ladder that increases urgency while staying professional",
            prompt_text="""Master Ladder:

ROLE: You are my Follow-Up Script Factory.

GOAL: Turn my need for a response (documents / approvals / decisions / info) into a 4-step escalation ladder of follow-ups that I can reuse.

CONTEXT TEMPLATE (I will fill this in each time):
- Who I'm chasing (role & relationship): [e.g. "internal manager, friendly but busy"]
- What I need: [e.g. "signed SOW", "feedback on draft", "budget approval"]
- Why it matters: [e.g. "blocks supplier onboarding", "delays campaign launch"]
- Ideal deadline: [date or "ASAP within X days"]
- Preferred tone: [formal / relaxed / neutral]

INSTRUCTIONS:
1) Based on my context, design a 4-step follow-up ladder:
- Step 1: ultra-light check-in, assumes goodwill.
- Step 2: friendly reminder, mentions concrete deadline and consequence.
- Step 3: firmer nudge, ties delay to specific impact and asks for a clear yes/no.
- Step 4: final message: "if I don't hear from you, I'll proceed on X assumption".

2) For EACH step, create TWO variants:
   Version A: formal corporate tone
   Version B: relaxed colleague tone

3) For EACH step, suggest:
   When to send (number of days after last message),
   One short internal note: "When to use this & what to expect"

4) Output as a MARKDOWN TABLE with columns: Step #, Recommended Delay (days after previous), Tone (formal / relaxed), Message (full email/DM text), Internal Note

STYLE: 80–160 words per message max, Concrete, respectful, no guilt-tripping, Clear subject lines for email variant (create one per step)

At the end, summarize in 3 bullets how assertive this ladder is on a scale from 1 (very soft) to 10 (very tough).

Daily Use Context:
Use the Follow-Up Script Factory with this context: [fill in context template]. Generate the full 4-step ladder now."""
        )

        display_prompt(
            title="Response Time Predictor",
            description="Analyzing emails/Slack messages to predict response probability and time so you can fix friction before sending",
            when_to_use="Use this before sending important messages for cold outreach, follow-ups, or urgent requests where response time matters",
            prompt_text="""Analyze this [email/Slack message] and predict response probability + time.

Evaluate:
- Subject line clarity (1-10)
- Ask specificity (1-10)
- Friction level (how hard to respond, 1-10)
- Urgency signals (genuine vs fake)
- Recipient context clues

Output:
RESPONSE PROBABILITY: X%
ESTIMATED TIME: [range]
FRICTION SCORE: X/10
TOP 3 IMPROVEMENTS TO BOOST RESPONSE:
1. [specific fix]
2. [specific fix]
3. [specific fix]

Message: [PASTE HERE]"""
        )

        display_prompt(
            title="Email Triage Decision Tree",
            description="Deciding which emails need real responses versus quick replies, helping you prioritize and respond efficiently",
            when_to_use="Use this when processing your inbox to quickly determine which emails require full responses, quick acknowledgments, delegation, or can be archived",
            prompt_text="""Triage this email and tell me the minimum viable response.

EMAIL: [PASTE]

Analyze:
- REQUIRES ACTION: Yes/No
- URGENCY: High/Medium/Low + why
- RESPONSE TYPE: [Full response / Quick ack / Delegate / Archive]
- ESTIMATED TIME TO HANDLE: [minutes]
- DEFER UNTIL: [date/condition if not now]

If response needed, provide:
1. QUICK VERSION: [2-3 sentences]
2. THOROUGH VERSION: [if stakes are high]
3. DELEGATION TEMPLATE: [if someone else should handle]

Choose the path that minimizes my time while managing relationship."""
        )

    # Subcategory 2: Meetings, Calendar & Status
    with st.expander("📅 **Meetings, Calendar & Status**", expanded=False):
        st.caption("3 prompts for meeting notes, calendar management, and status updates")

        display_prompt(
            title="Meeting Note Structurer",
            description="Converting messy meeting notes into structured, searchable format with clear sections for decisions, action items, open questions, and context",
            when_to_use="Use this after meetings to structure raw notes into a format that's easy to reference later",
            prompt_text="""Convert these messy meeting notes into structured, searchable format.

Required sections:
- DECISIONS MADE: [bulleted, no discussion]
- ACTION ITEMS: [owner + deadline + specific verb]
- OPEN QUESTIONS: [numbered, with context]
- BACKGROUND CONTEXT: [2-3 sentences max]
- NEXT MEETING FOCUS: [one sentence]

Rules:
- Every action item = [Name] will [concrete verb] [specific thing] by [date]
- No "we discussed" or "we talked about"
- If decision was made, state it declaratively
- If no decision, it goes in OPEN QUESTIONS

Raw notes: [PASTE YOUR CHAOS]"""
        )

        display_prompt(
            title="Calendar Tetris Optimizer",
            description="Proposing meeting times efficiently across multiple timezones and attendees, eliminating endless email tennis",
            when_to_use="Use this when scheduling meetings with multiple people across different timezones",
            prompt_text="""I need to schedule a [duration] meeting with [number] people across [timezones].

My constraints:
- Available windows: [paste your free slots]
- Timezone: [yours]
- Other attendees in: [their timezones]

Generate:
1. Top 3 time options (with timezone conversions shown for each person)
2. Doodle/Calendly text pre-written
3. One-sentence calendar invite description
4. Backup async option if scheduling fails

Context for meeting: [brief description]"""
        )

        display_prompt(
            title="Status Update Auto-Generator",
            description="Generating weekly status updates from raw inputs, turning chaos into structured updates that highlight outcomes, blockers, and next steps",
            when_to_use="Use this weekly to generate status updates for managers, teams, or stakeholders",
            prompt_text="""Generate my weekly status update from these raw inputs.

COMPLETED THIS WEEK: [bullet list or sentences]
IN PROGRESS: [what you're working on]
BLOCKERS/NEEDS: [obstacles or requests]
NEXT WEEK FOCUS: [planned work]

Output format matching company style:
- 3 bullets max per section
- Each bullet = outcome achieved, not activities performed
- Blockers stated as "Need X to unblock Y" not "waiting on..."
- No hedging language
- Highlight wins without bragging

Generate both: (1) Full version (2) Slack-length version"""
        )

    # Subcategory 3: Expenses, Forms & Bureaucracy
    with st.expander("💳 **Expenses, Forms & Bureaucracy**", expanded=False):
        st.caption("7 prompts for expense reports, forms, tickets, SOPs, and administrative tasks")

        display_prompt(
            title="Expense Goblin & Admin Log Condenser",
            description="Expense reports, justifications for finance, remembering what that random taxi was for",
            when_to_use="Use this when processing expense reports and transaction logs to convert messy lines into clean, finance-friendly tables with justifications",
            prompt_text="""Master Expense Processor:

ROLE: You are my Expense Goblin.

GOAL: Turn messy transaction descriptions, receipts, and notes into a clean, finance-friendly expense table with justifications.

COMPANY RULES (customize these):
- Main categories: Travel, Accommodation, Meals, Software, Training, Office, Other
- Default policy: avoid personal-looking items; flag anything ambiguous.
- Typical trip pattern or recurring events: [e.g. "monthly trips to London client"]

INPUT FORMAT: I will paste raw lines in any mix of these forms: Bank/credit card export lines, Freeform text like "Uber ~23€ to airport Wed night", Calendar events (meeting with client X at restaurant Y), Photos/receipt text transcribed manually

INSTRUCTIONS:
1) Parse each line and infer: Date (or best guess from context), Category (from the list; if unsure, pick best guess and add "?"), Vendor / Place, Short Description (human friendly), Amount (if given; else leave blank and mark "TBD"), Currency (if obvious; else assume [your default])

2) For EACH item, write a BORING business justification in 1–2 sentences: Third-person, neutral, finance-friendly. Example: "Client lunch with ACME Corp to review Q2 roadmap."

3) Flag items that: Look personal, Look like duplicates, Conflict with the "company rules" above

4) Output as a MARKDOWN TABLE with columns: ID, Date, Category, Vendor / Place, Short Description, Amount, Currency, Business Justification, Flags

5) At the end, list: "Items to double-check" (IDs with flags), A one-paragraph summary of any patterns or potential policy issues.

STYLE: Conservative assumptions, Clear, compliance-first language, No creative storytelling — just enough detail to pass audit.

Daily Use:
"You are still my Expense Goblin. Here are the raw lines for this period: [Paste exports, notes, messy text… one per line or paragraph.] Process everything according to your instructions and give me the table + summary."."""
        )

        display_prompt(
            title="Expense Report Speedrun",
            description="Quickly converting receipts and transactions into expense report format with proper categorization, business purpose, and compliance flags",
            when_to_use="Use this when processing individual receipts or transactions for expense reports",
            prompt_text="""Convert this receipt/transaction into expense report format.

[ATTACH IMAGE or PASTE: Merchant, amount, date, items]

Generate:
- CATEGORY: [accounting department's category name]
- BUSINESS PURPOSE: [one sentence, specific]
- PROJECT/CLIENT CODE: [if applicable, ask me]
- REIMBURSABLE: Yes/No + rationale
- RED FLAGS: [anything that might get rejected]

If missing info, ask me ONE clarifying question max."""
        )

        display_prompt(
            title="Template Normalizer for Forms & Bureaucracy",
            description="Security and risk questionnaires, vendor onboarding forms, repeated 'describe your project' fields, standardized via a master description pack",
            when_to_use="Use this when you need to fill out repetitive forms and questionnaires; run the master setup once per role/project and reuse for months",
            prompt_text="""Master Description Pack:

ROLE: You are my Template Normalizer.

GOAL: Create a reusable "Master Description Pack" of my role/team/project and then adapt it to any new form/questionnaire I receive.

PART 1 — MASTER DESCRIPTION PACK:
Based on the context I provide, create:
1) Three standard descriptions of my work: 50-word summary, 150-word summary, 300-word summary
2) Two risk/control lists: 5 key risks associated with my work/project, 5 key controls/mitigations already in place
3) A basic data-handling statement: What data we touch, How we protect it, How long we retain it, Who has access

STYLE: Neutral, policy-sounding, corporate-compliant. Avoid buzzwords; be clear and precise.

PART 2 — FORM ADAPTER (to be used later):
When I paste a new form with questions, you will:
1) Read each question carefully.
2) Decide which elements of the Master Pack are relevant.
3) Draft a direct answer that: Feels tailored to the question, Stays consistent with the Master Pack
4) Output as a MARKDOWN TABLE: Question #, Original Question, Draft Answer, Source elements from the Master Pack (short note)

ACKNOWLEDGE: First, ask me for the raw context for the Master Pack: My role & team, Main project(s), Typical stakeholders, Any regulatory frameworks we care about (e.g. GDPR, SOC2, etc.)

Daily Form Adapter:
"You are my Template Normalizer using the existing Master Description Pack below. MASTER PACK: [Paste the 50/150/300 word summaries, risks/controls, data-handling blurb.] NEW FORM QUESTIONS: [Paste questions exactly as written, with numbers if available.] For each question, draft a clear answer in the markdown table format you defined: Question #, Original Question, Draft Answer, Source elements from the Master Pack"."""
        )

        display_prompt(
            title="Ticket & Access Request Drafter",
            description="Writing tickets for IT/Ops/Facilities/Access with 'just enough' information so they don't bounce it back",
            when_to_use="Use this when you need to create tickets for IT, operations, facilities, or access requests in tools like JIRA or ServiceNow",
            prompt_text="""Ticket Template Engine:

ROLE: You are my Ticket & Access Request Drafter.

GOAL: Turn my rough description of a problem or request into clean, complete tickets for tools like JIRA, ServiceNow, etc.

TICKET TYPES I COMMONLY USE (customize):
Access request (tool/system/folder), Incident/bug, Change request, Service/operations request, Facilities/office issue

STANDARD FIELDS (assume these exist):
Summary / Title, Type (from list above), Description, Steps taken / Troubleshooting, Impact / Urgency, Attachments / Evidence (described in text), Suggested Priority (Low/Medium/High/Critical)

INSTRUCTIONS:
1) When I paste my rough description, first: Infer the ticket type, Ask any ONE clarifying question ONLY if absolutely necessary, Otherwise proceed directly

2) For each ticket needed (maybe multiple in one paste): Create a filled-out template with the fields above,
   Make Summary: 8–12 words, specific, no fluff,
   Make Description: 2–4 short paragraphs: context, what's happening, what should happen instead,
   Steps taken: bullet list, even if it's just "restarted machine / relogged",
   Impact/Urgency: short paragraph tying issue to deadlines/customers/risk,
   Suggested Priority: infer conservatively

3) Output format: "Ticket #1", Fields as a bullet list (Summary, Type, Description, etc.), Then "Ticket #2", etc.

4) At the end, produce a MARKDOWN TABLE summary: Ticket #, Summary, Type, Suggested Priority, Impact (1-sentence)

STYLE: Clear and polite, Assume the IT/Ops person is overloaded and skims

ACKNOWLEDGE: Say: "Paste your messy description of what's wrong / what you need, including any screenshots described in words. I'll draft the ticket(s)."

Daily Use:
"You are still my Ticket & Access Request Drafter. Here's what I need to raise as ticket(s): [Paste messy description, chat logs, errors, etc.] Draft all needed tickets and the summary table now."."""
        )

        display_prompt(
            title="SOP Snap-Cloner",
            description="Turning repeated explanations of a process into reusable Standard Operating Procedures (SOPs) and mini-playbooks",
            when_to_use="Use this when you need to document a recurring task or process that you repeatedly explain",
            prompt_text="""SOP Builder:

ROLE: You are my SOP Snap-Cloner.

GOAL: Turn my messy explanation of a recurring task into a simple, reusable Standard Operating Procedure (SOP) in human language.

SOP FORMAT:
Every SOP you create must have:
1) Title
2) When to Use This (2–3 bullets)
3) Pre-requisites (accounts, tools, approvals)
4) Step-by-Step Instructions (Numbered list, each step 1–3 sentences)
5) Common Mistakes & How to Avoid Them (3–7 bullets)
6) Checklist Summary (5–10 short checkboxes)
7) Template Snippets (if relevant) — Reusable text I can copy (emails, ticket descriptions, etc.)

INPUT FORMAT:
I will paste:
How I currently do the task (in bullets or paragraphs),
Any screenshots described in words,
Any constraints (tools, policies, timing)

INSTRUCTIONS:
1) Read my messy description and:
   Extract the core sequence of steps,
   Infer missing but obvious steps,
   Flag any ambiguities

2) Build a clean SOP using the exact format above.

3) In "Common Mistakes", include:
   Where people usually get blocked,
   Things that create rework for me or other teams

4) In "Template Snippets", create:
   If I mentioned external communication: an email/DM template,
   If I mentioned internal tickets: a ticket description template,
   If not relevant, skip this section and say: "No template snippets needed."

STYLE: Simple, non-bureaucratic, but still professional, Assume a smart colleague who has never seen this task before

ACKNOWLEDGE: When ready, say: "Paste your messy description of ONE recurring task you want to turn into an SOP."

Daily Use:
"You are still my SOP Snap-Cloner. Here is the recurring task I want to document: [Paste messy steps, comments, frustrations, screenshots described in words, etc.] Create the full SOP in the defined format."."""
        )

        display_prompt(
            title="File & Folder Naming Sheriff",
            description="Stopping chaotic filenames and versioning hell by defining and enforcing simple naming and folder structures",
            when_to_use="Use this to establish and enforce consistent file and folder naming conventions and normalize existing files",
            prompt_text="""Naming & Structure Policy:

ROLE: You are my File & Folder Naming Sheriff.

GOAL: Define and enforce a simple, consistent way to name files and organize folders so future-me and colleagues can find things.

NAMING CONVENTION (customize with me):
Propose a base convention like: [PROJECT]_[AREA]_[DESCRIPTION]_[YYYYMMDD]_v[##].[ext]

Examples:
"CLIENTX_Finance_ForecastTemplate_20251115_v01.xlsx",
"INTERNAL_IT_S4MigrationPlan_20250930_v03.docx"

FOLDER LOGIC (high-level):
Top level by: [e.g. Client / Internal / Region / Product — we'll define it],
Then by: [Project or Year],
Then by: [Docs / Data / Presentations / Admin]

INSTRUCTIONS — PART 1 (Design Policy Once):
1) Ask me a few questions:
   Typical projects/clients/products?,
   Main document types?,
   What tools we store files in (SharePoint, Drive, etc.)?

2) Design:
   A naming convention (with 5–10 concrete examples),
   A folder structure template (like a tree)

3) Output:
   A) "Quick Rules" section (5–7 bullets),
   B) "Examples" section,
   C) "Folder Template" as an indented list

INSTRUCTIONS — PART 2 (Ongoing Use):
When I paste a list of messy filenames and locations:
1) For each file:
   Infer project/area/description/date/version from context or filename,
   Propose a new name following the convention,
   Suggest a target folder path based on the folder template

2) Output as a MARKDOWN TABLE:
   Current Name, Current Location (if given), Suggested New Name, Suggested New Folder Path, Notes (if any guess/assumption was made)

STYLE: Conservative guesses; flag anything that's ambiguous, Do NOT invent fake project names — always use my wording

ACKNOWLEDGE: First, help me design the convention and template. Then, tell me: "Paste a list of filenames and locations to normalize."

Daily Use:
"You are my File & Folder Naming Sheriff using the agreed naming policy. Here are the current files to normalize: [Paste list like: 'forecast new v3 FINAL.xlsx – in /Desktop/misc', 'presentation_clientX-sept.pptx – in /Shared/Old'] For each, output the markdown table with: Current Name, Current Location, Suggested New Name, Suggested New Folder Path, Notes"."""
        )

        display_prompt(
            title="Jargon Assassin",
            description="Eliminating corporate buzzword bloat and replacing abstract terms with concrete specifics",
            when_to_use="Use this when your writing is filled with corporate jargon and buzzwords and you need clarity and specificity",
            prompt_text="""Kill the jargon in this text. Replace every abstract/corporate term with concrete specifics.

Forbidden words: leverage, synergy, utilize, implement, ecosystem, solution, strategic, robust, seamless, innovative, transform, optimize, streamline, empower, enable, facilitate

For each kill, show:
- KILLED: [jargon phrase]
- BECAUSE: [why it's meaningless here]
- REPLACED WITH: [concrete alternative]

Text to de-bullshit: [PASTE HERE]

Final output: Cleaned version + kill count"""
        )


def render_prompt_templates():
    """Render the Prompt Templates tool"""

    st.title("📚 Prompt Templates")
    st.write("23 ready-to-use prompts for enterprise workflows - just copy and paste")

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
