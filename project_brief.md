# My agent: AI Travel Planner Concierge

One-liner: An AI-powered travel planning concierge with Gemini 3.7 Flash, calculating city durations, road vs flight costs, generating landmark illustrations, and exporting custom markdown itineraries.

## What it does
- **City Duration Analysis**: Analyzes top must-visit attractions and recommends ideal stay length across relaxed, balanced, and packed paces.
- **Road vs Flight Transit Calculator**: Compares drive times, fuel/toll costs in INR/USD against airline fares and check-in overhead.
- **Multi-Agent Orchestration**: Built with Google ADK using an orchestrator (`travel_planner_main`) coordinating specialized sub-agents (`itinerary_agent`, `illustration_agent`, `markdown_exporter`).
- **Landmark Postcard Generation**: Illustrates iconic sights with photorealistic imagery.
- **Markdown Export**: Bundles structured itineraries into downloadable Markdown packages.
- **Wanderlust Web Interface**: FastAPI proxy on Cloud Run connecting browser users to Agent Engine over the A2A protocol.
