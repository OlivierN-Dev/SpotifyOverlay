from overlay.overlay_window import OverlayWindow

if __name__ == "__main__":
    try:
        OverlayWindow()
    except KeyboardInterrupt:
        print("Programme arrêté")
