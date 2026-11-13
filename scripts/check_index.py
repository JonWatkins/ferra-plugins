"""Checks index.toml: its shape, unique names and name order, and that each
plugin kept in this repository (`path`, no `repo`) is there, with a
ferra-plugin.toml of the same name.

Run with `python3 scripts/check_index.py` (Python 3.11+, for tomllib).
"""

import os
import re
import sys
import tomllib

NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")
REPO = re.compile(r"^[A-Za-z0-9-]+/[A-Za-z0-9._-]+$")
PATH = re.compile(r"^[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+)*$")
KEYS = {"name", "repo", "path", "description", "tags", "language"}


def check_folder(where: str, name: str, folder: str) -> list[str]:
    """A plugin kept in this repository: its manifest is there and agrees."""
    manifest = os.path.join(folder, "ferra-plugin.toml")
    if not os.path.isfile(manifest):
        return [f"{where}: no ferra-plugin.toml in {folder}"]
    try:
        with open(manifest, "rb") as f:
            found = tomllib.load(f).get("name")
    except tomllib.TOMLDecodeError as e:
        return [f"{where}: {manifest}: {e}"]
    if found != name:
        return [f"{where}: {manifest} is named {found!r}"]
    return []


def check(path: str) -> list[str]:
    root = os.path.dirname(os.path.abspath(path))
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
        folder = plugin.get("path")
        if repo is not None and (not isinstance(repo, str) or not REPO.match(repo)):
            errors.append(f"{where}: repo must be owner/name")
        if folder is not None and (
            not isinstance(folder, str) or not PATH.match(folder) or ".." in folder.split("/")
        ):
            errors.append(f"{where}: path must be a folder like plugins/{name}")
            folder = None
        if repo is None and folder is None:
            errors.append(f"{where}: needs a repo, or a path in this repository")
        if repo is None and folder is not None:
            errors.extend(check_folder(where, name, os.path.join(root, folder)))
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
