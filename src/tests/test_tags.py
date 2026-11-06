"""Preset-list normalization and the decoded strings its callers supply."""

import shlex
from itertools import permutations

import pytest

from prosiform.profile import parse
from prosiform.tags import read


@pytest.mark.parametrize("text", [None, "", " \t\r\n", ",", " , , \t,\n"])
def test_absent_or_empty_lists_select_no_names(text: str | None) -> None:
    assert read(text) == frozenset()


def test_each_name_loses_surrounding_unicode_whitespace() -> None:
    assert read(" \tChecks \r\n,\u2003Draft\u00a0 , \t") == {"checks", "draft"}


def test_names_use_unicode_case_folding() -> None:
    assert read("Straße,STRASSE,Σ,σ,ς") == {"strasse", "σ"}


def test_complete_names_keep_internal_spaces_and_word_boundaries() -> None:
    names = read("Checklist,Checks and Draft,Checks  and Draft")
    assert names == {"checklist", "checks and draft", "checks  and draft"}
    assert "checks" not in names
    assert "draft" not in names


def test_repetition_and_input_order_have_no_meaning() -> None:
    for names in permutations(("Checks", "draft", "CHECKS", "", " Draft ")):
        assert read(",".join(names)) == {"checks", "draft"}


def test_tokens_have_no_comma_quoting_or_escaping_grammar() -> None:
    assert read('"checks,draft"') == {'"checks', 'draft"'}
    assert read(r"checks\,draft") == {"checks\\", "draft"}


def test_normalization_retains_names_for_the_destination_to_match() -> None:
    assert read("DEFAULT,Unknown,checks") == {"default", "unknown", "checks"}


def test_the_selection_is_immutable() -> None:
    assert isinstance(read("checks,draft"), frozenset)


@pytest.mark.parametrize(
    "source",
    [
        '[Plan](guide.md " Checks&#44;Draft ")',
        '[Plan][target]\n\n[target]: guide.md " Checks&#44;Draft "\n',
    ],
)
def test_parsed_titles_and_shell_decoded_values_supply_the_same_list(
    source: str,
) -> None:
    titles = [
        child.attrGet("title")
        for token in parse(source)
        for child in token.children or []
        if child.type == "link_open"
    ]
    assert len(titles) == 1
    title = titles[0]
    assert isinstance(title, str)
    assert title == " Checks,Draft "
    argument = shlex.split("--presets ' Checks,Draft '")[1]
    assert read(title) == read(argument) == {"checks", "draft"}
