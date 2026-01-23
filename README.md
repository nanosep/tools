# ClarityCrew Tools

A local Streamlit application hosting 6 AI-powered prompt generation tools, powered by Anthropic's Claude API.

## Overview

ClarityCrew Tools provides an intuitive interface for generating high-quality prompts using advanced AI techniques. The application runs locally and uses a single Anthropic API key managed securely in the backend.

### Tools Included
- ✅ **Decision Storm** - Generate multiple strategic perspectives (Active)
- ✅ **Chain, Bundle & Inception** - Sequential/parallel/meta-prompts using 20 techniques (Active)
- 🔜 Advanced Techniques (Coming soon)
- 🔜 Correlation Explainer (Coming soon)
- 🔜 Creative Thinking (Coming soon)
- 🔜 Image Prompt Generator (Coming soon)

## Tech Stack
- **Frontend**: Streamlit
- **Backend**: Python
- **AI Model**: Claude Sonnet 4 (claude-sonnet-4-20250514)
- **Deployment**: Local only (localhost)

## Project Structure
```
Tools/
├── .env.example              # Template for API key
├── .gitignore               # Python + Streamlit ignores
├── README.md                # This file
├── requirements.txt         # Dependencies
├── app.py                   # Main Streamlit entry point
├── backend/
│   ├── __init__.py
│   ├── api_client.py       # Anthropic API wrapper
│   └── prompts.py          # System prompts storage
├── tools/
│   ├── __init__.py
│   ├── decision_storm.py           # Decision Storm tool
│   └── chain_bundle_inception.py   # Chain, Bundle & Inception tool
└── artifacts/              # Original JSX/HTML files
    ├── Decision_Storm.jsx
    ├── Advance_Techs.html
    ├── Chain_and_Bundle.html
    ├── correlation_explainer.jsx
    ├── creative_thinking.jsx
    └── image_prompt.jsx
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Setup Steps

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

## Usage

1. Launch the application using `streamlit run app.py`
2. Use the sidebar to navigate between tools
3. **Decision Storm**: Enter a scenario and generate 2-6 strategic perspectives
   - Each perspective analyzes your scenario through a different lens (Risk, Opportunity, Resource, etc.)
   - Results are generated sequentially and displayed incrementally
4. **Chain, Bundle & Inception**: Generate specialized prompts using 20 advanced techniques
   - **Chain**: Sequential 3-5 step workflow (Decompose → Analyze → Evaluate → Refine → Test)
   - **Bundle**: Parallel 3-7 alternative approaches using different techniques
   - **Inception**: Meta-prompts that generate more prompts on-demand
   - Choose individual methods or generate all three at once
5. Home page includes an API connectivity test

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

### Phase 2 (In Progress)
- ✅ Decision Storm tool migrated and active
- ✅ Chain, Bundle & Inception tool implemented
- ✅ Sidebar navigation implemented
- ✅ Sequential API calling with progress indicators
- ✅ XML parsing with fallback logic
- 🔜 Remaining 4 tools (Advanced Techniques, Correlation Explainer, etc.)

### Phase 3 (Planned)
- Add remaining 5 tools
- Enhanced UI/UX improvements
- Export/save functionality

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
