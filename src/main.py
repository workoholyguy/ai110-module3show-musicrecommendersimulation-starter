"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # User taste profile — target values the scoring rule compares each song against
    user_prefs = {
        "favorite_genre": "pop",  # categorical: exact-match bonus
        "favorite_mood": "happy",  # categorical: exact-match bonus
        "target_energy": 0.80,  # numeric: proximity score (closer = better)
        "likes_acoustic": False,  # boolean: prefers non-acoustic tracks
    }

    # Profile 2: Chill Lofi listener
    chill_user = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.30,
        "likes_acoustic": True,
    }

    # Profile 3: Intense Rock listener
    rock_user = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "likes_acoustic": False,
    }

    # Profile 4: Edge case — conflicting preferences
    edge_user = {
        "favorite_genre": "jazz",
        "favorite_mood": "sad",
        "target_energy": 0.95,  # wants high energy but sad mood?
        "likes_acoustic": True,
    }

    profiles = [
        ("Happy Pop Fan", user_prefs),
        ("Chill Lofi Listener", chill_user),
        ("Intense Rock Fan", rock_user),
        ("Edge Case: Sad + High Energy", edge_user),
    ]

    for name, prefs in profiles:
        recommendations = recommend_songs(prefs, songs, k=5)

        # --- Header ---
        print("\n" + "=" * 60)
        print(f"  {name}")
        print(
            f"  User Profile: genre={prefs['favorite_genre']}, "
            f"mood={prefs['favorite_mood']}, "
            f"energy={prefs['target_energy']}, "
            f"acoustic={'yes' if prefs['likes_acoustic'] else 'no'}"
        )
        print("=" * 60)

        # --- Ranked results ---
        for rank, (song, score, reasons) in enumerate(recommendations, start=1):
            bar_length = int(score / 5.0 * 20)
            bar = "#" * bar_length + "-" * (20 - bar_length)

            print(f"\n  #{rank}  {song['title']} — {song['artist']}")
            print(
                f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}"
            )
            print(f"       Score: {score:.2f} / 5.00  [{bar}]")
            print(f"       Reasons:")
            for reason in reasons:
                print(f"         + {reason}")

        # --- Footer ---
        print("\n" + "-" * 60)
        print(f"  Showing top {len(recommendations)} of {len(songs)} songs")
        print("-" * 60 + "\n")


if __name__ == "__main__":
    main()
