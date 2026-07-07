# Source

Vendored verbatim from
[stefano-bragaglia/pRETE](https://github.com/stefano-bragaglia/pRETE),
path `src/examples/declarative/prl/`. Originally fetched at commit
`3cf553d9fd0d42c617eefd789e99c0ff1921fcac` (2026-07-06); confirmed
byte-identical (no example file changed) through tag `v2.5.3.1`
(commit `e7572171810a32fa00c5e5c1a4f2a49565fcda22`, verified 2026-07-07),
so this grammar targets pRETE v2.5.3.1's PRL language, including the
v2.5.3 bracket-generics and field-defaults additions — those two
constructs aren't demonstrated in any of these 17 example files, though;
their grammar coverage is tested via inline snippets from pRETE's own
`tests/test_prl_parser.py`, not a vendored fixture.

Same author, no license concern. These are copies, not a live sync — if
pRETE's examples change later, these go stale until manually refreshed.
