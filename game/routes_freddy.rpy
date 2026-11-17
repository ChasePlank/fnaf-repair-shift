## Freddy — Show Stage
## Template for a repair route: intro → ARMS check → LEGS check → FULL REPAIR check.

label repair_freddy:
    $ nd = 1.0 + 0.06 * (night - 1)   # later nights are slightly faster
    $ bonus = 0
    scene bg stage
    with dissolve
    show freddy broken at twitch
    with dissolve

    "Freddy Fazbear slumps at center stage, one arm missing and the other stripped down to a bare metal endoskeleton."
    "His head hangs at an angle that makes my neck hurt to look at. One eye dangles from a red wire."
    "As my flashlight passes over him, the good eye rolls to follow it."
    fr "...Hhhh... ap... py... birth... day..."
    g "Hey, big guy. I'm here to help. Just hold still."

    menu:
        "Talk to him while you work.":
            $ trust["freddy"] += 1
            g "I'm going to start with your arms, okay? You'll be able to hold your mic again."
            fr "...mic..."
        "Get straight to work.":
            "No point talking to a machine. I pop open the toolbox."

    "I find his right arm under the stage, still in its fur sleeve. The shoulder socket is packed with dust."
    call skill_check("freddy", "ARMS", hits=1, speed=1.0 * nd, zone=62)
    play sound "audio/servo.wav"
    show freddy arms at twitch
    with flash

    "The servos catch. Both arms swing once, hard, and slam against the stage floor."
    "Then, slowly, they settle at his sides."
    fr "Hands. I... have hands again."
    fr "There used to be so many little hands. Clapping. Every Saturday."

    menu:
        "\"Tell me about the Saturdays.\"":
            $ trust["freddy"] += 1
            fr "Cake. Balloons. A song I sang one hundred times a day. I did not mind. They always laughed in the same place."
            fr "And then one day... they stopped coming."
        "\"Let's keep going.\"":
            fr "...Yes. Keep going."

    "His legs are bolted to the stage, but the knee joints are rusted solid. I'll have to realign the whole assembly."
    call skill_check("freddy", "LEGS", hits=1, speed=1.15 * nd, zone=52)
    play sound "audio/servo.wav"
    show freddy legs at twitch
    with flash

    "Freddy rises to his full height. He's taller than I expected. Much taller."
    fr "Thank you, night guard. One thing more. The hard part."
    fr "Inside my chest there was a music box. It played when the lights went out. It kept... the dark away."
    "The manual's FULL REPAIR page shows two options for the core: a {b}voice box{/b} or a {b}music box{/b}."

    menu:
        "Install the music box.":
            $ bonus = 14
            $ trust["freddy"] += 1
            fr "Yes. That one."
        "Install the voice box.":
            "Freddy's eyes flicker, uneasy. That wasn't what he wanted."

    "Last step. Wire the core, close the chest plate, recalibrate the eyes. One slip and he'll lose control."
    $ renpy.notify("Final check — harder than the others.")
    call skill_check("freddy", "FULL REPAIR", hits=3, speed=1.3 * nd, zone=46 + bonus, reverse=True)
    play sound "audio/chime.wav"
    show freddy fixed at repaired_glow
    with flash

    "Freddy's eyes clear to a steady blue. His bowtie is even straight."
    fr "Hello, [guard_name]. I remember your name now. I remember a lot of things."
    fr "Go to the others. They're frightened. I will keep watch until morning."
    return
