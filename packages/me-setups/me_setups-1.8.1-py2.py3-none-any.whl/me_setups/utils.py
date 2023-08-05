from __future__ import annotations

import contextlib
import logging
import os
import pathlib
import re
from typing import Generator


logger = logging.getLogger(__name__)

LCK_DIR = pathlib.Path("/var/lock/")
LCK_FMT = "LCK..{port}"


class PortInUse(Exception):
    pass


def _pid_exists(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False


def get_lck_file_path(port_link: pathlib.Path) -> pathlib.Path:
    port_lck_fmt = LCK_FMT.format(port=port_link.name)
    return LCK_DIR / port_lck_fmt


@contextlib.contextmanager
def lock_port_ctx(port: pathlib.Path | str) -> Generator[None, None, None]:
    try:
        lock_port(port)
        yield
    finally:
        release_port(port)


def lock_port(port: pathlib.Path | str) -> None:
    port_links = get_port_links(pathlib.Path(port))
    if in_use(port_links):
        raise PortInUse(f"Cannot lock {port}.")
    for port_link in port_links:
        lck_file_path = get_lck_file_path(port_link)
        try:
            lck_file_path.write_text(f"   {os.getpid()}\n")
        except PermissionError:
            logger.warning(f"Have no permission to edit {lck_file_path}")


def release_port(port: pathlib.Path | str) -> None:
    port_links = get_port_links(pathlib.Path(port))
    if in_use(port_links):
        raise PortInUse(f"Cannot lock {port}.")
    for port_link in port_links:
        os.unlink(get_lck_file_path(port_link))


def in_use(port_links: set[pathlib.Path]) -> bool:
    pids = get_pids_using_port(port_links)
    if pids:
        return any(_pid_exists(pid) for pid in pids if pid != os.getpid())
    return False


def get_pids_using_port(port_links: set[pathlib.Path]) -> set[int]:
    pids = set()
    for port_link in port_links:
        lck_file_path = get_lck_file_path(port_link)
        if lck_file_path.exists():
            lck_file_data = lck_file_path.read_text()
            pids.update({int(x.strip()) for x in lck_file_data.splitlines()})
    return pids


def get_port_links(port: pathlib.Path) -> set[pathlib.Path]:
    """get all the links to the port, include the path given.

    Args:
        port (pathlib.Path): Path to the port.

    Returns:
        set[pathlib.Path]: set of all Paths links
    """
    return {
        link for link in port.parent.iterdir() if (port.parent / link).samefile(port)
    }


def filter_ansi_escape(text: str) -> str:
    """filter ascii escape characters, removing coloring and unprintable chars.

    Args:
        text (str): the text to filter

    Returns:
        str: the text without the escape characters
    """
    COLOR_ESC = r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])"
    ESC_CHARS = r"[\x00-\x09]|[\x0B-\x1F]"
    ansi_escape = re.compile(f"{COLOR_ESC}|{ESC_CHARS}")
    return ansi_escape.sub("", text)
