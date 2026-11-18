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

### Chapter 2 — The New Location (FNAF 2) — BUILT
- Roster: **Toy Freddy, Toy Bonnie, Toy Chica, Mangle** and **Withered Freddy, Bonnie, Chica, Foxy**. No Balloon Boy, JJ, or Golden Freddy (he was the Chapter 1 finale).
- The player first picks a group (Toys or Withered), then repairs everyone in it, one per night, in any order. The other group only opens after the first group is finished.
- **Mangle is harder** (2 hits on arms and legs, 4 hits on full repair, faster needle).
- Finale: **the Puppet**. The player repairs her **music box**, not her. Hold to keep it wound while the meter drains faster and faster. If it runs out, the Puppet rises and you die. Order: wind, then CRANK, then wind, then COMB & SPRING, then wind, then FULL REPAIR (a harder check).
- Ending: trust ≥ 16 gives "The Gift", otherwise "The Quiet". Both **unlock Chapter 3**. The Puppet sends the player 30 years ahead.

### Carry-over and memory
- **Good endings make the next chapter easier**: a Chapter 1 good ending gives easier Chapter 2 checks, and a Chapter 2 good ending gives easier Chapter 3 checks, and so on (needle ×0.88 speed, wider zones).
- **Only the finale characters remember earlier chapters** (the Puppet and Springtrap). Everyone else meets the player fresh.

### Chapter 3 — Fazbear's Fright (FNAF 3) — BUILT
- Thirty years later. The Puppet sends the player here, but **she is gone when they arrive**.
- Phantoms: **Phantom Freddy** (missing his microphone), **Phantom Chica** (missing her cupcake) and **Phantom Foxy** (missing his hook). There's no Phantom Bonnie.
- Nights 1–3: the player picks one phantom per night and searches Fazbear's Fright for its item (arcade, prop storage, vents, old attraction rooms). **No skill checks.** Each wrong spot gives a clue and a harmless phantom jumpscare, because phantoms are hallucinations. Finding the item makes the phantom **ascend**, and it's gone for the rest of the game.
- Night 4: Springtrap confronts the player. He **remembers Chapters 1 and 2**. The player finds his weakness in three places (springlock manual, old Phone Guy tape, a pipe falling on his knee) and takes a crowbar. **A crowbar to the knees.**
- Night 5: the fight. Springtrap chases the player into the office. Then the checks alternate between **SWING** (hit his knees, and he cries out in pain) and **DODGE**, and every round gets faster with smaller zones.
  - It takes 3 knee hits to win and 3 misses to lose, but **the player is never told either number**.
  - **The fight is rigged.** The third knee hit is far harder than anything before it, and if somebody lands it anyway, Springtrap catches the crowbar.
  - Losing is **not a game over**. Springtrap sends the player into the Chapter 4 nightmare, and he is gone when they wake up there.
- Ending: calm ≥ 6 (phantoms found quickly, kind choices) gives "Set Free", otherwise "Still Haunted". Both **unlock Chapter 4**. A good ending makes Chapter 4 easier.

### Rule: chapter hand-offs
The character who sends the player to the next chapter talks to them about it first. When the player arrives, that character is gone.

### Chapter 4 — The Nightmare (FNAF 4) — BUILT
- **Real-time survival**, played like the original FNAF 4. It's not a visual novel: no dialogue and no choices. The nightmares never talk; they're in your head and just want you dead.
- **Intro tutorial** before Night 1 ("THIS CHAPTER IS DIFFERENT") explains that the nightmares are timed and that death can come at any moment, then walks through the controls.
- **5 nights, 5 real minutes each** (12 AM–6 AM).
- Views: room, left door, right door, closet, bed. Keys: A/D/W/S, F or Shift for the flashlight, Space to hold doors or the closet. On-screen buttons handle touch.
- Rules: if you hear breathing at a door, hold it shut and don't use the light. Far down the hall, the light scares them off. Foxy moves through closet stages. Freddles pile up on the bed.
- Roster: Nightmare Bonnie, Chica, Foxy, and Freddy, and **Nightmare Fredbear on Night 5**. Difficulty goes up each night.
- **Death → Retry Night** (restarts that night from 12 AM), Load a Save, or Main Menu. You can't save during a night; saves happen between nights. If the game menu interrupts a night, the night restarts.
- Assist Mode: captions for audio cues plus more reaction time. A good Chapter 3 ending also gives a little extra slack.
- Ending: wake up in the Sister Location elevator. ≤3 total deaths = **WIDE AWAKE** (good, Chapter 5 is easier), otherwise **STILL DREAMING**. Unlocks Chapter 5 (currently a stub).

### Chapter 5 — Sister Location (FNAF 5) — BUILT
- The player arrives (silent elevator) **after Ennard has escaped** and the animatronics have been **scooped**: empty shells. The facility is isolated.
- **HandUnit** greets you. He thinks you're the new technician getting things ready for "showtime", calls you "Eggs Benedict", and has no idea what happened, here or in earlier chapters.
- Each repair has **four** skill checks: arms, legs, **face**, then the full repair (hardest).
- Choices are **timed** and meant to feel rushed: 7 s on Baby's day, 5 s on Days 2–4, 4 s in the Ennard chase (Assist Mode +50%, good Ch4 ending +20%).
- A wrong answer, or running out of time, makes it worse: it fills that animatronic's meter (max 3 = death) and makes the next skill checks faster.
- **Circus Baby** can help, but you have to ask: once she's fixed, timed choices show "Ask Circus Baby for a hint". The clock keeps running. She knows what's needed in this chapter but nothing about earlier ones.
- Day 1: **Circus Baby** (easiest; she talks you through her own repair, with no meter).
- Day 2: **Funtime Freddy**, ANGER. He angers easily; use **Bon-Bon** to keep him calm.
- Day 3: **Funtime Foxy**, SEEN. He sees; be stealthy (move in the dark, freeze in the light).
- Day 4: **Ballora**, NOISE. She hears; be quiet (move under the music).
- Day 5: **Ennard returns.** He knows everything from Chapters 1–4. A chase with timed choices (CLOSE meter) and dodge checks: power the Scooping Room at the Breaker Room, lead him through Ballora Gallery, bait him onto the platform, dive, hit the SCOOP button.
- Death is a normal game over (load a save).
- Endings: 4 or fewer mistakes = **SHOWTIME** (good, Chapter 6 easier), otherwise **SCOOPED OUT**.
- Hand-off: Circus Baby tells you about a new pizzeria and sends you up the elevator. When you arrive, her voice is gone. Unlocks Chapter 6.

### Chapter 6 — Freddy Fazbear's Pizzeria (FNAF 6) — PLANNED
- Pizzeria Simulator: run the pizzeria by day, survive at night (true-game style).
- Salvage minigame first, for Scrap Baby, Molten Freddy, Lefty and the Springtrap variant (Scraptrap). **You can't abandon a salvage.** Failing isn't death: that animatronic becomes an enemy you have to survive at night. Passing means you don't have to deal with them.
- Scraptrap is the main antagonist. He's technically Springtrap, which is why he didn't die in Chapter 3. The whole game builds toward finding and killing him.
- **Final battle:** the characters who remember earlier chapters help you (Golden Freddy, the Puppet, Springtrap?, Ennard?). A chapter's good ending makes its helper stronger (e.g. good Ch1 ending = stronger Golden Freddy).

## Fan-made characters
The user plans to mix canon and fan-made animatronics. See the header of `game/characters.rpy` for how to add one.

## Content
Base game: horror, jump scares, dark themes. No 18+ content in the base game.
