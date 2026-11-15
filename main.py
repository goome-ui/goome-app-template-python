import sys

import goome

APP_NAME = "My Goome App"


class State(object):
    clicks = 0
    volume = 0.5
    overlay = False


def open_mode(overlay):
    if not overlay:
        return goome.open_app(APP_NAME, 640, 420), None
    g = goome.open(APP_NAME)
    mons = g.monitors()
    x = mons[0].area.x + mons[0].area.w - 340 if mons else 40
    return g, goome.Window(x, 60, 300)


def contents(ui, s):
    s.overlay = ui.toggle("Overlay mode", s.overlay)
    ui.separator()
    ui.heading("Hello from " + APP_NAME)
    if ui.button("Click me"):
        s.clicks += 1
    ui.label("clicked %d times" % s.clicks)
    s.volume = ui.slider("Volume", s.volume, 0.0, 1.0, "%.2f")


def main():
    s = State()
    mode = False
    try:
        g, win = open_mode(False)
    except goome.GoomeError as e:
        print("couldnt open a window: %s" % e, file=sys.stderr)
        return 1
    ui = g.ui()
    running = True
    while running:
        for ev in g.events(16):
            if ev.type in (goome.QUIT, goome.CLOSE):
                running = False
            ui.feed(ev)
        if not running:
            break
        if s.overlay != mode:
            g.close()
            try:
                g, win = open_mode(s.overlay)
            except goome.GoomeError:
                print("no overlay here, staying in window mode", file=sys.stderr)
                s.overlay = False
                g, win = open_mode(False)
            mode = s.overlay
            ui = g.ui()
            print("overlay mode" if mode else "window mode")
            sys.stdout.flush()
            continue
        if ui.begin(0) is None:
            continue
        if mode:
            if ui.window(APP_NAME, win, goome.WIN_MOVE | goome.WIN_COLLAPSE):
                contents(ui, s)
            ui.window_end()
        else:
            ui.app(APP_NAME)
            contents(ui, s)
            ui.app_end()
        ui.end()
    g.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
