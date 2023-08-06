import os.path
import subprocess
from reggisearch import search_values
import keyboard
import re
from gracefully_kill import kill_process

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
creationflags = subprocess.CREATE_NO_WINDOW
invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
    "start_new_session": True,
}


def kill_app(p, hotkey):
    kill_process(p)
    keyboard.remove_hotkey(hotkey)


def execute_app(
    file: str,
    path: str | tuple,
    exit_keys="ctrl+alt+o",
    add_options: tuple = (),
    headless=True,
    **kwargs,
):
    r"""
    Args:
        file (str): The file to be opened by the application.
        path (str): The path to the application executable (file path/or reg path)
        exit_keys (str, optional): The key combination to exit the application. Defaults to "ctrl+alt+o".
        add_options (tuple, optional): Additional options to pass to the application. Defaults to ().
        headless (bool, optional): Whether to run the application in headless mode. Defaults to True.
        **kwargs: Additional keyword arguments to pass to the subprocess.Popen() function.

    Returns:
        subprocess.Popen: A Popen object representing the executed application process.
    Examples:
        from subprocreg import execute_app
        proc=execute_app(
            file=r"F:\4 Promille - Oi the Meeting.mp3",
            path=(r"HKEY_CLASSES_ROOT\Directory\shell\AddToPlaylistVLC", "Icon"),
            exit_keys="ctrl+q",
            add_options=(
                "--input-repeat=0",
                "-Idummy",
                "--play-and-exit",
                "--qt-minimal-view",
            ),
            headless=True,

        )
        proc=execute_app(
            file=r"C:\ProgramData\anaconda3\envs\dfdir\gracefully_kill.py",
            path=r"C:\Windows\System32\notepad.exe",
            exit_keys="ctrl+b",
            add_options=(),
            headless=False,

        )
    """
    if not os.path.exists(str(path)):
        try:
            di = search_values(mainkeys=path[0], subkeys=(path[1],))
            path = re.findall(
                rf"\b\w\w?:\\.*?\.exe\b", str(di[path[0]][path[1]]), flags=re.I
            )[0]
        except Exception:
            raise OSError(f"{path} not found!")
    path = os.path.normpath(path)
    headlessdict = invisibledict if headless else {}
    p = subprocess.Popen(
        [path, *add_options, file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        shell=False,
        **kwargs,
        **headlessdict,
    )
    if exit_keys in keyboard.__dict__["_hotkeys"]:
        keyboard.remove_hotkey(exit_keys)
    keyboard.add_hotkey(exit_keys, lambda: kill_app(p, exit_keys))
    return p
