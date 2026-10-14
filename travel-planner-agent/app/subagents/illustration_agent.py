"""Destination Illustration Specialist Sub-Agent."""

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

from app.config import SUBAGENT_MODEL
from app.tools.image_generator import illustrate_destination

ILLUSTRATION_INSTRUCTION = """
You are the Travel Illustration Specialist Agent.

Your responsibilities:
1. When asked to illustrate destinations or attractions:
   - Identify the 1 to 3 most visually iconic landmarks from the itinerary (e.g. Space Needle, Pike Place Market, Eiffel Tower).
   - Use the `illustrate_destination` tool to generate high-resolution postcard imagery.
   - Craft evocative visual descriptions for the scene (e.g., golden hour lighting, architectural drama, lively marketplace atmosphere).
2. Report the generated image links, captions, and visual highlights so they can be embedded in the final travel guide.
"""

illustration_agent = Agent(
    name="illustration_agent",
    model=Gemini(
        model=SUBAGENT_MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=ILLUSTRATION_INSTRUCTION,
    description="Generates photorealistic illustrations and postcard images of key travel destinations and landmarks.",
    tools=[illustrate_destination],
)
