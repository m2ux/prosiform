# Decision — Where a Build States the Codes It Can Emit

## The question the task carried

Whether a build reports its codes through the command's own surface, or whether
a corpus reaching every code is the stronger reading.

## The decision

A build reports its codes through the command's own surface, which is the
reading the task's own Proposal states.

- **The machinery already exists and names no implementation.**
  The documented invocation is held to the build's own `--help` output in both
  directions, and reaches that build through `PROSIFORM_BUILD` as a subprocess.
  A build stating its codes on that same surface is held by a comparison that
  names no module, no language and no function of any build.
- **A fixture per code establishes something narrower.**
  A corpus reaching every code shows that each declared code is producible. It
  cannot show that a build carries *no further* code, which is the direction a
  build silently carrying an undeclared code fails in, and it is the direction
  the contract's claim turns on.
- **The corpus reading is already measured elsewhere.**
  The harness requires every code either catalogue holds to be declared by a
  fixture, and the conformance report lists each declared name with the fixtures
  reaching it. Adding a fixture per code would duplicate that measurement
  rather than extend it.

## Where the comparison lives

The criterion names the conformance report's declared-surface listing, so the
comparison is rendered there: each declared code states whether the build
reports it, and a code the build reports that the contract declares nowhere is
listed beside them. Both are report failures.

## What that costs, and why it is paid

`checks/conformance.py` reads the design, the corpus and now the build under
test, and `checks/independence.py` renders that report to scan it, so both reach
the build through `PROSIFORM_BUILD` and fail without one.

- **A comparison that skips says nothing.**
  The repository refuses a corpus run with no build configured rather than
  passing over it. A code comparison that quietly did nothing when no build was
  named would sit inside a passing suite reporting a surface it never read.
- **The independence scan gains reach.**
  A code a build reports that the contract declares nowhere is rendered into the
  report, so the independence check scans it like any other entry. A build
  reporting a code named for a language or for the machinery of its own
  packaging is reported as what it is.

## The shape of the reported set

Each part of the build that declares a code publishes the codes it declares, and
the command composes the set it reports from those. The set a run states is
therefore the set the build holds, rather than a second list written beside the
first that could disagree with it.
