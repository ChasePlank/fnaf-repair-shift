# Five Nights: Repair Shift

A FNAF fan visual novel built in [Ren'Py](https://www.renpy.org/) 8.3.7. You're a night guard who finds the first pizzeria and repairs its broken animatronics, one per night. Each repair has three timing-based skill checks. Fail one and you die, so save often.

> Non-commercial fan game. Five Nights at Freddy's and all related characters belong to Scott Cawthon. Not affiliated with or endorsed by Scott Games or Steel Wool.

## Status
- **Chapter 1 (FNAF 1): playable.** Freddy, Bonnie, Chica, Foxy, and Golden Freddy on Night 5.
- **Chapter 2 (FNAF 2): playable.** All Toys and Withereds (pick a group first), with the Puppet's music box finale.
- **Chapter 3 (FNAF 3): playable.** Free the three phantoms, find Springtrap's weakness, then survive (and lose) the fight.
- Chapters 4–5: planned. See [docs/DESIGN.md](docs/DESIGN.md).

## Playing
| Platform | How |
|---|---|
| Windows | Download `RepairShift-*-pc.zip` from the **latest** Release (or any Actions run), unzip, run `RepairShift.exe` |
| macOS | Download `RepairShift-*-mac.zip`, unzip, right-click → Open the first time (it's unsigned) |
| Android | Download the `.apk`, allow "install unknown apps", install |
| iPhone / iPad | Play the web build in Safari, then Share → Add to Home Screen. Native iOS builds need a Mac with Xcode (see below) |
| Any browser | Web build artifact (host the folder on any static host) |

## Building
Every push to `main` runs `.github/workflows/build.yml`. It builds the Windows/Linux, macOS, web, and Android versions and publishes them to a rolling `latest` GitHub Release. Pushing a tag like `v1.0` creates a permanent versioned Release.

Android signing uses repo secrets `ANDROID_KEYSTORE_B64` and `BUNDLE_KEYSTORE_B64` (base64 of `android.keystore` / `bundle.keystore`). Keep the same keystores, or phones won't install updates over the old version.

### Local
1. Install the [Ren'Py 8.3.7 SDK](https://www.renpy.org/latest.html).
2. Open the Ren'Py launcher → Preferences → Projects Directory → choose the folder that contains this repo.
3. Select **Five Nights: Repair Shift** → Launch Project.

### iOS (native)
Needs macOS + Xcode. In the Ren'Py launcher: iOS → Install the iOS toolkit → Create Xcode Project → open it in Xcode and run on your device. Installing to your own phone with a free Apple ID works for 7 days at a time. Sideloading long-term needs a $99/year Apple Developer account.

## Project layout
```
game/
  script.rpy            intro, night hub, Night 5, Chapter 1 ending, death screen
  routes_*.rpy          one file per animatronic repair
  skillcheck.rpy        the repair minigame + the label that handles death
  characters.rpy        characters, images, transforms, shared state
  chapters.rpy          chapter select + Chapter 2/3 stubs
  zz_devtest.rpy        developer-only test hooks (excluded from builds)
  images/bg, images/chars, audio/   placeholder assets
tools/make_placeholders.py   regenerates placeholder art/audio
docs/DESIGN.md               full chapter roadmap
```

### Replacing placeholder art
Drop a new PNG with the **same filename** into `game/images/chars/` or `game/images/bg/`. Character sprites are named `<key>_<stage>.png` with stages `broken`, `arms`, `legs`, `fixed`. Sprites are drawn on an 820×1060 canvas, bottom-aligned.

### Tuning skill checks
Each `call skill_check(who, part, hits=, speed=, zone=, reverse=)` in the route files controls one check:
- `hits` — hits needed in a row
- `speed` — needle speed multiplier (1.0 = 220°/s)
- `zone` — zone width in degrees (shrinks 8% per hit)
- `reverse` — alternate the needle direction every other hit
