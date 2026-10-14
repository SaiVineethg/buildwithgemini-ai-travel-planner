"""Markdown exporter tool for travel itineraries."""

import re
import uuid
from typing import Any, Dict, Optional

from google.genai import types
from google.adk.tools import ToolContext

from app.config import ITINERARIES_DIR


def _sanitize_slug(text: str) -> str:
    """Creates a clean filename slug from a string."""
    clean = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[-\s]+", "_", clean)[:40]


async def export_itinerary_markdown(
    destination: str,
    itinerary_markdown_content: str,
    trip_title: str = "",
    tool_context: Optional[ToolContext] = None,
) -> Dict[str, Any]:
    """Saves and exports a finalized travel itinerary as a Markdown document.

    Args:
        destination: Destination city or country (e.g. 'Seattle', 'Tokyo').
        itinerary_markdown_content: Complete formatted Markdown text of the itinerary.
        trip_title: Optional custom title for the itinerary.
        tool_context: ADK ToolContext for artifact persistence.

    Returns:
        A dictionary with export status, file path, filename, and file size.
    """
    slug = _sanitize_slug(destination)
    filename = f"itinerary_{slug}_{uuid.uuid4().hex[:6]}.md"
    target_path = ITINERARIES_DIR / filename

    # Prepare markdown header if not present
    final_content = itinerary_markdown_content.strip()
    if trip_title and trip_title not in final_content:
        header = f"# ✈️ {trip_title}\n\n"
        final_content = header + final_content
    elif not final_content.startswith("#"):
        header = f"# ✈️ Travel Itinerary: {destination.title()}\n\n"
        final_content = header + final_content

    # Write file to disk
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(final_content)

    # Save to ADK session artifact
    if tool_context:
        try:
            artifact_part = types.Part(
                inline_data=types.Blob(
                    mime_type="text/markdown",
                    data=final_content.encode("utf-8"),
                )
            )
            await tool_context.save_artifact(filename, artifact_part)
        except Exception:
            pass

    return {
        "status": "success",
        "destination": destination,
        "filename": filename,
        "file_path": str(target_path),
        "relative_url": f"/static/itineraries/{filename}",
        "size_bytes": len(final_content.encode("utf-8")),
        "message": f"Successfully exported Markdown itinerary to {filename}.",
    }
