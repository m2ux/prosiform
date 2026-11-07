# Decisions

## Confirmed

- The entry reference is a positional argument: `pf [OPTIONS] REF [--presets PRESETS]` (user, 2026-11-07).
- A leading-dash entry is not supported. The `--entry=-guide.md` spelling retires, and no `--` separator rule replaces it (user, 2026-11-07).
- The hot-fix targets `main` and is raised as `[F01]` on the Python board (user, 2026-11-07).

## Implementation Details

- One `REF` is accepted and a second is refused as `E_INVALID_USAGE` at exit 2, which is the "exactly one entry" rule the option enforced.
- `--presets`, `-o`, `-c`, `-d`, `--budget`, `-C`, `-v` and `-h` are unchanged, and each parses in any order around the entry.
- `entry()` normalization is untouched: a fragment alone still names `document#fragment` as its remedy, and a complete Markdown-link expression is still refused.
- The design's CLI contract states the positional grammar, its option table and its refusal list. The amendment lands on `engineering` and is pinned by the README badge and the corpus's design links.
- Removing an option is a major contract change; below `1.0.0` the minor carries it, so the release is `contract/v0.18.0` and `python/v0.18.0`, and the build declares `0.18.0` as the change lands.
- The change is one pull request into `main` from `f01-positional-entry`, with the design amendment as a separate commit on `engineering` that the pull request's pin depends on.
