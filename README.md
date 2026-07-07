# prl-highlight

Syntax highlighting for pRETE's PRL rule language (`.prl` files) in PyCharm.

![](logo.png)

![CI](https://github.com/stefano-bragaglia/prl-highlight/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Visuals

## Prerequisites

- PyCharm (or any JetBrains IDE) 2024.x+ (built-in TextMate bundle support)
- Targets [pRETE](https://github.com/stefano-bragaglia/pRETE) v2.5.3.1's PRL
  language (grammar built from pRETE's own lexer/parser/AST source, and
  tested against its example `.prl` files, at that version) — including
  v2.5.3's bracket-style generics (`list[str]`, `dict[str, int]`) and
  `declare` field default values (`field: type = value`)

## Installation

There is no one-click installer — PyCharm's TextMate Bundles and Live
Templates features both require a manual, one-time registration step
through their Preferences screens. These steps register this repo's copy
of the bundle in your IDE; run them again on any other machine/PyCharm
installation where you want highlighting too.

1. Clone this repository (a plain zip download won't work — the bundle's
  grammar file is a symlink, which only a real git clone preserves).
2. Get the bundle folder's absolute path:
  ```
   uv run python scripts/locate_bundle.py
  ```
   This prints the path to `bundle/PRL.tmbundle` and nothing else, so you
   can copy it straight from the terminal.
3. In PyCharm, go to **Preferences → Editor → TextMate Bundles**, click
  **+**, and select the folder printed above. `.prl` files should now
   render in color instead of plain text.
4. (Optional but recommended) Add the Live Templates skeletons. Recent
   PyCharm versions don't expose a "Live Templates → Import" button, so
   instead copy the file directly into the IDE's template folder and
   restart:
   ```
   mkdir -p "<PyCharm config dir>/templates"
   cp bundle/live-templates/prl.xml "<PyCharm config dir>/templates/PRL.xml"
   ```
   `<PyCharm config dir>` is version-specific:
   - macOS: `~/Library/Application Support/JetBrains/<Product><Version>`
   - Windows: `%APPDATA%\JetBrains\<Product><Version>`
   - Linux: `~/.config/JetBrains/<Product><Version>`

   (`<Product>` is `PyCharm` or `PyCharmCE`; check **PyCharm → About** for
   your exact version, e.g. `PyCharm2026.1`.) After restarting, a `PRL`
   group should appear under **Preferences → Editor → Live Templates**.
5. Verify: open any of the vendored example files under
   `tests/fixtures/prl_examples/` (or one of your own `.prl` files) and
   confirm keywords, strings, and comments render in color.

## Usage

### Live Templates

Copy `bundle/live-templates/prl.xml` into your PyCharm config's `templates/`
folder (see step 4 of Installation above) and restart, then type an
abbreviation and press Tab to expand it. Every abbreviation is prefixed
`prl-` and available in **any** file type (context "Other") — `.prl` has no
registered IntelliJ Language to scope them to, so this is expected
behavior, not a bug.


| Abbreviation          | Expands to                                                                                                     |
| --------------------- | -------------------------------------------------------------------------------------------------------------- |
| `prl-rule`            | a `rule "..." when ... then ... end` skeleton                                                                  |
| `prl-declare`         | a `declare TypeName ... end` skeleton                                                                          |
| `prl-declare-extends` | a `declare TypeName extends ParentType ... end` skeleton                                                       |
| `prl-not`             | a `not ( ... )` negated-condition skeleton                                                                     |
| `prl-accumulate`      | an `accumulate(...)` skeleton (cycle the function placeholder through `sum`/`count`/`min`/`max`/`collectList`) |
| `prl-forall`          | a `forall(...)` skeleton                                                                                       |
| `prl-or`              | an `... or ...` disjunction branch pair                                                                        |
| `prl-exists`          | an `exists ...` skeleton                                                                                       |
| `prl-import`          | a `from ... import ...` skeleton                                                                               |
| `prl-package`         | a `package ...;` skeleton                                                                                      |


## Contributing

Issues and PRs welcome. Run the test suite with `uv run pytest` before submitting.

## License

MIT — see [LICENSE](LICENSE).