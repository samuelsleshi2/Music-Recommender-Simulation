"""
Command line runner for the Music Recommender Simulation.

Run with:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print a labeled block of top-k recommendations for a given user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print(f"\n{'=' * 50}")
    print(f"Profile: {label}")
    print(f"Prefs:   genre={user_prefs['genre']}, mood={user_prefs['mood']}, energy={user_prefs['energy']}")
    print(f"{'=' * 50}")
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{i}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f} | {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")

    # --- Profile 1: High-Energy Pop ---
    print_recommendations(
        "High-Energy Pop",
        {"genre": "pop", "mood": "happy", "energy": 0.85},
        songs,
    )

    # --- Profile 2: Chill Lofi ---
    print_recommendations(
        "Chill Lofi",
        {"genre": "lofi", "mood": "chill", "energy": 0.38},
        songs,
    )

    # --- Profile 3: Deep Intense Rock ---
    print_recommendations(
        "Deep Intense Rock",
        {"genre": "rock", "mood": "intense", "energy": 0.92},
        songs,
    )


if __name__ == "__main__":
    main()
