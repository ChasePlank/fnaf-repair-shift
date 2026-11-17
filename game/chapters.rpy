## =============================================================================
## Chapters
## Each FNAF game is its own chapter with the repair mechanic.
##   Chapter 1 — Freddy Fazbear's Pizza (FNAF 1). Night 5: Golden Freddy.
##   Chapter 2 — The new location (FNAF 2). Ends with the Puppet.
##   Chapter 3 — Fazbear's Fright (FNAF 3). Most animatronics are hallucinations.
## Finishing a chapter raises persistent.chapter_unlocked.
## =============================================================================

init python:
    CHAPTERS = [
        {"num": 1, "title": "Freddy Fazbear's Pizza", "sub": "The first location", "label": "start"},
        {"num": 2, "title": "The New Location", "sub": "Toys, Withereds, and the Puppet's music box", "label": "chapter2_start"},
        {"num": 3, "title": "Fazbear's Fright", "sub": "Not everything here is real", "label": "chapter3_start"},
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


label chapter3_start:
    $ reset_chapter_state(3)
    $ chapter_ease = 2 in persistent.good_endings
    scene black
    with dissolve
    show text "{size=90}{b}CHAPTER 3{/b}{/size}\n{size=40}Fazbear's Fright{/size}" at truecenter
    with dissolve
    pause 2.0
    hide text
    "Thirty years later. Fazbear's Fright: The Horror Attraction."
    "{b}Chapter 3 is still being built.{/b} The phantoms, and Springtrap, are coming next."
    return
