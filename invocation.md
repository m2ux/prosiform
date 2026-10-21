# Invocation

The command answers to every option the contract declares, and `prosiform --help` reports them with their defaults and the exit statuses. The tables in this section reproduce that output word for word, and `make invocation` holds each row to the help the build under test prints, so the invocation a caller reads here and the one the command offers cannot drift apart.

| Option | Effect |
| --- | --- |
| `REF` | an entry reference: a root-relative document, a document and a fragment, or a fragment alone with --from |
| `--root DIR` | the allowed source root; required, and resolved from the working directory |
| `--from DOC` | the root-relative referring document a fragment-only reference resolves against |
| `-o, --output FILE` | publish the validated bundle to FILE, atomically; default or - is standard output |
| `--group SLUG:DEPTH` | merge every document under a directory named SLUG at source heading level DEPTH, 1 through 6; repeatable, once per slug |
| `--check` | discover, bundle and validate without emitting or publishing the bundle; accepted with --output |
| `--diagnostics {text,json}` | the diagnostic format on standard error; default text |
| `--fault {source-changed,internal}` | perform a fault on the run itself, so a conformance run reaches an outcome no source tree states; none by default |
| `--max-files N` | the budget of distinct source documents opened; a positive decimal integer, default 256 |
| `--max-file-bytes N` | the budget of raw bytes in one source; a positive decimal integer, default 1048576 |
| `--max-input-bytes N` | the budget of raw source bytes, counted once per source; a positive decimal integer, default 16777216 |
| `--max-output-bytes N` | the budget of bytes of the complete bundle; a positive decimal integer, default 262144 |
| `--max-targets N` | the budget of distinct document and section targets discovered; a positive decimal integer, default 4096 |
| `--max-links N` | the budget of authored link and image occurrences in selected content; a positive decimal integer, default 32768 |
| `--max-nesting N` | the budget of levels of container nesting in one source; a positive decimal integer, default 64 |
| `--max-expansion-depth N` | the budget of link hops from the nearest entry reference; a positive decimal integer, default 8 |
| `--version` | report the tool version and the profile identifier |
| `--help` | show this usage, the defaults, and the exit-status meanings |

Each effect is that argument's own help text, so the default an option carries is stated where the option is. A budget is a positive decimal integer; zero is refused rather than read as unlimited.

Bundling runs under it: a run reads every source its entry references name, requires it to be valid UTF-8, removes the one leading byte-order mark and the one leading frontmatter block it may carry ahead of its content, parses what is left under the `skill-markdown-v1` profile, selects the whole document or the section each reference names, and publishes each contributing document as one file group headed by that document's root-relative path. It then follows the dependencies its selected content carries — a link resolving to a Markdown document under the allowed source root — resolving each against the document carrying it and bundling what it reaches, until a round of the traversal reaches nothing new. A link resolving outside that root is a citation: it is emitted as its author wrote it and carries no document into the bundle. A source that is not valid UTF-8, one whose frontmatter opener no later line closes, one carrying raw HTML or an unsupported dependency or section-naming construct, two documents whose paths differ only by Markdown extension, and a reference under the root naming no document or no heading in the document it resolves to each return `1` naming the defect and the line of the file it sits on. A compiled link reaches the bundle with its destination repointed at the heading the bundle emits for what it named.

One mark says otherwise, and it defers a compilation rather than asking for one. A link whose text opens with `¬` is not compiled by this run: its target is confirmed to exist and carried nowhere, so the document it names is neither opened nor bundled through it. The bundle emits the link's text with its mark exactly as the author wrote it, the spaces following the character included, and gives the link its target's path from the allowed source root as its destination, so the agent reading the bundle needs that root and nothing else to compile it in a run of its own. A deferred reference naming no document, or no heading in the document it resolves to, fails like any other the root makes this run responsible for.

```bash
# A procedure and everything it reaches. The routing document the caller read
# to find it, SKILL.md, is not an entry reference and is not bundled.
prosiform --root example/work-tracker modes/plan-mode.md

# Selected sections
prosiform --root example/work-tracker 'artifacts/epic.md#delivery-findings'

# Every document under a named directory merged at a heading level
prosiform --root example/work-tracker \
  --group artifacts:2 --group modes:2 \
  modes/plan-mode.md

# Compile and validate without publishing
prosiform --root example/work-tracker --check modes/plan-mode.md
```

Standard output carries exactly one thing per run: the bundle a compiling run publishes, the response an informational run returns, or nothing at all. Diagnostics go to standard error, as text for a reader or, under `--diagnostics json`, as one JSON object per line and nothing else. A bundle opens by naming what it was built for, so the caller reaches its procedure without searching:

```markdown
This bundle was built for [modes/plan-mode](#modesplan-mode); everything else is material it references.
```

## Exit statuses

A run returns the status naming the category of its outcome, and a caller reads the result from that status rather than from what reached standard output.

| Exit | Meaning |
| --- | --- |
| `0` | successful compilation, validation, or informational response |
| `1` | input, dependency, policy, safety, or resource-limit failure |
| `2` | invalid usage or option combination |
| `3` | output publication or delivery failure, a broken pipe among them |
| `4` | unexpected internal error |

## A failed run stops the work

A failed run publishes nothing. The caller halts and surfaces the diagnostic, and reading the sources itself is unsupported: there is no option, no status and no documented path by which a caller meeting a failure resolves the closure for itself. A fallback restores the behaviour bundling replaces, and restores it silently, so the failure teaches nothing and the next run fails the same way.

## Supported environment

The supported environment is POSIX: Linux and macOS. The confinement of a run to its allowed source root rests on rooted, no-follow source access, which descends a path one segment at a time through the `O_NOFOLLOW`, `O_DIRECTORY` and `O_CLOEXEC` open flags, so a source reached through a symbolic link below the root is refused by the open rather than by a string comparison ahead of it. A platform offering no such flags cannot enforce that policy, and the build refuses to start there rather than weakening the confinement to a check on the spelling of a path.
