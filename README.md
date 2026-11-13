# ferra plugins

The directory of plugins for [ferra](https://github.com/JonWatkins/ferra),
the terminal text editor. `index.toml` lists them; ferra reads it to
browse and install plugins.

> ferra and its plugin system are in early development: the commands and
> the manifest below may still change.

## Installing a plugin

From inside ferra:

| Command | |
|---------|---|
| `:plugin_browse` | Pick from the plugins listed here |
| `:plugin_install owner/repo` | Install any plugin on GitHub, listed or not (`owner/repo@tag` for a tag, `owner/repo//folder` for one in a folder) |
| `:plugin_update [name]` | Update one or all, showing the new commits first |
| `:plugin_remove name` | Remove one |
| `:plugin_list` | What's installed, and at which commit |
| `:plugin_install` | Install what `plugins.toml` lists but isn't installed (a new machine) |
| `:plugin_reload` | Load every plugin again after changing one |

Plugins are git clones in `~/.local/share/ferra/plugins/`. What you've
installed, and the exact commit of each, is kept in `plugins.toml` and
`plugins.lock` in ferra's config folder, so your dotfiles reproduce your
setup.

**Plugins run with your permissions.** A plugin is Lua code that can read
and write files and run commands, as Neovim and VS Code extensions can.
ferra shows you the repository and asks before installing; the plugins
listed here are reviewed when they're added, but read the code of
anything you install.

## Writing a plugin

A plugin is a GitHub repository with a `ferra-plugin.toml` at its root:

```toml
name = "todos"                 # lowercase letters, digits and -
version = "0.1.0"
description = "List the file's TODOs in the sidebar"
ferra = ">=0.1"                # the ferra versions it works with
main = "init.lua"              # the file loaded first (the default)
```

and its Lua files (`require("todos.util")` loads `lua/todos/util.lua`
from the plugin). The API (`editor.command`, `editor.on`, `editor.map`,
`ctx:popup{...}`, sidebar views...) is in ferra's guide under
[Lua plugins](https://github.com/JonWatkins/ferra/blob/main/docs/GUIDE.md#lua-plugins).

A **language pack** adds a language ferra doesn't know, with
`[languages.<name>]` tables in `ferra-plugin.toml`, written as in ferra's
`config.toml` (a pack needs no Lua):

```toml
name = "zig"
version = "0.1.0"
description = "Zig: file types, comments and zls"

[languages.zig]
extensions = ["zig", "zon"]
comment = "//"
options = { tab-width = 4 }
language-server = { command = "zls" }
```

For highlighting, name the grammar's repository and the commit to build,
as Helix does; ferra fetches it and compiles it with the user's C
compiler when the pack is installed:

```toml
[grammars.zig]
git = "https://github.com/tree-sitter-grammars/tree-sitter-zig"
rev = "6479aa13f32f701c383083d8b28360ebd682fb7d"   # a full commit hash
```

The grammar repository's own queries are used unless the pack has its
own in `queries/<language>/` (`highlights.scm`, `injections.scm`,
`locals.scm`, `indents.scm`), file by file. Queries written for Neovim
work as they are. See `languages/lua` and `languages/zig`, and ferra's
guide, [Language packs](https://github.com/JonWatkins/ferra/blob/main/docs/GUIDE.md#language-packs).

List a pack in `index.toml` with `language = true`.

## Official plugins

Plugins maintained with ferra live in this repository, one folder each:
language packs under `languages/`, other plugins under `plugins/`. They're
listed without a `repo`:

```toml
[[plugin]]
name = "zig"
path = "languages/zig"
description = "Zig: highlighting, indentation, comments and zls"
language = true
```

ferra installs one by cloning only its folder (`:plugin_install
JonWatkins/ferra-plugins//plugins/zig`), and updates it only for commits
that touch that folder. Official plugins follow `main`.

## Getting listed

Open a pull request adding one `[[plugin]]` table to `index.toml`, in name
order:

```toml
[[plugin]]
name = "todos"
repo = "someone/ferra-todos"
description = "List the file's TODOs in the sidebar"
tags = ["sidebar", "notes"]
```

The name must match the plugin's `ferra-plugin.toml`. A check runs on
every pull request (`python3 scripts/check_index.py` runs it locally).
