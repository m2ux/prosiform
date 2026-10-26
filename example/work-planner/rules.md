---
prosiform:
  root: "."
---
# Rules

- **Decisions.**
  Ask one at a time, following the [¬ interview rules](guidelines.md#modes). A decision the run's [allowance](artifacts/plan-change.md#allowance) covers is taken with its recommended option rather than asked. Record each decision in the affected issues and, when there is one, the planning record.
- **Layers.**
  Modes, protocols, artifacts. A mode aggregates protocol calls, as an application calls services; a protocol runs artifact operations and other protocols; an artifact runs neither. A call goes down the stack, never up. A mode reaches an artifact operation directly only where no protocol owns that change.
- **Execution.**
  A call passes its named inputs. A protocol is one change that lands in several artifacts together, and is run whole. Run another mode, a protocol, or a named subsection only where the procedure calls it; finish that call and return its result before continuing, unless the procedure explicitly dispatches concurrent work.
