import sys
import time

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
    start = last = goome.now_ms()
    fps, hidden, running = 0.0, False, True
    pace = goome.Pacer(30)
    while running:
        for ev in g.events(pace.wait()):
            if ev.type == goome.QUIT:
                running = False
            if ev.type == goome.HOTKEY:
                hidden = not hidden
        if not running:
            break
        now = goome.now_ms()
        if now > last:
            fps = fps * 0.9 + 100.0 / (now - last)
        last = now
        with g.frame(0) as c:
            if c is None or hidden:
                continue
            c.round_rect(20, 20, 160, 92, 10, 0xB0141820)
            c.text(34, 30, time.strftime("%H:%M:%S"), 0xFFFFFFFF, big=True)
            c.text(34, 62, "up %ds" % ((now - start) // 1000), 0xFFC0C8D0)
            c.text(34, 84, "%.0f fps" % fps, 0xFF6FDC5F)
    g.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
