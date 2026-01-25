# 🛠️ ClarityCrew Tools

> **Version 1.0** | Powered by Claude Sonnet 4.5 | All 6 Tools Complete ✅

A local Streamlit application hosting 6 AI-powered prompt generation tools for strategic thinking and creative problem-solving.

## 📖 Table of Contents

- [Overview](#overview)
- [Tools Included](#tools-included)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Troubleshooting](#troubleshooting)
- [API Usage](#api-usage)
- [Project Structure](#project-structure)
- [Development Status](#development)

---

## Overview

ClarityCrew Tools provides an intuitive interface for generating high-quality prompts using advanced AI techniques. The application runs **100% locally** and uses a single Anthropic API key managed securely in the backend.

**Tech Stack:**
- **Frontend:** Streamlit (Python web framework)
- **AI Model:** Claude Sonnet 4.5 (`claude-sonnet-4-20250514`)
- **API:** Anthropic Messages API
- **Deployment:** Local only (localhost:8501)

---

## Tools Included

| # | Tool | Description | API Calls |
|---|------|-------------|-----------|
| 1 | 🔀 **Decision Storm** | Generate 2-6 strategic perspectives using different analytical lenses | 2-6 per run |
| 2 | 🔗 **Chain, Bundle & Inception** | Create sequential chains, parallel bundles, or meta-prompts | 1-3 per run |
| 3 | 🚀 **Advanced Techniques** | Apply 11 expert prompting techniques to your challenge | 1 per run |
| 4 | 🎨 **Creative Thinking** | Generate prompts using 24 creative methods, adapted by department | 1 per run |
| 5 | 🖼️ **Image Prompt Generator** | Craft optimized prompts for AI image generation (text + JSON output) | 1 per run |
| 6 | 🔬 **Correlation Explainer** | Educational tool teaching 8 types of correlation vs causation | 0 (no API) |

**All 6 tools are active and fully functional** ✅

## Project Structure

The application follows a clean, modular architecture:

```
Tools/
├── .env.example              # Template for API key configuration
├── .gitignore               # Python + Streamlit ignores
├── README.md                # This file
├── requirements.txt         # Python dependencies (Streamlit, Anthropic, python-dotenv)
├── app.py                   # Main entry point with navigation
│
├── backend/                 # API and shared utilities
│   ├── __init__.py
│   ├── api_client.py       # Anthropic API wrapper with rate limiting
│   └── prompts.py          # Shared system prompts (if any)
│
├── tools/                   # Individual tool modules
│   ├── __init__.py
│   ├── decision_storm.py           # 🔀 Decision Storm
│   ├── chain_bundle_inception.py   # 🔗 Chain, Bundle & Inception
│   ├── advance_techs.py            # 🚀 Advanced Techniques
│   ├── creative_thinking.py        # 🎨 Creative Thinking
│   ├── image_prompt.py             # 🖼️ Image Prompt Generator
│   └── correlation_explainer.py    # 🔬 Correlation Explainer
│
└── artifacts/              # Reference files (original React/HTML versions)
    ├── Decision_Storm.jsx
    ├── Advance_Techs.html
    ├── Chain_and_Bundle.html
    ├── correlation_explainer.jsx
    ├── creative_thinking.jsx
    └── image_prompt.jsx
```

**Key Files:**
- **`app.py`** - Sidebar navigation and tool routing
- **`backend/api_client.py`** - Handles all Anthropic API calls with error handling and rate limiting
- **`tools/*.py`** - Self-contained tool modules, each with a `render_*()` function

---

## Quick Start

### Prerequisites

- **Python 3.8+** installed on your system
- **Anthropic API key** - [Get one here](https://console.anthropic.com/) (free tier available)
- **10 minutes** for setup

### Installation Steps

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/nanosep/tools.git
   cd tools
   ```

2. **Create a virtual environment**:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   - Copy `.env.example` to `.env`:
     ```bash
     # On Windows
     copy .env.example .env

     # On macOS/Linux
     cp .env.example .env
     ```
   - Open `.env` and add your Anthropic API key:
     ```
     ANTHROPIC_API_KEY=sk-ant-api03-...
     ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**:
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in your terminal

---

## Usage Guide

### Getting Started

1. **Launch the application:**
   ```bash
   streamlit run app.py
   ```

2. **Access the interface:**
   - Browser opens automatically at `http://localhost:8501`
   - Use the sidebar to navigate between tools

3. **Test API connection:**
   - Go to Home page
   - Click "Test API Connection" button
   - Verify successful response

### Tool-Specific Instructions
**🔀 Decision Storm:**
   - Enter your scenario or decision
   - Choose 2-6 perspectives
   - Each perspective analyzes through a different lens (Risk, Opportunity, Resource, Timeline, Stakeholder, Strategic)
   - Results generate sequentially with progress indicators

**🔗 Chain, Bundle & Inception:**
   - Enter your goal or task
   - Choose method: Chain (sequential steps), Bundle (parallel approaches), Inception (meta-prompts), or All Three
   - **Chain:** 3-5 step workflow (Decompose → Analyze → Evaluate → Refine → Test)
   - **Bundle:** 3-7 parallel alternatives using different techniques
   - **Inception:** Meta-prompts that generate more prompts on-demand

**🚀 Advanced Techniques:**
   - Enter your challenge or goal
   - Select 3-5 techniques from 11 expert methods
   - Generates 5 specialized prompts, each demonstrating a different technique
   - Techniques: Multi-Persona Debate, Emotional Tipping, Chain-of-Symbol, Socratic Mirroring, Adversarial Red-Teaming, Dynamic Tone Morphing, and more

**🎨 Creative Thinking:**
   - Enter your creative challenge
   - Select 1-5 methods from 24 options across 6 categories (Divergent, Convergent, Lateral, Collaborative, Reframing, Structured)
   - Choose your department (Sales, Product, Operations, HR, etc.) for customized adaptation
   - Methods include: Brainstorming, SCAMPER, Six Thinking Hats, Five Whys, Mind Mapping, TRIZ, and more

**🖼️ Image Prompt Generator:**
   - **Step 1:** Select art category (7 options: Fine Art, Photography, Digital Art, Fantasy, 3D Rendering, Concept Art, Abstract)
   - **Step 2:** Choose subcategory (42 total options with artist references)
   - **Step 3:** Add 0-3 thematic elements (Light, Scale, Color, Composition, Material, Narrative, Temporal)
   - **Step 4:** Enter your subject description
   - **Output:** Dual format - Text prompt (30-50 words, copy-paste ready) + JSON metadata
   - Compatible with: DALL-E, Midjourney, Stable Diffusion, and other AI image generators

**🔬 Correlation Explainer:**
   - Educational tool (no API calls required)
   - Explore 8 correlation types with detailed explanations
   - Types covered: Direct Causation, Reverse Causation, Confounding Variable, Bidirectional, Coincidental, Selection Bias, Mediating Variable, Spurious
   - Learn testing methodologies, common mistakes, and historical case studies
   - Interactive navigation with visual diagrams and probability meters

---

## API Usage

### Cost & Rate Limits

Each tool makes a different number of API calls per generation:

| Tool | API Calls | Notes |
|------|-----------|-------|
| Decision Storm | 2-6 per run | One call per perspective selected |
| Chain/Bundle/Inception | 1-3 per run | 1 per method (Chain=1, Bundle=1, Inception=1, All=3) |
| Advanced Techniques | 1 per run | Single generation creates 5 prompts |
| Creative Thinking | 1 per run | Single generation for all selected methods |
| Image Prompt Generator | 1 per run | Generates both text and JSON outputs |
| Correlation Explainer | **0 calls** | Fully local/educational, no API required |

**Rate Limiting:** All tools implement 1-second delays between sequential API calls to avoid rate limits.

**Model Used:** `claude-sonnet-4-20250514` (Claude Sonnet 4.5)

**Token Usage:** Most generations use 1000-4000 tokens per call depending on complexity.

---

## Troubleshooting

### API Connection Fails
- **Problem**: "API call failed" error when testing connection
- **Solutions**:
  - Verify your `.env` file exists in the project root
  - Check that `ANTHROPIC_API_KEY` is set correctly in `.env`
  - Ensure your API key is valid and has available credits
  - Check your internet connection

### Module Import Errors
- **Problem**: `ModuleNotFoundError` when running the app
- **Solutions**:
  - Ensure virtual environment is activated
  - Run `pip install -r requirements.txt` again
  - Verify you're in the correct directory

### Streamlit Won't Start
- **Problem**: Command not found or port already in use
- **Solutions**:
  - Ensure Streamlit is installed: `pip list | grep streamlit`
  - Try a different port: `streamlit run app.py --server.port 8502`
  - Kill any existing Streamlit processes

### Rate Limit Errors
- **Problem**: Too many API requests
- **Solution**: The app includes a 1-second delay between calls, but if you hit limits, wait a few minutes before retrying

## Development

### Phase 1 (Completed)
- ✅ Project structure
- ✅ Backend API client
- ✅ Basic Streamlit interface
- ✅ API connectivity test

### Phase 2 (Completed)
- ✅ Decision Storm tool migrated and active
- ✅ Chain, Bundle & Inception tool implemented
- ✅ Advanced Techniques tool implemented
- ✅ Sidebar navigation implemented
- ✅ Sequential API calling with progress indicators
- ✅ XML parsing with fallback logic
- ✅ Technique selection UI with validation

### Phase 3 (Completed - 100% ✅)
- ✅ Creative Thinking tool implemented (24 methods, 6 categories, 18 departments)
- ✅ Image Prompt Generator implemented (7 categories, 42 subcategories, 7 thematic elements)
- ✅ Dual output format (text prompt + JSON metadata)
- ✅ Category-organized taxonomy with subcategory details
- ✅ Correlation Explainer implemented (8 correlation types, educational content, no API calls)
- ✅ All 6 tools now active and complete

### Future Enhancements
- Export/save functionality
- Prompt templates library
- Cross-tool workflows

## Security Notes

- Never commit your `.env` file (it's in `.gitignore`)
- Keep your API key private
- The application runs locally only - no data is stored externally

## Support

For issues or questions:
- GitHub: https://github.com/nanosep/tools
- Check the troubleshooting section above

## License

This is a private project for local use.

---

## 📊 Project Info

**Version:** 1.0 (Complete)
**Last Updated:** January 2026
**Model:** Claude Sonnet 4.5 (`claude-sonnet-4-20250514`)
**Status:** ✅ All 6 tools operational

**Built with:**
- [Streamlit](https://streamlit.io/) - Python web framework
- [Anthropic Claude API](https://www.anthropic.com/) - AI model
- [Python](https://www.python.org/) 3.8+

**Credits:**
- Original React/HTML artifacts created with Claude
- Migrated to Streamlit local application
- Built for strategic thinking and creative problem-solving

---

*Made with ❤️ using Claude Code*
