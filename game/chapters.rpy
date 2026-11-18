## =============================================================================
## Chapters
## Each FNAF game is its own chapter with the repair mechanic.
##   Chapter 1 — Freddy Fazbear's Pizza (FNAF 1). Night 5: Golden Freddy.
##   Chapter 2 — The new location (FNAF 2). Ends with the Puppet.
##   Chapter 3 — Fazbear's Fright (FNAF 3). Phantoms, then Springtrap. Sends you to Ch4.
##   Chapter 4 — The Nightmare (FNAF 4). Real time. Wake up in the elevator.
##   Chapter 5 — Sister Location. Coming next.
## Finishing a chapter raises persistent.chapter_unlocked.
## =============================================================================

init python:
    CHAPTERS = [
        {"num": 1, "title": "Freddy Fazbear's Pizza", "sub": "The first location", "label": "start"},
        {"num": 2, "title": "The New Location", "sub": "Toys, Withereds, and the Puppet's music box", "label": "chapter2_start"},
        {"num": 3, "title": "Fazbear's Fright", "sub": "Free the phantoms, then face Springtrap", "label": "chapter3_start"},
        {"num": 4, "title": "The Nightmare", "sub": "Five nights. Survive until 6 AM", "label": "chapter4_start"},
        {"num": 5, "title": "Sister Location", "sub": "After Ennard", "label": "chapter5_start"},
    ]

    def reset_chapter_state(num):
        store.chapter = num
        store.night = 0
        store.repaired = []
        store.current_anim = None
        store.total_checks = 0
        store.perfect_checks = 0
        store.trust = {k: 0 for k in store.trust}


screen chapter_select():
    tag menu
    use game_menu(_("Chapters")):
        vbox:
            spacing 26
            for c in CHAPTERS:
                $ unlocked = c["num"] <= persistent.chapter_unlocked
                button:
                    xsize 1100
                    padding (30, 20)
                    background ("#1a1012" if unlocked else "#0d0d0f")
                    hover_background "#3a1018"
                    action (Start(c["label"]) if unlocked else NullAction())
                    sensitive unlocked
                    vbox:
                        spacing 4
                        text ("CHAPTER %d — %s" % (c["num"], c["title"])) size 40 bold True color ("#eeeeee" if unlocked else "#555")
                        text (c["sub"] if unlocked else "Locked — finish the previous chapter") size 26 color ("#c8102e" if unlocked else "#444")


## Chapter 5 — Sister Location. Coming next.
label chapter5_start:
    $ reset_chapter_state(5)
    $ chapter_ease = 4 in persistent.good_endings
    scene black
    with dissolve
    show text "{size=90}{b}CHAPTER 5{/b}{/size}\n{size=40}Sister Location{/size}" at truecenter
    with dissolve
    pause 2.0
    hide text
    scene bg elevator
    with slowfade
    "The elevator doors open onto a dark, empty facility. Nobody here. Nobody at all."
    "{b}Chapter 5 is still being built.{/b} Circus Baby is coming next."
    return
