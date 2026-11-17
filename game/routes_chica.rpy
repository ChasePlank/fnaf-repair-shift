## Chica — Kitchen

label repair_chica:
    $ nd = 1.0 + 0.06 * (night - 1)
    $ bonus = 0
    scene bg kitchen
    with dissolve
    show chica broken at twitch
    with dissolve

    "The kitchen smells like something died in the walk-in freezer. Pots clatter as I step in."
    "Chica is half-folded into a corner by the ovens, beak hanging open, jaw unhinged on one side."
    ch "Ooooh, a customer! Are you hungry? Are you {i}hungry{/i}? I'm SO hungry."
    g "I'm not on the menu, right?"
    ch "Haha! ...Haha."

    menu:
        "\"I brought you a slice of pizza from the gas station.\"":
            $ trust["chica"] += 1
            ch "You brought me FOOD? Nobody brings me food! I can't eat it, but I'm going to hold it forever."
        "\"Let's just get this over with.\"":
            ch "Rude. Rude rude rude."

    "Her arms were left on the prep counter, like somebody started to repair her and gave up."
    call skill_check("chica", "ARMS", hits=1, speed=1.05 * nd, zone=60)
    play sound "audio/servo.wav"
    show chica arms at twitch
    with flash

    ch "Arms! Now I can bake! Do you like cupcakes? I {i}am{/i} a cupcake. Spiritually."

    menu:
        "\"What happened to you?\"":
            $ trust["chica"] += 1
            ch "The kitchen got shut down after... the thing. Nobody wanted to eat here anymore."
            ch "So they just stopped feeding the kitchen. And the kitchen stopped feeding me."
        "\"Let's do the legs.\"":
            ch "Fine, fine. Legs."

    "Her legs are jammed under the oven. I'll have to work them free and reseat both hip joints at once."
    call skill_check("chica", "LEGS", hits=1, speed=1.2 * nd, zone=50)
    play sound "audio/servo.wav"
    show chica legs at twitch
    with flash

    ch "I can walk! I'm going to walk directly into the pantry and never come out."
    ch "Wait. Wait. Where is Mr. Cupcake?"
    "The FULL REPAIR page mentions a companion unit — {b}Mr. Cupcake{/b} — linked to her voice processor. Or I could skip it and just use a {b}standard processor{/b}."

    menu:
        "Find Mr. Cupcake in the pantry and link him up.":
            $ bonus = 14
            $ trust["chica"] += 1
            "He's behind a bag of flour, one candle eye blinking. He makes a happy little chirp."
            ch "MY BABY."
        "Install the standard processor.":
            ch "Oh. Okay. I'll just... be by myself, then."

    "Last step: rebuild her jaw hinge and recalibrate her voice. If the jaw slips, it'll snap shut on my hand."
    $ renpy.notify("Final check — harder than the others.")
    call skill_check("chica", "FULL REPAIR", hits=3, speed=1.32 * nd, zone=44 + bonus, reverse=True)
    play sound "audio/chime.wav"
    show chica fixed at repaired_glow
    with flash

    "Chica's feathers fluff up, bright and yellow under the kitchen lights. Her bib is clean. It says LET'S EAT!!! in bold red letters."
    ch "[guard_name], you're my favorite customer. Ever. Of all time."
    ch "Go on, go help the others. I'll have something baking when you come back."
    return
