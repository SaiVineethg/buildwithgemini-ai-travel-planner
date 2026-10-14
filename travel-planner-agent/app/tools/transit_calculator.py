"""Transit cost and distance calculator for road vs flight comparison."""

import math
from typing import Any, Dict, Optional, Tuple

# Pre-indexed coordinate database for popular travel origins and destinations
CITY_COORDINATES: Dict[str, Tuple[float, float, str]] = {
    # US & Americas
    "san francisco": (37.7749, -122.4194, "North America"),
    "seattle": (47.6062, -122.3321, "North America"),
    "los angeles": (34.0522, -118.2437, "North America"),
    "new york": (40.7128, -74.0060, "North America"),
    "boston": (42.3601, -71.0589, "North America"),
    "chicago": (41.8781, -87.6298, "North America"),
    "las vegas": (36.1699, -115.1398, "North America"),
    "miami": (25.7617, -80.1918, "North America"),
    "austin": (30.2672, -97.7431, "North America"),
    "denver": (39.7392, -104.9903, "North America"),
    "portland": (45.5152, -122.6784, "North America"),
    "san diego": (32.7157, -117.1611, "North America"),
    "honolulu": (21.3069, -157.8583, "Oceania/Islands"),
    "toronto": (43.6532, -79.3832, "North America"),
    "vancouver": (49.2827, -123.1207, "North America"),
    # Europe
    "london": (51.5074, -0.1278, "Europe"),
    "paris": (48.8566, 2.3522, "Europe"),
    "rome": (41.9028, 12.4964, "Europe"),
    "barcelona": (41.3851, 2.1734, "Europe"),
    # Asia & Oceania
    "tokyo": (35.6762, 139.6503, "Asia"),
    "kyoto": (35.0116, 135.7681, "Asia"),
    "singapore": (1.3521, 103.8198, "Asia"),
    "sydney": (-33.8688, 151.2093, "Australia"),
    "dubai": (25.2048, 55.2708, "Asia"),
    # India destinations
    "delhi": (28.6139, 77.2090, "India"),
    "new delhi": (28.6139, 77.2090, "India"),
    "jaipur": (26.9124, 75.7873, "India"),
    "agra": (27.1767, 78.0081, "India"),
    "mumbai": (19.0760, 72.8777, "India"),
    "goa": (15.2993, 74.1240, "India"),
    "panaji": (15.4909, 73.8278, "India"),
    "bengaluru": (12.9716, 77.5946, "India"),
    "bangalore": (12.9716, 77.5946, "India"),
    "udaipur": (24.5854, 73.7125, "India"),
    "varanasi": (25.3176, 82.9739, "India"),
    "chennai": (13.0827, 80.2707, "India"),
    "kolkata": (22.5726, 88.3639, "India"),
    "hyderabad": (17.3850, 78.4867, "India"),
    "kochi": (9.9312, 76.2673, "India"),
    "cochin": (9.9312, 76.2673, "India"),
    "pune": (18.5204, 73.8567, "India"),
    "amritsar": (31.6340, 74.8723, "India"),
    "shimla": (31.1048, 77.1734, "India"),
    "manali": (32.2432, 77.1892, "India"),
}


def haversine_distance_miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates the great-circle distance between two points in miles."""
    r = 3958.8  # Earth radius in miles
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


def find_city_coordinates(city_name: str) -> Optional[Tuple[float, float, str]]:
    """Look up coordinates and region by city name."""
    clean_name = city_name.strip().lower()
    for name, data in CITY_COORDINATES.items():
        if name in clean_name or clean_name in name:
            return data
    return None


def calculate_transit_cost(
    origin: str,
    destination: str,
    num_travelers: int = 1,
) -> Dict[str, Any]:
    """Calculates and compares travel duration and approx costs by road vs. flight.

    Args:
        origin: Departure city or location (e.g. 'Delhi', 'San Francisco', 'Mumbai').
        destination: Arrival city or destination (e.g. 'Jaipur', 'Goa', 'Seattle', 'Tokyo').
        num_travelers: Number of people traveling together (default: 1).

    Returns:
        A structured dictionary with road vs flight distance, duration, cost breakdown,
        and travel recommendations.
    """
    origin_data = find_city_coordinates(origin)
    dest_data = find_city_coordinates(destination)

    # Check region and coordinate availability
    if not origin_data or not dest_data:
        straight_dist = 500.0
        same_landmass = True
        is_india_domestic = ("delhi" in origin.lower() or "mumbai" in origin.lower() or
                             "jaipur" in destination.lower() or "goa" in destination.lower() or
                             "india" in origin.lower() or "india" in destination.lower())
    else:
        straight_dist = haversine_distance_miles(
            origin_data[0], origin_data[1], dest_data[0], dest_data[1]
        )
        is_india_domestic = (origin_data[2] == "India" and dest_data[2] == "India")
        # Same landmass check
        same_landmass = (
            (origin_data[2] == dest_data[2])
            or (origin_data[2] in ["Asia", "India"] and dest_data[2] in ["Asia", "India"])
        ) and ("Islands" not in origin_data[2] and "Islands" not in dest_data[2])

    # Road travel analysis
    road_info: Dict[str, Any] = {}
    if not same_landmass or straight_dist > 4500:
        road_info = {
            "feasible": False,
            "message": f"Direct road travel between {origin} and {destination} is not feasible due to oceanic or continental divide. Flight is required.",
            "distance_miles": None,
            "distance_km": None,
            "estimated_driving_time": None,
            "fuel_cost": None,
            "tolls_cost": None,
            "total_estimated_road_cost": None,
        }
    else:
        road_distance_miles = round(straight_dist * 1.25)
        road_distance_km = round(road_distance_miles * 1.60934)

        if is_india_domestic:
            # Indian highway conditions: ~45 mph / ~70 km/h average with breaks
            driving_hours_raw = road_distance_miles / 45.0
            rest_stops = math.floor(driving_hours_raw / 2.5) * 0.4
            total_driving_hours = driving_hours_raw + rest_stops

            # Fuel in India: ~15 km/L, ₹100/L (~$1.20/L) -> approx ₹6.6 per km
            fuel_cost_inr = round(road_distance_km * 6.6)
            # FASTag tolls: ~₹2.2 per km
            tolls_cost_inr = round(road_distance_km * 2.2)
            total_road_inr = fuel_cost_inr + tolls_cost_inr

            # Convert to USD equivalent (~83 INR = 1 USD)
            fuel_cost_usd = round(fuel_cost_inr / 83.0, 2)
            tolls_cost_usd = round(tolls_cost_inr / 83.0, 2)
            total_road_usd = round(total_road_inr / 83.0, 2)

            cost_per_person_inr = round(total_road_inr / max(1, num_travelers))
            cost_per_person_usd = round(total_road_usd / max(1, num_travelers), 2)

            hours = int(total_driving_hours)
            minutes = int((total_driving_hours - hours) * 60)
            driving_time_str = f"{hours}h {minutes}m"

            road_info = {
                "feasible": True,
                "distance_miles": road_distance_miles,
                "distance_km": road_distance_km,
                "estimated_driving_time": driving_time_str,
                "fuel_cost": f"₹{fuel_cost_inr:,} (~${fuel_cost_usd:.2f})",
                "tolls_cost": f"₹{tolls_cost_inr:,} (~${tolls_cost_usd:.2f}) [FASTag]",
                "total_estimated_road_cost": f"₹{total_road_inr:,} (~${total_road_usd:.2f})",
                "cost_per_traveler": f"₹{cost_per_person_inr:,} (~${cost_per_person_usd:.2f}) shared among {num_travelers} traveler(s)",
                "overnight_stay_recommended": hours >= 10,
            }
        else:
            # US / International standard
            driving_hours_raw = road_distance_miles / 60.0
            rest_stops = math.floor(driving_hours_raw / 3.0) * 0.35
            total_driving_hours = driving_hours_raw + rest_stops

            hours = int(total_driving_hours)
            minutes = int((total_driving_hours - hours) * 60)
            driving_time_str = f"{hours}h {minutes}m"

            gallons_needed = road_distance_miles / 28.0
            fuel_cost = round(gallons_needed * 3.60, 2)
            tolls_cost = round((road_distance_miles / 400.0) * 15.0, 2)
            total_road_cost = round(fuel_cost + tolls_cost, 2)
            cost_per_person = round(total_road_cost / max(1, num_travelers), 2)

            road_info = {
                "feasible": True,
                "distance_miles": road_distance_miles,
                "distance_km": road_distance_km,
                "estimated_driving_time": driving_time_str,
                "fuel_cost": f"${fuel_cost:,.2f}",
                "tolls_cost": f"${tolls_cost:,.2f}",
                "total_estimated_road_cost": f"${total_road_cost:,.2f}",
                "cost_per_traveler": f"${cost_per_person:,.2f} (shared among {num_travelers} traveler(s))",
                "overnight_stay_recommended": hours >= 12,
            }

    # Flight travel analysis
    flight_cruise_hours = straight_dist / 480.0
    total_flight_duration_hours = flight_cruise_hours + 0.6
    flight_hrs = int(total_flight_duration_hours)
    flight_mins = int((total_flight_duration_hours - flight_hrs) * 60)
    flight_time_str = f"{flight_hrs}h {flight_mins}m in-air (~{flight_hrs + 2}h total with airport check-in)"

    if is_india_domestic:
        # Domestic Indian airfares (IndiGo, Air India, Akasa Air)
        if straight_dist < 300:
            low_inr, high_inr = 2500, 4500
        elif straight_dist < 800:
            low_inr, high_inr = 3500, 6500
        else:
            low_inr, high_inr = 4500, 9500

        low_usd = round(low_inr / 83.0)
        high_usd = round(high_inr / 83.0)
        tot_low_inr = low_inr * num_travelers
        tot_high_inr = high_inr * num_travelers

        flight_info: Dict[str, Any] = {
            "straight_line_distance_miles": round(straight_dist),
            "estimated_flight_time": flight_time_str,
            "economy_fare_per_traveler": f"₹{low_inr:,} - ₹{high_inr:,} (~${low_usd} - ${high_usd}) one-way",
            "total_group_flight_estimate": f"₹{tot_low_inr:,} - ₹{tot_high_inr:,} (~${low_usd * num_travelers} - ${high_usd * num_travelers}) one-way for {num_travelers} traveler(s)",
            "airline_options": "Major carriers: IndiGo, Air India, Akasa Air, SpiceJet.",
        }
    else:
        if straight_dist < 400:
            one_way_low, one_way_high = 90, 180
        elif straight_dist < 1200:
            one_way_low, one_way_high = 150, 310
        elif straight_dist < 3000:
            one_way_low, one_way_high = 230, 480
        else:
            one_way_low, one_way_high = 650, 1350

        total_flight_low = one_way_low * num_travelers
        total_flight_high = one_way_high * num_travelers

        flight_info = {
            "straight_line_distance_miles": round(straight_dist),
            "estimated_flight_time": flight_time_str,
            "economy_fare_per_traveler": f"${one_way_low} - ${one_way_high} one-way (approx ${one_way_low * 2} - ${one_way_high * 2} roundtrip)",
            "total_group_flight_estimate": f"${total_flight_low:,.2f} - ${total_flight_high:,.2f} one-way",
            "baggage_fees_note": "Budget an additional $35-$40 per checked bag each way.",
        }

    # Recommendation synthesis
    if not road_info["feasible"]:
        recommendation = f"Flight is required: Overland road transit is not feasible between {origin} and {destination}."
    elif road_info["distance_miles"] <= 250:
        recommendation = (
            f"Road travel (or Express Train/Cab) is highly recommended! At {road_info['distance_miles']} miles ({road_info['distance_km']} km), "
            f"driving takes ~{road_info['estimated_driving_time']} and costs approx {road_info['total_estimated_road_cost']} total. "
            f"With airport arrival buffers and security lines, driving is often faster and much cheaper than flying for {num_travelers} traveler(s)."
        )
    elif road_info["distance_miles"] > 550:
        recommendation = (
            f"Flight is recommended for speed and comfort: Driving takes {road_info['estimated_driving_time']} "
            f"while a direct flight takes only {flight_time_str}. Road travel would require long driving stints or overnight stops."
        )
    else:
        recommendation = (
            f"Both options are viable: Road travel (~{road_info['estimated_driving_time']}, {road_info['total_estimated_road_cost']} total) "
            f"offers scenic road-trip flexibility, while flying ({flight_info['economy_fare_per_traveler']}) saves significant travel fatigue."
        )

    return {
        "origin": origin,
        "destination": destination,
        "num_travelers": num_travelers,
        "road_transit": road_info,
        "flight_transit": flight_info,
        "recommendation": recommendation,
    }
