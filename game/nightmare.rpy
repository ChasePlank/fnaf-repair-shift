## =============================================================================
## Chapter 4 — The Nightmare (real-time, FNAF 4 style)
## Each night lasts 5 real minutes (12 AM to 6 AM, 50 seconds an hour).
##
## The bedroom has four places to watch:
##   LEFT DOOR / RIGHT DOOR  Nightmare Bonnie (left) and Nightmare Chica (right).
##       Far down the hall: shine the light on them and they back off.
##       Right outside the door: you'll HEAR BREATHING. Do NOT use the light.
##       Hold the door shut until they walk away. Ignore them and they come in.
##   CLOSET                  Nightmare Foxy. He creeps in, step by step.
##       Hold the closet shut to push him back. Shine the light on him when
##       he's all the way in, and he attacks.
##   BED                     Nightmare Freddy. Little Freddles pile up on the
##       bed. Shine the light on them to make them go away. Let three of them
##       sit there too long and Freddy comes for you.
##   Night 5: Fredbear joins. He giggles, then shows up at one of the four
##       spots. Deal with him the same way you deal with that spot.
##
## Keyboard: A / D = left / right door, W = closet, S = bed (or back),
##           F or Shift = hold flashlight, Space = hold door / closet.
## Mouse / touch: tap the door, closet or bed, then hold the on-screen
##           LIGHT or HOLD DOOR buttons. BACK returns to the middle of the room.
##
## The nightmares never talk. They're in your head, and they want you dead.
## =============================================================================

init -5 python:
    import random as _nrand
    import pygame_sdl2 as pygame

    renpy.music.register_channel("breath", mixer="sfx", loop=True)
    renpy.music.register_channel("nmsfx", mixer="sfx", loop=False)

    ## Difficulty per night: AI level 0-10 for each nightmare.
    NIGHTMARE_LEVELS = {
        1: dict(bonnie=2, chica=2, foxy=0, freddy=1, fredbear=0),
        2: dict(bonnie=4, chica=3, foxy=3, freddy=2, fredbear=0),
        3: dict(bonnie=5, chica=5, foxy=5, freddy=4, fredbear=0),
        4: dict(bonnie=7, chica=7, foxy=6, freddy=5, fredbear=0),
        5: dict(bonnie=6, chica=6, foxy=5, freddy=4, fredbear=7),
    }
    NIGHT_SECONDS = 300.0

    def _rect_hit(r, x, y):
        return r[0] <= x <= r[2] and r[1] <= y <= r[3]

    class NightmareNight(renpy.Displayable):
        W, H = 1920, 1080
        R_LEFT = (140, 180, 520, 820)
        R_CLOSET = (820, 160, 1100, 820)
        R_RIGHT = (1400, 180, 1780, 820)
        R_BED = (600, 740, 1320, 920)
        B_BACK = (760, 960, 1160, 1060)
        B_LIGHT = (1540, 860, 1890, 1050)
        B_DOOR = (30, 860, 380, 1050)

        def __init__(self, night=1, **kw):
            super(NightmareNight, self).__init__(**kw)
            self.night = night
            L = NIGHTMARE_LEVELS[night]
            self.L = dict(L)
            ## Assist Mode and the Chapter 3 good ending give more time to react.
            self.slack = 1.0
            if persistent.assist_mode:
                self.slack *= 1.45
            if getattr(store, "chapter_ease", False):
                self.slack *= 1.15
            self.length = float(getattr(store, "_night_len", NIGHT_SECONDS))
            self.t = 0.0
            self.last_st = None
            self.view = "room"
            self.moving = 0.0       # short black "turning" delay between views
            self.light = False
            self.hold = False
            self.mouse_light = False
            self.mouse_hold = False
            self.result = None
            self.dead_by = None
            self.dead_at = None
            ## door nightmares: stage 0 away, 1 far down the hall, 2 right outside
            self.door = {"left": dict(who="bonnie", stage=0, tick=0.0, timer=0.0, acc=0.0, lit=0.0),
                         "right": dict(who="chica", stage=0, tick=0.0, timer=0.0, acc=0.0, lit=0.0)}
            self.foxy = dict(stage=0, tick=0.0, timer=0.0, acc=0.0)
            self.freddles = 0
            self.fred_tick = 0.0
            self.fred_timer = 0.0
            self.fred_clear = 0.0
            self.bear = dict(spot=None, wait=14.0, timer=0.0, acc=0.0)
            self.caption = None
            self.caption_until = 0.0
            self.breath_on = False
            img = lambda p: renpy.displayable(p)
            self.bg_room = img("bg bedroom")
            self.bg_hall = img("images/bg/n4_hall.png")
            self.bg_hall_r = Transform(img("images/bg/n4_hall.png"), xzoom=-1.0)
            self.bg_door = img("images/bg/n4_door_closed.png")
            self.bg_closet = img("images/bg/n4_closet.png")
            self.bg_closet_shut = img("images/bg/n4_closet_closed.png")
            self.bg_bed = img("images/bg/n4_bed.png")
            self.spr = {k: img("nightmare%s broken" % k) for k in ("bonnie", "chica", "foxy", "freddy")}
            self.spr["fredbear"] = img("fredbear broken")
            self.dark = Solid("#000000ec")
            self.dim = Solid("#00000070")
            self.black = Solid("#000")

        # ------------------------------------------------------------- helpers
        def _cap(self, text, secs=2.0):
            ## Sound captions only appear in Assist Mode. The real cues are audio.
            if persistent.assist_mode:
                self.caption = text
                self.caption_until = self.t + secs

        def _sfx(self, f, vol=1.0):
            renpy.music.play(f, channel="nmsfx", relative_volume=vol)

        def _kill(self, who):
            if self.dead_by is None:
                self.dead_by = who
                self.dead_at = self.t
                renpy.music.stop(channel="breath")

        def _move_roll(self, level):
            return level > 0 and _nrand.randint(1, 10) <= level

        def _light_on(self):
            return (self.light or self.mouse_light) and not self._hold_on() and self.moving <= 0

        def _hold_on(self):
            return (self.hold or self.mouse_hold) and self.view in ("left", "right", "closet") and self.moving <= 0

        def _goto(self, v):
            if v != self.view:
                self.view = v
                self.moving = 0.28
                self.mouse_light = self.mouse_hold = False

        # ---------------------------------------------------------- simulation
        def _update(self, dt):
            self.t += dt
            if self.moving > 0:
                self.moving -= dt
            if config.developer and getattr(store, "_autohit", False):
                self._bot()
            light, hold = self._light_on(), self._hold_on()

            # ---- doors (Bonnie left, Chica right)
            breathing = False
            for side, d in self.door.items():
                lvl = self.L[d["who"]]
                here = self.view == side
                d["tick"] += dt
                if d["stage"] < 2 and d["tick"] >= 4.6:
                    d["tick"] = 0.0
                    if self._move_roll(lvl) and not (here and hold):
                        d["stage"] += 1
                        d["timer"] = 0.0
                        d["acc"] = 0.0
                        if d["stage"] == 2:
                            self._sfx("audio/footsteps.wav", 0.5)
                if d["stage"] == 1:
                    d["lit"] = d["lit"] + dt if (here and light) else 0.0
                    if d["lit"] >= 0.35:
                        d["stage"] = 0
                        d["lit"] = 0.0
                        self._sfx("audio/footsteps.wav", 0.7)
                        self._cap("(footsteps running away)")
                elif d["stage"] == 2:
                    d["timer"] += dt
                    if here and not hold:
                        breathing = True
                        self._cap("(breathing... right outside the door)", 0.3)
                    if here and light:
                        self._kill(d["who"])
                    if here and hold:
                        d["acc"] += dt
                        if d["acc"] >= 2.2:
                            d["stage"] = 0
                            d["tick"] = 0.0
                            self._sfx("audio/footsteps.wav", 0.7)
                            self._cap("(footsteps fading away)")
                    elif d["timer"] >= (9.0 - lvl * 0.35) * self.slack:
                        self._kill(d["who"])

            # ---- closet (Foxy)
            f = self.foxy
            f["tick"] += dt
            here = self.view == "closet"
            if here and hold and f["stage"] > 0:
                f["acc"] += dt
                if f["acc"] >= 1.6:
                    f["acc"] = 0.0
                    f["stage"] -= 1
                    f["timer"] = 0.0
            if f["stage"] < 3 and f["tick"] >= 5.2:
                f["tick"] = 0.0
                if self._move_roll(self.L["foxy"]) and not (here and hold):
                    f["stage"] += 1
                    f["timer"] = 0.0
                    self._sfx("audio/servo.wav", 0.25)
                    self._cap("(something creaks in the closet)")
            if f["stage"] == 3:
                f["timer"] += dt
                if here and light:
                    self._kill("foxy")
                elif f["timer"] >= 8.0 * self.slack and not (here and hold):
                    self._kill("foxy")

            # ---- bed (Freddy and the Freddles)
            self.fred_tick += dt
            if self.fred_tick >= 6.0:
                self.fred_tick = 0.0
                if self.freddles < 3 and self._move_roll(self.L["freddy"]):
                    self.freddles += 1
                    self._sfx("audio/giggle.wav", 0.35)
                    self._cap("(tiny giggles from the bed)")
            if self.view == "bed" and light and self.freddles > 0:
                self.fred_clear += dt
                if self.fred_clear >= 0.7:
                    self.fred_clear = 0.0
                    self.freddles -= 1
            else:
                self.fred_clear = 0.0
            if self.freddles >= 3:
                self.fred_timer += dt
                if self.fred_timer >= 9.0 * self.slack:
                    self._kill("freddy")
            else:
                self.fred_timer = 0.0

            # ---- Fredbear (night 5)
            b = self.bear
            if self.L["fredbear"]:
                if b["spot"] is None:
                    b["wait"] -= dt
                    if b["wait"] <= 0:
                        b["spot"] = _nrand.choice(["left", "right", "closet", "bed"])
                        b["timer"] = 0.0
                        b["acc"] = 0.0
                        self._sfx("audio/giggle.wav", 0.9)
                        self._cap("(a deep, slow giggle)")
                else:
                    s = b["spot"]
                    here = self.view == s
                    b["timer"] += dt
                    if s in ("left", "right"):
                        if here and not hold:
                            breathing = True
                            self._cap("(heavy breathing outside the door)", 0.3)
                        if here and light:
                            self._kill("fredbear")
                        ok = here and hold
                    elif s == "closet":
                        ok = here and hold
                    else:
                        ok = here and light
                    if ok:
                        b["acc"] += dt
                        if b["acc"] >= 2.4:
                            b["spot"] = None
                            b["wait"] = _nrand.uniform(10.0, 18.0) - self.L["fredbear"] * 0.4
                            self._sfx("audio/footsteps.wav", 0.6)
                    elif b["timer"] >= 9.5 * self.slack:
                        self._kill("fredbear")

            if breathing != self.breath_on:
                self.breath_on = breathing
                if breathing:
                    renpy.music.play("audio/breathing.wav", channel="breath", fadein=0.2)
                else:
                    renpy.music.stop(channel="breath", fadeout=0.2)

            if self.dead_by and self.t - self.dead_at >= 0.05:
                self.result = "dead:" + self.dead_by
            elif self.t >= self.length:
                renpy.music.stop(channel="breath")
                self.result = "win"

        ## Developer-only autoplayer for automated tests. Plays the way the
        ## rules say to play. Never active in release builds.
        def _bot(self):
            self.light = self.hold = False
            want = None
            for side, d in self.door.items():
                if d["stage"] == 2 or self.bear["spot"] == side:
                    want = (side, "hold")
            if want is None and (self.foxy["stage"] >= 2 or self.bear["spot"] == "closet"):
                want = ("closet", "hold")
            if want is None and (self.freddles >= 2 or self.bear["spot"] == "bed"):
                want = ("bed", "light")
            if want is None:
                for side, d in self.door.items():
                    if d["stage"] == 1:
                        want = (side, "light")
            if want is None:
                self._goto("room")
                return
            self._goto(want[0])
            if want[1] == "hold":
                self.hold = True
            else:
                self.light = True

        # -------------------------------------------------------------- render
        def _btn(self, rv, r, label, active, st, at):
            w, h = r[2] - r[0], r[3] - r[1]
            rv.blit(renpy.render(Solid("#c8102e" if active else "#1a1012d8"), w, h, st, at), (r[0], r[1]))
            t = renpy.render(Text(label, size=34, bold=True, color="#ffffff" if active else "#bbbbbb"), w, h, st, at)
            rv.blit(t, (r[0] + (w - t.width) / 2, r[1] + (h - t.height) / 2))

        def _full(self, rv, d, st, at, pos=(0, 0)):
            rv.blit(renpy.render(d, self.W, self.H, st, at), pos)

        def _sprite(self, rv, key, zoom, x, ybottom, st, at, alpha=1.0):
            d = Transform(self.spr[key], zoom=zoom, alpha=alpha)
            r = renpy.render(d, self.W, self.H, st, at)
            rv.blit(r, (int(x - r.width / 2), int(ybottom - r.height)))

        def render(self, width, height, st, at):
            dt = 0.0 if self.last_st is None else max(0.0, min(0.1, st - self.last_st))
            self.last_st = st
            if self.result is None:
                self._update(dt)
            rv = renpy.Render(self.W, self.H)
            light, hold = self._light_on(), self._hold_on()

            if self.moving > 0:
                self._full(rv, self.black, st, at)
            elif self.view == "room":
                self._full(rv, self.bg_room, st, at)
                self._full(rv, self.dim, st, at)
                for r, lab in ((self.R_LEFT, "LEFT DOOR"), (self.R_CLOSET, "CLOSET"), (self.R_RIGHT, "RIGHT DOOR"), (self.R_BED, "BED")):
                    t = renpy.render(Text(lab, size=26, color="#ffffff55"), 400, 60, st, at)
                    rv.blit(t, ((r[0] + r[2]) / 2 - t.width / 2, r[1] + 16))
            elif self.view in ("left", "right"):
                d = self.door[self.view]
                if hold:
                    self._full(rv, self.bg_door, st, at)
                else:
                    self._full(rv, self.bg_hall if self.view == "left" else self.bg_hall_r, st, at)
                    if light:
                        if d["stage"] == 1:
                            self._sprite(rv, d["who"], 0.32, 960, 760, st, at)
                        if d["stage"] == 2 or self.bear["spot"] == self.view:
                            self._sprite(rv, "fredbear" if self.bear["spot"] == self.view else d["who"], 1.0, 960, 1180, st, at)
                    else:
                        self._full(rv, self.dark, st, at)
            elif self.view == "closet":
                if hold:
                    self._full(rv, self.bg_closet_shut, st, at)
                else:
                    self._full(rv, self.bg_closet, st, at)
                    if light:
                        s = self.foxy["stage"]
                        if self.bear["spot"] == "closet":
                            self._sprite(rv, "fredbear", 0.8, 960, 1000, st, at)
                        elif s == 1:
                            self._sprite(rv, "foxy", 0.22, 960, 900, st, at, 0.9)
                        elif s == 2:
                            self._sprite(rv, "foxy", 0.5, 960, 1000, st, at, 0.6)
                        elif s == 3:
                            self._sprite(rv, "foxy", 0.85, 960, 1060, st, at)
                    else:
                        self._full(rv, self.dark, st, at)
            elif self.view == "bed":
                self._full(rv, self.bg_bed, st, at)
                if light:
                    if self.bear["spot"] == "bed":
                        self._sprite(rv, "fredbear", 0.7, 960, 900, st, at)
                    for i in range(self.freddles):
                        self._sprite(rv, "freddy", 0.16, 640 + i * 320, 780 + (i % 2) * 30, st, at)
                else:
                    self._full(rv, self.dark, st, at)

            # ---- HUD: clock, night, buttons
            hour = int(self.t / (self.length / 6.0))
            clock = "12 AM" if hour == 0 else "%d AM" % min(hour, 6)
            t = renpy.render(Text("%s\nNight %d" % (clock, self.night), size=40, bold=True, color="#dddddd", text_align=1.0,
                                  outlines=[(2, "#000", 0, 0)]), 400, 200, st, at)
            rv.blit(t, (self.W - t.width - 40, 30))
            if self.caption and self.t < self.caption_until:
                t = renpy.render(Text(self.caption, size=30, italic=True, color="#cfcfcf", outlines=[(2, "#000", 0, 0)]), 1400, 80, st, at)
                rv.blit(t, (self.W / 2 - t.width / 2, 780))
            if self.view != "room":
                self._btn(rv, self.B_BACK, "BACK", False, st, at)
                self._btn(rv, self.B_LIGHT, "HOLD: LIGHT", light, st, at)
                if self.view in ("left", "right", "closet"):
                    self._btn(rv, self.B_DOOR, "HOLD: DOOR" if self.view != "closet" else "HOLD: CLOSET", hold, st, at)

            if self.result is not None:
                renpy.timeout(0)
            renpy.redraw(self, 0)
            return rv

        # --------------------------------------------------------------- input
        def event(self, ev, x, y, st):
            if self.result is not None:
                return self.result
            if ev.type == pygame.KEYDOWN or ev.type == pygame.KEYUP:
                down = ev.type == pygame.KEYDOWN
                k = ev.key
                if k in (pygame.K_f, pygame.K_LSHIFT, pygame.K_RSHIFT):
                    self.light = down
                elif k == pygame.K_SPACE:
                    self.hold = down
                elif down and k in (pygame.K_a, pygame.K_LEFT):
                    self._goto("left" if self.view == "room" else "room")
                elif down and k in (pygame.K_d, pygame.K_RIGHT):
                    self._goto("right" if self.view == "room" else "room")
                elif down and k in (pygame.K_w, pygame.K_UP):
                    self._goto("closet" if self.view == "room" else "room")
                elif down and k in (pygame.K_s, pygame.K_DOWN, pygame.K_BACKSPACE):
                    self._goto("bed" if self.view == "room" else "room")
                raise renpy.IgnoreEvent()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if self.view == "room":
                    for r, v in ((self.R_LEFT, "left"), (self.R_CLOSET, "closet"), (self.R_RIGHT, "right"), (self.R_BED, "bed")):
                        if _rect_hit(r, x, y):
                            self._goto(v)
                            break
                else:
                    if _rect_hit(self.B_BACK, x, y):
                        self._goto("room")
                    elif _rect_hit(self.B_LIGHT, x, y):
                        self.mouse_light = True
                    elif _rect_hit(self.B_DOOR, x, y) and self.view != "bed":
                        self.mouse_hold = True
                raise renpy.IgnoreEvent()
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.mouse_light = self.mouse_hold = False
                raise renpy.IgnoreEvent()
            return None

        def visit(self):
            return []


screen nightmare_night(night):
    modal True
    ## No pausing mid-night. Save between nights.
    key "game_menu" action NullAction()
    key "hide_windows" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    key "dismiss" action NullAction()
    add NightmareNight(night=night)


## Shown once, before Night 1, so players know this chapter plays differently.
screen nightmare_intro():
    modal True
    add Solid("#000000f4")
    vbox:
        align (0.5, 0.45)
        spacing 26
        xmaximum 1500
        text "THIS CHAPTER IS DIFFERENT" size 70 bold True color "#c8102e" xalign 0.5
        text "Chapter 4 is not a visual novel. There's no dialogue and there are no choices." size 34 color "#eeeeee" xalign 0.5 text_align 0.5
        text "It's a {b}real-time survival{/b} section, played like FNAF 4." size 34 color "#eeeeee" xalign 0.5 text_align 0.5
        null height 6
        text "• Each night lasts {b}5 real minutes{/b}, from 12 AM to 6 AM." size 32 color "#dddddd"
        text "• The clock doesn't stop. Things can come for you {b}at any moment{/b}." size 32 color "#dddddd"
        text "• You can't pause or save during a night. Saves happen between nights." size 32 color "#dddddd"
        text "• If you die, you can {b}retry the night{/b} right away, from 12 AM." size 32 color "#dddddd"
        text "• Survive all 5 nights to wake up." size 32 color "#dddddd"
        null height 6
        text "Sound matters. Headphones help. Turn on Assist Mode in Preferences if you want captions and more time to react." size 28 color "#9a9aa2" xalign 0.5 text_align 0.5
        null height 16
        textbutton "Show me how to survive" action Return() xalign 0.5 text_size 46


screen nightmare_controls():
    modal True
    add Solid("#000000f0")
    vbox:
        align (0.5, 0.45)
        spacing 18
        xmaximum 1500
        text "HOW TO SURVIVE" size 64 bold True color "#c8102e" xalign 0.5
        null height 10
        text "{b}Doors (left and right):{/b} Shine the light down the hall to scare off anything far away. If you hear {b}breathing{/b}, it's right outside. Do NOT use the light. Hold the door shut until it leaves." size 30 color "#dddddd"
        text "{b}Closet:{/b} Something creeps in a little at a time. Hold the closet shut to push it back. Never shine the light on it once it's all the way in." size 30 color "#dddddd"
        text "{b}Bed:{/b} Little things pile up on your bed. Shine the light on them to make them go away." size 30 color "#dddddd"
        text "Survive 5 minutes, from 12 AM to 6 AM." size 30 color "#dddddd"
        null height 10
        if renpy.variant("touch"):
            text "Tap a door, the closet, or the bed to go there. Hold LIGHT or HOLD DOOR. Tap BACK to return." size 28 color "#9a9aa2"
        else:
            text "A / D: doors · W: closet · S: bed / back · F or Shift: light · Space: hold door. Or click and hold the on-screen buttons." size 28 color "#9a9aa2"
        text "Play with sound on. Turn on Assist Mode (Preferences) for sound captions and more reaction time." size 28 color "#9a9aa2"
        null height 20
        textbutton "I'm ready" action Return() xalign 0.5 text_size 48
