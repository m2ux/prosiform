"""The budgets a run holds: one entry per declared budget, each at its default
unless an entry names it."""

import pytest

from prosiform.limits import BUDGETS, NAMED, Budget, Crossed, in_force


def test_a_run_naming_no_budget_holds_every_budget_at_its_default() -> None:
    limits = in_force({})
    assert set(limits.declared) == set(BUDGETS)
    assert all(limits.of(budget) == budget.default for budget in BUDGETS)


@pytest.mark.parametrize("budget", BUDGETS, ids=lambda budget: budget.name)
def test_a_named_budget_holds_its_figure_and_the_rest_their_defaults(
    budget: Budget,
) -> None:
    limits = in_force({budget: budget.default + 1})
    assert set(limits.declared) == set(BUDGETS)
    assert limits.of(budget) == budget.default + 1
    assert all(
        limits.of(other) == other.default for other in BUDGETS if other is not budget
    )


def test_each_budget_is_declared_once_under_its_own_name() -> None:
    assert len(BUDGETS) == len(set(BUDGETS)) == len(NAMED)
    assert all(NAMED[budget.name] is budget for budget in BUDGETS)


def test_a_figure_past_the_budget_in_force_is_crossed() -> None:
    [budget, *_] = BUDGETS
    limits = in_force({budget: 3})
    limits.hold(budget, 3)
    with pytest.raises(Crossed) as crossed:
        limits.hold(budget, 4)
    assert (crossed.value.budget, crossed.value.limit, crossed.value.counted) == (
        budget,
        3,
        4,
    )
