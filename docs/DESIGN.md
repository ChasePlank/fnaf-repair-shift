# Five Nights: Repair Shift — Design Doc

A non-commercial FNAF fan visual novel made in Ren'Py. The player is a night guard who repairs broken animatronics, one per night. Each FNAF game is its own chapter. Five Nights at Freddy's and its characters belong to Scott Cawthon. This project is for fun, not for sale.

The base game is not 18+.

## Core mechanic: repairs

Every repair night has **3 skill checks**:

| Check | What it is | Difficulty |
|---|---|---|
| 1. ARMS | Reattach and calibrate the arms | 1 hit, widest zone |
| 2. LEGS | Reattach and calibrate the legs | 1 hit, faster needle |
| 3. FULL REPAIR | Core, face, voice, final calibration | 3+ hits in a row, needle reverses direction every other hit, zone shrinks each hit |

- A needle sweeps around a ring. Press **Space / Enter**, **click**, or **tap** when it's in the white zone. The red sliver at the start of the zone is a **GREAT** hit.
- Pressing early, missing, or letting the needle pass is a **failure = death** (jumpscare, then "YOU DIED").
- **No rollback.** Retry by loading a manual save. The game reminds players to save at the start of each night.
- Story choices raise **trust** and can give a **zone bonus** on the final check (picking the "right" part for that animatronic).
- Later nights speed the needle up slightly (`nd` multiplier in each route).
- **Assist Mode** (Preferences → Repairs) slows the needle and widens zones.

## Chapters

### Chapter 1 — Freddy Fazbear's Pizza (FNAF 1) — BUILT
- Setting: the original location, abandoned. Phone Guy left tapes on the answering machine.
- Nights 1–4: player chooses the order, one per night: **Freddy, Bonnie, Chica, Foxy**.
- Night 5: **Golden Freddy**. He's the most broken, so his checks are harder (2 hits on arms and legs, 4 hits on full repair, faster needle, smaller zones).
- Ending: trust ≥ 10 → "The Last Show", otherwise "Closing Time". Both **unlock Chapter 2**.

### Chapter 2 — The New Location (FNAF 2) — PLANNED
- **Every Toy and every Withered animatronic gets its own repair night**, so Chapter 2 is longer than Chapter 1.
- Repair mechanic continues.
- Ends with **the Puppet**, who sends the player to Chapter 3.

### Chapter 3 — Fazbear's Fright (FNAF 3) — PLANNED
- Most animatronics are **hallucinations (phantoms)**.
- Each day the player investigates **what is trapping one phantom**, then frees it from what holds it. One phantom per day.
- Last night: **the Springtrap fight**. During the night the player finds his weakness, then fights him.
- **The fight is rigged.** It should feel very hard but winnable, never obviously scripted. The player loses no matter what, but **it is not a game over**. Instead a scene plays where Springtrap sends the player to Chapter 4.

### Chapter 4 — The Nightmare (FNAF 4) — PLANNED
- A nightmare the player must **survive**, played a lot like the original FNAF 4 (doors, closet, bed, flashlight, listening).
- Surviving it means the player **wakes up in the Sister Location elevator** → Chapter 5.

### Chapter 5 — Sister Location (FNAF 5) — PLANNED
- The player arrives **after Ennard has escaped** and the animatronics have been **scooped**.
- The facility seems **isolated**.
- Day 1: **Circus Baby**
- Day 2: **Funtime Freddy**
- Day 3: **Funtime Foxy**
- Day 4: **Ballora**
- Day 5: **Ennard returns**, and the player has to **destroy** him.

## Fan-made characters
The user plans to mix canon and fan-made animatronics. See the header of `game/characters.rpy` for how to add one.

## Content
Base game: horror, jump scares, dark themes. No 18+ content in the base game.
