## Golden Freddy — Night 5 (Chapter 1 finale)
## He's the most broken animatronic in the building, so every check is harder:
## more hits needed, faster needle, smaller zones.

label repair_goldenfreddy:
    $ nd = 1.15
    $ bonus = 0
    scene bg office
    with dissolve
    "I sit back down in the office. The fan ticks. The monitors hiss."
    "When I look up from the desk, he's there."
    play sound "audio/servo.wav"
    show goldenfreddy broken at twitch
    with flash
    "A golden bear, slumped against the wall where nothing was a second ago. No endoskeleton inside. Just an empty suit."
    "His eyes are two black holes. They're looking at me anyway."
    gf "IT'S ME."
    g "...Yeah. I figured."

    menu:
        "\"I'm not scared of you.\"":
            $ trust["goldenfreddy"] += 1
            gf "YOU SHOULD BE. ...BUT THANK YOU."
        "Reach for the toolbox without a word.":
            gf "STRAIGHT TO WORK. LIKE THE OTHERS WHO CAME BEFORE YOU."

    "There's nothing to bolt his arms onto. The manual has one line for this model: {i}\"Suit is spring-locked. Do NOT attempt repair.\"{/i}"
    "I'll have to rebuild the arm frames from scrap and spring-lock them into the suit. Twice."
    $ renpy.notify("Golden Freddy is more broken. Every check is harder.")
    call skill_check("goldenfreddy", "ARMS", hits=2, speed=1.15 * nd, zone=52)
    play sound "audio/servo.wav"
    show goldenfreddy arms at twitch
    with flash

    gf "THE OTHERS. YOU FIXED THEM FIRST."
    gf "DID THEY TELL YOU WHAT HAPPENED HERE?"

    menu:
        "\"Some of it. I want to hear it from you.\"":
            $ trust["goldenfreddy"] += 1
            gf "THERE WAS A MAN IN PURPLE. THERE WERE CHILDREN WHO NEVER WENT HOME."
            gf "I WAS THE FIRST TO SEE IT. I HAVE BEEN WATCHING EVER SINCE."
        "\"I don't need to know.\"":
            gf "NO ONE EVER DOES."

    "His legs are two flat sacks of fur. Same job as the arms, but the springs are stiffer down here."
    call skill_check("goldenfreddy", "LEGS", hits=2, speed=1.28 * nd, zone=46)
    play sound "audio/servo.wav"
    show goldenfreddy legs at twitch
    with flash

    "He stands. He's not supposed to be able to stand. There's nothing in there to stand with."
    gf "ONE THING MORE. THE HARD PART."
    "His chest has a spring-lock control with two settings: {b}LOCK{/b} the springs for good, or {b}RELEASE{/b} the tension so they can never snap shut again."

    menu:
        "Release the springs.":
            $ bonus = 12
            $ trust["goldenfreddy"] += 1
            gf "...NO ONE HAS EVER CHOSEN THAT."
        "Lock them.":
            gf "AS YOU WISH."

    "Final repair. Every spring in the suit at once. Four hits in a row, and the needle won't wait."
    $ renpy.notify("Hardest check in Chapter 1.")
    call skill_check("goldenfreddy", "FULL REPAIR", hits=4, speed=1.42 * nd, zone=38 + bonus, reverse=True)
    play sound "audio/chime.wav"
    show goldenfreddy fixed at repaired_glow
    with flash

    "Golden Freddy's suit is gold again. Not new, but whole."
    "Two tiny white lights flicker on deep in his eyes."
    gf "Thank you, [guard_name]. I can speak softly now."
    return
