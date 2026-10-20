"""Assert the vocabulary check reads a contract's marks and a glossary's terms.

The contract carries its own inventory: the design italicises a term where it
first uses it, and the glossary defines each one. Both readings are held here
to text they would be read wrongly: a design whose marks sit beside bold runs,
code spans, fenced examples and an underscore inside a word, and a glossary
whose sections tell a definition from a term it names as deliberately not used.
"""

from pathlib import Path

import pytest
import vocabulary

DESIGN = """\
# Design

A *bundle* is what the compiler emits, and a **bundle** in bold marks nothing.
The *entry reference* names where a run starts, and a later *bundle* repeats a
term already marked.

The `*profile*` in a code span is an example rather than a mark, and so is
snake_case, whose underscore is a character of the word.

```markdown
A *fenced term* is an example of the marking rather than a mark.
```

The *Source Root* is marked under the case the design writes it in.

## Acceptance Criteria

- **AC1.** A bundle names every entry reference its source roots carry.
"""

GLOSSARY = """\
# Glossary

## Terms

| Term | Definition |
| --- | --- |
| **Bundle** | What the compiler emits. |
| **Entry reference** | Where a run starts. |
| **Source root (a directory)** | A tree a run reads. |

## Terms deliberately not used

| Term | Why |
| --- | --- |
| **Artifact** | It names anything, so it names nothing. |
"""


def test_a_marked_term_is_in_the_inventory() -> None:
    assert "bundle" in vocabulary.marked_terms(DESIGN)
    assert "entry reference" in vocabulary.marked_terms(DESIGN)


def test_a_term_marked_twice_is_one_term() -> None:
    assert vocabulary.marked_terms(DESIGN).count("bundle") == 1


def test_a_bold_run_is_not_a_mark() -> None:
    assert vocabulary.marked_terms("A **bundle** in bold.") == []


def test_a_mark_inside_a_code_span_or_a_fence_is_an_example() -> None:
    inventory = vocabulary.marked_terms(DESIGN)
    assert "profile" not in inventory
    assert "fenced term" not in inventory


def test_a_marked_term_is_inventoried_in_the_case_the_glossary_compares() -> None:
    assert "source root" in vocabulary.marked_terms(DESIGN)


def test_a_glossary_defines_the_terms_of_its_definition_sections() -> None:
    defined, _ = vocabulary.glossary_terms(GLOSSARY)
    assert defined == {"bundle", "entry reference", "source root"}


def test_a_term_a_glossary_names_as_avoided_is_not_a_definition() -> None:
    defined, avoided = vocabulary.glossary_terms(GLOSSARY)
    assert avoided == {"artifact"}
    assert "artifact" not in defined


def test_a_parenthetical_is_not_part_of_the_term() -> None:
    defined, _ = vocabulary.glossary_terms(GLOSSARY)
    assert "source root" in defined


def test_a_plural_of_a_defined_singular_holds() -> None:
    assert vocabulary.holds("bundles", {"bundle"})
    assert vocabulary.holds("bundle", {"bundle"})
    assert not vocabulary.holds("bundler", {"bundle"})


def test_a_term_is_used_in_its_plural_and_in_any_case() -> None:
    pattern = vocabulary.usage_pattern("entry reference")
    assert pattern.search("Every Entry References resolves.")
    assert pattern.search("the entry reference")
    assert not pattern.search("the entry  is a reference")


def test_the_criteria_are_the_text_their_section_carries() -> None:
    criteria = vocabulary.criteria_text(DESIGN)
    assert "A bundle names every entry reference" in criteria
    assert "the compiler emits" not in criteria


def test_the_design_is_read_from_the_link_the_readme_names(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    readme = tmp_path / "README.md"
    readme.write_text(
        "The [Design](https://github.com/m2ux/prosiform/blob/engineering/"
        "artifacts/planning/2026-10-17-prosiform-v1/design.md) states it.\n"
    )
    monkeypatch.setattr(vocabulary, "README", readme)
    assert vocabulary.design_reference() == (
        "engineering",
        "artifacts/planning/2026-10-17-prosiform-v1/design.md",
    )


def test_a_readme_naming_no_design_stops_the_check(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("# Prosiform\n\nNothing links the design.\n")
    monkeypatch.setattr(vocabulary, "README", readme)
    with pytest.raises(SystemExit):
        vocabulary.design_reference()
