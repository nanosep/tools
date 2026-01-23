# ClarityCrew Tools

A local Streamlit application hosting 6 AI-powered prompt generation tools, powered by Anthropic's Claude API.

## Overview

ClarityCrew Tools provides an intuitive interface for generating high-quality prompts using advanced AI techniques. The application runs locally and uses a single Anthropic API key managed securely in the backend.

### Tools Included
- Decision Storm
- Advanced Techniques
- Chain and Bundle
- Correlation Explainer
- Creative Thinking
- Image Prompt Generator

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
│   └── (tool modules)
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
2. Click "Test API Connection" to verify your API key is working
3. Navigate through the tools (Phase 2 - coming soon)

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

### Phase 1 (Current)
- ✅ Project structure
- ✅ Backend API client
- ✅ Basic Streamlit interface
- ✅ API connectivity test

### Phase 2 (Next)
- Migrate tools from JSX/HTML artifacts
- Implement 6 prompt generation tools
- Add navigation between tools

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
