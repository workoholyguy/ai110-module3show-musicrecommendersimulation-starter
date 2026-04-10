# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**TuneMatch 1.0**

---

## 2. Intended Use  

TuneMatch suggests 5 songs from a small catalog based on a listener's preferred genre, mood, energy level, and acoustic preference. It assumes the user knows what genre and mood they want ahead of time. This system is built for classroom exploration and learning about how recommender systems work. It is not intended for real-world use or production deployment.

---

## 3. How the Model Works  

The system looks at each song in the catalog and gives it a score based on how well it matches what the user likes. It checks four things:

- **Genre**: If the song's genre matches the user's favorite, it gets a big bonus. This is the strongest signal.
- **Mood**: If the song's mood matches, it gets a medium bonus.
- **Energy**: Songs with an energy level close to the user's target score higher. A calm person gets calm songs, an intense person gets intense songs.
- **Acousticness**: If the user likes acoustic music, songs that sound more acoustic get a small bonus. If not, less acoustic songs are rewarded instead.

Each song ends up with a score from 0 to 5. The system then sorts all songs by score and shows the top 5. During experimentation, I halved the genre weight and doubled the energy weight to see how the rankings would shift.

---

## 4. Data  

The catalog has 18 songs stored in a CSV file. Each song has 9 attributes: genre, mood, energy, tempo, valence, danceability, and acousticness, plus a title and artist.

The dataset covers 14 genres (pop, lofi, rock, ambient, jazz, synthwave, indie pop, r&b, hip-hop, classical, electronic, country, metal, reggae, latin) and 12 moods (happy, chill, intense, relaxed, focused, moody, romantic, energetic, sad, nostalgic, angry, uplifting).

Most genres only have 1 song, and lofi has 2. This means the system has very little to choose from within any single genre. The dataset also does not include any K-pop, afrobeat, or other globally popular styles, so it reflects a limited slice of musical taste.

---

## 5. Strengths  

The system works well for users with clear, consistent preferences. The Chill Lofi Listener got calm, acoustic tracks that felt like a real study playlist. The Happy Pop Fan got upbeat, energetic songs. When the user's preferences all point in the same direction, the recommendations feel natural and intuitive.

The scoring reasons printed alongside each result make it easy to understand exactly why a song was recommended. This transparency is a strength that many real-world systems lack.

---

## 6. Limitations and Bias 

Genre dominates the scoring even after reducing its weight. A pop listener will never be recommended a lofi track, even if it perfectly matches their mood and energy — creating a filter bubble. The edge case profile (sad mood + high energy) exposed that the system cannot handle contradictory preferences; it simply adds partial scores without recognizing the conflict.

Mood scoring is all-or-nothing. "Chill" and "relaxed" are very similar vibes, but the system treats them as completely different. There is no concept of similarity between moods or between genres.

The small catalog amplifies all of these issues. With most genres having only 1 song, a single bad metadata label could throw off the results significantly. The system also has no way to surface surprising or diverse picks — it always returns the closest matches, reinforcing whatever the user already likes.

---

## 7. Evaluation  

I tested four user profiles:

- **Happy Pop Fan** — pop, happy, 0.8 energy, non-acoustic
- **Chill Lofi Listener** — lofi, chill, 0.3 energy, acoustic
- **Intense Rock Fan** — rock, intense, 0.9 energy, non-acoustic
- **Edge Case** — jazz, sad, 0.95 energy, acoustic (contradictory preferences)

I looked at whether the top results matched my expectations for each listener type. The first three profiles all produced sensible results. The edge case was the most revealing — it still produced confident-looking scores even though the preferences were contradictory.

I also ran a weight shift experiment where I halved the genre weight (2.0 to 1.0) and doubled the energy weight (1.0 to 2.0). This caused songs with matching energy to climb the rankings even when their genre was wrong, showing how sensitive the results are to how you set the weights.

---

## 8. Future Work  

- **Mood similarity**: Instead of all-or-nothing matching, use a similarity score so "chill" and "relaxed" get partial credit.
- **Diversity penalty**: Prevent the top 5 from all being the same genre or artist. Real recommenders balance relevance with variety.
- **Bigger catalog**: With only 18 songs, the system is too constrained. A larger dataset would produce more meaningful rankings and reduce the impact of any single mislabeled song.

---

## 9. Personal Reflection  

Building this system taught me that recommenders are really just math rules applied to data — and those rules carry hidden opinions. Choosing to weight genre at 2.0 is a design decision that says "genre matters most," and that one choice shapes everything the user sees. It was surprising how much the results changed just from tweaking a single number.

The edge case experiment was the most eye-opening. The system looked confident even when the input made no sense. That made me think about how real apps like Spotify might also produce recommendations that look good on the surface but are based on contradictory or incomplete signals. It made me realize that the people designing these scoring rules have a lot of invisible power over what listeners discover.
