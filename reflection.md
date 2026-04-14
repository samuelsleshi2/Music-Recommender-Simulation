# Reflection: Comparing User Profiles

## High-Energy Pop vs. Chill Lofi

The pop profile (genre=pop, mood=happy, energy=0.85) and the lofi profile (genre=lofi, mood=chill, energy=0.38) produce completely non-overlapping top-5 lists. This makes sense: the two genre weights alone create a hard separation, and their energy targets are on opposite ends of the scale (0.85 vs 0.38). The pop profile rewards fast, upbeat tracks while the lofi profile rewards slow, acoustic ones. Both profiles found strong matches in the catalog, which confirms that having genre AND mood match at the same time is a reliable signal.

## Chill Lofi vs. Deep Intense Rock

Both profiles found a clear #1 result (Library Rain for lofi, Storm Runner for rock), but the rock profile's remaining top-4 were all from different genres. That happened because rock is the only "rock" song in the catalog — once Storm Runner wins on genre + mood + energy, there is no second rock song to fill spot 2. The system filled the gap with high-energy songs from edm, trap, and metal instead. This shows the system's biggest weakness: a one-song genre has nowhere to go after the first result. The lofi profile didn't hit this problem because there are three lofi songs, giving the ranker real choices.

## High-Energy Pop vs. Deep Intense Rock

Both users want intense, high-energy music. But because their genres differ (pop vs. rock), their top results diverge immediately. Gym Hero (pop/intense/0.93) appears in the pop profile's #2 slot but doesn't appear at all in the rock profile's top 5 — the rock profile's mood bonus pulls intense non-rock songs ahead of pop songs with slightly lower energy. This shows that mood and genre working together as filters is more powerful than energy alone. A user who only described their energy preference (0.9) without specifying genre would get a very different, more eclectic list.
