## =============================================================================
## Five Nights: Repair Shift — main flow
## A non-commercial FNAF fan game. FNAF and its characters belong to
## Scott Cawthon. Made for fun, not for sale.
## =============================================================================

label start:
    stop music
    scene black
    with dissolve

    "{i}This is a fan-made game. Save often — failing a repair is fatal.{/i}"

    $ guard_name = renpy.input("Night guard, what's your name?", default="Mike", length=16).strip() or "Mike"

    play music "audio/ambience.wav" fadein 2.0 volume 0.5
    scene bg exterior
    with slowfade

    "The listing said {i}\"Overnight security. Five nights. Demolition site. Cash.\"{/i}"
    "It didn't say the site was {b}the first one{/b}."
    "Freddy Fazbear's Pizza. The original location. Boarded up decades before I was old enough to want a birthday party here."
    g "Five nights. Sit in the office, watch nothing happen, get paid. Easy."
    "The key the contractor gave me sticks in the lock like it hasn't turned in years."

    scene bg dining
    with dissolve
    "Inside, the air is thick with dust and old cardboard. Party hats still sit on the tables, crushed flat."
    "Somewhere deeper in the building, metal ticks against metal. Just the building settling. Probably."

    scene bg office
    with dissolve
    "The security office is exactly as somebody left it. Monitors. A desk fan. An answering machine with a blinking red light."
    g "No way that still works."
    "I press play."
    play sound "audio/check_alert.wav"
    phone "Uh, hello? Hello, hello! If you're hearing this, then... wow. Somebody finally came back."
    phone "I don't know how long it's been. I'm recording this in case... well, in case."
    phone "The characters — Freddy and the gang — they aren't, uh, in the best shape. Somebody did a number on them. Took 'em apart, mostly."
    phone "Management says leave 'em alone. But between you and me? I think they just want to be put back together."
    phone "There's a toolkit in Parts and Service. And a manual. If you've got steady hands... maybe give it a shot."
    phone "Just — be careful. When they're half-built, they get... confused. One slip and, well. They don't really know their own strength."
    phone "Okay. That's all. Good night."
    "The tape clicks off."

    scene bg parts
    with dissolve
    "Parts and Service. A single bulb buzzes over a workbench."
    "There's a red toolbox, a binder labeled {b}FAZBEAR ANIMATRONIC SERVICE MANUAL — REV. 1{/b}, and a note taped to the lid."
    "{i}\"Arms first. Then legs. Then the hard part. Don't rush the hard part.\"{/i}"
    g "Arms, legs, and then... the hard part."
    "I count four of them on the floor plan. Freddy and Bonnie on the Show Stage. Chica in the Kitchen. Foxy in Pirate Cove."
    "Five nights. Four animatronics. One per night, if my hands hold out."

    jump night_hub


## ------------------------------------------------------------------ night hub
label night_hub:
    $ night += 1
    $ current_anim = None
    scene black
    with dissolve
    show text "{size=90}{b}NIGHT [night]{/b}{/size}\n{size=40}12:00 AM{/size}" at truecenter
    with dissolve
    pause 1.4
    hide text
    scene bg office
    with dissolve

    if night == 2:
        phone "Hey, uh, it's me again. If you're hearing this, you made it through. Good. Good."
        phone "I noticed one of 'em was standing a little straighter this morning. That you? Nice work."
    elif night == 3:
        phone "Halfway there. Listen... the ones you haven't fixed yet, they can tell. They've been watching the office door."
        phone "Not in a bad way. I think. I think they're waiting their turn."
    elif night == 4:
        phone "Okay, so, one thing I should probably mention. There's a room behind Parts and Service. Sealed. We don't talk about that room."
        phone "Just... if you ever hear singing from back there, uh. Don't sing along."

    $ renpy.notify("Good moment to save your game.")

    $ remaining = [k for k in REPAIR_ORDER if k not in repaired]
    if not remaining:
        jump night_final

    "Who should I work on tonight?"
    menu:
        "Freddy — Show Stage" if "freddy" not in repaired:
            $ current_anim = "freddy"
            call repair_freddy
        "Bonnie — Show Stage" if "bonnie" not in repaired:
            $ current_anim = "bonnie"
            call repair_bonnie
        "Chica — Kitchen" if "chica" not in repaired:
            $ current_anim = "chica"
            call repair_chica
        "Foxy — Pirate Cove" if "foxy" not in repaired:
            $ current_anim = "foxy"
            call repair_foxy

    $ repaired.append(current_anim)
    call six_am
    jump night_hub


label six_am:
    scene black
    with dissolve
    play sound "audio/chime.wav"
    show text "{size=110}{b}6:00 AM{/b}{/size}" at truecenter
    with dissolve
    pause 2.0
    hide text
    if len(repaired) < 4:
        "[len(repaired)] of 4 repaired."
    return


## ------------------------------------------------------------------ night 5
label night_final:
    phone "Hey, hey. Night five. Last one. I, uh... I don't have a script for this one."
    phone "If you fixed all four of them... then there's one more you should know about. He doesn't show up on the cameras."
    phone "If you see him, don't panic. And whatever you do, don't look away."
    "The tape clicks off. The office lights dim, then come back."
    play sound "audio/servo.wav"
    "Footsteps in the hall. Heavy ones. Four sets."

    scene bg dining
    with dissolve
    show freddy fixed at sprite_pos(0.14)
    show bonnie fixed at sprite_pos(0.38)
    show chica fixed at sprite_pos(0.62)
    show foxy fixed at sprite_pos(0.86)
    with dissolve
    "They're all here, standing in the dining room like a show is about to start."
    fr "[guard_name]. There is one more. The golden one."
    bo "He's not like us. He's... more broken. Way more broken."
    ch "He only comes out when he wants to. And he's been waiting for you."
    fo "Go back to yer office, matey. He'll find ye there."

    menu:
        "\"I'll fix him too.\"":
            $ trust["goldenfreddy"] += 1
            fr "We know you will."
        "\"Why didn't you warn me sooner?\"":
            fr "You were not ready. Neither were we."

    $ current_anim = "goldenfreddy"
    call repair_goldenfreddy
    $ repaired.append("goldenfreddy")
    jump chapter1_end


## ------------------------------------------------------------------ chapter 1 end
label chapter1_end:
    $ total_trust = sum(trust.values())
    scene bg stage
    with slowfade
    show freddy fixed at sprite_pos(0.14)
    show bonnie fixed at sprite_pos(0.38)
    show goldenfreddy fixed at sprite_pos(0.5)
    show chica fixed at sprite_pos(0.62)
    show foxy fixed at sprite_pos(0.86)
    with dissolve

    "The stage lights come on by themselves. Every bulb that still works."
    if total_trust >= 10:
        gf "One show. For the one who put us back together."
        "They play. It's rough, the speakers crackle, and Bonnie's guitar is a half-step flat."
        "It's the best thing I've ever heard."
        fr "We remember now, [guard_name]. Who we were. What happened here."
        ch "And we don't have to be scared of it anymore."
        $ persistent.endings.add("ch1_good")
        $ _ending_name = "THE LAST SHOW"
    else:
        gf "You fixed us. Every bolt. Every wire."
        fr "But you hurried, [guard_name]. You never really talked to us."
        bo "We're whole now. But we're still... lonely."
        "None of them move to play. They just watch me."
        $ persistent.endings.add("ch1_cold")
        $ _ending_name = "CLOSING TIME"

    if total_checks > 0 and perfect_checks == total_checks:
        gf "Not one slip. Steady hands. Steadier than ours ever were."

    gf "But this place was only the first."
    gf "There is a newer restaurant. Newer animatronics. Shinier faces. And something in the Prize Corner that never sleeps."
    gf "It will need you, [guard_name]. More than we did."
    fo "Ye'll be needin' a music box, lad. Keep it wound."

    scene black
    with slowfade
    play sound "audio/chime.wav"
    show text "{size=80}{b}CHAPTER 1 COMPLETE{/b}{/size}\n{size=40}Ending: [_ending_name]{/size}" at truecenter
    with dissolve
    pause 3.0
    hide text
    $ persistent.chapter_unlocked = max(persistent.chapter_unlocked, 2)
    show text "{size=60}{b}CHAPTER 2 UNLOCKED{/b}{/size}\n{size=36}Select it from Chapters on the main menu{/size}" at truecenter
    with dissolve
    pause
    return


## ------------------------------------------------------------------ death
label game_over:
    $ config.allow_skipping = True
    window hide
    stop music
    play sound "audio/jumpscare.wav"
    $ _who = current_anim or "freddy"
    $ _stage = getattr(store, "_death_stage", "broken")
    scene black
    show redflash at flicker
    $ renpy.show(_who + " " + _stage, at_list=[jumpscare_in])
    pause 1.3
    scene black
    with Dissolve(0.6)
    $ deaths_seen.add(_who)
    call screen game_over_screen(ANIM[_who]["name"])
    return


screen game_over_screen(who):
    modal True
    add Solid("#000")
    vbox:
        align (0.5, 0.45)
        spacing 30
        text "YOU DIED" size 130 bold True color "#c8102e" xalign 0.5 outlines [(4, "#000", 0, 0)]
        text "[who] wasn't ready to be fixed." size 36 color "#bbbbbb" xalign 0.5
        null height 20
        textbutton "Load a Save" action ShowMenu("load") xalign 0.5 text_size 46
        textbutton "Main Menu" action MainMenu(confirm=False) xalign 0.5 text_size 46
