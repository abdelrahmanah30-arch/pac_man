import json
import re
from pathlib import Path
from typing import List, NamedTuple, Optional, Union

MAX_ENTRIES = 10
MAX_NAME_LENGTH = 10
NAME_PATTERN = re.compile(r"^[A-Za-z0-9 ]+$")


class HighScoreEntry(NamedTuple):
    """A single highscore: a player's name and the score they reached."""

    name: str
    score: int


class HighScoreManager:
    """Loads, validates, ranks, and persists the top 10 highscores.

    The on-disk format is a JSON array of objects, e.g.::

        [
            {"name": "Sannaka", "score": 1110},
            {"name": "foliole", "score": 20}
        ]

    Every public method is resilient to a missing file, corrupted
    JSON, or malformed entries: none of these ever raise, they simply
    fall back to treating the list as empty.
    """

    def __init__(self, filename: Union[str, Path]) -> None:
        """Store the path of the highscore file to use.

        Args:
            filename: Path to the JSON file the highscores live in.
        """
        self.filename = Path(filename)
        self.scores: List[HighScoreEntry] = []

    def load(self) -> None:
        """Load the top scores from disk into memory.

        A missing file, invalid JSON, or an unexpected structure all
        simply result in an empty list rather than a crash.
        """
        try:
            raw_text = self.filename.read_text(encoding="utf-8")
        except OSError:
            self.scores = []
            return

        try:
            raw_entries = json.loads(raw_text)
        except json.JSONDecodeError:
            print(
                f"Highscore warning: '{self.filename}' is not valid "
                f"JSON, starting with an empty list"
            )
            self.scores = []
            return

        self.scores = self._parse_entries(raw_entries)

    def save(self) -> None:
        """Persist the current top scores to disk.

        Creates the target directory if it does not exist yet. A
        failure to write is reported but never crashes the game.
        """
        try:
            self.filename.parent.mkdir(parents=True, exist_ok=True)

            payload = [
                {"name": entry.name, "score": entry.score}
                for entry in self.scores
            ]

            self.filename.write_text(
                json.dumps(payload, indent=2), encoding="utf-8"
            )
        except OSError as error:
            print(
                f"Highscore warning: could not save '{self.filename}': "
                f"{error}"
            )

    def add_score(self, name: str, score: int) -> bool:
        """Validate and insert a new score, keeping only the top 10.

        Does not save to disk; call save() when the game ends.

        Args:
            name: The player's chosen name.
            score: The score they finished the game with.

        Returns:
            True if the name and score were both valid and the entry
            was recorded (even if it did not make the top 10), False
            if either failed validation.
        """
        clean_name = self._validate_name(name)
        clean_score = self._validate_score(score)

        if clean_name is None or clean_score is None:
            return False

        self.scores.append(HighScoreEntry(clean_name, clean_score))
        self.scores.sort(key=lambda entry: entry.score, reverse=True)
        self.scores = self.scores[:MAX_ENTRIES]

        return True

    def get_top_scores(self) -> List[HighScoreEntry]:
        """Return the current top scores, highest first."""
        return list(self.scores)

    def get_highscore(self) -> int:
        """Return the single highest score, or 0 if there are none."""
        return self.scores[0].score if self.scores else 0

    def _parse_entries(self, raw_entries: object) -> List[HighScoreEntry]:
        """Validate a decoded JSON payload into a clean entry list."""
        if not isinstance(raw_entries, list):
            print(
                f"Highscore warning: '{self.filename}' must contain a "
                f"JSON array, starting with an empty list"
            )
            return []

        entries: List[HighScoreEntry] = []

        for raw_entry in raw_entries:
            if not isinstance(raw_entry, dict):
                continue

            name = self._validate_name(raw_entry.get("name"))
            score = self._validate_score(raw_entry.get("score"))

            if name is not None and score is not None:
                entries.append(HighScoreEntry(name, score))

        entries.sort(key=lambda entry: entry.score, reverse=True)
        return entries[:MAX_ENTRIES]

    @staticmethod
    def _validate_name(name: object) -> Optional[str]:
        """Return a clean name, or None if it fails validation.

        A valid name is 1 to 10 characters long (after trimming) and
        contains only letters, digits, and spaces.
        """
        if not isinstance(name, str):
            return None

        trimmed = name.strip()

        if not trimmed or len(trimmed) > MAX_NAME_LENGTH:
            return None

        if not NAME_PATTERN.match(trimmed):
            return None

        return trimmed

    @staticmethod
    def _validate_score(score: object) -> Optional[int]:
        """Return a clean score, or None if it fails validation.

        A valid score is a non-negative integer. A bool is rejected
        even though Python treats bool as an int subclass.
        """
        if not isinstance(score, int) or isinstance(score, bool):
            return None

        if score < 0:
            return None

        return score
