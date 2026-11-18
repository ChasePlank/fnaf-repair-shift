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

## Chapter 4: a rule-following bot plays all 5 nights (shortened).
label devtest_ch4:
    pause 0.3
    python:
        _autohit = True
        _night_len = 40.0
        def _first(items, **kw):
            v = [v for (t, v) in items if v is not None][0]
            return getattr(v, "value", v)
        store.menu = _first
        renpy.display_menu = store.menu
        config.skipping = "fast"
        _preferences.skip_unseen = True
        reset_chapter_state(4)
        persistent.ch4_deaths = 0
        night = getattr(store, "_start_night", 0)
    jump ch4_night_hub

label devtest_ch4_n5:
    $ _start_night = 4
    jump devtest_ch4

## Chapter 4: nobody plays. Something should kill you.
label devtest_ch4_death:
    pause 0.3
    python:
        _night_len = 120.0
        def _first(items, **kw):
            v = [v for (t, v) in items if v is not None][0]
            return getattr(v, "value", v)
        store.menu = _first
        renpy.display_menu = store.menu
        reset_chapter_state(4)
        night = 3
    jump ch4_night_hub

label devtest_ch4_intro:
    scene bg bedroom
    call screen nightmare_intro
    call screen nightmare_controls
    return

label devtest_ch4_retry:
    python:
        _orig_cs = renpy.call_screen
        def _cs(name, *a, **k):
            if name == "ch4_death_screen":
                renpy.pause(2.0)
                return "retry"
            return _orig_cs(name, *a, **k)
        renpy.call_screen = _cs
    jump devtest_ch4_death

## Chapter 5: bot plays the whole chapter (right answer every time).
label devtest_ch5:
    pause 0.3
    python:
        _autohit = True
        def _first(items, **kw):
            v = [v for (t, v) in items if v is not None][0]
            return getattr(v, "value", v)
        store.menu = _first
        renpy.display_menu = store.menu
        config.skipping = "fast"
        _preferences.skip_unseen = True
        _orig_cs5 = renpy.call_screen
        def _cs5(name, *a, **k):
            if name == "ch5_intro":
                return None
            return _orig_cs5(name, *a, **k)
        renpy.call_screen = _cs5
    jump chapter5_start

## Chapter 5: bot picks the wrong answer every time on Funtime Freddy (ANGER fills -> death).
label devtest_ch5_bad:
    pause 0.3
    python:
        _badbot = True
        _autohit = True
        def _first(items, **kw):
            v = [v for (t, v) in items if v is not None][0]
            return getattr(v, "value", v)
        store.menu = _first
        renpy.display_menu = store.menu
        config.skipping = "fast"
        reset_chapter_state(5)
        repaired = ["circusbaby"]
        night = 1
    jump ch5_day_hub

## Chapter 5: timer runs out on a choice (nobody answers), Baby hint visible.
label devtest_ch5_timer:
    scene bg sl_parts
    show funtimefreddy broken at twitch
    $ repaired = ["circusbaby"]
    $ ch5_key = "funtimefreddy"
    $ meter = 1
    show screen ch5_meter
    $ renpy.call_screen("timed_choice", prompt=CH5["funtimefreddy"]["steps"][1][1], options=[o[0] for o in CH5["funtimefreddy"]["steps"][1][2]], seconds=30.0, hint=CH5["funtimefreddy"]["steps"][1][3], can_ask=True, auto_hint=True)
    return

label devtest_ch5_intro:
    scene bg sl_control
    call screen ch5_intro
    return

label devtest_chapters:
    $ persistent.chapter_unlocked = 6
    call screen chapter_select
    return
