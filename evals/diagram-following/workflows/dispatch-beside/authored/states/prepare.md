# Prepare

Write `actions/prepare.txt` containing `prepared`.

1. Hand the plan to a sub-agent: [plan](../plan.md#work). The sub-agent follows that section from its start and returns its result, putting no question to the user: it returns each question unanswered, and you put each returned question to the user before handing the answers back.
2. Hand the change to sub-agents of their own: [source](../review.md#source) and [tests](../review.md#tests). Start a sub-agent of its own for each, together, and continue when every one has returned. A returned question is put to the user with the other's result, and only the item that asked is handed the answers.

**Next.** Take the transition out of this state.

