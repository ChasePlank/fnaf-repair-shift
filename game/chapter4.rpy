## =============================================================================
## CHAPTER 4 — The Nightmare (FNAF 4)
## Springtrap sent you here. When you wake up, he's gone.
## Five real-time nights, 5 minutes each (see nightmare.rpy). No dialogue:
## the nightmares never talk. They're in your head and they just want you dead.
## Surviving Night 5 wakes you up in the Sister Location elevator.
## Good ending (died 3 times or fewer this chapter): easier Chapter 5.
## =============================================================================

label chapter4_start:
    $ reset_chapter_state(4)
    $ chapter_ease = 3 in persistent.good_endings
    $ persistent.ch4_deaths = 0
    $ guard_name = persistent.guard_name or "Mike"
    scene black
    with dissolve
    show text "{size=90}{b}CHAPTER 4{/b}{/size}\n{size=40}The Nightmare{/size}" at truecenter
    with dissolve
    pause 2.0
    hide text
    if chapter_ease:
        "{i}(You earned the good ending in Chapter 3. The nightmares give you a little more time to react.){/i}"
    scene bg bedroom
    with slowfade
    "A child's bedroom. A flashlight in my hand. Two doors, a closet, and a bed behind me."
    "No Springtrap. No smoke. Nothing that talks."
    "Just breathing, somewhere down the hall."
    call screen nightmare_intro
    call screen nightmare_controls
    jump ch4_night_hub


label ch4_night_hub:
    $ night += 1
label ch4_night_play:
    stop music fadeout 1.0
    scene black
    with dissolve
    show text "{size=90}{b}NIGHT [night]{/b}{/size}\n{size=40}12:00 AM{/size}" at truecenter
    with dissolve
    pause 1.6
    hide text
    scene bg bedroom
    with dissolve
    $ renpy.notify("Good moment to save your game.")
    if night == 5:
        "Something in the dark is laughing. Low and slow. It sounds bigger than the others."
    menu:
        "Start Night [night]":
            pass
        "Review how to survive":
            call screen nightmare_controls
    play music "audio/ambience.wav" fadein 1.0 volume 0.25
    $ quick_menu = False
    window hide
    $ _nr = renpy.call_screen("nightmare_night", night=night)
    $ quick_menu = True
    stop music fadeout 0.5
    if config.developer and getattr(store, "_night_len", None):
        $ open("/tmp/devlog.txt", "a").write("ch4 night=%s result=%s\n" % (night, _nr))
    if _nr != "win":
        $ current_anim = "nightmare" + _nr.split(":", 1)[1] if _nr.split(":", 1)[1] != "fredbear" else "fredbear"
        $ _death_stage = "broken"
        $ persistent.ch4_deaths = (persistent.ch4_deaths or 0) + 1
        jump ch4_death
    scene black
    with dissolve
    play sound "audio/chime.wav"
    show text "{size=110}{b}6:00 AM{/b}{/size}" at truecenter
    with dissolve
    pause 2.4
    hide text
    if night >= 5:
        jump ch4_end
    jump ch4_night_hub


label ch4_end:
    $ _good = (persistent.ch4_deaths or 0) <= 3
    scene black
    with slowfade
    "The alarm clock rings, and doesn't stop."
    "Then the ringing becomes a hum. Low. Mechanical. The floor drops under me, slowly."
    scene bg elevator
    with slowfade
    "I'm standing up. Metal walls. Buttons. A small screen with a logo on it."
    "{b}CIRCUS BABY'S ENTERTAINMENT AND RENTAL{/b}"
    "An elevator. Going down."
    if _good:
        $ persistent.endings.add("ch4_good")
        $ persistent.good_endings.add(4)
        $ _ending_name = "WIDE AWAKE"
    else:
        $ persistent.endings.add("ch4_cold")
        $ _ending_name = "STILL DREAMING"
    scene black
    with dissolve
    play sound "audio/chime.wav"
    show text "{size=80}{b}CHAPTER 4 COMPLETE{/b}{/size}\n{size=40}Ending: [_ending_name]{/size}" at truecenter
    with dissolve
    pause 3.0
    hide text
    $ persistent.chapter_unlocked = max(persistent.chapter_unlocked, 5)
    if _good:
        show text "{size=60}{b}CHAPTER 5 UNLOCKED{/b}{/size}\n{size=36}Good ending reward: easier skill checks in Chapter 5{/size}" at truecenter
    else:
        show text "{size=60}{b}CHAPTER 5 UNLOCKED{/b}{/size}\n{size=36}Select it from Chapters on the main menu{/size}" at truecenter
    with dissolve
    pause
    return


## Death can happen at any second here, so Chapter 4 offers Retry Night
## (restart the same night from 12 AM) on top of loading a save.
label ch4_death:
    $ quick_menu = True
    window hide
    stop music
    play sound "audio/jumpscare.wav"
    scene black
    show redflash at flicker
    $ renpy.show(current_anim + " broken", at_list=[jumpscare_in])
    pause 1.3
    scene black
    with Dissolve(0.6)
    $ deaths_seen.add(current_anim)
    $ _choice = renpy.call_screen("ch4_death_screen", ANIM[current_anim]["name"], ANIM[current_anim].get("death"))
    jump ch4_night_play


screen ch4_death_screen(who, death_line=None):
    modal True
    add Solid("#000")
    vbox:
        align (0.5, 0.45)
        spacing 30
        text "YOU DIED" size 130 bold True color "#c8102e" xalign 0.5 outlines [(4, "#000", 0, 0)]
        text ("%s got you on Night %d." % (who, night)) size 36 color "#bbbbbb" xalign 0.5
        if death_line:
            text death_line size 30 color "#888888" xalign 0.5
        null height 20
        textbutton "Retry Night [night]" action Return("retry") xalign 0.5 text_size 50
        textbutton "Load a Save" action ShowMenu("load") xalign 0.5 text_size 40
        textbutton "Main Menu" action MainMenu(confirm=False) xalign 0.5 text_size 40
