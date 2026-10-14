"""Configuration settings for Travel Planner Multi-Agent System."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "qwiklabs-gcp-04-3ad5cd1adcac")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
os.environ["GOOGLE_GENAI_USE_ENTERPRISE"] = "True"
os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID

# Models
ORCHESTRATOR_MODEL = "gemini-3.7-flash"
SUBAGENT_MODEL = "gemini-3.7-flash"
IMAGE_MODEL = "gemini-2.5-flash-image"

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"
IMAGES_DIR = STATIC_DIR / "images"
ITINERARIES_DIR = STATIC_DIR / "itineraries"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
ITINERARIES_DIR.mkdir(parents=True, exist_ok=True)
