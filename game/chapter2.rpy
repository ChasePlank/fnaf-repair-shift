## =============================================================================
## CHAPTER 2 — The New Location (FNAF 2)
## Night 1: choose Toys or Withereds first. The whole first group must be
## repaired (any order) before the second group unlocks. Night 9: the Puppet.
## Only the Puppet remembers Chapter 1. The Withereds do NOT remember the player.
## =============================================================================

init python:
    CH2_TOYS = ["toyfreddy", "toybonnie", "toychica", "mangle"]
    CH2_WITHERED = ["witheredfreddy", "witheredbonnie", "witheredchica", "witheredfoxy"]

## ---------------------------------------------------------------- route data
## Each line is (speaker, text). Speaker "n" = narrator, otherwise a Character
## variable name. Choices are (text, trust_gain, [lines]). Final choices are
## (text, zone_bonus, trust_gain, [lines]). Checks are dicts of skill_check args.
## Copy one of these blocks to add a fan-made animatronic.

init python:
    ROUTES = {}

    ROUTES["toyfreddy"] = dict(
        intro=[("n", "Toy Freddy stands alone at center stage, smile frozen wide. Both arms have been yanked off at the shoulder."),
               ("n", "Kids' handprints are smeared all over his plastic face."),
               ("tf", "Hiya, pal! Welcome to Freddy Fazbear's Pizza! I'm Freddy! Are you having fun? Are you having fun? Are you—"),
               ("g", "Okay. Your voice loop's stuck.")],
        c1=[("Tap his speaker grille until the loop breaks.", 1, [("tf", "—having fu— oh! Oh, thank you. That was getting so loud in here."), ("tf", "Wait. Who are you? You're not a kid.")]),
            ("Ignore it and grab his arms.", 0, [("tf", "Are you having fun? Are you having fun?")])],
        arms_pre=[("n", "His arms are in a lost-and-found bin, covered in stickers. The joints are cheap plastic. Easy to crack.")],
        arms=dict(hits=1, speed=1.0, zone=60),
        arms_post=[("tf", "Hands! Now I can wave at everybody again!"), ("tf", "...There's nobody here to wave at, is there.")],
        c2=[("\"You can wave at me.\"", 1, [("n", "He waves. It's slow and stiff and completely sincere."), ("tf", "Hi, pal.")]),
            ("\"The place is closing, buddy.\"", 0, [("tf", "Closing? But we're brand new!")])],
        legs_pre=[("n", "His legs are fine. The problem is the stage bolts. Someone welded them crooked.")],
        legs=dict(hits=1, speed=1.15, zone=50),
        legs_post=[("tf", "I can stand up straight! Mostly."), ("tf", "Hey, pal, my mic is gone. And my hat's cracked. Which one first?")],
        final_q=[("n", "The FULL REPAIR page says Toy Freddy's face recognition runs through either his {b}microphone{/b} or his {b}hat sensor{/b}.")],
        final=[("Fix the microphone.", 14, 1, [("tf", "Testing, testing! Oh, that's me!")]),
               ("Fix the hat sensor.", 0, 0, [("tf", "Oh. Okay! A hat's nice too.")])],
        full_pre=[("n", "Last step: rebuild his face recognition and reset his voice loop for good.")],
        full=dict(hits=3, speed=1.3, zone=46, reverse=True),
        outro=[("n", "Toy Freddy's eyes clear to a bright, happy blue."), ("tf", "Thanks, pal! You're the best customer we've ever had. I mean it!")],
    )

    ROUTES["toybonnie"] = dict(
        intro=[("n", "Toy Bonnie is sprawled across the edge of the stage, guitar strap tangled around his neck."),
               ("n", "His face is pristine. Everything below the neck looks like it went through a woodchipper."),
               ("tb", "Oh, hey! Don't mind me. I'm just, uh... resting. Very stylishly.")],
        c1=[("\"You look great. Seriously.\"", 1, [("tb", "I KNOW, right? At least the face survived.")]),
            ("\"You look awful.\"", 0, [("tb", "Wow. Okay. Rude, but fair.")])],
        arms_pre=[("n", "His arms are under the stage, still holding the guitar between them like he never let go.")],
        arms=dict(hits=1, speed=1.05, zone=58),
        arms_post=[("tb", "Hands! I can play! Oh wow, I'm so out of tune.")],
        c2=[("Tune the guitar for him.", 1, [("n", "It takes a minute. He watches every turn of the pegs like it's a magic trick."), ("tb", "You're a natural!")]),
            ("\"Tune it yourself later.\"", 0, [("tb", "...Sure. Later.")])],
        legs_pre=[("n", "His legs were taken off and stacked in the vent. Somebody was using them to prop it open.")],
        legs=dict(hits=1, speed=1.2, zone=50),
        legs_post=[("tb", "Legs! Okay, okay. One more thing. My blush. Without it I look like a mannequin.")],
        final_q=[("n", "The FULL REPAIR page says the blush lights run on either the {b}original cheek circuit{/b} or a cheaper {b}replacement panel{/b}.")],
        final=[("Use the original cheek circuit.", 14, 1, [("tb", "Yes! The good stuff!")]),
               ("Use the replacement panel.", 0, 0, [("tb", "I mean, sure. Whatever works.")])],
        full_pre=[("n", "Last step: wire the face, reseat the eyes, calibrate the jaw.")],
        full=dict(hits=3, speed=1.32, zone=44, reverse=True),
        outro=[("n", "Toy Bonnie's cheeks glow a soft pink. His green eyes sparkle."), ("tb", "I look AMAZING. Thank you. Seriously, thank you.")],
    )

    ROUTES["toychica"] = dict(
        intro=[("n", "Toy Chica sits at the end of the long party table in Party Room 3, beak missing, eyes dark."),
               ("n", "A paper plate in front of her has a single, very old slice of pizza on it."),
               ("tc", "Party time! Party time! Is it party time?")],
        c1=[("\"It's party time.\"", 1, [("tc", "YAY! I knew it!")]),
            ("\"No. The party's over.\"", 0, [("tc", "Oh. Then why are you here?")])],
        arms_pre=[("n", "Her arms are in the ball pit. Of course they are.")],
        arms=dict(hits=1, speed=1.05, zone=58),
        arms_post=[("tc", "Arms! Now I can hold my cupcake! Where's my cupcake?")],
        c2=[("Find her cupcake under the table.", 1, [("n", "It's scuffed but intact. Its candle eye blinks at me."), ("tc", "THERE you are!")]),
            ("\"Forget the cupcake.\"", 0, [("tc", "I will NOT forget the cupcake.")])],
        legs_pre=[("n", "One leg is bent backward at the knee. I'll have to straighten it and reseat the hip joint.")],
        legs=dict(hits=1, speed=1.2, zone=50),
        legs_post=[("tc", "I can walk! Now my beak. Please. I can't even say \"pizza\" right without it.")],
        final_q=[("n", "There are two beaks on the shelf: her {b}original beak{/b}, scuffed, and a {b}shiny new one{/b} still in its packaging.")],
        final=[("Use her original beak.", 14, 1, [("tc", "That's MY beak!")]),
               ("Use the shiny new one.", 0, 0, [("tc", "It's... nice. It's very shiny.")])],
        full_pre=[("n", "Last step: seat the beak, rebuild the jaw, reset her eyes.")],
        full=dict(hits=3, speed=1.32, zone=44, reverse=True),
        outro=[("n", "Toy Chica's eyes light up bright blue. She clacks her beak twice, testing it."), ("tc", "PIZZA! See? I can say it! Thank you, thank you, thank you!")],
    )

    ## Mangle is harder: more broken, so more hits, faster needle, smaller zones.
    ROUTES["mangle"] = dict(
        intro=[("n", "Kid's Cove is ankle-deep in plastic toys. On the ceiling, something white and pink is tangled in the rafters."),
               ("n", "It drops. It lands in a heap of limbs, wires and two heads. It is still moving."),
               ("mg", "kkkhhhh... welcome... to... kkhh... the... sh-sh-show..."),
               ("g", "...Oh, you're in rough shape.")],
        c1=[("Kneel down slowly so you're not towering over her.", 1, [("mg", "...kkh... soft... voice... ...thank... you...")]),
            ("Start pulling the tangle apart.", 0, [("mg", "KKKHHHHHHH—")])],
        arms_pre=[("n", "Kids took her apart and put her back together wrong, over and over. Her arms are knotted into her own frame."),
                  ("n", "I'll have to untangle both arms and reseat them. Twice the work.")],
        arms=dict(hits=2, speed=1.15, zone=52),
        arms_post=[("mg", "...arms... my arms... they're... MINE again...")],
        c2=[("\"Who did this to you?\"", 1, [("mg", "...the children... every day... they took me apart... I let them... I thought they'd stop..."), ("mg", "...they never stopped...")]),
            ("\"Keep still.\"", 0, [("mg", "...kkh...")])],
        legs_pre=[("n", "Her legs are wired to the ceiling rig. I'll have to cut her free and rebuild both hip joints from scratch.")],
        legs=dict(hits=2, speed=1.28, zone=46),
        legs_post=[("mg", "...standing... I'm... standing..."), ("n", "The second head, the endoskeleton one, turns to look at me."), ("mg", "...one more... but which head...?")],
        final_q=[("n", "Mangle has two heads. The FULL REPAIR page says I can rebuild her around {b}the white fox head{/b}, her original, or {b}remove both and start fresh{/b}.")],
        final=[("Keep her original fox head.", 12, 1, [("mg", "...me... keep... me...")]),
               ("Remove both and start fresh.", 0, 0, [("mg", "...kkkhhhh... no... no...")])],
        full_pre=[("n", "Last step: separate the second head, rebuild her frame, reset her voice. Four hits in a row, no mistakes.")],
        full=dict(hits=4, speed=1.4, zone=40, reverse=True),
        outro=[("n", "The second head comes free. Her voice clears up for the first time."), ("mg", "Hi. I'm Mangle. That's... not actually my name. But I like it now."), ("mg", "Thank you for putting me together right.")],
    )

    ROUTES["witheredfreddy"] = dict(
        intro=[("n", "Parts and Service. The old animatronics from the first location are dumped here like scrap."),
               ("n", "Withered Freddy sits slumped against the wall, fur rotted through, endoskeleton showing at every joint."),
               ("wf", "...Hhhh... who... are you?"),
               ("g", "I'm the night guard. Have we... met?"),
               ("wf", "No. I don't think so. I don't remember... much of anything.")],
        c1=[("\"That's okay. I'll help you anyway.\"", 1, [("wf", "...Kind. Thank you.")]),
            ("\"Never mind.\"", 0, [("wf", "...Hm.")])],
        arms_pre=[("n", "His arms are stripped bare. I'll have to rebuild the fur sleeves from scraps.")],
        arms=dict(hits=1, speed=1.05, zone=58),
        arms_post=[("wf", "Hands... It feels like I've had hands before. A long time ago. Somewhere else.")],
        c2=[("\"Tell me what you remember.\"", 1, [("wf", "A stage. Smaller than this one. A song. Someone... fixing me?"), ("wf", "No. That can't be right. Nobody ever fixed us.")]),
            ("\"Let's do the legs.\"", 0, [("wf", "...Yes.")])],
        legs_pre=[("n", "His legs are just endoskeleton. The fur is in a trash bag in the corner.")],
        legs=dict(hits=1, speed=1.2, zone=50),
        legs_post=[("wf", "I can stand. One more thing. My face. They took it apart to see how it worked.")],
        final_q=[("n", "The FULL REPAIR page says the old face can use either a {b}music box core{/b} or a {b}voice box core{/b}.")],
        final=[("Use a music box core.", 14, 1, [("wf", "...That feels... familiar. Yes.")]),
               ("Use a voice box core.", 0, 0, [("wf", "...Fine.")])],
        full_pre=[("n", "Last step: rebuild the face, re-fur the head, recalibrate the eyes.")],
        full=dict(hits=3, speed=1.32, zone=44, reverse=True),
        outro=[("n", "Withered Freddy's eyes clear to a pale blue. He looks old, but whole."), ("wf", "I don't know who you are, night guard. But thank you.")],
    )

    ROUTES["witheredbonnie"] = dict(
        intro=[("n", "Withered Bonnie has no face. Just an endoskeleton skull, two red pinprick eyes, and a row of teeth."),
               ("wb", "Don't... scream. Everyone screams."),
               ("g", "I'm not going to scream.")],
        c1=[("\"I've seen worse.\"", 1, [("wb", "...Really? ...Thank you.")]),
            ("Get to work without answering.", 0, [("wb", "...You're scared. It's fine.")])],
        arms_pre=[("n", "One arm is gone. The other is hanging by a single wire. I'll have to rebuild the whole left shoulder.")],
        arms=dict(hits=1, speed=1.08, zone=56),
        arms_post=[("wb", "My guitar... Did I have a guitar?")],
        c2=[("Find an old guitar in the storage closet.", 1, [("n", "It's cracked, but he holds it like it's the most precious thing in the world."), ("wb", "...I think I knew how to play this once.")]),
            ("\"I don't know.\"", 0, [("wb", "...No one knows anything here.")])],
        legs_pre=[("n", "His legs are rusted solid at the knee. The suit fabric has rotted into the joints.")],
        legs=dict(hits=1, speed=1.22, zone=48),
        legs_post=[("wb", "Please... my face. I want people to see me and not run.")],
        final_q=[("n", "There's no original face left. I can build one from {b}spare parts from the old Bonnie mold{/b}, or use a {b}Toy Bonnie spare face{/b}.")],
        final=[("Build it from the old Bonnie mold.", 14, 1, [("wb", "...Me. The old me.")]),
               ("Use the Toy Bonnie spare.", 0, 0, [("wb", "...That isn't my face. But it's a face.")])],
        full_pre=[("n", "Last step: build a face from nothing, then wire the eyes and jaw. This is the hardest face job I've done.")],
        full=dict(hits=3, speed=1.34, zone=42, reverse=True),
        outro=[("n", "When I step back, there's a face looking at me. Purple, patched, a little lopsided. But a face."), ("wb", "...Can I see? ...Oh. Oh, that's me.")],
    )

    ROUTES["witheredchica"] = dict(
        intro=[("n", "Withered Chica sits with her jaw unhinged, hanging open so wide it touches her chest. Her hands are just wires."),
               ("wc", "Hhhhungry... so... hungry..."),
               ("g", "I don't think you can eat anything."),
               ("wc", "I know. I just... remember being hungry. Somewhere else.")],
        c1=[("\"Where else?\"", 1, [("wc", "A kitchen. Ovens. Someone who brought me food once. I don't know who.")]),
            ("\"Hold still.\"", 0, [("wc", "...Hhhh.")])],
        arms_pre=[("n", "Her hands are completely gone. Just exposed wiring. I'll have to build new ones from spare parts.")],
        arms=dict(hits=1, speed=1.08, zone=56),
        arms_post=[("wc", "Hands! I can... I can hold things!")],
        c2=[("Give her a plastic cupcake from the prize shelf.", 1, [("wc", "...A cupcake. I had one of these. I think.")]),
            ("\"Let's keep going.\"", 0, [("wc", "...Okay.")])],
        legs_pre=[("n", "Her legs are okay, but her hip motor has burned out. I'll have to swap it.")],
        legs=dict(hits=1, speed=1.22, zone=48),
        legs_post=[("wc", "My jaw. Please. I can't close my mouth. It's been open for years.")],
        final_q=[("n", "The FULL REPAIR page says her jaw can be rebuilt with a {b}steel hinge{/b}, slow but strong, or a {b}spring hinge{/b}, quick but likely to snap.")],
        final=[("Use the steel hinge.", 14, 1, [("wc", "Strong. Good. I don't want it to break again.")]),
               ("Use the spring hinge.", 0, 0, [("wc", "...Okay. Be careful.")])],
        full_pre=[("n", "Last step: rebuild the jaw. If it slips, it'll snap shut on my hand.")],
        full=dict(hits=3, speed=1.34, zone=42, reverse=True),
        outro=[("n", "Her jaw closes with a soft click. She opens it. Closes it. Opens it again."), ("wc", "I can close my mouth. Thank you. That sounds silly, but... thank you.")],
    )

    ROUTES["witheredfoxy"] = dict(
        intro=[("n", "Withered Foxy is crouched in the darkest corner of Parts and Service. His jaw hangs loose. His suit is shredded down to strips."),
               ("wx", "Who goes there? State yer business, landlubber!"),
               ("g", "Night guard. I'm here to fix you."),
               ("wx", "Fix me? Hah. Nobody's fixed ol' Foxy in—... I don't remember how long. Ever, maybe.")],
        c1=[("\"Then I'll be the first.\"", 1, [("wx", "...Hmph. Bold words. We'll see.")]),
            ("\"Just hold still.\"", 0, [("wx", "Aye, aye.")])],
        arms_pre=[("n", "His hook is still attached, but the arm under it is bare metal. The other arm is gone at the elbow.")],
        arms=dict(hits=1, speed=1.12, zone=54),
        arms_post=[("wx", "Ahh, that's better. Now I can hold me hook proper.")],
        c2=[("\"You ever get to do your show here?\"", 1, [("wx", "Never. They brought us here for parts. We never once went on stage."), ("wx", "Before this, there was a cove. A little stage of me own. I think.")]),
            ("\"Legs next.\"", 0, [("wx", "Aye.")])],
        legs_pre=[("n", "His legs are fast, too fast. The servos are overclocked. I'll have to slow them down or he'll run himself apart.")],
        legs=dict(hits=1, speed=1.26, zone=46),
        legs_post=[("wx", "Ah! I could sprint the length of a ship! ...One more thing, matey. Me jaw."), ("wx", "Can't talk proper with it hangin' like this.")],
        final_q=[("n", "The FULL REPAIR page lists two voice modules: his {b}original pirate voice{/b}, or a {b}new Toy-line voice{/b} that's more stable.")],
        final=[("Keep the pirate voice.", 14, 1, [("wx", "Yarr! There's the good stuff!")]),
               ("Install the Toy-line voice.", 0, 0, [("wx", "Hello, friends! I'm Foxy! ...Blimey. That's awful.")])],
        full_pre=[("n", "Last step: rebuild the jaw, reset the voice, rein in those servos. Foxy is fast. If this slips, he won't be able to stop himself.")],
        full=dict(hits=3, speed=1.38, zone=42, reverse=True),
        outro=[("n", "Withered Foxy's jaw locks into place with a snap. His gold eye burns bright."), ("wx", "I don't know ye, matey. But I'd follow ye into any storm.")],
    )


## ---------------------------------------------------------------- route engine
label say_lines(lines):
    $ _li = 0
    while _li < len(lines):
        $ _sp, _tx = lines[_li]
        $ renpy.say(narrator if _sp == "n" else getattr(store, _sp), _tx)
        $ _li += 1
    return

label pick_choice(options):
    ## options: list of (text, trust, lines)  — applies trust, plays lines
    $ _pc = renpy.display_menu([(o[0], i) for i, o in enumerate(options)])
    $ trust[current_anim] += options[_pc][1]
    call say_lines(options[_pc][2])
    return

label repair_route(key):
    $ R = ROUTES[key]
    $ nd = 1.0 + 0.04 * (night - 1)
    $ bonus = 0
    $ current_anim = key
    scene expression "bg " + ANIM[key]["bg"]
    with dissolve
    $ renpy.show(key + " broken", at_list=[twitch])
    with dissolve
    call say_lines(R["intro"])
    call pick_choice(R["c1"])

    call say_lines(R["arms_pre"])
    call skill_check(key, "ARMS", hits=R["arms"]["hits"], speed=R["arms"]["speed"] * nd, zone=R["arms"]["zone"])
    play sound "audio/servo.wav"
    $ renpy.show(key + " arms", at_list=[twitch])
    with flash
    call say_lines(R["arms_post"])
    call pick_choice(R["c2"])

    call say_lines(R["legs_pre"])
    call skill_check(key, "LEGS", hits=R["legs"]["hits"], speed=R["legs"]["speed"] * nd, zone=R["legs"]["zone"])
    play sound "audio/servo.wav"
    $ renpy.show(key + " legs", at_list=[twitch])
    with flash
    call say_lines(R["legs_post"])

    call say_lines(R["final_q"])
    $ _fc = renpy.display_menu([(o[0], i) for i, o in enumerate(R["final"])])
    $ bonus = R["final"][_fc][1]
    $ trust[current_anim] += R["final"][_fc][2]
    call say_lines(R["final"][_fc][3])

    call say_lines(R["full_pre"])
    $ renpy.notify("Final check — harder than the others.")
    call skill_check(key, "FULL REPAIR", hits=R["full"]["hits"], speed=R["full"]["speed"] * nd, zone=R["full"]["zone"] + bonus, reverse=R["full"].get("reverse", True))
    play sound "audio/chime.wav"
    $ renpy.show(key + " fixed", at_list=[repaired_glow])
    with flash
    call say_lines(R["outro"])
    return


## ---------------------------------------------------------------- chapter start
label chapter2_start:
    $ reset_chapter_state(2)
    $ chapter_ease = 1 in persistent.good_endings
    $ ch2_first = None
    scene black
    with dissolve
    show text "{size=90}{b}CHAPTER 2{/b}{/size}\n{size=40}The New Location{/size}" at truecenter
    with dissolve
    pause 2.0
    hide text

    ## Same guard as Chapter 1, so default to the name they used before.
    $ guard_name = renpy.input("Night guard, what's your name?", default=persistent.guard_name or "Mike", length=16).strip() or "Mike"
    $ persistent.guard_name = guard_name
    if chapter_ease:
        "{i}(You earned the good ending in Chapter 1. Skill checks this chapter are a little easier.){/i}"

    play music "audio/ambience.wav" fadein 2.0 volume 0.5
    scene bg partyroom
    with slowfade
    "The new Freddy Fazbear's Pizza is all bright plastic and party streamers. Brand new. And already closing."
    "Something happened here. Nobody will tell me what. They just need a night guard until the doors close for good."
    scene bg office2
    with dissolve
    "The office is a desk at the end of a long, dark hallway. No doors. Just a flashlight and an empty Freddy mask on the desk."
    "The phone rings."
    phone "Uh, hello? Hello! Welcome to your new summer job at the new and improved Freddy Fazbear's Pizza!"
    phone "So, uh, between you and me, the new animatronics got a little... roughed up. And the old ones from the first location are in back, being used for parts."
    phone "Management wants them all looking presentable before the closing party. Every last one of 'em. That's, uh, kind of your job now."
    phone "There's a toolkit under the desk. Same model as the one from the old place, I think. Funny, somebody already used it. It's covered in old fingerprints."
    phone "Oh, and the music box in the Prize Corner? It's busted. Don't worry about that one yet. Just... don't let it get too quiet back there."
    phone "Okay! Good luck. Talk to you tomorrow."
    "Eight animatronics. Four shiny new ones on the floor. Four ruined old ones in the back."
    "I'll start with one group and finish it before I touch the other."
    jump ch2_night_hub


label ch2_night_hub:
    $ night += 1
    $ current_anim = None
    scene black
    with dissolve
    show text "{size=90}{b}NIGHT [night]{/b}{/size}\n{size=40}12:00 AM{/size}" at truecenter
    with dissolve
    pause 1.4
    hide text
    scene bg office2
    with dissolve

    if night == 3:
        phone "Hey, nice work so far. Oh, and if you hear a music box playing from the Prize Corner... that's normal. Probably."
    elif night == 5:
        phone "Halfway! The ones you fixed have been standing around the office hallway. Watching. I think they're just curious."
    elif night == 7:
        phone "So, uh, that music box. It's getting quieter every night. Whatever's in that box... I don't think it likes the quiet."

    $ renpy.notify("Good moment to save your game.")

    if ch2_first is None:
        "Which group should I start with? I'll have to finish all of them before I move on to the other group."
        menu:
            "The Toys — the shiny new animatronics":
                $ ch2_first = "toys"
                "The new ones first. They're the face of this place."
            "The Withereds — the old ones in the back":
                $ ch2_first = "withered"
                "The old ones first. They've been waiting longer."

    $ _primary = CH2_TOYS if ch2_first == "toys" else CH2_WITHERED
    $ _secondary = CH2_WITHERED if ch2_first == "toys" else CH2_TOYS
    $ _group = [k for k in _primary if k not in repaired] or [k for k in _secondary if k not in repaired]

    if not _group:
        jump ch2_finale

    if _group[0] in _secondary and all(k in repaired for k in _primary) and not any(k in repaired for k in _secondary):
        "That's the whole first group done. Time for the others."

    "Who should I work on tonight?"
    $ _pick = renpy.display_menu([("%s — %s" % (ANIM[k]["name"], ANIM[k]["where"]), k) for k in _group])
    call repair_route(_pick)
    $ repaired.append(_pick)

    scene black
    with dissolve
    play sound "audio/chime.wav"
    show text "{size=110}{b}6:00 AM{/b}{/size}" at truecenter
    with dissolve
    pause 2.0
    hide text
    $ _done = len(repaired)
    "[_done] of 8 repaired."
    jump ch2_night_hub


## ---------------------------------------------------------------- Puppet finale
label ch2_finale:
    phone "Hey, uh... night nine. All eight of 'em are fixed. Management's thrilled."
    phone "But listen. That music box in the Prize Corner stopped playing today. Completely."
    phone "If you can fix it... do it fast. And keep it wound while you work. Whatever you do, don't let it run down."
    "The tape clicks off. The hallway is silent."

    scene bg prize
    with slowfade
    "The Prize Corner. A big gift box sits on the counter, ribbon faded. On top of it, a music box. Its crank lies on the floor."
    "The lid of the gift box is open an inch. Something inside is looking at me."
    show puppet broken at sprite_pos(0.5)
    with dissolve
    pp "You came back."
    g "...Do I know you?"
    pp "You fixed them before. At the first place. Freddy. Bonnie. Chica. Foxy. The golden one."
    pp "The old ones here don't remember you. Their memories were taken apart with everything else. But I remember."
    pp "I remember everyone."
    $ current_anim = "puppet"

    menu:
        "\"Then you know I'll fix your box too.\"":
            $ trust["puppet"] += 1
            pp "I know you will try."
        "\"What are you?\"":
            pp "Something that gives gifts. And gives life. And sometimes... takes it."

    pp "Fix the box. Not me. The box keeps me calm. Let it run down, and I won't be able to stop myself."
    hide puppet
    with dissolve
    show musicbox broken at sprite_pos(0.5)
    with dissolve
    "It's half wound. I'll have to keep it going while I work."
    $ renpy.notify("HOLD to wind the music box. Don't let it run out.")
    call wind_music_box(duration=9.0, drain=0.09)

    "First: the crank. The shaft is bent."
    call skill_check("musicbox", "CRANK", hits=1, speed=1.1, zone=56)
    play sound "audio/servo.wav"
    show musicbox arms at sprite_pos(0.5)
    with flash
    pp "Good. Keep going. The music is getting quieter."
    call wind_music_box(duration=11.0, drain=0.12)

    "Next: the comb and the spring. Half the teeth are snapped off."
    call skill_check("musicbox", "COMB & SPRING", hits=2, speed=1.22, zone=50)
    play sound "audio/servo.wav"
    show musicbox legs at sprite_pos(0.5)
    with flash
    pp "One more. The hard part. You always save it for last."

    menu:
        "\"How do you know that?\"":
            $ trust["puppet"] += 1
            pp "A note. Taped to a toolbox. At the first place. You read it every night."
        "Stay focused.":
            pass

    call wind_music_box(duration=13.0, drain=0.15)
    "Final repair: rebuild the cylinder and retune every tooth. Three in a row."
    $ renpy.notify("Final check — the box must be perfect.")
    call skill_check("musicbox", "FULL REPAIR", hits=3, speed=1.36, zone=44, reverse=True)
    play sound "audio/chime.wav"
    show musicbox fixed at repaired_glow
    with flash
    play music "audio/musicbox.wav" volume 0.8
    "The music box plays. Clear, slow, and perfectly in tune."
    jump ch2_end


label ch2_end:
    $ total_trust = sum(trust.values())
    scene bg prize
    with dissolve
    show puppet fixed at sprite_pos(0.5)
    with dissolve
    pp "Thank you, [guard_name]. I can rest a little now."
    if total_trust >= 16:
        pp "You were gentle with all of them. The new ones and the old ones. Even the ones who didn't remember you."
        pp "That's rare. I want to give you something for that."
        $ persistent.endings.add("ch2_good")
        $ persistent.good_endings.add(2)
        $ _ending_name = "THE GIFT"
    else:
        pp "You fixed them. All of them. But you didn't listen to them."
        pp "Maybe you'll learn to listen where you're going next."
        $ persistent.endings.add("ch2_cold")
        $ _ending_name = "THE QUIET"
    pp "There is one more who needs to be found. He isn't broken. He's trapped."
    pp "Thirty years from now, in a place built to remember all of this... he'll be waiting."
    pp "The others there aren't real. Not really. You'll have to figure out what's holding each of them."
    "The Puppet reaches out one long, striped hand and touches my forehead."
    "The music box gets louder. And louder. The Prize Corner melts into static."
    scene black
    with slowfade
    stop music fadeout 2.0
    play sound "audio/chime.wav"
    show text "{size=80}{b}CHAPTER 2 COMPLETE{/b}{/size}\n{size=40}Ending: [_ending_name]{/size}" at truecenter
    with dissolve
    pause 3.0
    hide text
    $ persistent.chapter_unlocked = max(persistent.chapter_unlocked, 3)
    if 2 in persistent.good_endings:
        show text "{size=60}{b}CHAPTER 3 UNLOCKED{/b}{/size}\n{size=36}Good ending reward: easier skill checks in Chapter 3{/size}" at truecenter
    else:
        show text "{size=60}{b}CHAPTER 3 UNLOCKED{/b}{/size}\n{size=36}Select it from Chapters on the main menu{/size}" at truecenter
    with dissolve
    pause
    return
