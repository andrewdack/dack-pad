import PySimpleGUI as sg

from utils import DPWindows, THEME_MODES, ZOOM_OPTIONS, SOURCES, current_theme
import events


def main() -> None:
    """Main PySimpleGui event loop"""
    window = DPWindows.create_main_window(current_theme)
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "Exit":
            exit = events.exit_attempt(values, window)
            if exit:
                break

        if event == "-textbox-":
            events.char_typed(window)

        if event in THEME_MODES:
            events.change_theme(event, values, window)

        if event in ZOOM_OPTIONS:
            events.change_zoom(event, window)

        if event == "Open":
            events.open_file(window)

        if event == "Save":
            events.save_file(values, window)

        if event == "Text Statistics":
            events.text_stats(values)

        if event == "Date/Time":
            events.date_time(values, window)

        if event == "Replace":
            events.replace_text(values, window)

        if event in SOURCES:
            pass

        if event in ["About DSI", "About DackPad", "DackPad GitHub (About)"]:
            match event:
                case "About DSI":
                    pass
                case "DackPad GitHub (About)":
                    events.open_github("dack-pad")

    window.close()


if __name__ == "__main__":
    main()
