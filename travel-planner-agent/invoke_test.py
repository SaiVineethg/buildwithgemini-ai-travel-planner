"""Interactive end-to-end test script for the AI Travel Planner Agent."""

import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agent import root_agent
from app.config import IMAGES_DIR, ITINERARIES_DIR


def main():
    print("=" * 70)
    print("🌍 Starting AI Travel Planner Multi-Agent End-to-End Test")
    print("=" * 70)

    session_service = InMemorySessionService()
    session = session_service.create_session_sync(user_id="traveler_1", app_name="travel_planner")
    runner = Runner(agent=root_agent, session_service=session_service, app_name="travel_planner")

    default_india_prompt = (
        "I'm planning a trip from Delhi to Jaipur for 2 travelers. "
        "1. How many days are required to cover the must-visit places in Jaipur? "
        "2. What is the approx cost and time if traveling by road vs flight? "
        "3. Please assemble a 3-day itinerary, illustrate an iconic landmark (like Hawa Mahal or Amber Fort), and export it to markdown."
    )

    test_prompt = sys.argv[1] if len(sys.argv) > 1 else default_india_prompt

    print(f"\nUser Query:\n{test_prompt}\n")
    print("-" * 70)
    print("🤖 Agent Response:\n")

    message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=test_prompt)],
    )

    events = runner.run(
        new_message=message,
        user_id="traveler_1",
        session_id=session.id,
        run_config=RunConfig(streaming_mode=StreamingMode.NONE),
    )

    full_response = []
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text, end="", flush=True)
                    full_response.append(part.text)

    print("\n" + "=" * 70)
    print("🔍 Output Verification:")
    print("=" * 70)

    # Check generated images
    images = list(IMAGES_DIR.glob("*.png"))
    print(f"📸 Destination images generated in {IMAGES_DIR}: {len(images)}")
    for img in images:
        print(f"   - {img.name} ({img.stat().st_size} bytes)")

    # Check generated itineraries
    itineraries = list(ITINERARIES_DIR.glob("*.md"))
    print(f"\n📝 Markdown itineraries exported in {ITINERARIES_DIR}: {len(itineraries)}")
    for it in itineraries:
        print(f"   - {it.name} ({it.stat().st_size} bytes)")

    print("\n✅ Multi-Agent Travel Planner execution completed successfully!")


if __name__ == "__main__":
    main()
