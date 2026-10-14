"""City attractions and duration estimation tool."""

from typing import Any, Dict, List, Optional

# Curated benchmark city information with top attractions, clusters, and hours
CITY_DATA: Dict[str, Dict[str, Any]] = {
    "jaipur": {
        "city": "Jaipur (The Pink City), Rajasthan, India",
        "description": "The capital of Rajasthan, famous for royal palaces, hilltop forts, pink sandstone architecture, and bustling bazaars.",
        "attractions": [
            {"name": "Amber Palace (Amer Fort)", "cluster": "Amer / North Hills", "est_hours": 3.5, "must_visit": True},
            {"name": "Hawa Mahal (Palace of Winds)", "cluster": "Old Walled City", "est_hours": 1.5, "must_visit": True},
            {"name": "City Palace & Jantar Mantar", "cluster": "Old Walled City", "est_hours": 3.0, "must_visit": True},
            {"name": "Nahargarh Fort (Sunset Viewpoint)", "cluster": "Aravalli Hills", "est_hours": 2.5, "must_visit": True},
            {"name": "Jal Mahal (Water Palace)", "cluster": "Man Sagar Lake", "est_hours": 1.0, "must_visit": True},
            {"name": "Johari Bazaar & Bapu Bazaar", "cluster": "Historic Markets", "est_hours": 2.5, "must_visit": True},
            {"name": "Albert Hall Museum & Ram Niwas Garden", "cluster": "Central Jaipur", "est_hours": 2.0, "must_visit": False},
            {"name": "Chokhi Dhani Ethnic Village", "cluster": "Cultural Outskirts", "est_hours": 4.0, "must_visit": False},
        ],
        "default_pace_days": {"relaxed": 4, "balanced": 3, "packed": 2},
    },
    "delhi": {
        "city": "Delhi (National Capital Territory), India",
        "description": "India's historic capital combining Mughal monuments, British colonial heritage, and bustling contemporary markets.",
        "attractions": [
            {"name": "Red Fort & Chandni Chowk Food Walk", "cluster": "Old Delhi", "est_hours": 3.5, "must_visit": True},
            {"name": "Qutub Minar & Mehrauli Archaeological Park", "cluster": "South Delhi", "est_hours": 2.5, "must_visit": True},
            {"name": "Humayun's Tomb & Sunder Nursery", "cluster": "Central / Nizamuddin", "est_hours": 2.5, "must_visit": True},
            {"name": "India Gate & Kartavya Path", "cluster": "Central Vista", "est_hours": 1.5, "must_visit": True},
            {"name": "Lotus Temple & Akshardham Temple", "cluster": "East / South Delhi", "est_hours": 4.0, "must_visit": True},
            {"name": "Lodhi Art District & Khan Market", "cluster": "Central Heritage", "est_hours": 2.5, "must_visit": True},
        ],
        "default_pace_days": {"relaxed": 5, "balanced": 3, "packed": 2},
    },
    "goa": {
        "city": "Goa, India",
        "description": "Tropical paradise famous for sun-kissed beaches, Portuguese-colonial architecture, vibrant night markets, and spice plantations.",
        "attractions": [
            {"name": "Basilica of Bom Jesus & Se Cathedral", "cluster": "Old Goa Heritage", "est_hours": 2.5, "must_visit": True},
            {"name": "Fort Aguada & Sinquerim Beach", "cluster": "North Goa Coastal", "est_hours": 2.5, "must_visit": True},
            {"name": "Anjuna Beach & Vagator / Chapora Fort", "cluster": "North Goa", "est_hours": 3.5, "must_visit": True},
            {"name": "Fontainhas Latin Quarter (Panaji)", "cluster": "Panaji City", "est_hours": 2.0, "must_visit": True},
            {"name": "Palolem Beach & Cabo de Rama", "cluster": "South Goa", "est_hours": 4.0, "must_visit": True},
            {"name": "Dudhsagar Waterfalls Day Excursion", "cluster": "Western Ghats", "est_hours": 6.0, "must_visit": False},
        ],
        "default_pace_days": {"relaxed": 5, "balanced": 4, "packed": 2},
    },
    "agra": {
        "city": "Agra, Uttar Pradesh, India",
        "description": "Home of the sublime Taj Mahal and royal Mughal architecture along the Yamuna River.",
        "attractions": [
            {"name": "Taj Mahal (Sunrise Experience)", "cluster": "Yamuna Riverfront", "est_hours": 3.0, "must_visit": True},
            {"name": "Agra Fort", "cluster": "Central Agra", "est_hours": 2.5, "must_visit": True},
            {"name": "Fatehpur Sikri Royal Complex", "cluster": "Excursion (35 km west)", "est_hours": 4.0, "must_visit": True},
            {"name": "Mehtab Bagh (Sunset Taj View)", "cluster": "Across Yamuna", "est_hours": 1.5, "must_visit": True},
        ],
        "default_pace_days": {"relaxed": 2, "balanced": 2, "packed": 1},
    },
    "mumbai": {
        "city": "Mumbai, Maharashtra, India",
        "description": "The City of Dreams, India's financial hub celebrated for Victorian Gothic architecture, Bollywood, and Marine Drive sunset.",
        "attractions": [
            {"name": "Gateway of India & Taj Mahal Palace Hotel", "cluster": "South Mumbai Waterfront", "est_hours": 2.0, "must_visit": True},
            {"name": "Elephanta Caves Ferry Tour", "cluster": "Mumbai Harbor", "est_hours": 4.0, "must_visit": True},
            {"name": "Marine Drive & Chowpatty Beach", "cluster": "Queens Necklace", "est_hours": 2.0, "must_visit": True},
            {"name": "Chhatrapati Shivaji Maharaj Terminus (CSMT)", "cluster": "Fort District", "est_hours": 1.5, "must_visit": True},
            {"name": "Bandra Bandstand & Linking Road", "cluster": "Bandra West", "est_hours": 3.0, "must_visit": True},
            {"name": "Colaba Causeway Shopping & Cafe Leopold", "cluster": "Colaba", "est_hours": 2.5, "must_visit": True},
        ],
        "default_pace_days": {"relaxed": 5, "balanced": 3, "packed": 2},
    },
    "seattle": {
        "city": "Seattle, Washington, USA",
        "description": "Emerald City nestled between Puget Sound and Lake Washington, famous for coffee, tech, and evergreen nature.",
        "attractions": [
            {"name": "Pike Place Market", "cluster": "Downtown / Waterfront", "est_hours": 3, "must_visit": True},
            {"name": "Space Needle & Chihuly Garden and Glass", "cluster": "Seattle Center", "est_hours": 3.5, "must_visit": True},
            {"name": "Museum of Pop Culture (MoPOP)", "cluster": "Seattle Center", "est_hours": 2.5, "must_visit": True},
            {"name": "Bainbridge Island Ferry", "cluster": "Waterfront / Islands", "est_hours": 3.5, "must_visit": True},
            {"name": "Pioneer Square & Underground Tour", "cluster": "Historic District", "est_hours": 2.5, "must_visit": True},
            {"name": "Olympic Sculpture Park", "cluster": "Waterfront", "est_hours": 1.5, "must_visit": False},
            {"name": "Ballard Locks & Golden Gardens", "cluster": "North Seattle", "est_hours": 3, "must_visit": True},
            {"name": "Kerry Park Skyline View", "cluster": "Queen Anne", "est_hours": 1, "must_visit": True},
        ],
        "default_pace_days": {"relaxed": 5, "balanced": 3, "packed": 2},
    },
    "san francisco": {
        "city": "San Francisco, California, USA",
        "description": "Iconic city of rolling hills, historic cable cars, Golden Gate vistas, and diverse culinary neighborhoods.",
        "attractions": [
            {"name": "Golden Gate Bridge & Battery Spencer", "cluster": "North Bay / Marin", "est_hours": 2.5, "must_visit": True},
            {"name": "Alcatraz Island Tour", "cluster": "Bay / Pier 33", "est_hours": 3.5, "must_visit": True},
            {"name": "Fisherman's Wharf & Pier 39", "cluster": "North Waterfront", "est_hours": 2.5, "must_visit": True},
            {"name": "Chinatown & North Beach", "cluster": "Central Historic", "est_hours": 3, "must_visit": True},
            {"name": "Golden Gate Park & Japanese Tea Garden", "cluster": "West / Sunset", "est_hours": 3.5, "must_visit": True},
            {"name": "Painted Ladies & Alamo Square", "cluster": "Western Addition", "est_hours": 1.5, "must_visit": True},
        ],
        "default_pace_days": {"relaxed": 5, "balanced": 3, "packed": 2},
    },
    "tokyo": {
        "city": "Tokyo, Japan",
        "description": "A dazzling metropolis blending ultramodern skyscrapers, pop culture epicenters, and centuries-old shrines.",
        "attractions": [
            {"name": "Senso-ji Temple & Asakusa Nakamise", "cluster": "Asakusa / Taito", "est_hours": 3, "must_visit": True},
            {"name": "Shibuya Crossing & Hachiko Statue", "cluster": "Shibuya", "est_hours": 2, "must_visit": True},
            {"name": "Meiji Jingu Shrine & Harajuku", "cluster": "Harajuku / Omotesando", "est_hours": 3, "must_visit": True},
            {"name": "Shinjuku Gyoen & Omoide Yokocho", "cluster": "Shinjuku", "est_hours": 3.5, "must_visit": True},
            {"name": "teamLab Borderless / Planets", "cluster": "Odaiba / Toyosu", "est_hours": 3, "must_visit": True},
            {"name": "Akihabara Electric Town", "cluster": "Akihabara", "est_hours": 2.5, "must_visit": True},
        ],
        "default_pace_days": {"relaxed": 7, "balanced": 5, "packed": 3},
    },
    "paris": {
        "city": "Paris, France",
        "description": "The City of Light, celebrated for art museums, grand boulevards, cafe culture, and romantic architecture.",
        "attractions": [
            {"name": "Eiffel Tower & Champ de Mars", "cluster": "7th Arrondissement", "est_hours": 3, "must_visit": True},
            {"name": "Louvre Museum", "cluster": "1st Arrondissement", "est_hours": 4, "must_visit": True},
            {"name": "Montmartre & Sacré-Cœur Basilica", "cluster": "18th Arrondissement", "est_hours": 3, "must_visit": True},
            {"name": "Notre-Dame Cathedral & Île de la Cité", "cluster": "4th Arrondissement", "est_hours": 2.5, "must_visit": True},
            {"name": "Musée d'Orsay", "cluster": "7th Arrondissement", "est_hours": 3, "must_visit": True},
            {"name": "Arc de Triomphe & Champs-Élysées", "cluster": "8th Arrondissement", "est_hours": 2, "must_visit": True},
        ],
        "default_pace_days": {"relaxed": 6, "balanced": 4, "packed": 3},
    },
    "new york": {
        "city": "New York City, New York, USA",
        "description": "The Big Apple, world capital of theater, finance, iconic skylines, and diverse cultural enclaves.",
        "attractions": [
            {"name": "Central Park & The Met", "cluster": "Uptown / Museum Mile", "est_hours": 4.5, "must_visit": True},
            {"name": "Statue of Liberty & Ellis Island", "cluster": "Lower Manhattan / Harbor", "est_hours": 4, "must_visit": True},
            {"name": "Times Square & Broadway Show", "cluster": "Midtown", "est_hours": 3.5, "must_visit": True},
            {"name": "Empire State Building / Top of the Rock", "cluster": "Midtown", "est_hours": 2, "must_visit": True},
            {"name": "Brooklyn Bridge & DUMBO", "cluster": "Brooklyn Waterfront", "est_hours": 2.5, "must_visit": True},
        ],
        "default_pace_days": {"relaxed": 6, "balanced": 4, "packed": 3},
    },
}


def calculate_city_duration(
    city: str,
    pace: str = "balanced",
) -> Dict[str, Any]:
    """Calculates how many days are required to cover must-visit places in a given city.

    Args:
        city: Name of the destination city (e.g., 'Jaipur', 'Goa', 'Delhi', 'Seattle', 'Tokyo').
        pace: Desired travel pace: 'relaxed' (2 spots/day), 'balanced' (3-4 spots/day), or 'packed' (5+ spots/day).

    Returns:
        A structured breakdown of recommended duration, must-visit places by cluster,
        estimated visit hours, and daily pacing recommendations.
    """
    clean_city = city.strip().lower()
    matched_key = None
    for key in CITY_DATA:
        if key in clean_city or clean_city in key:
            matched_key = key
            break

    normalized_pace = pace.lower().strip()
    if normalized_pace not in ["relaxed", "balanced", "packed"]:
        normalized_pace = "balanced"

    if matched_key:
        data = CITY_DATA[matched_key]
        attractions = data["attractions"]
        must_visits = [a for a in attractions if a.get("must_visit", True)]
        total_must_visit_hours = sum(a["est_hours"] for a in must_visits)

        recommended_days = data["default_pace_days"].get(normalized_pace, 3)

        clusters: Dict[str, List[str]] = {}
        for a in attractions:
            c = a["cluster"]
            if c not in clusters:
                clusters[c] = []
            clusters[c].append(f"{a['name']} (~{a['est_hours']}h)")

        return {
            "city": data["city"],
            "description": data["description"],
            "pace": normalized_pace,
            "recommended_days": recommended_days,
            "pace_breakdown": {
                "relaxed": f"{data['default_pace_days']['relaxed']} days (2-3 sights/day at leisurely pace)",
                "balanced": f"{data['default_pace_days']['balanced']} days (3-4 sights/day, optimal balance)",
                "packed": f"{data['default_pace_days']['packed']} days (fast-paced highlight whirlwind)",
            },
            "total_must_visit_attractions": len(must_visits),
            "total_estimated_sightseeing_hours": total_must_visit_hours,
            "neighborhood_clusters": clusters,
            "guidance": (
                f"For {city.title()}, a {normalized_pace} trip requires {recommended_days} days to comfortably "
                f"cover the top {len(must_visits)} must-visit highlights without burnout."
            ),
        }

    # Dynamic fallback for cities not in pre-indexed database
    hours_per_day = {"relaxed": 4.5, "balanced": 6.5, "packed": 9.0}.get(normalized_pace, 6.5)
    default_days = {"relaxed": 4, "balanced": 3, "packed": 2}.get(normalized_pace, 3)

    return {
        "city": city.title(),
        "description": f"Exploring the vibrant landmarks and cultural destinations in {city.title()}.",
        "pace": normalized_pace,
        "recommended_days": default_days,
        "pace_breakdown": {
            "relaxed": "4 days (leisurely pace, 2 sights per day)",
            "balanced": "3 days (standard pace, 3-4 sights per day)",
            "packed": "2 days (express pace, highlights only)",
        },
        "total_must_visit_attractions": 8,
        "total_estimated_sightseeing_hours": default_days * hours_per_day,
        "neighborhood_clusters": {
            "Historic Center": ["Historic Old Town & Market", "Central Plaza & Landmark"],
            "Scenic / Waterfront District": ["Promenade & Lake / River", "Panoramic Viewpoint"],
            "Cultural Quarter": ["Premier City Museum / Palace", "Heritage Bazaar"],
        },
        "guidance": (
            f"For {city.title()}, {default_days} days are recommended under a {normalized_pace} pace "
            f"to cover all primary landmarks and experience local dining and culture."
        ),
    }
