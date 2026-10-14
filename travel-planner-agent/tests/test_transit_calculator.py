"""Unit tests for transit cost and distance calculator."""

from app.tools.transit_calculator import (
    calculate_transit_cost,
    find_city_coordinates,
    haversine_distance_miles,
)


def test_city_coordinates_lookup():
    """Verify coordinate lookup for known cities."""
    sf = find_city_coordinates("San Francisco")
    assert sf is not None
    assert sf[2] == "North America"

    tokyo = find_city_coordinates("Tokyo")
    assert tokyo is not None
    assert tokyo[2] == "Asia"


def test_haversine_distance():
    """Verify distance between SF and Seattle is approximately 680-700 miles straight line."""
    sf = find_city_coordinates("San Francisco")
    seattle = find_city_coordinates("Seattle")
    dist = haversine_distance_miles(sf[0], sf[1], seattle[0], seattle[1])
    assert 650 < dist < 750


def test_domestic_route_road_vs_flight():
    """Test road vs flight calculation for SF to Seattle."""
    result = calculate_transit_cost("San Francisco", "Seattle", num_travelers=2)
    assert result["origin"] == "San Francisco"
    assert result["destination"] == "Seattle"
    assert result["num_travelers"] == 2

    # Road travel must be feasible
    road = result["road_transit"]
    assert road["feasible"] is True
    assert road["distance_miles"] > 700
    assert "fuel_cost" in road
    assert "tolls_cost" in road
    assert "total_estimated_road_cost" in road

    # Flight travel must have estimates
    flight = result["flight_transit"]
    assert "estimated_flight_time" in flight
    assert "economy_fare_per_traveler" in flight
    assert "total_group_flight_estimate" in flight


def test_oceanic_route_road_infeasible():
    """Test that transoceanic route between SF and Tokyo disables road travel."""
    result = calculate_transit_cost("San Francisco", "Tokyo", num_travelers=1)
    road = result["road_transit"]
    assert road["feasible"] is False
    assert "not feasible" in road["message"].lower()

def test_india_delhi_to_jaipur_transit():
    """Test road vs flight calculation for Delhi to Jaipur in India."""
    result = calculate_transit_cost("Delhi", "Jaipur", num_travelers=2)
    assert result["origin"] == "Delhi"
    assert result["destination"] == "Jaipur"
    
    road = result["road_transit"]
    assert road["feasible"] is True
    assert "₹" in road["total_estimated_road_cost"]
    assert "FASTag" in road["tolls_cost"]
    
    flight = result["flight_transit"]
    assert "₹" in flight["economy_fare_per_traveler"]
    assert "IndiGo" in flight["airline_options"]
