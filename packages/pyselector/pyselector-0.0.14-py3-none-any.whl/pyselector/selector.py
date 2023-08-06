# menu.py

from __future__ import annotations

import logging

from pyselector import logger
from pyselector.menus.dmenu import Dmenu
from pyselector.menus.fzf import Fzf
from pyselector.menus.rofi import Rofi

menus: dict[str, Menu] = {
    "dmenu": Dmenu,
    "rofi": Rofi,
    "fzf": Fzf,
}


class Menu:
    @staticmethod
    def rofi() -> Rofi:
        return Rofi()

    @staticmethod
    def dmenu() -> Dmenu:
        return Dmenu()

    @staticmethod
    def fzf() -> Fzf:
        return Fzf()

    @staticmethod
    def menu_list() -> list[str]:
        return list(menus.keys())

    @staticmethod
    def logging_debug(verbose: bool = False) -> None:
        logging.basicConfig(
            level=logging.DEBUG if verbose else logging.INFO,
            format="%(levelname)s %(name)s - %(message)s",
            handlers=[logger.handler],
        )
