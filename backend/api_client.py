import os
import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv
import time

# Load .env for local development only
load_dotenv()

def get_api_key():
    """
    Get API key from Streamlit secrets (deployment) or environment variable (local)

    Priority:
    1. Streamlit secrets (for deployment on Streamlit Cloud)
    2. Environment variable (for local development)

    Returns:
        str: API key

    Raises:
        ValueError: If API key is not found
    """
    # Try Streamlit secrets first (deployment)
    try:
        if hasattr(st, 'secrets') and 'ANTHROPIC_API_KEY' in st.secrets:
            return st.secrets['ANTHROPIC_API_KEY']
    except Exception:
        pass

    # Fallback to environment variable (local development)
    api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not found. "
            "For local development: Add it to .env file. "
            "For Streamlit Cloud: Add it in Settings → Secrets"
        )

    return api_key

def call_anthropic(system_prompt, user_message, max_tokens=1000):
    """
    Call Anthropic API with error handling

    Args:
        system_prompt (str): System-level instructions for Claude
        user_message (str): User's input/query
        max_tokens (int): Maximum tokens in response (default: 1000)

    Returns:
        str: Text content from Claude's response

    Raises:
        Exception: If API call fails with descriptive error message
    """
    try:
        # Get API key
        api_key = get_api_key()

        # Initialize client
        client = Anthropic(api_key=api_key)

        # Add 1-second delay to avoid rate limits
        time.sleep(1)

        # Make API call
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        # Extract text from response
        return message.content[0].text

    except ValueError as e:
        # API key not found
        raise Exception(str(e))

    except Exception as e:
        # Other API errors
        error_msg = str(e)
        if "authentication" in error_msg.lower():
            raise Exception("Authentication failed. Please check your API key.")
        elif "rate_limit" in error_msg.lower():
            raise Exception("Rate limit exceeded. Please wait a moment and try again.")
        elif "overloaded" in error_msg.lower():
            raise Exception("Anthropic API is currently overloaded. Please try again in a moment.")
        else:
            raise Exception(f"API call failed: {error_msg}")

def test_api_connection():
    """
    Test API connection and return status

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        response = call_anthropic(
            system_prompt="You are a helpful assistant.",
            user_message="Respond with just the word 'Connected' if you receive this.",
            max_tokens=10
        )
        return True, f"✅ API Connection Successful!\n\nResponse: {response}"
    except Exception as e:
        return False, f"❌ API Connection Failed\n\nError: {str(e)}"
