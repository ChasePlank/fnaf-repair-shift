## =============================================================================
## Characters, images, transforms and shared state
## To add a fan-made animatronic:
##   1. Add art: images/chars/<key>_broken.png, _arms.png, _legs.png, _fixed.png
##   2. Add an entry to ANIM below and a Character() for their dialogue
##   3. Write  label repair_<key>:  (copy routes_bonnie.rpy as a template)
##   4. Add <key> to REPAIR_ORDER so it appears in the night menu
## =============================================================================

## ---------------------------------------------------------------- speakers
define narrator = Character(None, what_italic=False)
define g = Character("[guard_name]", color="#9fc4ff")
define phone = Character("Phone Guy", color="#d9c27a", what_prefix="{i}", what_suffix="{/i}")
define fr = Character("Freddy", color="#c8874a")
define bo = Character("Bonnie", color="#8f86ff")
define ch = Character("Chica", color="#ffd23f")
define fo = Character("Foxy", color="#ff5a3c")
define gf = Character("Golden Freddy", color="#e2b84a", what_prefix="{b}", what_suffix="{/b}")
define unk = Character("???", color="#b0b0b0")
## Chapter 2
define tf = Character("Toy Freddy", color="#d89a5a")
define tb = Character("Toy Bonnie", color="#6fb6ff")
define tc = Character("Toy Chica", color="#ffe14d")
define mg = Character("Mangle", color="#ff8fc8", what_prefix="{i}", what_suffix="{/i}")
define wf = Character("Withered Freddy", color="#a8794a")
define wb = Character("Withered Bonnie", color="#8078c8")
define wc = Character("Withered Chica", color="#d8b840")
define wx = Character("Withered Foxy", color="#d8503a")
define pp = Character("The Puppet", color="#e8e8e8", what_prefix="{b}", what_suffix="{/b}")

## ---------------------------------------------------------------- data
init python:
    ANIM = {
        "freddy":   {"name": "Freddy",   "where": "Show Stage",  "bg": "stage"},
        "bonnie":   {"name": "Bonnie",   "where": "Show Stage",  "bg": "stage"},
        "chica":    {"name": "Chica",    "where": "Kitchen",     "bg": "kitchen"},
        "foxy":     {"name": "Foxy",     "where": "Pirate Cove", "bg": "cove"},
        "goldenfreddy": {"name": "Golden Freddy", "where": "Security Office", "bg": "office"},
        # Chapter 2
        "toyfreddy":      {"name": "Toy Freddy",      "where": "Show Stage",        "bg": "stage"},
        "toybonnie":      {"name": "Toy Bonnie",      "where": "Show Stage",        "bg": "stage"},
        "toychica":       {"name": "Toy Chica",       "where": "Party Room 3",      "bg": "partyroom"},
        "mangle":         {"name": "Mangle",          "where": "Kid's Cove",        "bg": "kidscove"},
        "witheredfreddy": {"name": "Withered Freddy", "where": "Parts & Service",   "bg": "parts"},
        "witheredbonnie": {"name": "Withered Bonnie", "where": "Parts & Service",   "bg": "parts"},
        "witheredchica":  {"name": "Withered Chica",  "where": "Parts & Service",   "bg": "parts"},
        "witheredfoxy":   {"name": "Withered Foxy",   "where": "Parts & Service",   "bg": "parts"},
        "puppet":         {"name": "The Puppet",      "where": "Prize Corner",      "bg": "prize",
                           "death": "You let the music stop."},
        "musicbox":       {"name": "Music Box",       "where": "Prize Corner",      "bg": "prize"},
    }
    ## The four selectable on Nights 1-4. Golden Freddy is always Night 5.
    REPAIR_ORDER = ["freddy", "bonnie", "chica", "foxy"]

## ---------------------------------------------------------------- state
default guard_name = "Mike"
default night = 0
default repaired = []          # keys of fully repaired animatronics
default trust = {k: 0 for k in ("freddy", "bonnie", "chica", "foxy", "goldenfreddy",
                                 "toyfreddy", "toybonnie", "toychica", "mangle",
                                 "witheredfreddy", "witheredbonnie", "witheredchica", "witheredfoxy", "puppet")}
default current_anim = None
default total_checks = 0
default perfect_checks = 0
default deaths_seen = set()
default _death_stage = "broken"

default persistent.assist_mode = False
default persistent.endings = set()
## Highest chapter the player has unlocked (1 = FNAF 1, 2 = FNAF 2, 3 = FNAF 3)
default persistent.chapter_unlocked = 1
default chapter = 1
## Chapters whose GOOD ending the player has earned. A good ending makes the
## NEXT chapter's skill checks easier (see chapter_ease in skillcheck.rpy).
default persistent.good_endings = set()
default chapter_ease = False

## Rollback would let players undo a failed skill check for free.
## Saves are the retry system, so rollback is turned off.
define config.rollback_enabled = False
define config.has_autosave = True
define config.autosave_on_choice = False

## ---------------------------------------------------------------- images
image bg exterior = "images/bg/exterior.png"
image bg office   = "images/bg/office.png"
image bg dining   = "images/bg/dining.png"
image bg stage    = "images/bg/stage.png"
image bg cove     = "images/bg/cove.png"
image bg kitchen  = "images/bg/kitchen.png"
image bg parts    = "images/bg/parts.png"
image bg menu     = "images/bg/menu.png"
image bg kidscove = "images/bg/kidscove.png"
image bg office2 = "images/bg/office2.png"
image bg prize = "images/bg/prize.png"
image bg partyroom = "images/bg/partyroom.png"
image black = Solid("#000")
image redflash = Solid("#b0001a")

init python:
    for _k in ("freddy", "bonnie", "chica", "foxy", "goldenfreddy",
               "toyfreddy", "toybonnie", "toychica", "mangle",
               "witheredfreddy", "witheredbonnie", "witheredchica", "witheredfoxy", "puppet", "musicbox"):
        for _s in ("broken", "arms", "legs", "fixed"):
            renpy.image((_k, _s), "images/chars/%s_%s.png" % (_k, _s))

## ---------------------------------------------------------------- transforms
transform sprite_pos(x=0.5):
    xalign x yalign 1.0 zoom 0.8

transform twitch:
    xalign 0.5 yalign 1.0 zoom 0.8
    block:
        pause 1.6
        linear 0.04 xoffset 8 rotate 1.5
        linear 0.04 xoffset -8 rotate -1.5
        linear 0.04 xoffset 0 rotate 0
        pause 2.3
        linear 0.05 yoffset 6
        linear 0.05 yoffset 0
        repeat

transform jumpscare_in:
    xanchor 0.5 xpos 0.5 yanchor 0.24 ypos 0.42 zoom 0.5 alpha 1.0
    easein 0.12 zoom 1.9
    block:
        linear 0.03 xoffset 30 yoffset -20
        linear 0.03 xoffset -30 yoffset 20
        linear 0.03 xoffset 20 yoffset 30
        linear 0.03 xoffset -20 yoffset -30
        repeat

transform flicker:
    alpha 0.0
    linear 0.05 alpha 0.6
    linear 0.05 alpha 0.0
    linear 0.04 alpha 0.4
    linear 0.15 alpha 0.0

transform repaired_glow:
    xalign 0.5 yalign 1.0 zoom 0.8 alpha 0.0
    easein 1.0 alpha 1.0

define flash = Fade(0.08, 0.0, 0.25, color="#fff")
define slowfade = Fade(1.0, 0.6, 1.0)
