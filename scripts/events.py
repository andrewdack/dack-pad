"""Collection of functions used for each PySimpleGui event in dackpad.main()"""
from webbrowser import open as open_tab
from datetime import datetime
from os import path

import PySimpleGUI as sg
from PySimpleGUI import Window

from textstats import number_of_characters, number_of_lines, number_of_words

# flake8 err: dpwindows.font_size imported but unused
from utils import (  # NOQA
    LOGO_FILE_PATH,
    DPWindows,
    current_theme,
    file_name,
    file_saved,
    font_size,
)


class SGEvent:
    """Representation of PySimpleGui Event. Only used for type annotations"""

    def __new__(cls):  # make Event uncallable
        raise TypeError(f"{cls.__name__} is not callable")


class SGValues:
    """Representation of PySimpleGui Values. Only used for type annotations"""

    def __new__(cls):  # make Values uncallable
        raise TypeError(f"{cls.__name__} is not callable")


# !
# ! EVENT LOOP FUNCTIONS
# !


def exit_attempt(values: SGValues, window: Window) -> bool:
    """if event in [sg.WIN_CLOSED, "Exit"]:"""
    if not file_saved:
        save_popup = DPWindows.create_popup_save(file_name)
        if save_popup:
            save_file(values, window)
        elif save_popup is None:
            return False
        return True

    return True


def char_typed(window: Window) -> None:
    """if event == "-textbox-":"""
    global file_saved
    file_saved = False
    window["-docname-"].update(f"*{file_name} - DackPad")


# def change_theme(event: SGEvent, values: SGValues, window: Window) -> sg.Window:
#     """if event in THEME_MODES:"""
#     global current_theme
#     cur_text = values["-textbox-"]
#     window.close()
#     if event == "Dark Mode":
#         current_theme = "Darkgray9"
#         return DPWindows.create_main_window(current_theme, cur_text)
#     if event == "Light Mode":
#         current_theme = "GrayGrayGray"
#         return DPWindows.create_main_window(current_theme, cur_text)


def change_zoom(event: SGEvent, window: Window) -> None:
    """if event in ZOOM_OPTIONS:"""
    global font_size
    match event:
        case "Zoom In":
            if font_size <= 36:
                font_size += 3
                window["-textbox-"].update(font=f"Verdana {font_size}")
        case "Zoom Out":
            if font_size >= 3:
                font_size -= 3
                window["-textbox-"].update(font=f"Verdana {font_size}")
        case "Restore Default Zoom":
            font_size = 12
            window["-textbox-"].update(font=f"Verdana {font_size}")


def open_file(window: Window) -> None:
    """if event == "Open":"""
    global file_name

    if not file_saved:
        save_popup = DPWindows.create_popup_save(file_name)
        if save_popup is None:
            return

    file_path = sg.popup_get_file(
        message="kys lol", no_window=True, icon=LOGO_FILE_PATH
    )
    try:
        if file_path:  # file_path is not empty
            with open(file_path, "r") as f:
                contents = f.read()
                window["-textbox-"].update(contents)
                file_name = path.basename(file_path)
                window["-docname-"].update(f"{file_name} - DackPad")
    except (PermissionError, OSError, IsADirectoryError) as e:
        DPWindows.create_popup_error(
            msg="Your specified path was not detected to be a file.",
            title="Path Error",
            exception=e,
        )
    except UnicodeError as e:
        DPWindows.create_popup_error(
            msg="Your specified text file was not compatible with DackPad.",
            title="File Error",
            exception=e,
        )


def save_file(values: SGValues, window: Window) -> None:
    """if event == "Save":"""
    global file_saved
    global file_name
    file_path = (
        sg.popup_get_file("Save As", no_window=True, save_as=True, icon=LOGO_FILE_PATH)
        + ".txt"
    )

    if file_path == ".txt":
        return

    try:
        with open(file_path, "w") as f:
            f.write(values["-textbox-"])
        file_name = path.basename(file_path)
        sg.popup_auto_close(
            f"{file_name} sucessfully saved.",
            title=file_name,
            auto_close_duration=2,
            icon=LOGO_FILE_PATH,
        )
        window["-docname-"].update(f"{file_name} - DackPad")
        file_saved = True
    except Exception:
        sg.popup_error(
            "There was an Error!",
            "Something went wrong while saving a Dackpad text file.",
            icon=LOGO_FILE_PATH,
        )


def text_stats(values: SGValues) -> None:
    """if event == "Text Statistics":"""
    full_text = values["-textbox-"]
    sg.Window(
        "Stats",
        [
            [sg.Text(f"Stats for file: {file_name}")],
            [
                sg.Text(
                    f"Words: {number_of_words(full_text)}",
                    font="Verdana 10",
                )
            ],
            [
                sg.Text(
                    f"Char: {number_of_characters(full_text)}",
                    font="Verdana 10",
                )
            ],
            [
                sg.Text(
                    f"Lines: {number_of_lines(full_text)}",
                    font="Verdana 10",
                )
            ],
            [sg.Button("Continue")],
        ],
        element_justification="center",
        size=(200, 150),
        icon=LOGO_FILE_PATH,
    ).read(close=True)


def date_time(values: SGValues, window: Window) -> None:
    """if event == "Date/Time":"""
    current_text = values["-textbox-"]
    time = datetime.now().strftime("%I:%M %p %m/%d/%Y")
    new_text = f"{current_text} {time}"
    window["-textbox-"].update(new_text)


def replace_text(values: SGValues, window: Window) -> None:
    global file_saved
    """if event == "Replace":"""
    case_sens = False
    replace_window = sg.Window(
        "Replace",
        [
            [sg.Text("Find What:")],
            [sg.Input(key="-target-")],
            [sg.Text("Replace With:")],
            [sg.Input(key="-replacement-")],
            [
                sg.Checkbox(  # unchecked by default
                    "Case Sensitive",
                    font="Calibri 8",
                    enable_events=True,
                    key="-case-",
                ),
            ],
            [sg.Button("Replace")],
            [sg.Button("Cancel")],
        ],
        size=(400, 200),
        icon=LOGO_FILE_PATH,
    )

    while True:
        replace_events, replace_values = replace_window.read()

        match replace_events:
            case sg.WINDOW_CLOSED:
                break
            case "Cancel":
                break
            case "-case-":
                case_sens = not case_sens

            case "Replace":
                begin_text = values["-textbox-"]
                current_text = values["-textbox-"]

                if case_sens:
                    current_text = begin_text.replace(
                        replace_values["-target-"], replace_values["-replacement-"]
                    )
                else:  # not case_sensitive
                    split_text = begin_text.split()
                    replace_words = [
                        word
                        for word in split_text
                        if word.lower() == replace_values["-target-"]
                    ]
                    for each_word in replace_words:
                        current_text = current_text.replace(
                            each_word, replace_values["-replacement-"]
                        )
                break
    replace_window.close()
    # text changed:
    if begin_text != current_text:
        window["-textbox-"].update(current_text)
        sg.popup_auto_close(
            f"Successfully replaced words in {file_name}",
            title=file_name,
            auto_close_duration=1,
            icon=LOGO_FILE_PATH,
        )
        char_typed(window)
        return

    # text didn't change
    sg.popup_auto_close(
        f"No replacements done on {file_name}",
        title=file_name,
        auto_close_duration=1,
        icon=LOGO_FILE_PATH,
    )


def open_source_win(event: SGEvent) -> sg.Window:
    """if event in SOURCES:"""
    with open(f"scripts\\{event}", "r") as f:
        f_cont = f.read()
    sg.Window(
        title=event,
        layout=[
            [sg.Text(f"{event} - DackPad Source", font="Calibri 13")],
            [
                sg.Multiline(
                    default_text=f_cont,
                    # write_only=False,
                    no_scrollbar=True,
                    font="Verdana 12",
                    size=(70, 40),
                    expand_x=True,
                    expand_y=True,
                    pad=(10, 5),
                    border_width=0,
                    disabled=True
                )
            ],
        ],
        element_justification="center",
        size=(800, 600),
        icon=LOGO_FILE_PATH,
    ).read(close=True)


def open_github(link: str) -> None:
    """if event in ["About DSI", "About DackPad", "DackPad GitHub (About)"]:"""
    open_tab(f"https://github.com/DackCodes/{link}")
