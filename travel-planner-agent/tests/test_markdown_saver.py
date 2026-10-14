"""Unit tests for markdown export tool."""

import os
import pytest
from app.tools.markdown_saver import export_itinerary_markdown


@pytest.mark.asyncio
async def test_export_itinerary_markdown():
    """Verify that exporting markdown writes a file and returns metadata."""
    sample_content = """## Day 1: Downtown Highlights
- Morning: Space Needle
- Lunch: Pike Place Chowder
- Afternoon: Chihuly Garden
- Evening: Kerry Park Sunset
"""
    result = await export_itinerary_markdown(
        destination="Seattle",
        itinerary_markdown_content=sample_content,
        trip_title="3-Day Seattle Adventure",
    )

    assert result["status"] == "success"
    assert result["destination"] == "Seattle"
    assert os.path.exists(result["file_path"])
    assert result["size_bytes"] > 0

    with open(result["file_path"], "r", encoding="utf-8") as f:
        saved_text = f.read()

    assert "3-Day Seattle Adventure" in saved_text
    assert "Space Needle" in saved_text
