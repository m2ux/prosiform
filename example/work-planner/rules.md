---
prosiform:
  root: "."
---
# Rules

- **Decisions.**
  A question the user must decide is put as an interview, one question at a time. A decision the run's [allowance](artifacts/plan-change.md#allowance) covers is taken with its recommended option rather than asked. Record each decision in the affected issues and, when there is one, the planning record.
  - A plain-language paragraph before the question gives the context the user needs to answer it.
  - The question offers more than one choice. The recommended choice is marked on its option.
  - Wait for the user's answer. An unanswered question stays pending. A recommendation or elapsed time supplies no answer.
  - The user can select Other and specify a response beyond the options.
  - Use the native tool for presenting the question when one is available.
- **Layers.**
  Modes, protocols, artifacts. A mode aggregates protocol calls, as an application calls services; a protocol runs artifact operations and other protocols; an artifact runs neither. A call goes down the stack, never up. A mode reaches an artifact operation directly only where no protocol owns that change.
- **Execution.**
  A call passes its named inputs. A protocol is one change that lands in several artifacts together, and is run whole. Run another mode, a protocol, or a named subsection only where the procedure calls it; finish that call and return its result before continuing, unless the procedure explicitly dispatches concurrent work.
