"""The two kinds of gum a player can eat."""

from enum import Enum


class PacgumType(Enum):
    """A gum's type: a regular pacgum or a power-granting super-pacgum."""

    NORMAL = "NORMAL"
    SUPER = "SUPER"
