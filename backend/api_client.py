import os
import time
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Anthropic client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def call_anthropic(system_prompt, user_message, max_tokens=1000):
    """
    Call Anthropic API with system and user prompts.

    Args:
        system_prompt (str): The system prompt to guide the model
        user_message (str): The user's input message
        max_tokens (int): Maximum tokens in response (default: 1000)

    Returns:
        str: The text content from the API response

    Raises:
        Exception: If API call fails
    """
    try:
        # Add 1-second delay to avoid rate limits
        time.sleep(1)

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        # Return only the text content
        return response.content[0].text

    except Exception as e:
        raise Exception(f"API call failed: {str(e)}")
