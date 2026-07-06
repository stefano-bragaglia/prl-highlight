`PRL.tmLanguage.json` is a symlink to `src/prl_highlight/grammar/prl.tmLanguage.json`
— the canonical grammar file owned by the `prl-grammar` feature — so the two
can never silently drift apart. This requires a real git clone (symlinks
aren't preserved by a plain zip download of the repo); anyone installing the
bundle should clone the repository rather than downloading a zip archive.
