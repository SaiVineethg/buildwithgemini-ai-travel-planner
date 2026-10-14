import vertexai
from vertexai.preview import reasoning_engines

# 1. Initialize Vertex AI
vertexai.init(
    project="qwiklabs-gcp-04-3ad5cd1adcac",
    location="us-east1"
)

# 2. Connect to the deployed Reasoning Engine instance
agent = reasoning_engines.ReasoningEngine(
    "projects/746450897275/locations/us-east1/reasoningEngines/6326041249920843776"
)

# 3. Create a session (optional, or pass None)
session = agent.create_session(user_id="alice")

# 4. Stream response
for event in agent.stream_query(
    message="What's the weather and time in San Francisco?",
    user_id="alice",
    session_id=session["id"],
):
    print(event)