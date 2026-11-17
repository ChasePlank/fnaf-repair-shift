## Bonnie — Show Stage

label repair_bonnie:
    $ nd = 1.0 + 0.06 * (night - 1)
    $ bonus = 0
    scene bg stage
    with dissolve
    show bonnie broken at twitch
    with dissolve

    "Bonnie sits slumped against the back wall of the stage, his guitar smashed beside him."
    "One ear is gone completely. Wires spill from his shoulder like spaghetti."
    bo "D-d-don't look. Don't look at me. I'm not — I'm not ready for the show."
    g "There's no show tonight. I'm just here to fix you."

    menu:
        "\"You look fine. Really.\"":
            $ trust["bonnie"] += 1
            bo "...You're lying. But that's nice of you."
        "\"Yeah, you're pretty wrecked.\"":
            bo "I {i}know{/i}. You don't have to say it."

    "His arms are in a box labeled {i}BONNIE — DO NOT REUSE{/i}. Somebody meant to replace him."
    call skill_check("bonnie", "ARMS", hits=1, speed=1.05 * nd, zone=60)
    play sound "audio/servo.wav"
    show bonnie arms at twitch
    with flash

    "Bonnie flexes his fingers. They strum the air out of habit."
    bo "My guitar... is it...?"

    menu:
        "Pick up the guitar and tape the neck back together.":
            $ trust["bonnie"] += 1
            "It isn't pretty. Half the strings are missing. I put it in his hands anyway."
            bo "Oh. Oh, it's {i}terrible{/i}. I love it."
        "\"It's beyond saving, sorry.\"":
            bo "...Right. Of course."

    "His legs are stiff with old grime. The hip bolts have been stripped by someone in a hurry."
    call skill_check("bonnie", "LEGS", hits=1, speed=1.2 * nd, zone=50)
    play sound "audio/servo.wav"
    show bonnie legs at twitch
    with flash

    bo "I can stand! I can — whoa — okay, still working on balance."
    bo "One more thing. Please. My face. People used to say I looked friendly."
    "The FULL REPAIR page says Bonnie's faceplate needs either the {b}original mold{/b} or a {b}newer, sleeker model{/b} from the shelf."

    menu:
        "Use the original mold.":
            $ bonus = 14
            $ trust["bonnie"] += 1
            bo "Yes. Me. The real me."
        "Use the newer model.":
            bo "That's... fine. That's fine. I guess."

    "Last step: seat the faceplate, rebuild the ear, recalibrate the eyes."
    $ renpy.notify("Final check — harder than the others.")
    call skill_check("bonnie", "FULL REPAIR", hits=3, speed=1.32 * nd, zone=44 + bonus, reverse=True)
    play sound "audio/chime.wav"
    show bonnie fixed at repaired_glow
    with flash

    "Both ears stand tall. His eyes go from a panicked red to a soft, even pink."
    bo "[guard_name]! I'm — I'm {i}me{/i} again!"
    bo "Okay, okay. I'm going to go practice. Very quietly. Probably."
    return
