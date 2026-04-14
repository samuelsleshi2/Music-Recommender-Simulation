import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its audio/metadata attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences used for scoring songs."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP recommender that scores and ranks Song objects against a UserProfile."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by score for the given user profile."""
        return sorted(self.songs, key=lambda song: self._score(user, song), reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string explaining why a song was recommended."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append("genre match (+2.0)")
        if song.mood == user.favorite_mood:
            reasons.append("mood match (+1.0)")
        energy_gap = abs(song.energy - user.target_energy)
        energy_score = round((1 - energy_gap) * 1.5, 2)
        reasons.append(f"energy similarity (+{energy_score})")
        if user.likes_acoustic and song.acousticness > 0.6:
            reasons.append("acoustic preference (+0.5)")
        return "; ".join(reasons)

    def _score(self, user: UserProfile, song: Song) -> float:
        """Compute a numeric score for a single song against a user profile."""
        score = 0.0
        if song.genre == user.favorite_genre:
            score += 2.0
        if song.mood == user.favorite_mood:
            score += 1.0
        energy_gap = abs(song.energy - user.target_energy)
        score += (1 - energy_gap) * 1.5
        if user.likes_acoustic and song.acousticness > 0.6:
            score += 0.5
        return score


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return them as a list of dicts with typed values."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Score a single song against user preferences.

    Scoring rules:
      +2.0  genre match
      +1.0  mood match
      +0-1.5 energy similarity (scales with closeness to target)

    Returns a (score, explanation) tuple.
    """
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"] == user_prefs.get("mood"):
        score += 1.0
        reasons.append("mood match (+1.0)")

    target_energy = user_prefs.get("energy", 0.5)
    energy_gap = abs(song["energy"] - target_energy)
    energy_score = round((1 - energy_gap) * 1.5, 2)
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score})")

    return round(score, 2), "; ".join(reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, then return the top-k sorted from highest to lowest score."""
    scored = [(*( (song,) + score_song(user_prefs, song) ),) for song in songs]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
