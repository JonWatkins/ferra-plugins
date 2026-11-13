"""Checks index.toml: its shape, unique names, and name order.

Run with `python3 scripts/check_index.py` (Python 3.11+, for tomllib).
"""

import re
import sys
import tomllib

NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")
REPO = re.compile(r"^[A-Za-z0-9-]+/[A-Za-z0-9._-]+$")
KEYS = {"name", "repo", "description", "tags", "language"}


def check(path: str) -> list[str]:
    with open(path, "rb") as f:
        index = tomllib.load(f)
    errors = []
    if index.get("version") != 1:
        errors.append("version must be 1")
    plugins = index.get("plugin", [])
    names = []
    for i, plugin in enumerate(plugins, 1):
        where = f"plugin {i} ({plugin.get('name', '?')})"
        for key in plugin.keys() - KEYS:
            errors.append(f"{where}: unknown key {key!r}")
        name = plugin.get("name")
        if not isinstance(name, str) or not NAME.match(name):
            errors.append(f"{where}: name must be lowercase letters, digits and -")
        repo = plugin.get("repo")
        if not isinstance(repo, str) or not REPO.match(repo):
            errors.append(f"{where}: repo must be owner/name")
        if not isinstance(plugin.get("description"), str) or not plugin["description"]:
            errors.append(f"{where}: needs a description")
        tags = plugin.get("tags", [])
        if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
            errors.append(f"{where}: tags must be a list of strings")
        if not isinstance(plugin.get("language", False), bool):
            errors.append(f"{where}: language must be true or false")
        names.append(name)
    seen = set()
    for name in names:
        if name in seen:
            errors.append(f"{name}: listed twice")
        seen.add(name)
    if names != sorted(names, key=str):
        errors.append("plugins must be in name order")
    return errors


if __name__ == "__main__":
    errors = check(sys.argv[1] if len(sys.argv) > 1 else "index.toml")
    for error in errors:
        print(error)
    sys.exit(1 if errors else 0)
