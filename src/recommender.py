from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def score_song(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Score a single song against a user profile, returning (score, reasons)."""
        total = 0.0
        reasons = []

        if song.genre == user.favorite_genre:
            genre_pts = 2.0
            reasons.append(f"genre match: {song.genre} (+{genre_pts:.2f})")
        else:
            genre_pts = 0.0
            reasons.append(f"genre mismatch: {song.genre} vs {user.favorite_genre} (+{genre_pts:.2f})")
        total += genre_pts

        if song.mood == user.favorite_mood:
            mood_pts = 1.5
            reasons.append(f"mood match: {song.mood} (+{mood_pts:.2f})")
        else:
            mood_pts = 0.0
            reasons.append(f"mood mismatch: {song.mood} vs {user.favorite_mood} (+{mood_pts:.2f})")
        total += mood_pts

        energy_pts = 1.0 - abs(song.energy - user.target_energy)
        reasons.append(f"energy proximity: |{song.energy:.2f} - {user.target_energy:.2f}| (+{energy_pts:.2f})")
        total += energy_pts

        if user.likes_acoustic:
            acoustic_pts = song.acousticness * 0.5
            reasons.append(f"acoustic fit: {song.acousticness:.2f} × 0.5 (+{acoustic_pts:.2f})")
        else:
            acoustic_pts = (1.0 - song.acousticness) * 0.5
            reasons.append(f"non-acoustic fit: (1 - {song.acousticness:.2f}) × 0.5 (+{acoustic_pts:.2f})")
        total += acoustic_pts

        return total, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by score descending."""
        scored = [(song, self.score_song(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, score in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string explaining why a song was recommended."""
        total, reasons = self.score_song(user, song)
        return " | ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with typed values."""
    import csv
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song (0.0–5.0) against user preferences and return (score, reasons)."""
    total = 0.0
    reasons = []

    # --- Genre: +2.0 for exact match ---
    if song["genre"] == user_prefs["favorite_genre"]:
        genre_pts = 2.0
        reasons.append(f"genre match: {song['genre']} (+{genre_pts:.2f})")
    else:
        genre_pts = 0.0
        reasons.append(f"genre mismatch: {song['genre']} vs {user_prefs['favorite_genre']} (+{genre_pts:.2f})")
    total += genre_pts

    # --- Mood: +1.5 for exact match ---
    if song["mood"] == user_prefs["favorite_mood"]:
        mood_pts = 1.5
        reasons.append(f"mood match: {song['mood']} (+{mood_pts:.2f})")
    else:
        mood_pts = 0.0
        reasons.append(f"mood mismatch: {song['mood']} vs {user_prefs['favorite_mood']} (+{mood_pts:.2f})")
    total += mood_pts

    # --- Energy: proximity score, 0.0 to 1.0 ---
    energy_pts = 1.0 - abs(song["energy"] - user_prefs["target_energy"])
    reasons.append(f"energy proximity: |{song['energy']:.2f} - {user_prefs['target_energy']:.2f}| (+{energy_pts:.2f})")
    total += energy_pts

    # --- Acoustic: preference score, 0.0 to 0.5 ---
    if user_prefs["likes_acoustic"]:
        acoustic_pts = song["acousticness"] * 0.5
        reasons.append(f"acoustic fit: {song['acousticness']:.2f} × 0.5 (+{acoustic_pts:.2f})")
    else:
        acoustic_pts = (1.0 - song["acousticness"]) * 0.5
        reasons.append(f"non-acoustic fit: (1 - {song['acousticness']:.2f}) × 0.5 (+{acoustic_pts:.2f})")
    total += acoustic_pts

    return total, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Rank all songs by score descending and return the top k as (song, score, reasons) tuples."""
    # Step 1-2: Score every song in the catalog
    scored = [(song, *score_song(user_prefs, song)) for song in songs]

    # Step 3-4: Rank by score descending, return top k
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
