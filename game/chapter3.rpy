## =============================================================================
## CHAPTER 3 — Fazbear's Fright (FNAF 3)
## Thirty years later. Most of what you see here are hallucinations.
##   Nights 1-3: free one phantom per night by finding what holds them here
##               (Freddy's microphone, Chica's cupcake, Foxy's hook). No skill
##               checks. Finding the item lets the phantom ascend for good.
##   Night 4:    find Springtrap's weakness (a crowbar to the knees).
##   Night 5:    the fight. Swing / dodge skill checks that keep getting harder.
##               3 misses and he has you. The player is never told how many
##               hits win or how many misses lose, so it feels winnable. The fight is meant to be lost, but it
##               should only LOOK impossibly hard. Losing is not a game over:
##               Springtrap sends you into the Chapter 4 nightmare.
## Only Springtrap remembers Chapters 1 and 2. The phantoms do not.
## =============================================================================

init python:
    CH3_PHANTOMS = ["phantomfreddy", "phantomchica", "phantomfoxy"]

    ## Places you can search. Each phantom's item is in exactly one of them.
    CH3_SPOTS = [
        ("arcade",     "The arcade hall",          "fright_arcade"),
        ("storage",    "Prop storage",             "fright_storage"),
        ("vent",       "The ventilation shafts",   "fright_vent"),
        ("attraction", "The old attraction rooms", "fright_attraction"),
    ]

    ## Lines are (speaker, text) — see say_lines in chapter2.rpy.
    ## choice: (text, calm_gain, [lines]). wrong: spot -> [lines] (each one is a clue).
    PHANTOMS = {}

    PHANTOMS["phantomfreddy"] = dict(
        item="microphone", spot="attraction",
        intro=[("n", "Something walks past the office window. Slow. Heavy. Burnt."),
               ("n", "Then it's standing in the window, looking in. A bear, charred black, with nothing but two white pinpricks for eyes."),
               ("pf", "...the... song... I can't... sing the song..."),
               ("g", "You're not real. The Phone Dude said nothing in here is real."),
               ("pf", "...real enough... to stay... I can't leave... without it..."),
               ("pf", "...my microphone... I always had it... on stage... where is the stage...?")],
        choice=[("\"I'll find your microphone.\"", 1, [("pf", "...you... would do that...? ...for something that isn't real...?")]),
                ("\"Go away.\"", 0, [("n", "He doesn't go away. He just stares, until the camera static swallows him.")])],
        wrong={
            "arcade": [("n", "Rows of dead arcade cabinets. A prize counter, empty. No microphone."),
                       ("n", "One cabinet screen flickers on by itself. It shows a tiny stage, and a bear on it, singing.")],
            "storage": [("n", "Boxes of Fazbear junk. Masks, a plastic cupcake, an old pirate sign. No microphone."),
                        ("n", "Scribbled on a crate: {i}\"stage props → back to the old rooms\"{/i}.")],
            "vent": [("n", "I crawl into the shaft. It's tight and hot and smells like old smoke. Nothing in here but dust."),
                     ("n", "Somewhere ahead, through the metal, I hear a song. It's coming from the old attraction rooms.")],
            "attraction": [],
        },
        found=[("n", "The old attraction rooms. Somebody rebuilt a tiny show stage out of plywood, for the tourists."),
               ("n", "A burnt microphone is lying on it. Its cord is melted to the boards."),
               ("n", "I pull it free and hold it up to the dark.")],
        ascend=[("pf", "...my song... I remember it now..."),
                ("pf", "...thank you... I don't know you... but thank you..."),
                ("n", "He takes the microphone. For a second he isn't burnt at all. Just a brown bear in a top hat, smiling."),
                ("n", "Then he's gone. Not hiding. Gone.")],
    )

    PHANTOMS["phantomchica"] = dict(
        item="cupcake", spot="arcade",
        intro=[("n", "One of the monitors goes black. When it comes back, there's a face on it. Huge, burnt, yellow, mouth hanging open."),
               ("pc", "...let's... eat..."),
               ("g", "That's just a screen. That's just a screen."),
               ("pc", "...my... cupcake... someone took... my cupcake..."),
               ("pc", "...I can't go... without it... I always carried it... always...")],
        choice=[("\"What does it look like?\"", 1, [("pc", "...pink... a candle on top... it has eyes... it watches the games..."), ("g", "Watches the games?")]),
                ("Turn the monitor off.", 0, [("n", "It doesn't turn off. The face just sits there behind the glass, smiling.")])],
        wrong={
            "storage": [("n", "There's a plastic cupcake in here. My heart jumps. Then I see it's a cheap gift-shop copy, still in the plastic."),
                        ("n", "On the box: {i}\"originals displayed at the prize counter.\"{/i}")],
            "vent": [("n", "Nothing in the vent. Just a faint beep... beep... from somewhere nearby. Like an old game cabinet."),
                     ("n", "The vent opens above the arcade hall.")],
            "attraction": [("n", "The old attraction rooms. A fake stage. A rubber Foxy hook nailed to the wall. No cupcake."),
                           ("n", "Somebody taped a sign to the door: {i}\"ARCADE → prizes, tokens, display items\"{/i}.")],
            "arcade": [],
        },
        found=[("n", "The arcade hall. One cabinet is still on, a little game with a pixel cupcake bouncing across the screen."),
               ("n", "And on top of the cabinet, sitting right where it can watch the game, is a pink cupcake with one candle."),
               ("n", "It's burnt around the edges. Its eyes are still bright.")],
        ascend=[("pc", "...there you are... there you are..."),
                ("pc", "...I don't know you... but you found it... thank you..."),
                ("n", "She cradles the cupcake. For a moment her bib is clean and white, and the words on it are bright red."),
                ("n", "{b}LET'S EAT!!!{/b}"),
                ("n", "Then the monitor shows only an empty room.")],
    )

    PHANTOMS["phantomfoxy"] = dict(
        item="hook", spot="storage",
        intro=[("n", "Something's crouched in the office doorway. A fox, charred to the frame, one arm ending in a bare stump."),
               ("px", "...ye... ye took it... didn't ye..."),
               ("g", "Took what? I didn't take anything."),
               ("px", "...me hook... a pirate's nothin' without his hook..."),
               ("px", "...can't sail on... can't leave this place... without it...")],
        choice=[("\"I'll get it back for you, captain.\"", 1, [("px", "...captain... nobody's called me that... in a long time...")]),
                ("\"I don't have it.\"", 0, [("px", "...then FIND IT...")])],
        wrong={
            "arcade": [("n", "Arcade cabinets. A pirate-themed one, with a plastic hook bolted to the side. It's a toy. It snaps off in my hand."),
                       ("n", "Not his. His would be real metal. Old. Heavy. Something they'd box up and forget.")],
            "vent": [("n", "Halfway down the shaft, something scrapes the metal. Long, slow scratches. Like a hook dragged along a wall."),
                     ("n", "The scratches lead toward prop storage.")],
            "attraction": [("n", "The old attraction rooms. There's a rubber hook nailed up on the wall as decoration."),
                           ("n", "There's a label under it: {i}\"replica — original in storage, too sharp for display.\"{/i}")],
            "storage": [],
        },
        found=[("n", "Prop storage. Under a pile of masks and cardboard cutouts there's a long box marked {b}FOXY — DO NOT DISPLAY{/b}."),
               ("n", "Inside, wrapped in an old pirate flag, is a hook. Real steel. Burnt black, but still sharp.")],
        ascend=[("px", "...that's it... that's MINE..."),
                ("px", "...I don't know who ye are, matey... but ye'd make a fine first mate..."),
                ("n", "The hook clicks onto his arm. For one second he's red and bright, eyepatch up, grinning."),
                ("n", "Then the doorway is empty, and the office is quiet.")],
    )


## ---------------------------------------------------------------- helpers
## A phantom jumpscare. Phantoms are hallucinations, so this is NOT a death.
label phantom_scare(key):
    play sound "audio/jumpscare.wav"
    show redflash at flicker
    $ renpy.show(key + " broken", at_list=[jumpscare_in])
    pause 0.7
    $ renpy.hide(key)
    hide redflash
    with Dissolve(0.3)
    "...It's gone. It wasn't real. My heart doesn't believe that."
    return


## Search Fazbear's Fright for a phantom's item. No skill checks.
## Each wrong spot gives a clue and a (harmless) phantom scare.
label ch3_search(key):
    $ P = PHANTOMS[key]
    $ _tried = []
    $ _wrong = 0
    $ _item = P["item"]
    while True:
        $ _opts = [(name, sid) for (sid, name, bg) in CH3_SPOTS if sid not in _tried]
        "Where should I look for the [_item]?"
        $ _spot = renpy.display_menu(_opts)
        $ _bg = [bg for (sid, name, bg) in CH3_SPOTS if sid == _spot][0]
        scene expression "bg " + _bg
        with dissolve
        if _spot == P["spot"]:
            call say_lines(P["found"])
            jump ch3_search_done
        $ _tried.append(_spot)
        $ _wrong += 1
        call say_lines(P["wrong"][_spot])
        call phantom_scare(key)
label ch3_search_done:
    ## Finding things fast keeps the phantoms (and you) calm.
    $ calm += 2 if _wrong <= 1 else (1 if _wrong == 2 else 0)
    return


label free_phantom(key):
    $ P = PHANTOMS[key]
    $ current_anim = key
    scene bg fright_office
    with dissolve
    $ renpy.show(key + " broken", at_list=[phantom_flicker(0.5)])
    with dissolve
    call say_lines(P["intro"])
    $ _c = renpy.display_menu([(o[0], i) for i, o in enumerate(P["choice"])])
    $ calm += P["choice"][_c][1]
    call say_lines(P["choice"][_c][2])
    $ renpy.hide(key)
    with dissolve
    "It's just me and the hum of the cameras again."
    call ch3_search(key)
    play sound "audio/chime.wav"
    $ renpy.show(key + " fixed", at_list=[sprite_pos(0.5)])
    with flash
    call say_lines(P["ascend"][:2])
    $ renpy.show(key + " fixed", at_list=[ascend])
    call say_lines(P["ascend"][2:])
    $ renpy.hide(key)
    $ freed.append(key)
    return


## A fight check: like skill_check, but failing does NOT jump to game over.
label fight_check(title, speed, zone, reverse=False):
    $ _skip_was = config.allow_skipping
    $ config.allow_skipping = False
    $ renpy.block_rollback()
    play sound "audio/check_alert.wav"
    $ _sc = renpy.call_screen("skill_check", who="Springtrap", part="", hits=1, speed=speed, zone=zone, reverse=reverse, title=title)
    $ config.allow_skipping = _skip_was
    if config.developer and getattr(store, "_autohit", False):
        $ open("/tmp/devlog.txt", "a").write("springtrap %s %s round=%s speed=%.2f zone=%.0f\n" % (title, _sc, fight_round, speed, zone))
        $ config.skipping = "fast"
    return _sc


## ---------------------------------------------------------------- chapter start
label chapter3_start:
    $ reset_chapter_state(3)
    $ chapter_ease = 2 in persistent.good_endings
    $ calm = 0
    $ freed = []
    $ weakness_clues = []
    scene black
    with dissolve
    show text "{size=90}{b}CHAPTER 3{/b}{/size}\n{size=40}Fazbear's Fright{/size}" at truecenter
    with dissolve
    pause 2.0
    hide text

    $ guard_name = renpy.input("Night guard, what's your name?", default=persistent.guard_name or "Mike", length=16).strip() or "Mike"
    $ persistent.guard_name = guard_name
    if chapter_ease:
        "{i}(You earned the good ending in Chapter 2. Skill checks this chapter are a little easier.){/i}"

    ## The Puppet sent you here. When you arrive, she is gone.
    "The music box is still playing when I open my eyes. Then it isn't."
    scene bg fright_office
    with slowfade
    play music "audio/ambience.wav" fadein 3.0 volume 0.45
    "I'm in a security office. But not the Prize Corner. Not any office I know."
    g "Hello? Are you there?"
    "No striped hands. No white mask. No gift box. The Puppet is gone, like she was never here."
    "There's a newspaper on the desk. The date is thirty years after the night I fixed her music box."
    "{b}FAZBEAR'S FRIGHT: THE HORROR ATTRACTION — OPENING SOON{/b}"
    "The phone on the desk rings."
    pdude "Hey, hey! You made it! Welcome to Fazbear's Fright, man!"
    pdude "So, we spent all year looking for real Fazbear stuff for the attraction. And we found... one. One real one. He's, uh, in the back."
    pdude "Everything else is props. Masks, cutouts, a couple of old arcade games. Oh, and the wiring's bad. You might see stuff on the cameras."
    pdude "Like, burnt-looking stuff. Don't worry about it. It's not real. Probably the smoke from the fire. Old fire. Totally out now."
    pdude "Alright, see you tomorrow!"
    "Not real. That's what the Puppet said, too."
    "{i}\"The others there aren't real. Not really. You'll have to figure out what's holding each of them.\"{/i}"
    jump ch3_night_hub


label ch3_night_hub:
    $ night += 1
    $ current_anim = None
    scene black
    with dissolve
    show text "{size=90}{b}NIGHT [night]{/b}{/size}\n{size=40}12:00 AM{/size}" at truecenter
    with dissolve
    pause 1.4
    hide text
    scene bg fright_office
    with dissolve
    $ renpy.notify("Good moment to save your game.")

    if night == 4:
        jump ch3_weakness
    if night == 5:
        jump ch3_fight

    if night == 2:
        pdude "Hey, man! Night two. Somebody on the cleaning crew said they heard a, uh, voice? From the back room? Saying a name?"
        pdude "I think it was your name. Weird, right? Anyway!"
        spt "{size=-6}...[guard_name]...{/size}"
        "The voice comes through the vent. Low. Rotten. And it {i}knows my name{/i}."
    elif night == 3:
        pdude "Okay, so, the attraction's almost ready. That one real animatronic? We can't find him. He's not where we left him."
        pdude "He's probably fine."
        "On Camera 08, something tall and green stands in the hallway. When I blink, it's closer to the camera."

    $ _left = [k for k in CH3_PHANTOMS if k not in freed]
    "Something in this place is haunted tonight. Which one should I help?"
    $ _pick = renpy.display_menu([("%s — %s" % (ANIM[k]["name"], ANIM[k]["where"]), k) for k in _left])
    call free_phantom(_pick)

    scene black
    with dissolve
    play sound "audio/chime.wav"
    show text "{size=110}{b}6:00 AM{/b}{/size}" at truecenter
    with dissolve
    pause 2.0
    hide text
    $ _done = len(freed)
    "[_done] of 3 set free."
    if _done == 3:
        "The phantoms are gone. All of them. The cameras show empty rooms."
        "All except one."
    jump ch3_night_hub


## ---------------------------------------------------------------- Night 4: the weakness
label ch3_weakness:
    pdude "Hey, man. So. I'm gonna be honest with you. We found him, and then we lost him again."
    pdude "He's an old suit. A springlock suit. Like a costume with a robot inside, with these spring things that hold the robot parts back."
    pdude "And there's... something inside. We think it's just, like, old stuffing. We really hope it's just stuffing."
    pdude "Look, if anything goes wrong tonight, there's a fire cabinet by the office. Just, uh, don't break anything. It's all we've got."
    "The phone clicks off."
    scene bg fright_hall
    with dissolve
    show springtrap broken at sprite_pos(0.5)
    with dissolve
    "He's standing at the end of the hallway. Green. Rotted. Patched together. And unlike the others, he doesn't flicker."
    "He's real."
    spt "There you are."
    spt "The Puppet's little night guard. [guard_name]."
    g "...How do you know me?"
    spt "Oh, I know all about you. I was {i}there{/i}."
    spt "The first place. You screwed the golden one back together, bolt by bolt."
    spt "The second place. You wound up that ugly music box so the Puppet could sleep."
    spt "You fix things. That's what you do. You put back together everything I took apart."
    spt "You set my little ghosts free, too. Freddy. Chica. Foxy. They don't remember you. But I remember everything."
    menu:
        "\"What do you want?\"":
            spt "Tomorrow night, I'll show you."
        "Say nothing.":
            $ calm += 1
            spt "Quiet. Smart. It won't help."
    hide springtrap
    with dissolve
    "When the static clears, the hallway is empty."
    "I have one night to find out how to hurt something that won't die."

    $ _clues_left = [("manual", "Read the old springlock manual in prop storage"),
                     ("tape", "Play the old training tapes in the arcade office"),
                     ("vent", "Follow the scraping sound into the vents")]
    while _clues_left:
        $ _c = renpy.display_menu([(t, k) for (k, t) in _clues_left])
        $ _clues_left = [(k, t) for (k, t) in _clues_left if k != _c]
        if _c == "manual":
            scene bg fright_storage
            with dissolve
            "A binder, water-damaged, labeled {b}SPRING BONNIE / SPRINGLOCK SUIT — EMPLOYEE GUIDE{/b}."
            "{i}\"The springlocks are under tension at every joint. The KNEE locks are the thinnest and the most worn. Never strike, kneel on, or bend the knees past their limit.\"{/i}"
            "The knees. Underlined twice. Someone circled it in red pen a long time ago."
            $ weakness_clues.append("manual")
        elif _c == "tape":
            scene bg fright_arcade
            with dissolve
            "A box of old cassettes behind the arcade. I find one labeled {b}TRAINING — SPRINGLOCK SAFETY{/b}."
            phone "Uh, hello, hello! So the springlock suits are, uh, temporarily retired. Just don't put weight on the legs."
            phone "The locks in the knees are, uh, the first to go. One good knock and — well. You'll hear it."
            "I know that voice. Phone Guy. From the first place. Thirty years and he still sounds nervous."
            $ weakness_clues.append("tape")
        else:
            scene bg fright_vent
            with dissolve
            "I crawl toward the scraping. It stops. Right below me, through the vent grate, is the top of a green head."
            "My elbow knocks a loose piece of metal pipe off a ledge. It drops straight down."
            play sound "audio/servo.wav"
            with vpunch
            "It hits his knee with a hollow clang."
            spt "{size=+10}AAAAGH—!{/size}"
            "He staggers. He actually staggers. Then he drags himself off into the dark, hissing."
            g "...That hurt him. Something actually hurt him."
            $ weakness_clues.append("vent")

    scene bg fright_office
    with dissolve
    "Three different places. Three times the same answer."
    "{b}The knees.{/b}"
    "The fire cabinet by the office door. Behind the glass: an extinguisher, a hose, and a long steel crowbar."
    menu:
        "Take the crowbar.":
            pass
        "Take the crowbar. And the extinguisher, just in case.":
            "The extinguisher is empty. Of course it is. I keep the crowbar."
    "Heavy. Cold. Good."
    g "A crowbar to the knees. That's the plan. That's the whole plan."
    spt "{size=-6}...I heard that...{/size}"
    scene black
    with dissolve
    play sound "audio/chime.wav"
    show text "{size=110}{b}6:00 AM{/b}{/size}" at truecenter
    with dissolve
    pause 2.0
    hide text
    jump ch3_night_hub


## ---------------------------------------------------------------- Night 5: the fight
## The fight is designed to be lost, but it should only LOOK impossibly hard.
## Every round both checks get faster with smaller zones. The third knee hit
## (the one that would win) is far harder than the rest. If somebody still
## lands it, Springtrap catches the crowbar at the last second.
label ch3_fight:
    $ st_hits = 0
    $ st_fails = 0
    $ fight_round = 0
    pdude "Last night, man! The attraction opens tomorrow! Just get through tonight and—"
    "The line goes dead. The lights go dead. Then the emergency lights come on, red."
    scene bg fright_hall
    with dissolve
    show springtrap broken at sprite_pos(0.5)
    with vpunch
    spt "No more cameras. No more ghosts. Just you and me."
    "He's fast. Much faster than something that rotten should be."
    "I run."
    scene bg fright_attraction
    with Dissolve(0.25)
    "Through the old attraction rooms. Past the plywood stage."
    scene bg fright_arcade
    with Dissolve(0.25)
    "Past the dead arcade cabinets. His footsteps are right behind me. Clank. Clank. Clank."
    scene bg fright_office
    with Dissolve(0.25)
    "Into the office. Dead end. I turn around with the crowbar up."
    show springtrap broken at sprite_pos(0.5)
    with vpunch
    spt "Go on, then. Hit me."

    while st_fails < 3:
        ## ---- swing
        $ _sp = 1.15 + 0.45 * fight_round
        $ _zn = max(14, 52 - 10 * fight_round)
        if st_hits == 2:
            ## The winning blow. Far harder than anything before it.
            $ _sp = _sp * 1.8 + 0.6
            $ _zn = 12
        call fight_check("SWING — HIS KNEES", _sp, _zn, reverse=(fight_round % 2 == 1))
        if _return != "fail" and st_hits == 2:
            ## Even a perfect swing doesn't land the third time.
            play sound "audio/servo.wav"
            show springtrap broken at hit_shake
            with vpunch
            "The crowbar is an inch from his knee— and his hand closes around it."
            spt "Not. This. Time."
            "He rips it sideways and slams me into the desk."
            $ st_fails += 1
        elif _return != "fail":
            $ st_hits += 1
            play sound "audio/jumpscare.wav"
            show springtrap hurt at hit_shake
            with vpunch
            if st_hits == 1:
                "The crowbar cracks into his left knee. Something inside the suit {i}snaps{/i}."
                spt "{size=+12}AAAAAGH!{/size}"
                spt "You— you little—"
            else:
                "Right knee. Square on. He drops to one leg, howling."
                spt "{size=+14}GRAAAAAHH!{/size}"
                "He's slowing down. Maybe. Maybe I can actually do this."
            show springtrap broken at sprite_pos(0.5)
        else:
            $ st_fails += 1
            show redflash at flicker
            with vpunch
            "I swing wide. The crowbar clangs off the wall and he's right on me, claws first."
        if st_fails >= 3:
            jump ch3_end

        ## ---- dodge
        $ _sp = 1.3 + 0.45 * fight_round
        $ _zn = max(14, 48 - 10 * fight_round)
        "He lunges."
        call fight_check("DODGE!", _sp, _zn, reverse=(fight_round % 2 == 0))
        if _return != "fail":
            "I throw myself sideways. His hand punches through the wall where my head just was."
        else:
            $ st_fails += 1
            show redflash at flicker
            with vpunch
            "Too slow. He catches my shoulder and throws me into the monitors."
        $ fight_round += 1

    jump ch3_end


## ---------------------------------------------------------------- ending
## Not a game over. Springtrap sends you to Chapter 4. When you arrive, he's gone.
label ch3_end:
    stop music fadeout 1.0
    scene bg fright_office
    show springtrap broken at sprite_pos(0.5)
    with vpunch
    "I'm on the floor. The crowbar is somewhere under the desk. I can't feel my arm."
    "He leans over me. Close enough to smell the smoke on him."
    if st_hits >= 2:
        spt "Two. You hit me {i}twice{/i}. Nobody has hurt me like that in thirty years."
    elif st_hits == 1:
        spt "One hit. That's one more than anybody else ever landed."
    else:
        spt "All that running. All that planning. And not one hit."
    spt "Did you really think you could fix {i}me{/i}, [guard_name]? Put me back together, like the golden one? Like the Puppet's box?"
    spt "No. I don't think I'll kill you. That's too quick. You'd just wake up somewhere new and start fixing again."
    spt "I'll send you somewhere you {i}can't{/i} fix anything."
    spt "A nightmare. A little child's nightmare. Full of the worst versions of all your friends."
    spt "Survive it, if you can. I'll be waiting at the end."
    "His hand closes over my face. The office folds in on itself like paper."

    $ _good = calm >= 6
    if _good:
        $ persistent.endings.add("ch3_good")
        $ persistent.good_endings.add(3)
        $ _ending_name = "SET FREE"
    else:
        $ persistent.endings.add("ch3_cold")
        $ _ending_name = "STILL HAUNTED"

    scene black
    with slowfade
    play sound "audio/jumpscare.wav"
    pause 1.0
    scene bg bedroom
    with slowfade
    "I wake up in a bed. A small one. A child's bed, in a child's bedroom."
    "There's a plush Fredbear on the dresser, and a flashlight in my hand."
    "No smoke. No green claws. No Springtrap. He's gone, like he was never here."
    "Down the hall, a door creaks open. Something big breathes in the dark."
    if _good:
        "Somewhere far away, very faintly, I think I hear a song. A bear. A chicken. A pirate. Together."
    scene black
    with dissolve
    play sound "audio/chime.wav"
    show text "{size=80}{b}CHAPTER 3 COMPLETE{/b}{/size}\n{size=40}Ending: [_ending_name]{/size}" at truecenter
    with dissolve
    pause 3.0
    hide text
    $ persistent.chapter_unlocked = max(persistent.chapter_unlocked, 4)
    if _good:
        show text "{size=60}{b}CHAPTER 4 UNLOCKED{/b}{/size}\n{size=36}Good ending reward: easier skill checks in Chapter 4{/size}" at truecenter
    else:
        show text "{size=60}{b}CHAPTER 4 UNLOCKED{/b}{/size}\n{size=36}Select it from Chapters on the main menu{/size}" at truecenter
    with dissolve
    pause
    return
