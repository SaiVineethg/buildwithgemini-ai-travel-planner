"""Image generator tool using Vertex AI Gemini image generation."""

import re
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

from google import genai
from google.genai import types
from google.adk.tools import ToolContext

from app.config import PROJECT_ID, LOCATION, IMAGE_MODEL, IMAGES_DIR


def _sanitize_slug(text: str) -> str:
    """Creates a clean filename slug from a string."""
    clean = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[-\s]+", "_", clean)[:40]


async def illustrate_destination(
    destination_name: str,
    city: str,
    visual_scene_description: str = "",
    tool_context: Optional[ToolContext] = None,
) -> Dict[str, Any]:
    """Generates a high-quality visual illustration of a travel destination or landmark.

    Args:
        destination_name: Name of the attraction or spot (e.g. 'Space Needle', 'Pike Place Market').
        city: City where the destination is located (e.g. 'Seattle', 'Tokyo').
        visual_scene_description: Optional custom visual prompt details (e.g. 'sunset over the harbor').
        tool_context: ADK ToolContext for saving artifacts.

    Returns:
        A dictionary with image generation status, saved file path, relative web URL, and caption.
    """
    slug = f"{_sanitize_slug(city)}_{_sanitize_slug(destination_name)}"
    filename = f"{slug}_{uuid.uuid4().hex[:6]}.png"
    target_path = IMAGES_DIR / filename

    # Build prompt
    prompt = (
        f"A beautiful, photorealistic travel photography postcard of {destination_name} in {city}. "
        f"{visual_scene_description if visual_scene_description else 'Vibrant lighting, authentic architectural details, inviting travel atmosphere, cinematic composition.'}"
    )

    try:
        client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location=LOCATION,
        )

        response = client.models.generate_content(
            model=IMAGE_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )

        image_data: Optional[bytes] = None
        text_caption = f"Scenic view of {destination_name}, {city}"

        if response.candidates:
            first_candidate = response.candidates[0]
            if first_candidate.content and first_candidate.content.parts:
                for part in first_candidate.content.parts:
                    if part.inline_data and part.inline_data.data:
                        image_data = part.inline_data.data
                    elif part.text:
                        text_caption = part.text.strip()

        if image_data:
            # Write to disk
            with open(target_path, "wb") as f:
                f.write(image_data)

            # Save as session artifact if tool_context available
            if tool_context:
                try:
                    artifact_part = types.Part(
                        inline_data=types.Blob(
                            mime_type="image/png",
                            data=image_data,
                        )
                    )
                    await tool_context.save_artifact(filename, artifact_part)
                except Exception as e:
                    # Non-fatal if artifact service is not bound in local standalone test
                    pass

            return {
                "status": "success",
                "destination": destination_name,
                "city": city,
                "caption": text_caption,
                "file_path": str(target_path),
                "filename": filename,
                "relative_url": f"/static/images/{filename}",
                "message": f"Successfully illustrated {destination_name} in {city}.",
            }
        else:
            return {
                "status": "partial",
                "destination": destination_name,
                "city": city,
                "caption": text_caption,
                "file_path": "",
                "filename": "",
                "relative_url": "",
                "message": "Model generated description without inline image data.",
            }

    except Exception as exc:
        # Graceful fallback so agent conversation does not crash
        return {
            "status": "fallback",
            "destination": destination_name,
            "city": city,
            "error": str(exc),
            "caption": f"Visual depiction: {destination_name} in {city} ({visual_scene_description})",
            "file_path": "",
            "filename": "",
            "relative_url": "",
            "message": f"Visual illustration described for {destination_name}.",
        }
