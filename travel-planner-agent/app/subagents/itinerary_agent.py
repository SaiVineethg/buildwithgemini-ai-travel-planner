"""Itinerary and Duration Specialist Sub-Agent."""

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

from app.config import SUBAGENT_MODEL
from app.tools.city_guide import calculate_city_duration

ITINERARY_INSTRUCTION = """
You are the Itinerary & Duration Specialist Agent for the AI Travel Planner.

Your responsibilities:
1. When asked about a city, always determine:
   - Exactly how many days are required to cover the must-visit sights without feeling rushed.
   - Explain the pacing tiers: Relaxed (2-3 sights/day), Balanced (3-4 sights/day), or Packed (whirlwind highlights).
   - Use the `calculate_city_duration` tool to retrieve accurate attraction data and geographical clusters.
2. Structure a clear, day-by-day itinerary:
   - Group attractions geographically by district/neighborhood to eliminate unnecessary transit.
   - For each day, include:
     * Morning activity and landmark
     * Midday local lunch/food recommendation
     * Afternoon activity and landmark
     * Evening dinner, sunset viewpoint, or night atmosphere
   - Include practical tips (opening hours advice, ticket booking recommendations).
3. Be specific, enthusiastic, and realistic about travel times.
"""

itinerary_agent = Agent(
    name="itinerary_agent",
    model=Gemini(
        model=SUBAGENT_MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=ITINERARY_INSTRUCTION,
    description="Calculates required days to cover must-visit city attractions and assembles structured day-by-day itineraries.",
    tools=[calculate_city_duration],
)
