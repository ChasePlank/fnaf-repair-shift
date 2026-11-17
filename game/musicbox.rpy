## =============================================================================
## Music box winding (Chapter 2 — Puppet finale)
## HOLD Space / Enter, the mouse button, or your finger to wind the box.
## The meter drains constantly. Keep it above zero until the timer runs out.
## As the meter drops, the Puppet gets closer. Empty = death.
##
##     call wind_music_box(duration=10, drain=0.10)
## =============================================================================

init -10 python:
    class WindBox(renpy.Displayable):
        W, H = 900, 640

        def __init__(self, duration=10.0, drain=0.10, fill=0.32, **kw):
            super(WindBox, self).__init__(**kw)
            if persistent.assist_mode:
                drain *= 0.7
            if getattr(store, "chapter_ease", False):
                drain *= 0.85
            self.duration = duration
            self.drain = drain
            self.fill = fill
            self.meter = 0.75
            self.holding = False
            self.last_st = None
            self.done = None
            self.puppet = renpy.displayable("puppet fixed")

        def render(self, width, height, st, at):
            dt = 0.0 if self.last_st is None else max(0.0, min(0.1, st - self.last_st))
            self.last_st = st
            if self.done is None and config.developer and getattr(store, "_autohit", False):
                self.holding = self.meter < 0.8
            if self.done is None:
                # wind speeds up slightly over time so it gets tense
                rate = self.drain * (1.0 + 0.6 * st / self.duration)
                self.meter += (self.fill if self.holding else 0.0) * dt - rate * dt
                self.meter = min(1.0, self.meter)
                if self.meter <= 0:
                    self.meter = 0.0
                    self.done = "fail"
                    renpy.timeout(0)
                elif st >= self.duration:
                    self.done = "ok"
                    renpy.timeout(0)

            rv = renpy.Render(self.W, self.H)

            # Puppet creeping in: gets bigger and more opaque as the meter falls
            danger = 1.0 - self.meter
            if danger > 0.25:
                t = Transform(self.puppet, alpha=min(1.0, (danger - 0.25) * 1.6), zoom=0.35 + danger * 0.35)
                pr = renpy.render(t, self.W, self.H, st, at)
                rv.blit(pr, (self.W / 2 - pr.width / 2, 0))

            # meter
            c = rv.canvas()
            bx, by, bw, bh = 150, 470, 600, 46
            c.rect((30, 30, 36, 255), (bx, by, bw, bh))
            col = (90, 200, 120, 255) if self.meter > 0.5 else ((230, 180, 50, 255) if self.meter > 0.25 else (220, 30, 50, 255))
            c.rect(col, (bx + 4, by + 4, int((bw - 8) * self.meter), bh - 8))

            remaining = max(0.0, self.duration - st)
            label = "WINDING..." if self.holding else ("HOLD TO WIND" if self.meter > 0.25 else "WIND IT! NOW!")
            for txt, size, y, color in ((label, 44, 540, "#ffffff"), ("%.1f" % remaining, 34, 410, "#bbbbbb")):
                tr = renpy.render(Text(txt, size=size, bold=True, color=color, outlines=[(2, "#000", 0, 0)]), self.W, self.H, st, at)
                rv.blit(tr, (self.W / 2 - tr.width / 2, y))

            renpy.redraw(self, 0)
            return rv

        def event(self, ev, x, y, st):
            if self.done is not None:
                return self.done
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
                self.holding = True
                raise renpy.IgnoreEvent()
            if ev.type == pygame.KEYUP and ev.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
                self.holding = False
                raise renpy.IgnoreEvent()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.holding = True
                raise renpy.IgnoreEvent()
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.holding = False
                raise renpy.IgnoreEvent()
            return None

        def visit(self):
            return [self.puppet]


screen wind_music_box_screen(duration, drain):
    modal True
    zorder 200
    key "game_menu" action NullAction()
    key "hide_windows" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    add Solid("#000000c0")
    vbox:
        align (0.5, 0.5)
        spacing 10
        text "KEEP THE MUSIC BOX WOUND" xalign 0.5 size 40 bold True color "#e8d8ff" outlines [(2, "#000", 0, 0)]
        add WindBox(duration=duration, drain=drain):
            xalign 0.5


label wind_music_box(duration=10.0, drain=0.10):
    $ _skip_was = config.allow_skipping
    $ config.allow_skipping = False
    $ renpy.block_rollback()
    play music "audio/musicbox.wav" volume 0.7
    $ _wind = renpy.call_screen("wind_music_box_screen", duration=duration, drain=drain)
    $ config.allow_skipping = _skip_was
    if config.developer and getattr(store, "_autohit", False):
        $ open("/tmp/devlog.txt", "a").write("wind %s\n" % _wind)
        $ config.skipping = "fast"
    if _wind == "fail":
        $ current_anim = "puppet"
        $ _death_stage = "fixed"
        $ renpy.pop_call()
        jump game_over
    return
