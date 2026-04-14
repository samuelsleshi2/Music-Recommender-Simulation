# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

This system suggests up to five songs from a 20-song catalog based on a user's preferred genre, mood, and energy level. It is built for classroom exploration and learning purposes only — not for production use with real listeners. The model assumes users can express their preferences as a single genre, mood, and a numeric energy target between 0.0 and 1.0.

---

## 3. How the Model Works

VibeFinder scores every song in the catalog against a user profile and ranks them from best to worst match. The scoring has three parts:

1. **Genre match** — if a song's genre matches the user's favorite genre, it gets the most points. Genre is weighted highest because it is the strongest signal of whether two songs belong in the same listening session.
2. **Mood match** — if the song's mood matches the user's preferred mood, it earns a smaller bonus. Mood is secondary because a song can cross moods depending on context.
3. **Energy closeness** — the system measures how far the song's energy level is from the user's target. A song with energy exactly equal to the target earns the maximum energy points; a song at the opposite end of the scale earns almost none. This is a continuous reward, not a yes/no check.

The song with the highest combined total of these three scores is recommended first. There is no randomness — the same preferences always produce the same ranking.

---

## 4. Data

The catalog contains 20 songs stored in `data/songs.csv`. Each song has the following features: `genre`, `mood`, `energy` (0.0–1.0), `tempo_bpm`, `valence`, `danceability`, and `acousticness`. The genres represented are: pop, lofi, rock, ambient, jazz, synthwave, indie pop, edm, country, classical, hip-hop, r&b, folk, metal, blues, reggae, and trap. The moods covered are: happy, chill, intense, relaxed, moody, focused. The dataset was hand-generated for simulation purposes and does not reflect any real streaming platform's catalog or listener population.

---

## 5. Strengths

- Works well for users with common, clearly defined preferences (e.g., "pop/happy/high energy"). For those profiles, the top result is intuitive and easy to explain.
- Every recommendation comes with a plain-language explanation of which features matched, making the system fully transparent.
- The continuous energy scoring means small differences in energy level are captured rather than being rounded to a binary match.
- The system is fast, simple, and has no external dependencies beyond Python's standard `csv` module.

---

## 6. Limitations and Bias

- **Genre dominance:** Because genre is worth +2.0 points and the next highest rule is only +1.0, a genre match effectively guarantees a top-3 finish. Users whose preferred genre has few songs in the catalog will keep seeing the same results.
- **Small catalog:** With only 20 songs, some moods (e.g., "focused") appear only once. This means a user targeting that mood will only ever get one mood match regardless of what else they prefer.
- **No diversity enforcement:** The system always returns the closest matches. If three songs tie on genre and mood, all three may be nearly identical in feel, creating a "filter bubble" with no variety.
- **Mood/genre conflict blind spot:** A user who wants high-energy music in a sad mood will find no song matches both, and the system silently ignores the unmet preference rather than flagging it.
- **No user history:** The same profile returns the same songs every time. The system cannot learn that a user skipped a song or discover changing tastes over time.

---

## 7. Evaluation

Three distinct user profiles were tested:

| Profile | Top Result | As Expected? |
|---|---|---|
| High-Energy Pop (`pop/happy/0.85`) | Sunrise City — genre + mood + high energy | Yes — clear winner |
| Chill Lofi (`lofi/chill/0.38`) | Library Rain & Midnight Coding tied at ~4.45 | Yes — both are genre + mood matches |
| Deep Intense Rock (`rock/intense/0.92`) | Storm Runner — only rock song, genre + mood | Yes, but only one real competitor |

An adversarial profile (`edm/sad/0.95`) revealed that when genre and mood point in opposite directions within the catalog, the system defaults to energy similarity as the tiebreaker. This produced a musically incoherent result — high-energy trap and metal songs ranked above any EDM track — because no EDM song carries a sad mood.

---

## 8. Future Work

- **Add collaborative filtering:** Collect data from multiple simulated users and recommend songs that similar users enjoyed, even if the content features don't obviously match.
- **Enforce diversity:** Cap how many songs from the same genre or artist can appear in a single top-5 list to prevent filter bubbles.
- **Weight experimentation interface:** Let the user adjust genre/mood/energy weights at runtime to see how the ranking changes, rather than hard-coding them.
- **Expand the catalog:** A larger dataset would make genre-specific recommendations more meaningful and reduce the repeat-result problem.
- **Use tempo and valence in scoring:** Both features are already stored per song but unused in the scoring formula. A user who prefers slow, melancholic music could benefit from matching on those dimensions too.

---

## 9. Personal Reflection

Building VibeFinder made it clear how much complexity is hidden behind a "simple" feature weight. Deciding that genre should be worth twice as much as mood felt intuitive at first, but testing the adversarial EDM/sad profile exposed that this single ratio can cause the system to completely ignore a preference when the catalog doesn't support it. Real platforms like Spotify solve this by blending dozens of signals — audio embeddings, playlist co-occurrence, skip rates — so no single feature can dominate the way genre does here.

The most surprising moment was seeing how well the system worked for the "mainstream" profiles (pop, lofi, rock) and how quickly it fell apart at the edges. That gap mirrors what happens in production AI systems: they perform well on common cases because most training data reflects common users, and they silently fail on edge cases because no one explicitly tested for them. This project gave a concrete, hands-on feel for why fairness and bias evaluation — not just accuracy — have to be part of building any recommender.
