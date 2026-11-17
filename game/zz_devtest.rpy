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


## Automated full playthrough of Chapter 3 (first choice every time).
label devtest_ch3:
    pause 0.3
    python:
        _autohit = True
        def _first(items, **kw):
            v = [v for (t, v) in items if v is not None][0]
            return getattr(v, "value", v)
        store.menu = _first
        renpy.display_menu = store.menu
        renpy.input = lambda *a, **k: "Tester"
        config.skipping = "fast"
        _preferences.skip_unseen = True
    jump chapter3_start

## Chapter 3 scenes at reading speed (auto-forward), for screenshots.
label devtest_ch3_scenes:
    pause 0.3
    python:
        def _first(items, **kw):
            v = [v for (t, v) in items if v is not None][-1]
            return getattr(v, "value", v)
        store.menu = _first
        renpy.display_menu = store.menu
        _preferences.afm_enable = True
        _preferences.afm_time = 1
        _preferences.text_cps = 0
        calm = 0
        freed = []
        guard_name = "Tester"
        st_hits = 2
        st_fails = 3
    call free_phantom("phantomfoxy")
    jump ch3_end
