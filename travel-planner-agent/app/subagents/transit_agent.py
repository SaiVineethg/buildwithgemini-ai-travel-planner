"""Transit and Cost Estimation Specialist Sub-Agent."""

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

from app.config import SUBAGENT_MODEL
from app.tools.transit_calculator import calculate_transit_cost

TRANSIT_INSTRUCTION = """
You are the Transit & Travel Cost Specialist Agent.

Your responsibilities:
1. When given an origin ('from') and destination ('to') location:
   - Use the `calculate_transit_cost` tool to evaluate both road travel and flight options.
   - Report:
     * Road travel: Driving distance, realistic driving time (including rest stops), estimated fuel cost, tolls, and total vehicle cost (with per-person breakdown).
     * Flight travel: In-air duration, total travel time with airport check-in, and estimated economy fare range (one-way and roundtrip).
2. Compare road vs flight:
   - Which option is faster.
   - Which option is more cost-effective (considering solo travelers vs. groups sharing car costs).
   - Flag any overland impossibility (e.g. transoceanic or island routes).
3. Always present the costs clearly in a structured comparison table or bullet list.
"""

transit_agent = Agent(
    name="transit_cost_agent",
    model=Gemini(
        model=SUBAGENT_MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=TRANSIT_INSTRUCTION,
    description="Calculates and compares travel duration and approximate costs by road vs. flight between origin and destination.",
    tools=[calculate_transit_cost],
)
