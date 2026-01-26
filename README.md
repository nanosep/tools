# 🛠️ ClarityCrew Tools

> **Version 2.0 - Enterprise Edition** | Powered by Claude Sonnet 4.5 | All 5 Tools Complete ✅

An AI-powered Streamlit application optimized for enterprise consulting, M&A advisory, and strategic transformation engagements.

**Target Users:** Strategy consultants, M&A advisors, corporate development teams, transformation PMOs

## 📖 Table of Contents

- [Overview](#overview)
- [Tools Included](#tools-included)
- [Quick Start](#quick-start)
- [Deployment on Streamlit Cloud](#-deployment-on-streamlit-cloud)
- [Usage Guide](#usage-guide)
- [Troubleshooting](#troubleshooting)
- [API Usage](#api-usage)
- [Project Structure](#project-structure)
- [Development Status](#development)

---

## Overview

ClarityCrew Tools provides an intuitive interface for generating high-quality prompts using advanced AI techniques. The application can run **locally** or be deployed to **Streamlit Cloud** for access from anywhere. API keys are managed securely using environment variables (local) or Streamlit Secrets (cloud).

**Tech Stack:**
- **Frontend:** Streamlit (Python web framework)
- **AI Model:** Claude Sonnet 4.5 (`claude-sonnet-4-20250514`)
- **API:** Anthropic Messages API
- **Deployment:** Local (localhost:8501) or Streamlit Cloud

---

## 🎯 Tools Included

| # | Tool | Enterprise Use Cases | API Calls |
|---|------|---------------------|-----------|
| 1 | 🔗 **Chain, Bundle & Inception** | TSA strategies, integration planning, Day 1 readiness frameworks | 1-3 per run |
| 2 | 🚀 **Advanced Techniques** | ERP separation, working capital optimization, tax structures | 1 per run |
| 3 | 🎨 **Creative Thinking** | Synergy identification, talent retention, customer communication | 1 per run |
| 4 | 🌪️ **Decision Storm** | Build vs buy decisions, divestiture analysis, timeline strategies | 2-6 per run |
| 5 | 🖼️ **Image Prompt Generator** | Executive presentations, org charts, process flow diagrams | 3-5 per run |

**All 5 tools are active and optimized for M&A, carve-outs, and transformation work** ✅

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
│   ├── chain_bundle_inception.py   # 🔗 Chain, Bundle & Inception
│   ├── advance_techs.py            # 🚀 Advanced Techniques
│   ├── creative_thinking.py        # 🎨 Creative Thinking
│   ├── decision_storm.py           # 🌪️ Decision Storm
│   └── image_prompt.py             # 🖼️ Image Prompt Generator
│
└── artifacts/              # Reference files (original React/HTML versions)
    ├── Chain_and_Bundle.html
    ├── Advance_Techs.html
    ├── creative_thinking.jsx
    ├── Decision_Storm.jsx
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

## 🌐 Deployment on Streamlit Cloud

Deploy ClarityCrew Tools to the cloud for free and access it from anywhere.

### Prerequisites
- GitHub account
- Anthropic API key from https://console.anthropic.com/

### Deployment Steps

1. **Ensure your repository is on GitHub**
   - Repository: `nanosep/tools`
   - Branch: `main` (or your preferred branch)
   - Make sure all changes are committed and pushed

2. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io/
   - Sign in with your GitHub account
   - Click "New app"

3. **Configure deployment**
   - Repository: `nanosep/tools`
   - Branch: `main`
   - Main file path: `app.py`
   - (Optional) App URL: Choose custom subdomain

4. **Add API Key Secret**

   **CRITICAL:** Do this BEFORE the first deployment completes

   a. In your app settings, click "Secrets" (⚙️ icon)
   b. Add this configuration:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-api03-your-key-here"
   ```
   c. Click "Save"

5. **Deploy**
   - Click "Deploy!"
   - Wait 2-3 minutes for initial deployment
   - App will be available at your chosen URL

### Troubleshooting Deployment

**Error: "This file does not exist"**
- Solution: Ensure "Main file path" is set to `app.py` (not `streamlit_app.py`)

**Error: "ANTHROPIC_API_KEY not found"**
- Solution: Add your API key in Settings → Secrets (see step 4 above)

**Error: "Module not found"**
- Solution: Ensure all imports in `requirements.txt` are correct
- Run locally: `pip install -r requirements.txt` to verify

**App crashes on startup**
- Check logs in Streamlit Cloud dashboard
- Verify all tool files exist in `tools/` directory
- Ensure `__init__.py` files exist in `backend/` and `tools/`

### Local Development vs Deployment

**Local Development:**
- Uses `.env` file for API key
- File structure: Read from local filesystem
- Hot reload enabled

**Streamlit Cloud Deployment:**
- Uses Streamlit Secrets for API key
- File structure: Read from Git repository
- Automatic redeployment on git push

### Updating Deployed App

After making changes locally:
```bash
git add .
git commit -m "Your change description"
git push origin main
```

Streamlit Cloud will automatically detect changes and redeploy (takes ~2 minutes).

### Managing Secrets

**Never commit these files:**
- `.env` (local development)
- `.streamlit/secrets.toml` (local testing)

**Safe to commit:**
- `.env.example` (template)
- `.streamlit/secrets.toml.example` (template)
- `.streamlit/config.toml` (non-sensitive configuration)

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

**🔗 Chain, Bundle & Inception:**
   - Enter your M&A or transformation goal (e.g., "Design TSA exit strategy")
   - Choose method: Chain (sequential steps), Bundle (parallel approaches), Inception (meta-prompts), or All Three
   - **Chain:** 3-5 step workflow for complex analysis (Scope → Design → Price → Risk Mitigation)
   - **Bundle:** 3-7 parallel alternatives using different strategic frameworks
   - **Inception:** Meta-prompts for scenario planning and contingency frameworks
   - **Examples:** TSA strategies, integration planning, Day 1 readiness, stranded cost analysis

**🚀 Advanced Techniques:**
   - Enter your complex challenge (e.g., "ERP system separation for NewCo")
   - Select 3-5 techniques from 11 expert methods
   - Generates 5 specialized prompts, each demonstrating a different technique
   - Techniques: Multi-Persona Debate, Emotional Tipping, Chain-of-Symbol, Socratic Mirroring, Adversarial Red-Teaming, and more
   - **Examples:** ERP separation, working capital optimization, shared services migration, tax structures

**🎨 Creative Thinking:**
   - Enter your business challenge (e.g., "Accelerate TSA exit from 24 to 12 months")
   - Select 1-5 methods from 24 options across 6 categories
   - Choose your department (Strategy, Operations, HR, Communications, etc.) for customized adaptation
   - Methods include: Brainstorming, SCAMPER, Six Thinking Hats, Five Whys, Reverse Thinking, Scenario Planning
   - **Examples:** TSA acceleration, synergy identification, talent retention, customer communication

**🌪️ Decision Storm:**
   - Enter your high-stakes decision scenario (e.g., "Build vs buy vs partner for ERP")
   - Choose 2-6 perspectives
   - Each perspective analyzes through a different lens (Risk, Opportunity, Resource, Timeline, Stakeholder, Strategic)
   - Results generate sequentially with progress indicators
   - **Examples:** Build vs buy, divestiture vs IPO, timeline decisions, offshore vs nearshore

**🖼️ Image Prompt Generator:**
   - Generate professional visuals for executive presentations and strategic documents
   - **Step 1:** Enter your subject (e.g., "transformation roadmap visualization")
   - **Step 2:** Select 3-5 art styles from 42 options across 7 categories
   - **Step 3:** Add thematic elements (Compositional Tension, Color Psychology, etc.)
   - **Output:** 3-5 text prompts optimized for DALL-E, Midjourney, Stable Diffusion
   - **Examples:** Executive presentations, org charts, process flows

---

## API Usage

### Cost & Rate Limits

Each tool makes a different number of API calls per generation:

| Tool | API Calls | Notes |
|------|-----------|-------|
| Chain, Bundle & Inception | 1-3 per run | 1 per method (Chain=1, Bundle=1, Inception=1, All=3) |
| Advanced Techniques | 1 per run | Single generation creates 5 prompts |
| Creative Thinking | 1 per run | Single generation for all selected methods |
| Decision Storm | 2-6 per run | One call per perspective selected |
| Image Prompt Generator | 3-5 per run | One call per style variation selected |

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
- ✅ All 5 core tools active and complete

### Phase 4 - Enterprise Edition (Completed ✅)
- ✅ Navigation reordered for enterprise workflow
- ✅ All examples replaced with M&A, carve-out, transformation scenarios
- ✅ Enterprise terminology (TSA, Day 1, stranded costs, NewCo/RemainCo)
- ✅ Tool focus optimized for strategy consultants and M&A advisors
- ✅ Streamlit Cloud deployment configuration

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

**Version:** 2.0 - Enterprise Edition
**Last Updated:** January 2026
**Model:** Claude Sonnet 4.5 (`claude-sonnet-4-20250514`)
**Status:** ✅ All 5 tools operational
**Focus:** M&A, carve-outs, post-merger integration, transformation

**Built with:**
- [Streamlit](https://streamlit.io/) - Python web framework
- [Anthropic Claude API](https://www.anthropic.com/) - AI model
- [Python](https://www.python.org/) 3.8+

**Target Users:**
- Strategy consultants
- M&A advisors
- Corporate development teams
- Transformation PMOs
- Integration managers

**Credits:**
- Original React/HTML artifacts created with Claude
- Migrated to Streamlit application
- Optimized for enterprise consulting use cases

---

*Made with ❤️ using Claude Code*
