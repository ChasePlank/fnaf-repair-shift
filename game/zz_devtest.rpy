## Developer test hooks. Excluded from release builds (see options.rpy).
label devtest_success:
    pause 0.5
    $ _autohit = True
    $ current_anim = "goldenfreddy"
    call skill_check("goldenfreddy", "FULL REPAIR", hits=4, speed=0.5, zone=60, reverse=True)
    $ renpy.notify("devtest passed: [_return] checks=[total_checks] perfect=[perfect_checks]")
    pause 1.0
    $ _autohit = False
    $ current_anim = "foxy"
    call skill_check("foxy", "LEGS", hits=1, speed=1.0, zone=50)
    "should not reach"

## Automated full playthrough of Chapter 2 (first choice every time).
label devtest_ch2:
    pause 0.3
    python:
        _autohit = True
        persistent.assist_mode = True
        def _first(items, **kw):
            v = [v for (t, v) in items if v is not None][0]
            return getattr(v, "value", v)
        store.menu = _first
        renpy.display_menu = store.menu
        renpy.input = lambda *a, **k: "Tester"
        config.skipping = "fast"
        _preferences.skip_unseen = True
    jump chapter2_start

