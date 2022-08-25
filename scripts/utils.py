import webbrowser
import PySimpleGUI as sg

LOGO_FILE_PATH = r"C:\Users\Andrew Hu\OneDrive\Documents\Programming\Python\Projects\PySimpleGUI\Projects\dackpad\graphics\dack-logo.ico"

THEME_MODES = ["Dark Mode", "Light Mode"]
ZOOM_OPTIONS = ["Zoom In", "Zoom Out", "Restore Default Zoom"]
SOURCES = ["dackpad.py", "utils.py", "textstats.py", "events.py"]
MENU_LAYOUT = [
    ["File", ["Open", "Save", "---", "Exit"]],
    ["Tools", ["Text Statistics", "---"]],
    ["Edit", ["Replace", "Date/Time"]],
    ["View", ["Zoom", ZOOM_OPTIONS, "Theme", THEME_MODES]],
    ["About", ["About DSI", "About DackPad", "Source Code", SOURCES, "GitHub"]]
]

file_name = "Untitled.txt"
file_saved = True
font_size = 12
current_theme = "DarkGray9"


class DPWindows:
    """Repeated Windows/Popups used during operation of DackPad GUI"""

    @staticmethod
    def create_popup_save(fname) -> bool | None:
        """Returns:
        True (bool): If user chose to save.
        False (bool): If user chose to not save.
        None (Nonetype): If user canceled the save prompt.
        """
        save_window = sg.Window(
            "Save?",
            [
                [
                    sg.Text(
                        f"{fname} is not saved, do you want to save it?",
                        font="Calibri 11",
                    )
                ],
                [
                    sg.Push(),
                    sg.Button("Save", pad=(5, 20)),
                    sg.Button("Don't Save", pad=(5, 20)),
                    sg.Button("Cancel", pad=(5, 20)),
                ],
            ],
            size=(400, 100),
            icon=LOGO_FILE_PATH,
        )

        while True:
            save_events = save_window.read()[0]

            match save_events:
                case "Save":
                    # TODO SAVE FUNCTION
                    save_window.close()
                    return True
                case "Don't Save":
                    save_window.close()
                    return False
                case sg.WIN_CLOSED | "Cancel":
                    save_window.close()
                    return

    @staticmethod
    def create_popup_error(msg: str, title: str, exception: Exception) -> sg.Window:
        return sg.popup_error(
            f"{msg}\n Python Exception: {type(exception).__name__}",
            title=title,
            line_width=75,
            icon=LOGO_FILE_PATH,
        )

    @staticmethod
    def create_basic_popup(msg: str, title: str, exception: Exception) -> sg.Window:
        return sg.popup_error(
            msg,
            title=title,
            line_width=75,
            icon=LOGO_FILE_PATH,
        )

    @staticmethod
    def create_main_window(theme: str, text: str = "") -> sg.Window:
        global font_size
        sg.theme(theme)
        layout = [
            [sg.Menu(MENU_LAYOUT)],
            [sg.Text(f"{file_name} - DackPad", key="-docname-", font="Calibri 13")],
            [
                sg.Multiline(
                    default_text=text,
                    no_scrollbar=True,
                    font=f"Verdana {font_size}",
                    size=(70, 40),
                    expand_x=True,
                    expand_y=True,
                    pad=(10, 5),
                    border_width=0,
                    enable_events=True,
                    key="-textbox-",
                )
            ],
        ]

        return sg.Window(
            "DackPad",
            layout=layout,
            size=(800, 600),
            use_custom_titlebar=False,
            icon=LOGO_FILE_PATH,
        )


def open_source_win():
    pass


def open_github(link):
    webbrowser.open(link)
