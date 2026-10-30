#!/usr/bin/env bash
# Rebuilds the probe trees and re-runs every observation the README cites.
#
# Usage: bash reproduce.sh > evidence.log 2>&1
#
# Each section heading is its label alone, so the slug of `### LSP-6` is
# `#lsp-6` and the report's citations resolve. The sentence under the
# heading states what the run is meant to show. Every command records its
# exit status, so a verdict rests on an observed outcome rather than on the
# absence of visible output.
#
# Writes nothing outside PROBE and stdout.

PF=/home/mike1/projects/dev/md-composer/.project/main/src/.venv/bin/pf
PROBE=/tmp/solid-probe

rm -rf "$PROBE"
mkdir -p "$PROBE/skill/modes" "$PROBE/skill/rules" "$PROBE/skill/artifacts" "$PROBE/lib"

sec() {
  printf '\n### %s\n\n%s\n\n```console\n' "$1" "$2"
}

end() {
  printf '\n[exit %s]\n```\n' "$?"
}

# A grep exit status is grep's own: 1 means no line matched, which is the
# observation when the point is that a target contributed no headings.
endgrep() {
  printf '\n[exit %s: grep, not pf — 1 means no line matched]\n```\n' "$?"
}

# A diff's exit status is diff's own: 0 when the files agree, 1 when they differ.
enddiff() {
  printf '\n[exit %s: diff, not pf — 0 means the files agree]\n```\n' "$?"
}

run() {
  sec "$1" "$2"
  printf '$ %s\n' "$3"
  shift 3
  "$@" 2>&1
  end
}

# ---------------------------------------------------------------- probe tree

cat > "$PROBE/lib/policy.md" <<'EOF'
# Policy

House policy for every skill in this tree.
EOF

cat > "$PROBE/skill/SKILL.md" <<'EOF'
---
name: demo
prosiform:
  root: "."
  dispatch: Compile the marked link and hand it to a sub-agent.
---
# Demo Skill

Read the mode for your task. The [policy](../../lib/policy.md) governs every mode.

- [Plan](modes/plan.md)
- [Review](modes/review.md)
EOF

cat > "$PROBE/skill/modes/plan.md" <<'EOF'
---
prosiform:
  root: ".."
  group: "modes"
  group-depth: 2
---
# Plan Mode

Scopes work.

## Procedure

1. Follow [the link rule](../rules/common.md#check-every-link).
2. Delegate delivery to [» Record Delivery](../artifacts/delivery.md).

## Outcomes

- A scoped plan.
EOF

cat > "$PROBE/skill/modes/review.md" <<'EOF'
---
prosiform:
  root: ".."
  group: "modes"
  group-depth: 2
---
# Review Mode

Reviews work.

## Procedure

1. Follow [the link rule](../rules/common.md#check-every-link).
EOF

cat > "$PROBE/skill/modes/full.md" <<'EOF'
---
prosiform:
  root: ".."
  group: "modes"
  group-depth: 2
---
# Full Mode

Carries the whole rule set.

## Procedure

1. Follow [the rules](../rules/common.md).
EOF

cat > "$PROBE/skill/modes/compiled.md" <<'EOF'
---
prosiform:
  root: ".."
  group: "modes"
  group-depth: 2
---
# Compiled Mode

Carries a compiled link only.

## Procedure

1. Run [Record Delivery](../artifacts/delivery.md).
EOF

cat > "$PROBE/skill/modes/lone.md" <<'EOF'
---
prosiform:
  root: ".."
  group: "modes"
  group-depth: 2
---
# Lone Mode

## Procedure

1. Do the work, citing no rule.

## Outcomes

- Work done.
EOF

cat > "$PROBE/skill/rules/common.md" <<'EOF'
---
prosiform:
  root: ".."
  group: "rules"
  group-depth: 2
---
# Common

## Check Every Link

- Check every link.

## Wording

- Prefer plain words.

Follow [Agents](rules/agents.md).
EOF

cat > "$PROBE/skill/rules/agents.md" <<'EOF'
---
prosiform:
  root: ".."
  group: "rules"
  group-depth: 2
---
# Agents

## Check Every Link

- Check every link.

Select your harness:

- If you are Claude, compile [¬ Claude](rules/claude.md).
- If you are Codex, compile [¬ Codex](rules/codex.md).
EOF

cat > "$PROBE/skill/rules/claude.md" <<'EOF'
---
prosiform:
  root: ".."
---
# Claude Rules

- Review the change.
EOF

cat > "$PROBE/skill/rules/codex.md" <<'EOF'
---
prosiform:
  root: ".."
---
# Codex Rules

- Keep patches focused.
EOF

cat > "$PROBE/skill/artifacts/delivery.md" <<'EOF'
---
prosiform:
  root: ".."
---
# Record Delivery

## Procedure

1. Sync the tracker.
EOF

cd "$PROBE/skill" || exit 1

# ------------------------------------------------------------------- SRP

run SRP-1 \
  "Selecting one section carries that section and nothing else in its document." \
  "pf -o - 'modes/plan.md#outcomes'" \
  "$PF" -o - 'modes/plan.md#outcomes'

cp "$PROBE/skill/modes/plan.md" "$PROBE/plan-before.md"
"$PF" -o "$PROBE/plan-before.bundle.md" modes/plan.md 2>/dev/null

cat > "$PROBE/skill/modes/refactor.md" <<'EOF'
---
prosiform:
  root: ".."
  group: "modes"
  group-depth: 2
---
# Refactor Mode

Restructures code.

## Procedure

1. Restructure.
EOF

"$PF" -o "$PROBE/plan-after.bundle.md" modes/plan.md 2>/dev/null

sec SRP-2 \
  "An unrelated sibling added to the same group leaves the bundle byte-identical. No output below is the observation."
printf '$ diff plan-before.bundle.md plan-after.bundle.md\n'
diff "$PROBE/plan-before.bundle.md" "$PROBE/plan-after.bundle.md"
enddiff

rm -f "$PROBE/skill/modes/refactor.md"

cat > "$PROBE/skill/rules/bullets.md" <<'EOF'
---
prosiform:
  root: ".."
---
# Bullets

## Style

- Prefer plain words.
- Check every link.
EOF

run SRP-3 \
  "A fragment naming a bullet's text resolves to nothing, so a bullet is not an addressable unit." \
  "pf -o - 'rules/bullets.md#prefer-plain-words'" \
  "$PF" -o - 'rules/bullets.md#prefer-plain-words'

run SRP-4 \
  "The heading holding the bullets is the smallest unit a caller can select." \
  "pf -o - 'rules/bullets.md#style'" \
  "$PF" -o - 'rules/bullets.md#style'

rm -f "$PROBE/skill/rules/bullets.md"

run SRP-5 \
  "A selected section still drags every document it links, so the unit is the section and its closure." \
  "pf -o - 'rules/common.md#wording'" \
  "$PF" -o - 'rules/common.md#wording'

# ------------------------------------------------------------------- OCP

cat > "$PROBE/skill/modes/refactor.md" <<'EOF'
---
prosiform:
  root: ".."
  group: "modes"
  group-depth: 2
---
# Refactor Mode

Restructures code.

## Procedure

1. Restructure.
EOF

run OCP-1 \
  "A new mode joins the group by declaring it, with no existing file edited and no manifest to update." \
  "pf -o - modes/plan.md modes/refactor.md" \
  "$PF" -o - modes/plan.md modes/refactor.md

rm -f "$PROBE/skill/modes/refactor.md"

cat > "$PROBE/skill/rules/depth.md" <<'EOF'
---
prosiform:
  root: ".."
  group: "rules"
  group-depth: 3
---
# Depth

### Own Heading
EOF

cat > "$PROBE/skill/modes/depth.md" <<'EOF'
---
prosiform:
  root: ".."
  group: "modes"
  group-depth: 2
---
# Depth Mode

## Procedure

1. [Depth](../rules/depth.md)
2. [Common](../rules/common.md)
EOF

run OCP-2 \
  "A new member whose heading depth differs is refused, so it must be reshaped to the group's existing depth." \
  "pf -o - modes/depth.md" \
  "$PF" -o - modes/depth.md

rm -f "$PROBE/skill/rules/depth.md" "$PROBE/skill/modes/depth.md"

cat > "$PROBE/skill/modes/wording.md" <<'EOF'
---
prosiform:
  root: ".."
  dispatch: Dispatch instead.
  group: "modes"
  group-depth: 2
---
# Wording Mode

## Procedure

1. [» Delivery](../artifacts/delivery.md)
EOF

run OCP-3 \
  "A member declaring the dispatch text while its siblings declare none puts its own sentence in the bundle: the declaration is not additive." \
  "pf -o - modes/wording.md modes/plan.md" \
  "$PF" -o - modes/wording.md modes/plan.md

cat > "$PROBE/skill/modes/wording2.md" <<'EOF'
---
prosiform:
  root: ".."
  dispatch: Compile it elsewhere.
  group: "modes"
  group-depth: 2
---
# Wording Two

## Procedure

1. [» Delivery](../artifacts/delivery.md)
EOF

run OCP-4 \
  "Two members declaring different dispatch texts are refused, naming both locations." \
  "pf -o - modes/wording.md modes/wording2.md" \
  "$PF" -o - modes/wording.md modes/wording2.md

rm -f "$PROBE/skill/modes/wording.md" "$PROBE/skill/modes/wording2.md"

# ------------------------------------------------------------------- LSP

mkdir -p "$PROBE/lsp/strict" "$PROBE/lsp/loose" "$PROBE/lsp/elsewhere" "$PROBE/lsp/plain"

cat > "$PROBE/lsp/strict/rules.md" <<'EOF'
---
prosiform:
  root: ".."
  group: "rules"
  group-depth: 2
---
# Style

## Naming

- snake case in file names

## Length

- 88 columns
EOF

cat > "$PROBE/lsp/loose/rules.md" <<'EOF'
---
prosiform:
  root: ".."
  group: "rules"
  group-depth: 2
---
# Style

## Naming

- camel case in function names

## Length

- 100 columns
EOF

cat > "$PROBE/lsp/use-strict.md" <<'EOF'
---
prosiform:
  root: "."
---
# App

1. [Style](strict/rules.md#naming)
EOF

cat > "$PROBE/lsp/use-loose.md" <<'EOF'
---
prosiform:
  root: "."
---
# App

1. [Style](loose/rules.md#naming)
EOF

cd "$PROBE/lsp" || exit 1
"$PF" -o "$PROBE/lsp/strict.bundle.md" use-strict.md 2>/dev/null
"$PF" -o "$PROBE/lsp/loose.bundle.md" use-loose.md 2>/dev/null

sec LSP-1 \
  "One provider swapped for another at a different path, with the same heading set, differs only in its prose."
printf '$ diff strict.bundle.md loose.bundle.md\n'
diff "$PROBE/lsp/strict.bundle.md" "$PROBE/lsp/loose.bundle.md"
enddiff

cp "$PROBE/lsp/strict/rules.md" "$PROBE/lsp/strict/keep.md"
sed -i 's|^## Naming|## House Naming|' "$PROBE/lsp/strict/rules.md"

run LSP-2 \
  "A provider that retitles a heading fails at the consumer's own line, with the chain and a remedy." \
  "pf -o - use-strict.md" \
  "$PF" -o - use-strict.md

cp "$PROBE/lsp/strict/keep.md" "$PROBE/lsp/strict/rules.md"
rm -f "$PROBE/lsp/strict/keep.md"

cp "$PROBE/lsp/strict/rules.md" "$PROBE/lsp/elsewhere/rules.md"

cat > "$PROBE/lsp/use-moved.md" <<'EOF'
---
prosiform:
  root: "."
---
# App

1. [Style](elsewhere/rules.md#naming)
EOF

"$PF" -o "$PROBE/lsp/moved.bundle.md" use-moved.md 2>/dev/null

sec LSP-3 \
  "The same provider relocated within its group keeps its destination, because the destination derives from the heading and not the path."
printf '$ diff strict.bundle.md moved.bundle.md\n'
diff "$PROBE/lsp/strict.bundle.md" "$PROBE/lsp/moved.bundle.md"
enddiff

cat > "$PROBE/lsp/plain/style-guide.md" <<'EOF'
# Style Guide

## Naming

- snake case in file names
EOF
cat > "$PROBE/lsp/plain/other-name.md" <<'EOF'
# Style Guide

## Naming

- snake case in file names
EOF
cat > "$PROBE/lsp/use-plain-a.md" <<'EOF'
# App

1. [Style](plain/style-guide.md#naming)
EOF
cat > "$PROBE/lsp/use-plain-b.md" <<'EOF'
# App

1. [Style](plain/other-name.md#naming)
EOF

cat > "$PROBE/lsp/use-whole-a.md" <<'EOF'
# App

1. Read [the guide](plain/style-guide.md).
EOF
cat > "$PROBE/lsp/use-whole-b.md" <<'EOF'
# App

1. Read [the guide](plain/other-name.md).
EOF

run LSP-4 \
  "Outside a group the file heading states the filename, so a whole-document reference is named after the path." \
  "pf -o - use-whole-a.md" \
  "$PF" -o - use-whole-a.md

run LSP-5 \
  "The same bytes under another filename give a whole-document reference another destination, so a file-named provider is substitutable only at the same path." \
  "pf -o - use-whole-b.md" \
  "$PF" -o - use-whole-b.md

run LSP-5b \
  "A fragment reference is unaffected by the filename, because a source fragment resolves against the provider's own headings." \
  "pf -o - use-plain-b.md" \
  "$PF" -o - use-plain-b.md

mkdir -p "$PROBE/lsp/stab/g/a" "$PROBE/lsp/stab/g/b"

cat > "$PROBE/lsp/stab/g/a/rules.md" <<'EOF'
---
prosiform:
  root: ".."
  group: "g"
  group-depth: 2
---
# Rules A

## Style

- plain words
EOF

cat > "$PROBE/lsp/stab/one.md" <<'EOF'
---
prosiform:
  root: "."
---
# App

1. Read [the rules](g/a/rules.md).
EOF

cat > "$PROBE/lsp/stab/g/b/rules.md" <<'EOF'
---
prosiform:
  root: ".."
  group: "g"
  group-depth: 2
---
# Rules B

## Style

- plain words too
EOF

cat > "$PROBE/lsp/stab/two.md" <<'EOF'
---
prosiform:
  root: "."
---
# App

1. Read [the rules](g/a/rules.md).

2. Read [the others](g/b/rules.md).
EOF

cd "$PROBE/lsp/stab" || exit 1

run LSP-6 \
  "While the group holds one member, a whole-document reference resolves to the merged heading." \
  "pf -o - one.md" \
  "$PF" -o - one.md

run LSP-7 \
  "Adding a second member repoints that same reference to a variant heading, so an addition is not address-preserving." \
  "pf -o - two.md" \
  "$PF" -o - two.md

mkdir -p "$PROBE/lsp/pool"

cat > "$PROBE/lsp/pool/plan.md" <<'EOF'
---
prosiform:
  root: "."
  group: "modes"
  group-depth: 2
---
# Plan Mode

## Procedure

Scope the work.
EOF

cat > "$PROBE/lsp/pool/review.md" <<'EOF'
---
prosiform:
  root: "."
  group: "modes"
  group-depth: 2
---
# Review Mode

## Procedure

Review the work.
EOF

cat > "$PROBE/lsp/pool/entry.md" <<'EOF'
---
prosiform:
  root: "."
---
# Entry

The planning run is [plan.md](plan.md#procedure) and the review run is [review.md](review.md#procedure).
EOF

cd "$PROBE/lsp/pool" || exit 1

run LSP-8 \
  "Two documents' same-named sections share one destination, so the review link lands on a heading whose first subsection is the plan's content." \
  "pf -o - entry.md" \
  "$PF" -o - entry.md

# ------------------------------------------------------------------- ISP

cd "$PROBE/skill" || exit 1
"$PF" -o "$PROBE/full.bundle.md" modes/full.md 2>/dev/null
"$PF" -o "$PROBE/plan.bundle.md" modes/plan.md 2>/dev/null

sec ISP-1 \
  "A deferred link carries its text, strips the mark and opens nothing: the target document contributes no headings."
printf '$ grep -n "Claude" full.bundle.md\n'
grep -n "Claude" "$PROBE/full.bundle.md"
printf '\n$ grep -c "^# Claude Rules" full.bundle.md\n'
grep -c "^# Claude Rules" "$PROBE/full.bundle.md"
endgrep

sec ISP-2 \
  "A dispatched link withholds its target exactly as a deferral does and publishes its mark, because the mark states who compiles the slot."
printf '$ grep -n "Record Delivery" plan.bundle.md\n'
grep -n "Record Delivery" "$PROBE/plan.bundle.md"
printf '\n$ grep -c "^# Record Delivery" plan.bundle.md\n'
grep -c "^# Record Delivery" "$PROBE/plan.bundle.md"
endgrep

run ISP-3 \
  "stdout is the bundle alone and the entry destinations go to stderr as data, so a wrapper reads them without scraping Markdown." \
  "pf -o - modes/plan.md 2>/dev/null" \
  bash -c "\"$PF\" -o - modes/plan.md 2>/dev/null"

cat > "$PROBE/skill/modes/missing.md" <<'EOF'
---
prosiform:
  root: ".."
  group: "modes"
  group-depth: 2
---
# Missing Mode

## Procedure

1. [» Gone](../artifacts/gone.md)

2. [¬ Also Gone](../artifacts/also-gone.md)
EOF

run ISP-4 \
  "A withheld target that does not exist is refused, because a dispatch an agent will follow is one that can succeed." \
  "pf -c modes/missing.md" \
  "$PF" -c modes/missing.md

rm -f "$PROBE/skill/modes/missing.md"

sec ISP-5 \
  "A consumer carries a document it never names, reached through one it does, so segregation cannot be enforced from outside the consumer."
printf '$ grep -n "Agents" modes/full.md\n'
grep -n "Agents" "$PROBE/skill/modes/full.md"
printf '(no output above: full.md never names agents.md)\n\n'
printf '$ grep -c "^### Agents" full.bundle.md\n'
grep -c "^### Agents" "$PROBE/full.bundle.md"
endgrep

# ------------------------------------------------------------------- DIP

cd "$PROBE" || exit 1
"$PF" -o "$PROBE/compiled-skill.bundle.md" skill/modes/compiled.md 2>/dev/null
cd "$PROBE/skill" || exit 1
"$PF" -o "$PROBE/compiled-parent.bundle.md" modes/compiled.md 2>/dev/null

sec DIP-1a \
  "Over a closure of compiled links the bundle is independent of the working directory, because every root is declared by its source. No output below is the observation."
printf '$ diff compiled-skill.bundle.md compiled-parent.bundle.md\n'
diff "$PROBE/compiled-skill.bundle.md" "$PROBE/compiled-parent.bundle.md"
enddiff

cd "$PROBE" || exit 1
"$PF" -o "$PROBE/full-skill.bundle.md" skill/modes/full.md 2>/dev/null
cd "$PROBE/skill" || exit 1
"$PF" -o "$PROBE/full-parent.bundle.md" modes/full.md 2>/dev/null

sec DIP-1b \
  "Over a closure holding withheld links, only those destinations move, because a withheld destination is deliberately working-directory-relative so a later invocation can be handed it."
printf '$ diff full-skill.bundle.md full-parent.bundle.md\n'
diff "$PROBE/full-skill.bundle.md" "$PROBE/full-parent.bundle.md"
enddiff

run DIP-2 \
  "The caller cannot retarget a dependency root: structure is source-owned and only operational flags are the caller's." \
  "pf -o - modes/plan.md -r ." \
  "$PF" -o - modes/plan.md -r .

run DIP-3 \
  "The caller cannot retarget a group for the same reason." \
  "pf -o - modes/plan.md -g other" \
  "$PF" -o - modes/plan.md -g other

mkdir -p "$PROBE/dip"
cat > "$PROBE/dip/provider-one.md" <<'EOF'
# Provider One

## Naming

- snake case
EOF
cat > "$PROBE/dip/provider-two.md" <<'EOF'
# Provider Two

## Naming

- camel case
EOF
cat > "$PROBE/dip/role.md" <<'EOF'
---
prosiform:
  root: "."
---
# Lint Role

Follow [the provider](provider-one.md).
EOF
cat > "$PROBE/dip/app.md" <<'EOF'
---
prosiform:
  root: "."
---
# App

1. Follow [Lint](role.md).
EOF

cd "$PROBE/dip" || exit 1

run DIP-4 \
  "An indirection document is the only seam available: the consumer names a role and never names a provider." \
  "pf -o - app.md" \
  "$PF" -o - app.md

sed -i 's|provider-one.md|provider-two.md|' role.md

run DIP-5 \
  "Repointing the role swaps the provider with no edit to the consumer." \
  "pf -o - app.md" \
  "$PF" -o - app.md

cat > "$PROBE/dip/rule-links-up.md" <<'EOF'
# Rule

## Naming

Read [the caller](app.md) before applying this.
EOF
cat > "$PROBE/dip/app2.md" <<'EOF'
---
prosiform:
  root: "."
---
# App Two

1. Follow [Rule](rule-links-up.md).
EOF

run DIP-6 \
  "Nothing enforces a layering direction: a provider that links its consumer drags the consumer's whole closure into the bundle." \
  "pf -o - app2.md" \
  "$PF" -o - app2.md

# ------------------------------------------------------- cross-cutting

mkdir -p "$PROBE/cross"
cd "$PROBE/cross" || exit 1

cat > a.md <<'EOF'
# Shared Rule

- Check every link.
EOF
cp a.md b.md
cat > app.md <<'EOF'
---
prosiform:
  root: "."
---
# App

1. [A](a.md)

2. [B](b.md)
EOF

run X-1 \
  "Identical bytes reachable at two paths are two source identities, so both are emitted under their own headings." \
  "pf -o - app.md" \
  "$PF" -o - app.md

"$PF" -o "$PROBE/cross/bundle.md" app.md 2>/dev/null

run X-2 \
  "A bundle is not a source: offering one back as input is refused." \
  "pf -o - bundle.md" \
  "$PF" -o - bundle.md

cat > html.md <<'EOF'
# Html

<div>raw</div>
EOF

run X-3 \
  "Raw HTML is outside the declared profile and is refused rather than copied." \
  "pf -o - html.md" \
  "$PF" -o - html.md

cat > container.md <<'EOF'
# Container

- item
  # In List
  text
EOF

run X-4 \
  "A heading a container carries is not a selectable section root." \
  "pf -o - 'container.md#in-list'" \
  "$PF" -o - 'container.md#in-list'

cd "$PROBE/skill" || exit 1

run X-5 \
  "A mode citing no shared rule at all bundles cleanly, so completeness follows the links an author wrote." \
  "pf -o - modes/lone.md" \
  "$PF" -o - modes/lone.md

# ---------------------------------------------------------------- baseline

sec BASELINE-CORPUS \
  "The corpus the build under test is held to. Every behaviour above is conformant to this corpus, so where this report calls a behaviour intended, this run is the ground."
cd /home/mike1/projects/dev/md-composer/.project/main || exit 1
PROSIFORM_BUILD="$PF" uv run --project src --frozen python checks/corpus.py 2>&1 | tail -1
end

sec BASELINE-BUILD \
  "The build these observations are of."
printf '$ pf -v ; git rev-parse HEAD\n'
"$PF" -v
git rev-parse HEAD
end
