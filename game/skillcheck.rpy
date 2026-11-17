## =============================================================================
## Repair skill check
## A rotating needle sweeps around a ring. Press SPACE / ENTER, click, or tap
## while the needle is inside the highlighted zone. The bright inner sliver is a
## "GREAT" hit. Missing the zone, pressing too early, or letting the needle pass
## completely is a failure.
##
## Usage from script:
##     call skill_check("Bonnie", "ARMS", hits=1, speed=1.0, zone=55)
##     # result is stored in  _return  ("great", "good" or "fail")
## =============================================================================

init -10 python:
    import math
    import random
    import pygame_sdl2 as pygame

    def _arc_poly(cx, cy, r_in, r_out, a0, a1, steps=24):
        """Polygon points for a thick arc. Angles in degrees, 0 = up, clockwise."""
        pts = []
        steps = max(2, int(steps))
        for i in range(steps + 1):
            a = math.radians(a0 + (a1 - a0) * i / steps)
            pts.append((cx + r_out * math.sin(a), cy - r_out * math.cos(a)))
        for i in range(steps, -1, -1):
            a = math.radians(a0 + (a1 - a0) * i / steps)
            pts.append((cx + r_in * math.sin(a), cy - r_in * math.cos(a)))
        return pts

    class SkillCheck(renpy.Displayable):
        SIZE = 560
        R_OUT = 230
        R_IN = 196

        def __init__(self, hits=1, speed=1.0, zone=55, great_frac=0.22, reverse_alternate=False, **kw):
            super(SkillCheck, self).__init__(**kw)
            ease = 0.75 if persistent.assist_mode else 1.0
            zone_mult = 1.35 if persistent.assist_mode else 1.0
            # Reward for the previous chapter's good ending
            if getattr(store, "chapter_ease", False):
                ease *= 0.88
                zone += 8
            self.hits_needed = hits
            self.hits = 0
            self.greats = 0
            self.base_speed = 220.0 * speed * ease      # degrees per second
            self.zone_w = max(12.0, zone * zone_mult)   # degrees
            self.great_frac = great_frac
            self.reverse_alternate = reverse_alternate
            self.state = "wait"       # wait -> run -> (flash) -> run ... -> done
            self.t0 = None
            self.st = 0.0
            self.flash = None         # (kind, until_st)
            self.result = None
            self._new_round(0.0)

        # --- round setup -----------------------------------------------------
        def _new_round(self, st):
            r = self.hits
            self.speed = self.base_speed * (1.0 + 0.10 * r)
            self.width = max(10.0, self.zone_w * (1.0 - 0.08 * r))
            self.direction = -1 if (self.reverse_alternate and r % 2 == 1) else 1
            # zone placed somewhere between 110 and 300 degrees of travel
            self.zone_start = random.uniform(110.0, 300.0 - self.width)
            self.round_start = st + (0.9 if r == 0 else 0.45)
            self.state = "wait"

        def _progress(self, st):
            return max(0.0, (st - self.round_start) * self.speed)

        # --- drawing ---------------------------------------------------------
        def render(self, width, height, st, at):
            self.st = st
            S = self.SIZE
            rv = renpy.Render(S, S)
            c = rv.canvas()
            cx = cy = S / 2.0

            if self.state == "wait" and st >= self.round_start:
                self.state = "run"

            prog = self._progress(st) if self.state == "run" else 0.0
            # developer-only auto player used by automated tests
            if self.state == "run" and config.developer and getattr(store, "_autohit", False):
                if prog >= self.zone_start + 0.5:
                    self._press(self.round_start + (self.zone_start + 1.0) / self.speed)
                    prog = self._frozen
            if self.state == "run" and prog > self.zone_start + self.width + 2:
                self._finish("fail")

            d = self.direction
            def ang(p):
                return p * d

            # ring background
            c.polygon((40, 40, 46, 255), _arc_poly(cx, cy, self.R_IN, self.R_OUT, 0, 360, 90))
            # zone
            zs, ze = ang(self.zone_start), ang(self.zone_start + self.width)
            c.polygon((205, 205, 210, 255), _arc_poly(cx, cy, self.R_IN - 4, self.R_OUT + 4, min(zs, ze), max(zs, ze), 30))
            gw = self.width * self.great_frac
            gs, ge = ang(self.zone_start), ang(self.zone_start + gw)
            c.polygon((200, 16, 46, 255), _arc_poly(cx, cy, self.R_IN - 8, self.R_OUT + 8, min(gs, ge), max(gs, ge), 10))

            # hit pips
            for i in range(self.hits_needed):
                col = (200, 16, 46, 255) if i < self.hits else (70, 70, 76, 255)
                px = cx - (self.hits_needed - 1) * 22 + i * 44
                c.circle(col, (int(px), int(cy + 70)), 12)

            # needle
            if self.state in ("run", "flash", "done"):
                a = math.radians(ang(prog if self.state == "run" else self._frozen))
                x1 = cx + (self.R_IN - 34) * math.sin(a)
                y1 = cy - (self.R_IN - 34) * math.cos(a)
                x2 = cx + (self.R_OUT + 22) * math.sin(a)
                y2 = cy - (self.R_OUT + 22) * math.cos(a)
                c.line((255, 70, 40, 255), (x1, y1), (x2, y2), 9)

            # center text
            if self.flash and st < self.flash[1]:
                kind = self.flash[0]
                txt, col = {"great": ("GREAT", "#ff2a4f"), "good": ("GOOD", "#e6e6e6"), "fail": ("MISS", "#ff3b3b")}[kind]
                t = renpy.render(Text(txt, size=64, bold=True, color=col, outlines=[(3, "#000", 0, 0)]), S, S, st, at)
                rv.blit(t, (cx - t.width / 2, cy - t.height / 2 - 10))
            elif self.state == "wait":
                blink = int(st * 6) % 2 == 0
                t = renpy.render(Text("!" if blink else "", size=110, bold=True, color="#ff2a4f"), S, S, st, at)
                rv.blit(t, (cx - t.width / 2, cy - t.height / 2 - 14))

            if self.flash and st >= self.flash[1]:
                kind = self.flash[0]
                self.flash = None
                if self.state == "done":
                    renpy.timeout(0)
                elif kind != "fail":
                    self._new_round(st)

            renpy.redraw(self, 0)
            return rv

        # --- input -----------------------------------------------------------
        def _press(self, st):
            if self.state == "wait":
                # pressing before the needle moves counts as a miss (prevents mashing)
                self._frozen = 0.0
                self._finish("fail")
                return
            if self.state != "run":
                return
            prog = self._progress(st)
            self._frozen = prog
            if self.zone_start <= prog <= self.zone_start + self.width * self.great_frac:
                kind = "great"
            elif self.zone_start <= prog <= self.zone_start + self.width:
                kind = "good"
            else:
                self._finish("fail")
                return
            self.hits += 1
            if kind == "great":
                self.greats += 1
                renpy.sound.play("audio/check_great.wav", channel="audio")
            else:
                renpy.sound.play("audio/check_good.wav", channel="audio")
            if self.hits >= self.hits_needed:
                self.result = "great" if self.greats == self.hits_needed else "good"
                self.state = "done"
            else:
                self.state = "flash"
            self.flash = (kind, st + 0.45)

        def _finish(self, kind):
            if not hasattr(self, "_frozen"):
                self._frozen = self._progress(self.st)
            self.result = "fail"
            self.state = "done"
            self.flash = ("fail", self.st + 0.5)

        def event(self, ev, x, y, st):
            if self.state == "done":
                if self.flash is None:
                    return self.result
                raise renpy.IgnoreEvent()
            pressed = False
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
                pressed = True
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                pressed = True
            if pressed:
                self._press(st)
                raise renpy.IgnoreEvent()
            return None

        def visit(self):
            return []


screen skill_check(who, part, hits=1, speed=1.0, zone=55, reverse=False, title=None):
    modal True
    zorder 200
    ## Block menus / skipping during a check so it can't be paused or cheesed.
    key "game_menu" action NullAction()
    key "hide_windows" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()

    add Solid("#000000a8")

    vbox:
        align (0.5, 0.5)
        spacing 18
        text (title or ("REPAIR: %s — %s" % (who.upper(), part.upper()))):
            xalign 0.5 size 40 bold True color "#e8e8e8" outlines [(2, "#000", 0, 0)]
        if hits > 1:
            text "Hit the zone [hits] times in a row":
                xalign 0.5 size 26 color "#ff5a6e"
        add SkillCheck(hits=hits, speed=speed, zone=zone, reverse_alternate=reverse):
            xalign 0.5
        text ("TAP when the needle hits the white zone" if renpy.variant("touch") else "Press SPACE / ENTER or CLICK when the needle hits the white zone"):
            xalign 0.5 size 24 color "#9a9aa2"


## The label the story calls. Handles sound, result bookkeeping, and death.
label skill_check(who_key, part, hits=1, speed=1.0, zone=55, reverse=False):
    $ _skip_was = config.allow_skipping
    $ config.allow_skipping = False
    $ renpy.block_rollback()
    $ _death_stage = {"ARMS": "broken", "LEGS": "arms"}.get(part, "legs")
    play sound "audio/check_alert.wav"
    $ _sc = renpy.call_screen("skill_check", who=ANIM[who_key]["name"], part=part, hits=hits, speed=speed, zone=zone, reverse=reverse)
    $ config.allow_skipping = _skip_was
    if config.developer and getattr(store, "_autohit", False):
        $ open("/tmp/devlog.txt", "a").write("%s %s %s night=%s\n" % (who_key, part, _sc, night))
        $ config.skipping = "fast"
    if _sc == "fail":
        $ renpy.pop_call()
        jump game_over
    $ total_checks += 1
    if _sc == "great":
        $ perfect_checks += 1
    return _sc
