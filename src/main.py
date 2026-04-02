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
        "favorite_genre": "pop",         # categorical: exact-match bonus
        "favorite_mood": "happy",        # categorical: exact-match bonus
        "target_energy": 0.80,           # numeric: proximity score (closer = better)
        "likes_acoustic": False,         # boolean: prefers non-acoustic tracks
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # --- Header ---
    print("\n" + "=" * 60)
    print(f"  User Profile: genre={user_prefs['favorite_genre']}, "
          f"mood={user_prefs['favorite_mood']}, "
          f"energy={user_prefs['target_energy']}, "
          f"acoustic={'yes' if user_prefs['likes_acoustic'] else 'no'}")
    print("=" * 60)

    # --- Ranked results ---
    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        bar_length = int(score / 5.0 * 20)
        bar = "#" * bar_length + "-" * (20 - bar_length)

        print(f"\n  #{rank}  {song['title']} — {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
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
