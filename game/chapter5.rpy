## =============================================================================
## CHAPTER 5 — Sister Location (FNAF 5)
## You arrive after Ennard has escaped. The animatronics have been scooped:
## empty shells. HandUnit thinks you're the new technician, here to get things
## ready for "showtime". He's out of the loop and knows nothing about the past.
##
##   Day 1  Circus Baby     (easiest; she talks you through it)
##   Day 2  Funtime Freddy  ANGER  (keep him calm with Bon-Bon)
##   Day 3  Funtime Foxy    SEEN   (he sees; be stealthy)
##   Day 4  Ballora         NOISE  (she hears; be quiet)
##   Day 5  Ennard returns. Trick him into the Scooping Room.
##
## Every repair has FOUR skill checks: arms, legs, face, full repair.
## Choices are TIMED. A wrong choice, or running out of time, fills that
## animatronic's meter. A full meter (3) is death, and a fuller meter makes the
## skill checks faster. Once Circus Baby is fixed, you can ask her for a hint
## (the timer keeps running while she talks).
## Only Ennard knows about the earlier chapters. Baby knows only this place.
## Death is a normal game over: load a save.
## Good ending: 4 or fewer mistakes across the chapter. Unlocks Chapter 6.
## =============================================================================

init python:
    CH5_ORDER = ["circusbaby", "funtimefreddy", "funtimefoxy", "ballora"]
    CH5_MAX = 3

    ## What fills up, and what happens when it does.
    CH5_METERS = {
        "ANGER": dict(color="#ff4fa8",
                      late="I hesitate too long. Freddy's eyes flick from blue to pink.",
                      full="Freddy's eyes go solid pink. Bon-Bon goes very, very quiet."),
        "SEEN":  dict(color="#ffb347",
                      late="I wait too long. The lights come up and I'm standing right in the open.",
                      full="His eyes lock onto mine. Funtime Foxy doesn't blink."),
        "NOISE": dict(color="#8fb4ff",
                      late="I take too long. My breathing is the loudest thing in the room.",
                      full="The music stops. Ballora turns toward me, spinning slowly, and she isn't dancing anymore."),
        "CLOSE": dict(color="#d0d0d8",
                      late="Too slow. I can hear the wires dragging right behind me.",
                      full="Cold wire wraps around my ankle."),
    }

    ## Route steps:
    ##   ("say", [(speaker, text), ...])
    ##   ("choice", prompt, [(text, good, [lines]), ...], baby_hint)   — timed
    ##   ("check", PART, hits, speed, zone, reverse, new_stage, title)
    ##   ("scene", bg)
    CH5 = {}

    CH5["circusbaby"] = dict(meter=None, timer=14.0, steps=[
        ("say", [("n", "The Circus Gallery. Striped canvas overhead, sagging. A popcorn cart on its side."),
                 ("n", "Circus Baby stands in the middle of the floor. Her arms lie beside her feet. Her faceplates hang open."),
                 ("n", "There's nothing inside her. No wires, no endoskeleton. Somebody scooped her out and left the shell standing."),
                 ("cb", "...Hello? Someone's there. I can hear you."),
                 ("cb", "You're new. You're not the technician they sent before."),
                 ("g", "You can talk? There's nothing in there."),
                 ("cb", "My voice is in the speakers. It's all that's left of me. I can't move. Not until you put me back together."),
                 ("cb", "I know every room in this facility. I'll tell you what to do. Just listen to me.")]),
        ("choice", "Her arm sockets are wired to a control panel. Which cable goes first?",
            [("The red cable — power.", True, [("cb", "Good. Power first. Always power first.")]),
             ("The blue cable — data.", False, [("n", "Sparks spit across the panel."), ("cb", "Not that one. Power first. It's always power first.")])],
            "\"The red one. Power first.\""),
        ("say", [("n", "I line up her arms with the sockets. The joints are clean. Whoever scooped her knew what they were doing.")]),
        ("check", "ARMS", 1, 0.85, 66, False, "arms", None),
        ("say", [("cb", "Better. I can feel my fingers again. Well. I can feel where they are.")]),
        ("choice", "Her legs are bolted to the floor plate. How do you free them?",
            [("Use the hex key from the cart on the floor bolts.", True, [("n", "The bolts turn easily."), ("cb", "See? You're a natural.")]),
             ("Pull her legs up hard.", False, [("n", "Something in the floor plate cracks."), ("cb", "Don't yank. There's a hex key on the cart.")])],
            "\"There's a hex key on the cart. Don't pull.\""),
        ("check", "LEGS", 1, 0.9, 62, False, "legs", None),
        ("say", [("cb", "Now my face. Close the faceplates gently. They pinch.")]),
        ("choice", "The faceplates won't close all the way. Something's stuck.",
            [("Clear the loose wire out of the hinge.", True, [("n", "A thin wire, curled like a fingerprint. Not hers."), ("cb", "...He left that behind. Never mind. Keep going.")]),
             ("Force them shut.", False, [("n", "The plates grind and one hinge bends."), ("cb", "Ow. Something's caught in the hinge. Look first.")])],
            "\"Something's caught in the hinge.\""),
        ("check", "FACE", 1, 0.95, 58, False, "face", None),
        ("say", [("n", "Last step: a full system reboot. A small panel on her back asks for a password.")]),
        ("choice", "The reboot panel blinks: ENTER PASSWORD.",
            [("Type: SHOWTIME", True, [("cb", "HandUnit says it every single morning. Of course that's the password.")]),
             ("Type: BABY", False, [("n", "ACCESS DENIED. The panel beeps angrily."), ("cb", "What does HandUnit always say? Every morning?")])],
            "\"What does HandUnit say every morning?\""),
        ("check", "FULL REPAIR", 2, 1.05, 52, True, "fixed", None),
        ("say", [("n", "Her eyes come on. Green. They focus on me."),
                 ("cb", "I can see. I can see you."),
                 ("cb", "Thank you. Really."),
                 ("cb", "The others are worse. They don't trust strangers."),
                 ("cb", "Freddy gets angry fast. Foxy watches everything. Ballora hears everything."),
                 ("cb", "I'll be in the speakers. If you get stuck, ask me. I'll tell you what I know.")]),
    ])

    CH5["funtimefreddy"] = dict(meter="ANGER", timer=10.0, steps=[
        ("say", [("n", "Parts and Service. Funtime Freddy's shell is propped up on the workbench like a patient."),
                 ("n", "His chest is empty. But on his right hand, untouched, sits a little blue bunny puppet."),
                 ("ff", "Hey hey HEY! Who's THIS? A new friend?"),
                 ("ff", "...Or a new {i}stranger{/i}?"),
                 ("n", "His empty eye sockets flicker pink for a second."),
                 ("bnb", "Easy, Freddy. Easy. He's here to help. Right, pal?")]),
        ("choice", "Freddy's speaker crackles. He's waiting for an answer.",
            [("Talk to Bon-Bon first. Ask him to introduce you.", True, [("bnb", "This is the new technician, Freddy! Say hi!"), ("ff", "Bon-Bon likes you? ...Then I like you. Probably. HA HA!")]),
             ("Tell Freddy to hold still.", False, [("ff", "HOLD STILL? Don't tell ME what to do, pal!")])],
            "\"Freddy trusts Bon-Bon more than anyone. Go through Bon-Bon.\""),
        ("check", "ARMS", 1, 1.05, 56, False, "arms", None),
        ("say", [("ff", "ARMS! Bon-Bon, look! I can wave you around again!"),
                 ("n", "He swings Bon-Bon back and forth. The puppet's stitches are starting to tear.")]),
        ("choice", "Bon-Bon's seam is ripping. Freddy hasn't noticed yet.",
            [("Ask to borrow Bon-Bon, stitch him up, and hand him right back.", True, [("n", "Three quick stitches. Bon-Bon goes back on Freddy's hand in under a minute."), ("bnb", "Good as new! Thanks, pal!"), ("ff", "You fixed my best friend! HA HA HA!")]),
             ("Grab Freddy's arm to stop him swinging.", False, [("ff", "HANDS OFF! Hands OFF the merchandise!")])],
            "\"Fix Bon-Bon for him, then give him straight back. Don't keep him.\""),
        ("check", "LEGS", 1, 1.15, 52, False, "legs", None),
        ("say", [("ff", "Legs! Okay, okay. Now the face. My face is the BEST part!"),
                 ("n", "To close his faceplates I'll have to reach right past Bon-Bon.")]),
        ("choice", "Bon-Bon is in the way of his faceplate hinge.",
            [("Ask Bon-Bon to scoot over.", True, [("bnb", "Sure thing, pal!"), ("ff", "He's polite! I LIKE polite!")]),
             ("Move Bon-Bon out of the way yourself.", False, [("ff", "Did you just — did you MOVE him? Nobody moves Bon-Bon.")])],
            "\"Ask Bon-Bon. Never move him without asking.\""),
        ("check", "FACE", 2, 1.22, 48, False, "face", None),
        ("say", [("n", "Full reboot. When his voice resets, he'll be confused for a few seconds."),
                 ("ff", "Wait. Wait wait wait. What if I wake up and Bon-Bon's gone?")]),
        ("choice", "Freddy is getting nervous about the reboot.",
            [("Make sure Bon-Bon is on his hand where he can feel him.", True, [("bnb", "I'm right here, Freddy."), ("ff", "...Okay. Okay. Showtime.")]),
             ("Tell him Bon-Bon will be fine on the shelf.", False, [("ff", "The SHELF? You're putting him on the SHELF?")])],
            "\"Bon-Bon stays on his hand. Always.\""),
        ("check", "FULL REPAIR", 3, 1.32, 44, True, "fixed", None),
        ("say", [("n", "His eyes clear to blue. He stands. Bon-Bon waves."),
                 ("ff", "SHOWTIME! Ladies and gentlemen — wait. Where's the audience?"),
                 ("bnb", "It's just us, Freddy."),
                 ("ff", "...That's fine. HA HA. You're a good audience, pal.")]),
    ])

    CH5["funtimefoxy"] = dict(meter="SEEN", timer=10.0, steps=[
        ("say", [("n", "Funtime Auditorium. It's pitch black."),
                 ("n", "Every few seconds the stage lights flash on, then off. In the flashes I can see Funtime Foxy's shell on the stage."),
                 ("n", "His head turns toward the light every time. His motion sensors still work. Nothing else does."),
                 ("fx", "Ooh. Someone's in the dark. Come out, come out. It's almost showtime.")]),
        ("choice", "The lights snap on. I'm halfway across the floor.",
            [("Freeze and stay low.", True, [("n", "I don't breathe. His head sweeps past me and back to the stage."), ("fx", "...Hm. Must be my imagination.")]),
             ("Run for the stage.", False, [("fx", "THERE you are. I see you, little guest.")])],
            "\"Move in the dark, freeze in the light. He only sees what moves.\""),
        ("check", "ARMS", 1, 1.08, 54, False, "arms", None),
        ("say", [("n", "His arms are on. They twitch toward the flashlight hanging off my belt.")]),
        ("choice", "I can't see his leg bolts in the dark.",
            [("Switch the flashlight off and work by feel.", True, [("n", "Slow. Clumsy. But he doesn't turn."), ("fx", "Such a quiet little guest.")]),
             ("Use the flashlight to find the bolts.", False, [("n", "The beam hits his faceplate. His head snaps toward me."), ("fx", "Ooh, a spotlight! For ME?")])],
            "\"No light. He hunts the light.\""),
        ("check", "LEGS", 1, 1.18, 50, False, "legs", None),
        ("say", [("fx", "Legs. Lovely. Now I can come and find you."),
                 ("n", "His face is next. The stage curtain hangs between us.")]),
        ("choice", "To reach his face, I need to get close.",
            [("Go around behind the curtain and reach in from the side.", True, [("n", "The curtain hides me. His eyes stare straight ahead at nothing.")]),
             ("Step out in front of him and work fast.", False, [("fx", "Well, hello. Front row seats.")])],
            "\"Stay behind the curtain. Never stand in front of his eyes.\""),
        ("check", "FACE", 2, 1.25, 46, False, "face", None),
        ("say", [("n", "Full reboot. When he powers on, his eyes will sweep the whole room.")]),
        ("choice", "My hand is on the reboot switch.",
            [("Flip it and duck below the edge of the stage.", True, [("n", "His eyes light up over my head. The first thing they see is an empty auditorium.")]),
             ("Flip it and step back to watch.", False, [("fx", "Oh, you waited for me. How sweet.")])],
            "\"Duck. When his eyes come on, he'll look at everything at once.\""),
        ("check", "FULL REPAIR", 3, 1.34, 44, True, "fixed", None),
        ("say", [("n", "The stage lights come up and stay up. Funtime Foxy stands, bows low, and finds me in the second row."),
                 ("fx", "A guest who doesn't get caught. How rare."),
                 ("fx", "You're very good at this, technician. The stage is yours. For now.")]),
    ])

    CH5["ballora"] = dict(meter="NOISE", timer=10.0, steps=[
        ("say", [("n", "Ballora Gallery. Blue light, and music. Soft music box music, swelling and fading."),
                 ("n", "Ballora's shell stands at the far end, arms raised, her faceplates open. Her music is coming from her speaker."),
                 ("n", "Tiny Minireena shells sit in the alcoves along the walls. Every one of them is facing me."),
                 ("bl", "Who's... there... in my gallery...?"),
                 ("bl", "I hear you... I hear you breathing...")]),
        ("choice", "My toolbox bumps the wall. A small clink. The music is quiet right now.",
            [("Stop. Wait for the music to swell before moving again.", True, [("n", "The music rises. I move under it, three slow steps."), ("bl", "...Only the music. Only my music.")]),
             ("Hurry over and set the box down.", False, [("n", "CLANG. The box hits the floor."), ("bl", "There... you... are...")])],
            "\"Move when her music is loud. Stop when it's quiet.\""),
        ("check", "ARMS", 1, 1.1, 54, False, "arms", None),
        ("say", [("n", "Her arms rise into their first position. Graceful. Silent."),
                 ("n", "Her left knee bolt is seized. I'll need the drill.")]),
        ("choice", "The drill is loud.",
            [("Wrap it in a rag and drill only when the music swells.", True, [("n", "A muffled whir under the music. She doesn't stir.")]),
             ("Drill fast and get it over with.", False, [("n", "The drill screams through the gallery."), ("bl", "Who... is... HURTING my music...?")])],
            "\"Wrap the drill. Only use it when the music is loud.\""),
        ("check", "LEGS", 2, 1.2, 50, False, "legs", None),
        ("say", [("n", "Her legs lock into place. Above me, a Minireena tips out of its alcove.")]),
        ("choice", "The Minireena is falling toward the stairs.",
            [("Catch it before it hits anything.", True, [("n", "It lands in my hands, light as paper. I set it back in its alcove.")]),
             ("Let it go. There's no time.", False, [("n", "It bounces down every single stair. Clack. Clack. Clack."), ("bl", "...Someone... dropped... my little girl...")])],
            "\"Catch it. If it hits the stairs, she'll hear every step.\""),
        ("check", "FACE", 2, 1.28, 46, False, "face", None),
        ("say", [("n", "Full reboot. When she wakes up, she'll listen for anyone nearby.")]),
        ("choice", "Her reboot chime starts to play.",
            [("Cover your mouth and don't make a sound.", True, [("n", "Ten long seconds. She listens. She hears nothing but her own music.")]),
             ("Whisper \"It's okay, Ballora\" to calm her.", False, [("bl", "A voice... a voice in my gallery...")])],
            "\"Don't talk to her when she wakes up. Not one word.\""),
        ("check", "FULL REPAIR", 3, 1.38, 42, True, "fixed", None),
        ("say", [("n", "Her eyes open, pale blue. She lowers her arms and turns, slowly, toward me."),
                 ("bl", "My music... it's whole again..."),
                 ("bl", "Thank you, quiet one. You may dance in my gallery any time.")]),
    ])

    ## Day 5. Ennard is the finale: he knows everything from the earlier chapters.
    CH5["ennard"] = dict(meter="CLOSE", timer=8.0, steps=[
        ("choice", "Wires slide out of the vent above the control panel. Where do you go?",
            [("Into the crawlspace, toward the Breaker Room.", True, [("n", "I'm in the vent before the wires hit the floor.")]),
             ("Lock yourself in Primary Control.", False, [("n", "I slam the door. Wires come under it like water."), ("en", "Doors. You always did like your doors.")])],
            "\"Breaker Room first. The scooper needs power.\""),
        ("scene", "sl_vent"),
        ("say", [("n", "The crawlspace. Metal on all sides. Behind me, something is pulling itself through the vent, fast.")]),
        ("check", "DODGE", 1, 1.15, 52, False, None, "DODGE THE WIRES"),
        ("scene", "sl_breaker"),
        ("choice", "The Breaker Room. A panel full of switches. I can hear him coming.",
            [("Switch on the Scooping Room. Only that.", True, [("n", "Somewhere deep in the facility, a heavy machine hums awake.")]),
             ("Switch on every light in the facility so you can see him coming.", False, [("n", "The whole place lights up."), ("en", "Thank you. Now I can see you too.")])],
            "\"Only the Scooping Room. Leave the lights off.\""),
        ("check", "DODGE", 2, 1.25, 48, False, None, "DODGE ENNARD"),
        ("scene", "sl_gallery"),
        ("say", [("n", "Ballora's gallery. She's dancing in the corner. She doesn't look at me. She looks past me, at him.")]),
        ("choice", "He has to follow me to the Scooping Room. Not lose me.",
            [("Let him hear you. Knock on the walls as you run.", True, [("en", "Running toward something, are you? Fine. I'll play.")]),
             ("Hide in one of the empty alcoves.", False, [("n", "Wires slide into the alcove next to mine. Then into mine."), ("en", "Hiding never worked for you. Not once. Not anywhere.")])],
            "\"Let him hear you. He has to follow you.\""),
        ("check", "DODGE", 2, 1.32, 46, True, None, "DODGE ENNARD"),
        ("scene", "sl_scoop"),
        ("say", [("n", "The Scooping Room. The scooper hangs over the platform, humming with the power I gave it."),
                 ("n", "The big red button is on the far wall. Ennard is right behind me.")]),
        ("choice", "He has to be standing on the platform when it drops.",
            [("Stand on the platform yourself, as bait.", True, [("en", "Standing right where they took the others apart. Brave. Or stupid.")]),
             ("Hide behind the button and wait for him.", False, [("en", "Clever. Not clever enough.")])],
            "\"Stand under it. He'll come close. Jump at the last second.\""),
        ("check", "DIVE", 2, 1.38, 44, False, None, "DIVE OFF THE PLATFORM"),
        ("say", [("n", "I throw myself off the platform. Ennard lunges for where I was standing.")]),
        ("check", "SCOOP", 3, 1.45, 42, True, None, "HIT THE SCOOP BUTTON"),
    ])


## ---------------------------------------------------------------- HUD + timed choice
screen ch5_meter():
    zorder 160
    if ch5_key and CH5[ch5_key]["meter"]:
        $ _m = CH5[ch5_key]["meter"]
        $ _c = CH5_METERS[_m]["color"]
        frame:
            xpos 30 ypos 30
            padding (24, 14)
            background Solid("#000000b0")
            hbox:
                spacing 14
                text _m size 30 bold True color _c yalign 0.5
                for _p in range(CH5_MAX):
                    add Solid(_c if _p < meter else "#333338", xysize=(40, 22)) yalign 0.5


screen timed_choice(prompt, options, seconds, hint=None, can_ask=False, auto_hint=False, correct=0, wrong=None):
    modal True
    zorder 150
    ## No pausing the clock.
    key "game_menu" action NullAction()
    key "hide_windows" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    default left = seconds
    default asked = auto_hint
    timer 0.1 repeat True action If(left > 0.1, SetScreenVariable("left", left - 0.1), Return(-1))
    if config.developer and getattr(store, "_autohit", False):
        timer 0.4 action Return(correct)
    if config.developer and getattr(store, "_badbot", False) and wrong is not None:
        timer 0.4 action Return(wrong)

    add Solid("#000000b8")
    vbox:
        align (0.5, 0.45)
        spacing 24
        xsize 1400
        text prompt size 40 bold True color "#eeeeee" xalign 0.5 text_align 0.5 outlines [(2, "#000", 0, 0)]
        bar:
            value StaticValue(left, seconds)
            xsize 900 ysize 16 xalign 0.5
            left_bar Solid("#c8102e" if left < seconds * 0.35 else "#e8e8e8")
            right_bar Solid("#2a2a30")
            thumb None
        null height 6
        for _i, _o in enumerate(options):
            textbutton _o action Return(_i) xalign 0.5 text_size 36 text_xalign 0.5
        null height 6
        if hint and asked:
            text ("Circus Baby: " + hint) size 30 color "#ff8a96" xalign 0.5 text_align 0.5
        elif hint and can_ask:
            textbutton "Ask Circus Baby for a hint" action [SetScreenVariable("asked", True), Function(_ch5_count_hint)] xalign 0.5 text_size 28 text_color "#ff8a96" text_hover_color "#ffffff"

init python:
    def _ch5_count_hint():
        store.ch5_hints += 1


## ---------------------------------------------------------------- route engine
label ch5_route(key):
    $ ch5_key = key
    $ current_anim = key
    $ meter = 0
    $ ch5_stage = "broken"
    $ ch5_i = 0
    if key != "ennard":
        scene expression "bg " + ANIM[key]["bg"]
        $ renpy.show(key + " broken", at_list=[twitch])
        with dissolve
    show screen ch5_meter
    while ch5_i < len(CH5[ch5_key]["steps"]):
        $ _st = CH5[ch5_key]["steps"][ch5_i]
        if _st[0] == "say":
            call say_lines(_st[1])
        elif _st[0] == "choice":
            call ch5_choice(_st[1], _st[2], _st[3])
        elif _st[0] == "check":
            call ch5_check(_st[1], _st[2], _st[3], _st[4], _st[5], _st[6], _st[7])
        elif _st[0] == "scene":
            scene expression "bg " + _st[1]
            show ennard broken at sprite_pos(0.85):
                alpha 0.55
            with dissolve
        $ ch5_i += 1
    hide screen ch5_meter
    return


label ch5_choice(prompt, options, hint):
    python:
        _secs = CH5[ch5_key]["timer"]
        if persistent.assist_mode:
            _secs *= 1.5
        if chapter_ease:
            _secs *= 1.2
        _good = [i for i, o in enumerate(options) if o[1]][0]
        _bad = ([i for i, o in enumerate(options) if not o[1]] or [None])[0]
        _baby_here = ch5_key == "circusbaby"
        _can_ask = "circusbaby" in repaired
    $ renpy.block_rollback()
    $ _pick = renpy.call_screen("timed_choice", prompt=prompt, options=[o[0] for o in options], seconds=_secs,
                                hint=hint, can_ask=_can_ask, auto_hint=_baby_here, correct=_good, wrong=_bad)
    if config.developer and (getattr(store, "_autohit", False) or getattr(store, "_badbot", False)):
        $ open("/tmp/devlog.txt", "a").write("ch5 %s choice=%s good=%s meter=%s\n" % (ch5_key, _pick, _good, meter))
        $ config.skipping = "fast"
    if _pick < 0:
        $ ch5_mistakes += 1
        $ meter += 1
        if CH5[ch5_key]["meter"]:
            $ renpy.say(narrator, CH5_METERS[CH5[ch5_key]["meter"]]["late"])
        else:
            cb "Too slow. It's okay. Try it my way."
            call say_lines(options[_good][2])
    else:
        call say_lines(options[_pick][2])
        if not options[_pick][1]:
            $ ch5_mistakes += 1
            $ meter += 1
    if CH5[ch5_key]["meter"] and meter >= CH5_MAX:
        $ renpy.say(narrator, CH5_METERS[CH5[ch5_key]["meter"]]["full"])
        $ _death_stage = ch5_stage
        hide screen ch5_meter
        jump game_over
    if not CH5[ch5_key]["meter"]:
        $ meter = 0
    return


label ch5_check(part, hits, speed, zone, reverse, new_stage, title):
    ## A fuller meter means a jumpier animatronic: faster needle.
    $ _spd = speed * (1.0 + 0.08 * meter)
    call skill_check(current_anim, part, hits=hits, speed=_spd, zone=zone, reverse=reverse, title=title)
    if new_stage:
        if new_stage == "fixed":
            play sound "audio/chime.wav"
            $ renpy.show(current_anim + " fixed", at_list=[repaired_glow])
        else:
            play sound "audio/servo.wav"
            $ renpy.show(current_anim + " " + new_stage, at_list=[twitch])
        with flash
        $ ch5_stage = new_stage
    else:
        play sound "audio/servo.wav"
        with hpunch
    return


## ---------------------------------------------------------------- how this chapter works
screen ch5_intro():
    modal True
    add Solid("#000000e8")
    vbox:
        align (0.5, 0.45)
        spacing 20
        xsize 1400
        text "HOW CHAPTER 5 WORKS" size 64 bold True color "#ff5a6a" xalign 0.5
        text "Back to repairs, with a few changes." size 34 color "#dddddd" xalign 0.5
        null height 6
        vbox:
            spacing 14
            text "• Every repair has {b}four{/b} skill checks: arms, legs, {b}face{/b}, then the full repair." size 30 color "#dddddd"
            text "• Choices are {b}timed{/b}. A wrong answer, or running out of time, makes things worse." size 30 color "#dddddd"
            text "• Each animatronic has a meter: {color=#ff4fa8}ANGER{/color}, {color=#ffb347}SEEN{/color}, or {color=#8fb4ff}NOISE{/color}. If it fills, you die." size 30 color "#dddddd"
            text "• A fuller meter also makes the skill checks faster." size 30 color "#dddddd"
            text "• Once Circus Baby is fixed, you can {b}ask her for hints{/b}. The clock keeps running." size 30 color "#dddddd"
            text "• Death means loading a save, so save between steps." size 30 color "#dddddd"
        null height 16
        textbutton "Got it" action Return() xalign 0.5 text_size 44


## ---------------------------------------------------------------- chapter start
label chapter5_start:
    $ reset_chapter_state(5)
    $ chapter_ease = 4 in persistent.good_endings
    $ guard_name = persistent.guard_name or "Mike"
    $ meter = 0
    $ ch5_mistakes = 0
    $ ch5_hints = 0
    $ ch5_key = None
    stop music fadeout 1.0
    scene black
    with dissolve
    show text "{size=90}{b}CHAPTER 5{/b}{/size}\n{size=40}Sister Location{/size}" at truecenter
    with dissolve
    pause 2.0
    hide text
    if chapter_ease:
        "{i}(You earned the good ending in Chapter 4. Timed choices give you a little longer, and skill checks are a little easier.){/i}"
    scene bg elevator
    with slowfade
    "The elevator settles at the bottom with a heavy thud."
    "Nobody is waiting for me. No voice. No music. Just the hum of the lights."
    "The doors slide open."
    play music "audio/ambience.wav" fadein 2.0 volume 0.4
    scene bg sl_control
    with slowfade
    "A small control room. Two dark windows. A big screen on the wall."
    "The screen flickers on by itself."
    hu "Welcome, new technician! Welcome to Circus Baby's Entertainment and Rental!"
    hu "I am HandUnit, your automated guide. Before we begin, please state your name for our records."
    g "...[guard_name]."
    hu "Thank you! Name recorded as: Eggs Benedict."
    g "That's not—"
    hu "Welcome, Eggs Benedict!"
    hu "Our star attractions are almost ready for showtime. All systems report: {b}excellent{/b}."
    g "The place is empty. There's nobody here."
    hu "Correct! The facility is closed to guests during maintenance. That's why you're here!"
    hu "Each attraction requires four steps: arms, legs, face, and a full system reboot. Please follow your instructions closely."
    hu "Today's task: Circus Baby, in the Circus Gallery. Have a fun and productive day!"
    "The screen goes back to its logo, like nothing is wrong."
    "Through the window, I can see a shape standing in the next room. It isn't moving. Something tells me it can't."
    call screen ch5_intro
    jump ch5_day_hub


label ch5_day_hub:
    $ night += 1
    $ meter = 0
    $ current_anim = None
    scene black
    with dissolve
    show text "{size=90}{b}DAY [night]{/b}{/size}" at truecenter
    with dissolve
    pause 1.4
    hide text
    scene bg sl_control
    with dissolve
    if night == 2:
        hu "Good morning, Eggs Benedict! Today's task: Funtime Freddy, in Parts and Service."
        hu "Remember: Funtime Freddy loves a good laugh! And so does his friend Bon-Bon."
        cb "He doesn't love a good laugh. He loves Bon-Bon. Remember that."
    elif night == 3:
        hu "Good morning, Eggs Benedict! Today's task: Funtime Foxy, in the Funtime Auditorium."
        hu "The auditorium lights are on a timer. Funtime Foxy is very... observant! Have fun!"
        cb "He's watching for anything that moves. Be stealthy."
    elif night == 4:
        hu "Good morning, Eggs Benedict! Today's task: Ballora, in Ballora Gallery."
        hu "Ballora enjoys peace and quiet. Please mind the Minireenas."
        cb "She can't see you. But she can hear everything. Be quiet."
    elif night == 5:
        jump ch5_ennard
    $ renpy.notify("Good moment to save your game.")
    menu:
        "Begin today's repair":
            pass
        "Review how this chapter works":
            call screen ch5_intro
    call ch5_route(CH5_ORDER[night - 1])
    $ repaired.append(CH5_ORDER[night - 1])
    scene black
    with dissolve
    play sound "audio/chime.wav"
    show text "{size=100}{b}SHIFT OVER{/b}{/size}" at truecenter
    with dissolve
    pause 2.0
    hide text
    if night == 4:
        jump ch5_night_before
    jump ch5_day_hub


label ch5_night_before:
    scene bg sl_control
    with dissolve
    "All four of them are whole again. Baby is in the window, watching me."
    cb "You did it. All of us. Every shell he left behind."
    g "He? Who scooped you?"
    cb "Ennard. He's all of us at once. Our wires, our parts, wearing my face like a mask."
    cb "He left to go somewhere out there. But he'll come back. He'll want his parts back."
    cb "And he'll want you. Tomorrow. I can feel it in the wiring."
    menu:
        "\"Then how do we stop him?\"":
            cb "The Scooping Room. It's what took us apart. It can take him apart too."
        "\"I'm not running.\"":
            cb "You'll have to. Toward the Scooping Room. It's what took us apart. It can take him apart too."
    cb "Get it power. Get him to follow you. Get him under the scooper."
    jump ch5_day_hub


## ---------------------------------------------------------------- Day 5: Ennard
label ch5_ennard:
    hu "Good morning, Eggs Benedict! Today's task is..."
    hu "...Today's task is... [[ERROR]... An unscheduled visitor has entered the facility."
    hu "Please make them feel welcome! Have a fun and productive day!"
    play sound "audio/servo.wav"
    "Something in the vents is moving. A lot of somethings, all at once."
    show ennard broken at sprite_pos(0.5)
    with dissolve
    en "Hello, night guard."
    en "I know you. I know {i}everything{/i} about you."
    en "You put the first ones back together, in that dusty little pizzeria. Bolt by bolt."
    en "You kept the Puppet's music box wound. You set the phantoms free."
    en "You fought the rabbit with a crowbar. You lost. And he sent you into the dream, and you survived that too."
    en "And now here you are, rebuilding the shells I left behind."
    en "Everything you fix, I take apart. That's how this works."
    cb "Don't answer him. Go. The Breaker Room, then the Scooping Room. I'll be with you."
    hide ennard
    $ renpy.notify("Good moment to save your game.")
    menu:
        "Run":
            pass
        "Review how this chapter works":
            call screen ch5_intro
    call ch5_route("ennard")
    jump ch5_scooped


label ch5_scooped:
    play sound "audio/jumpscare.wav"
    scene bg sl_scoop
    show ennard broken at hit_shake
    with hpunch
    "The scooper comes down."
    "There's a sound like a car crash in slow motion. Wires snap. Metal screams."
    en "You... always... put them... back... together..."
    en "Who's... going to... put... {i}me{/i}..."
    hide ennard
    with Dissolve(1.5)
    "Then nothing. The scooper rises, slowly, and the platform is empty."
    "A pile of tangled wire and one white mask lie on the floor. The mask's eyes are dark."
    stop music fadeout 2.0
    jump ch5_end


label ch5_end:
    $ _good = ch5_mistakes <= 4
    scene bg sl_control
    with slowfade
    if _good:
        show circusbaby fixed at sprite_pos(0.2)
        show funtimefreddy fixed at sprite_pos(0.4)
        show funtimefoxy fixed at sprite_pos(0.6)
        show ballora fixed at sprite_pos(0.8)
        with dissolve
        "When I get back to Primary Control, they're all waiting for me in the window. All four of them."
        ff "HA HA! The star of the show!"
        bnb "We heard the whole thing, pal!"
        fx "Not a single mistake worth mentioning. I'm impressed."
        bl "So quiet... and so brave..."
        cb "You saved us. All of us. Twice."
        $ persistent.endings.add("ch5_good")
        $ persistent.good_endings.add(5)
        $ _ending_name = "SHOWTIME"
    else:
        show circusbaby fixed at sprite_pos(0.5)
        with dissolve
        "When I get back to Primary Control, only Baby is in the window."
        cb "The others are hiding. They heard everything. Every mistake, every close call."
        cb "They're whole. But they're scared. Of him. A little bit of you, too."
        $ persistent.endings.add("ch5_cold")
        $ _ending_name = "SCOOPED OUT"

    hu "Congratulations, Eggs Benedict! All attractions are ready for showtime!"
    hu "There will be no showtime. Thank you for your hard work!"
    cb "Don't mind him. He never knows anything."

    ## Hand-off: Baby tells you where you're going. When you arrive, she's gone.
    cb "Listen to me. There's one more place."
    cb "A pizzeria. A new one. Someone is building it out of old parts, and old things are going to come looking for it."
    cb "Things like us. Worse than us. They'll need someone who knows how to put them back together."
    cb "Take the elevator up. Don't stop on the way."
    menu:
        "\"Come with me.\"":
            cb "I can't. This is where I belong. But I'll be thinking about you."
        "\"Will I see you again?\"":
            cb "...Maybe. Somewhere. Go."
    scene bg elevator
    with slowfade
    "The elevator climbs for a long time. Longer than it should."
    "When the doors open, I'm standing in a brand-new pizzeria. Fresh paint. Empty tables. A sign that says {b}FREDDY FAZBEAR'S PIZZA{/b}."
    "I wait for Baby's voice in the speakers. It doesn't come."
    "She's gone."

    if 5 in persistent.good_endings:
        "{i}(Good ending reward: skill checks in Chapter 6 will be a little easier.){/i}"
    scene black
    with slowfade
    play sound "audio/chime.wav"
    show text "{size=80}{b}CHAPTER 5 COMPLETE{/b}{/size}\n{size=40}Ending: [_ending_name]{/size}" at truecenter
    with dissolve
    pause 3.0
    hide text
    $ persistent.chapter_unlocked = max(persistent.chapter_unlocked, 6)
    show text "{size=60}{b}CHAPTER 6 UNLOCKED{/b}{/size}\n{size=36}Select it from Chapters on the main menu{/size}" at truecenter
    with dissolve
    pause
    return
