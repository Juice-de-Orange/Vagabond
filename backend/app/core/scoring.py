"""Scoring-Algorithmus fuer POI-Bewertung.

Standardgewichtung:
  - distance:      30%  (Luftlinie zum POI)
  - time:          35%  (echte Gehzeit via GraphHopper)
  - reliability:   35%  (wie aktuell/verifiziert sind die Daten)

Mit Barrierefreiheits-Modus:
  - distance:      20%
  - time:          25%
  - reliability:   25%
  - accessibility: 30%

Oeffnungszeiten werden nicht als Score behandelt sondern als Filter:
geschlossene POIs (bei relevanten Kategorien) werden aus den
Ergebnissen entfernt, es sei denn sie oeffnen bald oder der Nutzer
kommt rechtzeitig an.
"""

# Kategorien bei denen Oeffnungszeiten relevant sind
CATEGORIES_WITH_HOURS = {
    "supermarket", "pharmacy", "restaurant",
}

WEIGHTS_DEFAULT = {
    "distance": 0.30,
    "time": 0.35,
    "reliability": 0.35,
}

WEIGHTS_ACCESSIBLE = {
    "distance": 0.20,
    "time": 0.25,
    "reliability": 0.25,
    "accessibility": 0.30,
}


def score_distance(distance_m: float, max_distance_m: float) -> float:
    """Naeher = besser. Linear von 100 (0m) bis 0 (max_distance)."""
    if max_distance_m <= 0:
        return 100.0
    score = max(0.0, 100.0 * (1.0 - distance_m / max_distance_m))
    return round(score, 1)


def score_time(time_s: float | None, max_time_s: float = 3600.0) -> float:
    """Kuerzere Gehzeit = besser. Max 1 Stunde als Referenz."""
    if time_s is None:
        return 50.0
    score = max(0.0, 100.0 * (1.0 - time_s / max_time_s))
    return round(score, 1)


def score_reliability(
    reliability: float | None,
    verified_count: int = 0,
) -> float:
    """Hoehere Zuverlaessigkeit = besser.

    reliability: 0.0-1.0 aus der Datenbank
    verified_count: Anzahl Community-Verifizierungen (Phase 2)
    """
    base = (reliability or 0.5) * 80.0
    verify_bonus = min(20.0, verified_count * 5.0)
    return round(min(100.0, base + verify_bonus), 1)


def score_accessibility(wheelchair: str | None) -> float:
    """Barrierefreiheit basierend auf OSM wheelchair-Tag."""
    mapping = {
        "yes": 100.0,
        "limited": 60.0,
        "no": 20.0,
    }
    return mapping.get(wheelchair, 50.0)


def should_filter_closed(
    poi_type: str,
    is_open: bool | None,
    walking_time_s: float | None = None,
    opens_in_s: float | None = None,
) -> bool:
    """Entscheidet ob ein geschlossener POI aus den Ergebnissen entfernt wird.

    Returns True wenn der POI rausfallen soll.

    Logik:
      - Kategorien ohne Oeffnungszeiten (Brunnen, etc.): nie filtern
      - Oeffnungszeiten unbekannt: nicht filtern (lieber anzeigen)
      - Geoeffnet: nicht filtern
      - Geschlossen, aber oeffnet in <= 30 min: nicht filtern
      - Geschlossen, aber Gehzeit > opens_in: nicht filtern (man kommt rechtzeitig an)
      - Sonst: filtern
    """
    if poi_type not in CATEGORIES_WITH_HOURS:
        return False
    if is_open is None:
        return False
    if is_open:
        return False

    # Geschlossen -- pruefen ob er bald oeffnet
    if opens_in_s is not None:
        # Oeffnet in weniger als 30 Minuten
        if opens_in_s <= 1800:
            return False
        # Gehzeit ist laenger als Zeit bis Oeffnung
        if walking_time_s is not None and walking_time_s >= opens_in_s:
            return False

    # Geschlossen und oeffnet nicht bald genug
    return True


def calculate_score(
    distance_m: float,
    max_distance_m: float,
    poi_type: str = "",
    time_s: float | None = None,
    reliability: float | None = None,
    verified_count: int = 0,
    wheelchair: str | None = None,
    accessible_mode: bool = False,
) -> float:
    """Berechnet den Gesamtscore (0-100) fuer einen POI.

    Args:
        accessible_mode: Wenn True, wird Barrierefreiheit stark gewichtet.
                         Wird spaeter als App-Einstellung gesteuert.
    """
    scores = {
        "distance": score_distance(distance_m, max_distance_m),
        "time": score_time(time_s),
        "reliability": score_reliability(reliability, verified_count),
        "accessibility": score_accessibility(wheelchair),
    }

    weights = WEIGHTS_ACCESSIBLE if accessible_mode else WEIGHTS_DEFAULT
    total = sum(scores.get(k, 50.0) * w for k, w in weights.items())
    return round(total, 1)