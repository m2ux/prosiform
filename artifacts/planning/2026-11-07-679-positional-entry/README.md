# Positional Entry — November 2026

> Hot-fix · Created 2026-11-07

## Executive Summary

`pf` requires `--entry` before the document it compiles. The option carries no decision: a run compiles exactly one document, and the option's only job is to name it. This hot-fix returns the entry reference to a positional argument, so `pf guide.md --presets checks` compiles what `pf --entry guide.md --presets checks` compiles today.

The option arrived with the tag selection in `ad0332c74`, replacing the positional `references` list, and the planning record states the two as separate decisions. Reversing the entry spelling alone leaves `--presets` untouched. The change is wide rather than deep: the compiler reads one normalized reference either way, and the corpus harness already accepts a positional entry.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Issue body](issue-body.md) | The published hot-fix body |
| [Change surface](change-surface.md) | Every file the change touches, by area, with the treatment each needs |
| [Decisions](decisions.md) | The confirmed grammar, the dropped leading-dash case and the version |

## Links

| Resource | Link |
| --- | --- |
| Hot-fix issue | https://github.com/m2ux/prosiform/issues/679 |
| Python board | https://github.com/users/m2ux/projects/18 |
| Design, CLI contract | https://github.com/m2ux/prosiform/blob/795bbfb67c66b02193f0313138f59f18aa6c5274/artifacts/planning/2026-10-17-prosiform-v1/design.md#cli-contract |
| Link-Tag Presets record | https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-06-i10-link-tag-presets/decisions.md |
