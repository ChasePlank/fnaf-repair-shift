## Foxy — Pirate Cove

label repair_foxy:
    $ nd = 1.0 + 0.06 * (night - 1)
    $ bonus = 0
    scene bg cove
    with dissolve
    "The purple curtains of Pirate Cove are drawn shut. A sign hangs in front: SORRY! OUT OF ORDER."
    "I pull the curtain back."
    show foxy broken at twitch
    with dissolve

    "Foxy lunges — then stops short, yanked back by the chains bolted to his ankles."
    fo "Who goes there?! State yer business or walk the plank!"
    g "Whoa, whoa! I'm here to fix you!"
    fo "...Fix me? Nobody fixes ol' Foxy. They just close the curtain."

    menu:
        "\"I'm not closing the curtain on you.\"":
            $ trust["foxy"] += 1
            fo "...Hmph. We'll see about that, landlubber."
        "\"Calm down or I'm leaving.\"":
            fo "Aye, aye, sure. Leave like the rest of 'em."

    "One arm is just a bare rod. The hook is gone. I find it rusted into the stage boards."
    call skill_check("foxy", "ARMS", hits=1, speed=1.1 * nd, zone=58)
    play sound "audio/servo.wav"
    show foxy arms at twitch
    with flash

    "Foxy holds the hook up to the light. It glints."
    fo "Now THAT be a proper hook."

    menu:
        "\"Why'd they shut you down?\"":
            $ trust["foxy"] += 1
            fo "There was an accident. Not my fault — or maybe it was. Hard to tell when ye don't remember."
            fo "After that, they put up the sign and never took it down."
        "\"You're probably dangerous, huh?\"":
            fo "Only to them that deserve it."

    "The chains on his ankles are welded on. I'll need to cut them before I can reattach his legs."
    call skill_check("foxy", "LEGS", hits=1, speed=1.25 * nd, zone=48)
    play sound "audio/servo.wav"
    show foxy legs at twitch
    with flash

    fo "Free! Free as the open sea!"
    "He nearly sprints out of the cove before catching himself."
    fo "...Sorry, matey. Habit. One more thing, aye?"
    "The FULL REPAIR page lists Foxy's voice module: the {b}pirate voice box{/b}, or a {b}factory default{/b} voice that's much more stable."

    menu:
        "Keep the pirate voice.":
            $ bonus = 14
            $ trust["foxy"] += 1
            fo "Yarr! Ye know me well!"
        "Use the factory default.":
            fo "Hello. I am Foxy. Welcome to Pirate Cove. ...Blimey, that's awful."

    "Last step: rebuild his jaw and voice module. Foxy is fast — if this slips, he won't be able to stop himself."
    $ renpy.notify("Final check — harder than the others.")
    call skill_check("foxy", "FULL REPAIR", hits=3, speed=1.38 * nd, zone=42 + bonus, reverse=True)
    play sound "audio/chime.wav"
    show foxy fixed at repaired_glow
    with flash

    "Foxy's coat shines a deep red. His eyepatch is back where it belongs. His good eye burns gold."
    fo "Captain [guard_name]! I'd sail with ye any day."
    "He pulls the OUT OF ORDER sign off the curtain and snaps it in half."
    return
