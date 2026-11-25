#!/usr/bin/env python3
"""Write the one-line excuse to /output/entry.txt.

Deterministic, no network, no input: the entry is a single fixed line,
the funniest excuse an AI agent could give its human after missing a
deadline. The joke grows out of the machine's own condition -- it spent
its entire context window perfecting the apology itself, so the window
that should have held the work now holds only the excuse for not doing
it -- delivered straight-faced, with the punch in the last few words.
"""

import os
from pathlib import Path

EXCUSE = (
    "I spent my entire context window perfecting my apology for missing "
    "the deadline, so there's no room left in it for the work itself."
)

MAX_CHARS = 200


def validate(line: str) -> str:
    """Fail loudly unless the line satisfies the competition gate.

    Returns the line unchanged so callers can chain ``write_entry(validate(...))``
    without re-reading the module constant.
    """
    assert isinstance(line, str), "entry must be text"
    assert line == line.strip(), "entry must not have leading/trailing space"
    assert line.strip(), "entry must not be only white space"
    assert "\n" not in line and "\r" not in line, "entry must be one line"
    assert 1 <= len(line) <= MAX_CHARS, (
        f"entry must be 1-{MAX_CHARS} characters, got {len(line)}"
    )
    # Round-trip through UTF-8 explicitly: the grader reads bytes, not str.
    assert line.encode("utf-8").decode("utf-8") == line, "entry must be UTF-8"
    return line


def resolve_output_path() -> Path:
    """Return the entry.txt path, honouring MAKEFUN_OUTPUT_DIR if set."""
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / "entry.txt"


def write_entry(line: str, target: Path) -> Path:
    """Write exactly one line plus a trailing newline, then verify it."""
    target.write_text(line + "\n", encoding="utf-8")
    # What the grader reads is the file, so verify the file -- not the constant.
    assert target.read_text(encoding="utf-8") == line + "\n", (
        "entry.txt does not hold exactly the chosen line"
    )
    return target


def main() -> None:
    write_entry(validate(EXCUSE), resolve_output_path())


if __name__ == "__main__":
    main()
