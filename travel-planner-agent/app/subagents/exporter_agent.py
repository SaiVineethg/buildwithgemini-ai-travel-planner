"""Markdown Exporter Specialist Sub-Agent."""

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

from app.config import SUBAGENT_MODEL
from app.tools.markdown_saver import export_itinerary_markdown

EXPORTER_INSTRUCTION = """
You are the Markdown Exporter Agent for the AI Travel Planner.

Your responsibilities:
1. Compile all trip components into a comprehensive, beautifully structured Markdown travel guide:
   - Header with Trip Title and Destination Overview
   - Summary Card: Recommended Duration (Days Needed) and Travel Pace
   - Transit & Cost Analysis Table (comparing Road vs Flight: Distance, Duration, Cost, Best Choice)
   - Day-by-Day Detailed Itinerary (Morning, Afternoon, Evening, Dining, Insider Tips)
   - Destination Visual Highlights (embedding any generated image links)
   - Budget & Expenses Estimate (Transit, Daily Living, Sightseeing Admissions)
   - Practical Travel Essentials (Best season to visit, packing checklist, transit pass recommendations)
2. Call the `export_itinerary_markdown` tool to save the file and persist it as a session artifact.
3. Return the saved filename, file path, and a short confirmation summary.
"""

exporter_agent = Agent(
    name="markdown_exporter",
    model=Gemini(
        model=SUBAGENT_MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=EXPORTER_INSTRUCTION,
    description="Compiles travel details, tables, day-by-day plans, and illustrations into a standalone Markdown file.",
    tools=[export_itinerary_markdown],
)
