# Baseline fact coverage

Reviewed against the complete invocation at `9e11aedb062d8afdaffe111e6af9af454a1b8a68`. Every row below is retained in the candidate invocation. Option and exit rows are also checked against live help by `make invocation`. Short spellings follow the confirmed mapping; they do not change the facts.

| Baseline fact | Candidate location |
| --- | --- |
| Compile a document or section and its local Markdown dependencies into one validated bundle | Opening; REF row; Closure |
| Help lists options, defaults and exit statuses; make invocation verifies agreement | Options introduction; -h row |
| REF is a root-relative document, document plus fragment, or fragment alone with referring document | REF row |
| Source root required and resolved relative to working directory | -r row |
| Referring document is root-relative and supplies fragment-only references | -f row |
| File output is atomic and validated; default or dash is stdout | -o row |
| Group every document under directories named by slug at source heading depth 1–6 | -g row |
| Groups repeat, once per slug | -g row |
| Check discovers, bundles and validates; emits/publishes nothing; accepts output option | -c row |
| Diagnostics choose text or JSON on stderr, default text | -d row; Output |
| Fault injection acts on the run for conformance outcomes unavailable from a source tree; source-changed/internal choices; default none | -x row (run fault injection, choices and default) |
| Files budget counts distinct opened documents; default 256 | -F row |
| File bytes budget counts raw bytes in one source; default 1048576 | -B row |
| Input bytes budget counts raw bytes once per source; default 16777216 | -I row |
| Output bytes budget counts complete bundle bytes; default 262144 | -O row |
| Targets budget counts distinct document/section targets discovered; default 4096 | -T row |
| Links budget counts authored link/image occurrences in selected content; default 32768 | -L row |
| Nesting budget counts source container levels; default 64 | -N row |
| Expansion budget counts link hops from nearest entry; default 8 | -E row |
| Every budget requires a positive decimal integer; zero invalid | Options introduction; all budget rows |
| Code listing reports errors and warnings this build can emit | -C row |
| Version reports tool version and profile identifier | -v row |
| Help shows usage, defaults, exit-status meanings | -h row |
| Examples run from repository root; worked examples provide input/output excerpts | Examples introduction |
| Procedure bundling example with same root and entry | Example command 1 |
| Section selection example with same root and fragment | Example command 2 |
| Repeated grouping example with same root, slugs, depths and entry | Example command 3 |
| Validation-only example with same root and entry | Example command 4 |
| Sources valid UTF-8 | Sources |
| Strip one leading byte-order mark and one leading frontmatter block | Sources |
| Parse under skill-markdown-v1 | Sources |
| Entries select whole documents or named sections | Closure |
| Follow in-root Markdown links relative to source until no new dependencies remain | Closure |
| Each contributing document has title-cased root-relative-path group heading unless merged | Groups |
| Compiled links target bundle headings | Closure |
| Outside-root links remain authored and contribute no content | Closure |
| Merged directory heading is title-cased | Groups |
| Member subsections hold content above grouping depth | Groups |
| Overview wraps those subsections if merged sections exist at grouping depth; otherwise directly under group | Groups |
| Distinct member destinations | Groups |
| Generated member headings use shortest distinguishing path and title case | Groups |
| Authored heading and filesystem-path spelling retained | Groups |
| Leading ¬ in link text defers target compilation | Deferred links |
| Deferred target document and named section must exist but add no content through that link | Deferred links |
| Emitted deferred text, marker and following spaces retained | Deferred links |
| Deferred destination is root-relative, ready for separate run | Deferred links |
| Invalid UTF-8 and unterminated frontmatter fail | Invalid input |
| Raw HTML and unsupported dependency or section-naming constructs fail | Invalid input |
| Document paths differing only by Markdown extension fail | Invalid input |
| Missing in-root documents/sections, including deferred targets, fail | Invalid input |
| Invalid-input failures return 1 with defect and source location | Invalid input |
| Stdout carries bundle, informational response or nothing | Output |
| Bundle opens with entry-point links and the specified declaration example | Output example, byte-identical |
| Diagnostics on stderr; default text; JSON is one object per line | Output |
| Exit 0: successful compilation, validation or informational response | Exit table |
| Exit 1: input, dependency, policy, safety or resource-limit failure | Exit table |
| Exit 2: invalid usage or option combination | Exit table |
| Exit 3: output publication/delivery failure, including broken pipe | Exit table |
| Exit 4: unexpected internal error | Exit table |
| Caller uses status to determine outcome | Output |
| Failed run publishes nothing; caller halts and surfaces diagnostic | Failed-run paragraph |
| Reading sources itself is unsupported | Failed-run paragraph |
| Supported POSIX environment: Linux and macOS | Supported environment |
| Root confinement uses rooted no-follow access and O_NOFOLLOW, O_DIRECTORY, O_CLOEXEC | Supported environment |
| Refuse symlinks below root | Supported environment |
| Refuse startup when required flags unavailable | Supported environment |

The navigation-only grouped-example link is consolidated into the existing worked-examples link. Its behavioral explanation remains self-contained in Groups. All 66 fact rows are covered; no baseline contract fact is intentionally omitted.
