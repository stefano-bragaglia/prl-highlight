# prl-highlight

Syntax highlighting for pRETE's PRL rule language (`.prl` files) in PyCharm.

[![CI](https://github.com/stefano-bragaglia/prl-highlight/actions/workflows/ci.yml/badge.svg)](https://github.com/stefano-bragaglia/prl-highlight/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
<!-- PyPI badge added by /publish once a release exists -->

## Visuals

<!-- Add a before/after screenshot of a .prl file once the bundle is ready. -->

## Prerequisites

- PyCharm (or any JetBrains IDE) 2024.x+ (built-in TextMate bundle support)
- [pRETE](https://github.com/stefano-bragaglia/pRETE) if you want to try the bundle against real `.prl` files

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
4. (Optional but recommended) Import the Live Templates skeletons: go to
   **Preferences → Editor → Live Templates**, click the gear icon, choose
   **Import**, and select `bundle/live-templates/prl.xml` from this repo.
5. Verify: open any of the vendored example files under
   `tests/fixtures/prl_examples/` (or one of your own `.prl` files) and
   confirm keywords, strings, and comments render in color.

## Usage

### Live Templates

Import `bundle/live-templates/prl.xml` via Preferences → Editor → Live
Templates → gear icon → Import, then type an abbreviation and press Tab to
expand it. Every abbreviation is prefixed `prl-` and available in **any**
file type (context "Other") — `.prl` has no registered IntelliJ Language to
scope them to, so this is expected behavior, not a bug.

| Abbreviation | Expands to |
|---|---|
| `prl-rule` | a `rule "..." when ... then ... end` skeleton |
| `prl-declare` | a `declare TypeName ... end` skeleton |
| `prl-declare-extends` | a `declare TypeName extends ParentType ... end` skeleton |
| `prl-not` | a `not ( ... )` negated-condition skeleton |
| `prl-accumulate` | an `accumulate(...)` skeleton (cycle the function placeholder through `sum`/`count`/`min`/`max`/`collectList`) |
| `prl-forall` | a `forall(...)` skeleton |
| `prl-or` | an `... or ...` disjunction branch pair |
| `prl-exists` | an `exists ...` skeleton |
| `prl-import` | a `from ... import ...` skeleton |
| `prl-package` | a `package ...;` skeleton |

## Contributing

Issues and PRs welcome. Run the test suite with `uv run pytest` before submitting.

## License

MIT — see [LICENSE](LICENSE).
