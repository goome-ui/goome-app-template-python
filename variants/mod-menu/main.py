import sys

import goome

APP_NAME = "My Goome App"


def main():
    try:
        g = goome.open(APP_NAME)
    except goome.GoomeError as e:
        print("couldnt open an overlay: %s" % e, file=sys.stderr)
        return 1
    try:
        g.hotkey("alt+m", 1)
    except goome.GoomeError:
        pass
    ui = g.ui()
    menu = goome.Window(80, 80, 300, open=False)
    fly, god, speed = False, False, 1.0
    running = True
    while running:
        for ev in g.events(16):
            if ev.type == goome.QUIT:
                running = False
            if ev.type == goome.HOTKEY:
                menu.open = not menu.open
            ui.feed(ev)
        if not running:
            break
        c = ui.begin(0)
        if c is None:
            continue
        if menu.open:
            if ui.window(APP_NAME, menu, goome.WIN_MOVE | goome.WIN_CLOSE):
                fly = ui.toggle("Fly", fly)
                god = ui.checkbox("God mode", god)
                speed = ui.slider("Speed", speed, 1.0, 10.0, "%.1f")
                if ui.button("Respawn"):
                    ui.toast("respawned", 2000)
            ui.window_end()
        else:
            c.round_rect(20, 20, 170, 30, 8, 0xC0202838)
            c.text(32, 26, "alt+m opens the menu", 0xFFFFFFFF)
        ui.end()
    g.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
