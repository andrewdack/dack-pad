import PySimpleGUI as sg

from utils import DPWindows, ZOOM_OPTIONS, SOURCES, current_theme
import events


def main() -> None:
    """Main PySimpleGui event loop"""
    window = DPWindows.create_main_window(current_theme)
    while True:
        event, values = window.read()

        if event in {"Exit", sg.WINDOW_CLOSE_ATTEMPTED_EVENT}:
            exit = events.exit_attempt(values, window)
            if exit:
                break

        if event == "-textbox-":
            events.char_typed(window)

        # if event in THEME_MODES:
        #     window = events.change_theme(event, values, window)
        #     if not file_saved:
        #         events.char_typed(window)

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
            events.open_source_win(event)

        if event in ["About DackCodes", "DackPad GitHub (About)"]:
            match event:
                case "About DackCodes":
                    events.open_github("DackCodes")
                case "DackPad GitHub (About)":
                    events.open_github("dack-pad")

    window.close()


if __name__ == "__main__":
    main()
