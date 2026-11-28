# F43 Verification

Reviewed head: bb0c444c781816d777911f40d14945d737ac05d1. Target: main. Python build: 0.37.0, profile prosiform-markdown.

## Required Checks

The final [make check](make-check.log) exits 0: **2114 source tests, 1266 check-harness tests and 711 corpus fixtures pass**. Frozen lock, lint, formatting, types, reachability, installed-wheel smoke, layout, command tables, online links, vocabulary, invocation, conformance, independence and release-tag checks pass.

The earlier [network-isolated attempt](sandbox-attempt.log) reaches 2101 passed tests but cannot download hatchling for 13 wheel-install setup cases. The subsequent [pre-version host run](pre-version-check.log) passes all runtime checks and stops at the final vocabulary check on one fixture description. Its wording correction passes [independence](independence.log). Both attempts are retained; the final full check passes at the committed 0.37.0 head.

## Version Choice

The [previous 0.36.0 corpus](previous-corpus.log), pinned at 8cedda4cc06b0486168addc05f057161192a22a6, has **708 passes and two output differences out of 710 fixtures** against 0.37.0. Both differences are the immediate and deferred inline Mermaid labels corrected by F43. The repository's pre-1.0 policy assigns the next minor when previous output bytes change. [Version validation](version-validation.log) confirms the installed 0.37.0 wheel and lockfile. Release tags await the release merge.

## Review

The [exact-head review](agent-review.json) inspects all changed definitions, affected callers, negative candidate checks and complete generic expected bundles. It records no findings. The [specimen index](specimens/README.md) links identical source and actual before/after bundles. Compiler output inspection establishes no native-agent performance claim.
