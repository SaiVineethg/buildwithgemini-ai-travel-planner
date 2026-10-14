"""Unit tests for city attractions and duration calculation tool."""

from app.tools.city_guide import calculate_city_duration


def test_known_city_duration_seattle():
    """Verify duration calculation for Seattle."""
    result = calculate_city_duration("Seattle", pace="balanced")
    assert "Seattle" in result["city"]
    assert result["recommended_days"] == 3
    assert result["total_must_visit_attractions"] > 0
    assert "neighborhood_clusters" in result
    assert "Downtown / Waterfront" in result["neighborhood_clusters"]


def test_pace_variations_tokyo():
    """Verify pace tiers for Tokyo."""
    relaxed = calculate_city_duration("Tokyo", pace="relaxed")
    balanced = calculate_city_duration("Tokyo", pace="balanced")
    packed = calculate_city_duration("Tokyo", pace="packed")

    assert relaxed["recommended_days"] > balanced["recommended_days"]
    assert balanced["recommended_days"] > packed["recommended_days"]


def test_dynamic_fallback_city():
    """Verify fallback for an unlisted city."""
    result = calculate_city_duration("Reykjavik", pace="balanced")
    assert result["city"] == "Reykjavik"
    assert result["recommended_days"] >= 2
    assert "neighborhood_clusters" in result

def test_india_jaipur_city_duration():
    """Verify duration and cluster calculation for Jaipur, Rajasthan."""
    result = calculate_city_duration("Jaipur", pace="balanced")
    assert "Jaipur" in result["city"]
    assert result["recommended_days"] == 3
    assert "Amer / North Hills" in result["neighborhood_clusters"]
