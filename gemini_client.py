"""
Gemini API Client — thin wrapper around the Google GenAI SDK.
Exposes a single function: call_gemini()
"""

from google import genai
from google.genai import types


def call_gemini(system_prompt: str, message: str, api_key: str) -> str:
    """
    Send a message to Gemini with a system prompt and return the response text.

    Args:
        system_prompt: The system instruction that defines the agent's persona.
        message: The user message (scenario + any prior agent outputs).
        api_key: The user's Gemini API key.

    Returns:
        The model's text response.

    Raises:
        Exception: With a descriptive message if the API call fails.
    """
    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
            ),
        )

        return response.text

    except Exception as e:
        raise Exception(f"Gemini API call failed: {str(e)}") from e
