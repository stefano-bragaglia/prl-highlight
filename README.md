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

<!-- Filled in once the bundle is built: exact PyCharm menu path
     (Preferences -> Editor -> TextMate Bundles) and any setup script usage. -->

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

<!-- More templates added as further live-templates stories land. -->

## Contributing

Issues and PRs welcome. Run the test suite with `uv run pytest` before submitting.

## License

MIT — see [LICENSE](LICENSE).
