# 🌍 AI Travel Planner Concierge

> An intelligent, multi-agent travel concierge powered by **Google Gemini 3.7 Flash** and the **Google Agent Development Kit (ADK)**. It benchmarks sightseeing durations, calculates door-to-door transit costs (Road vs. Flight), generates landmark illustration postcards, and exports complete itineraries to Markdown.

---

## 🌟 Key Features

- **⏱️ Must-Visit Duration Analysis**: Calculates optimal trip duration based on must-visit landmark clusters for any city across *Relaxed*, *Balanced*, or *Packed* paces.
- **🚗 Transit Cost Calculator (Road vs. Flight)**: Real-world comparisons between driving (fuel, FASTag tolls, driving hours) and flights (fares, airport buffer times, baggage) in INR and USD.
- **🤖 Multi-Agent Orchestration**:
  - `travel_planner_main`: Root orchestrator coordinating tasks and synthesizing responses.
  - `itinerary_agent`: Day-by-day morning/afternoon/evening itinerary scheduling.
  - `illustration_agent`: Generates scenic destination postcards and visuals.
  - `markdown_exporter`: Assembles structured, formatted Markdown export files.
- **🖼️ Postcard Image Rendering**: Produces photorealistic imagery of iconic landmarks and heritage sites.
- **📥 One-Click Markdown Export**: Generates complete, offline-ready `.md` itinerary packages with a direct download button.
- **🎨 Glassmorphic Wanderlust Web UI**: Responsive chat interface built with FastAPI, Glassmorphism, and modern typography.

---

## 🏗️ Architecture

```
                                  ┌───────────────────────────┐
                                  │   Web Chat UI (FastAPI)   │
                                  └─────────────┬─────────────┘
                                                │ (A2A Protocol)
                                                ▼
                                  ┌───────────────────────────┐
                                  │    travel_planner_main    │
                                  │    (Root Orchestrator)    │
                                  └──────┬────┬────┬────┬─────┘
                                         │    │    │    │
            ┌────────────────────────────┘    │    │    └────────────────────────────┐
            ▼                                 ▼    ▼                                 ▼
┌─────────────────────────┐     ┌──────────────────┐    ┌──────────────────┐   ┌─────────────────────────┐
│ calculate_city_duration │     │ calculate_transit│    │ illustrate_dest  │   │ export_itinerary_md     │
│ (Attraction Clustering) │     │ (Road vs Flight) │    │ (Postcard Image) │   │ (Markdown Package)      │
└─────────────────────────┘     └──────────────────┘    └──────────────────┘   └─────────────────────────┘
```

---

## 📁 Repository Structure

```
.
├── travel-planner-agent/       # Backend Agent (ADK & Reasoning Engine)
│   ├── app/                    # Agent definition, sub-agents & custom tools
│   │   ├── agent.py            # travel_planner_main orchestrator
│   │   ├── tools/              # City duration, transit costs, illustration, markdown export
│   │   └── static/             # Generated postcards & markdown files
│   ├── tests/                  # Automated pytest test suite
│   ├── pyproject.toml          # Poetry / UV dependencies
│   └── agents-cli-manifest.yaml# Manifest for Agent Engine deployment
├── frontend/                   # Modern Web Frontend
│   ├── main.py                 # FastAPI proxy communicating via A2A protocol
│   ├── static/index.html       # Wanderlust chat interface with marked.js
│   ├── Dockerfile              # Container definition for Cloud Run
│   └── requirements.txt        # Frontend Python dependencies
├── project_brief.md            # Lab submission brief
└── README.md                   # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) or pip
- Google Cloud Project with Vertex AI enabled (`roles/aiplatform.user`)

### 1. Run the Travel Planner Agent Backend
```bash
cd travel-planner-agent
uv sync
uv run adk web app/
```
The ADK playground will be available at `http://localhost:8000`.

### 2. Run the Web Frontend
```bash
cd ../frontend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080
```
Open your browser to `http://localhost:8080`.

### 3. Run Automated Tests
```bash
cd ../travel-planner-agent
uv run pytest tests/ -v
```

---

## 📜 License

Apache 2.0
