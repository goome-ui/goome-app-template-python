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
        g.hotkey("alt+h", 1)
    except goome.GoomeError:
        pass
    ui = g.ui()
    win = goome.Window(60, 60, 280)
    clicks, hidden = 0, False
    while win.open:
        for ev in g.events(16):
            if ev.type == goome.QUIT:
                win.open = False
            if ev.type == goome.HOTKEY:
                hidden = not hidden
            ui.feed(ev)
        if not win.open or ui.begin(0) is None:
            continue
        if not hidden:
            if ui.window(APP_NAME, win, goome.WIN_MOVE | goome.WIN_CLOSE):
                ui.label("im on top of everything")
                if ui.button("Click me"):
                    clicks += 1
                ui.label("clicked %d times" % clicks)
                ui.label("alt+h hides me")
            ui.window_end()
        ui.end()
    g.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
