"""Assert the link check's heading-slug rule generates GitHub's own anchors.

The oracle is GitHub, not an expectation written here. `anchors.json` holds a
document of headings and the anchor ids GitHub generated for it, captured in
one call to the Markdown API:

```bash
gh api --method POST markdown -f mode=markdown -F text=@headings.md
```

The capture carries the bytes GitHub was given, so the test feeds the fragment
reader the very document the anchors came from and compares what it generates
with what GitHub did. The headings are the ones a rule parts company with
GitHub over: an emoji, a variation selector, an accent, a code span, a link,
emphasis of each spelling, an ampersand between two spaces, an underscore
inside a word, a trailing run of hash marks and a heading repeated, whose
second occurrence GitHub numbers.

Refreshing the capture is that one call against `document`, with the `id`
attributes of the response read in order and the `user-content-` prefix
removed.
"""

import json
from pathlib import Path

import links

CAPTURE = json.loads(Path(__file__).with_name("anchors.json").read_text())
DOCUMENT: str = CAPTURE["document"]
ANCHORS: list[str] = CAPTURE["anchors"]

HEADINGS = [heading for _, heading in links.HEADING.findall(DOCUMENT)]


def test_the_capture_covers_every_heading_of_its_document() -> None:
    assert len(HEADINGS) == len(ANCHORS)
    assert HEADINGS, "the capture holds no heading, so the rule is held to nothing"


def test_a_repeated_heading_is_in_the_capture() -> None:
    assert len(set(ANCHORS)) < len(ANCHORS) or any(
        anchor.endswith("-1") for anchor in ANCHORS
    ), "no heading repeats, so GitHub's numbering of the second is unobserved"


def test_every_fragment_the_document_generates_is_one_github_generates() -> None:
    assert links.fragments_of(DOCUMENT) == set(ANCHORS)


def test_each_heading_generates_the_anchor_github_generated_for_it() -> None:
    first: dict[str, str] = {}
    for heading, anchor in zip(HEADINGS, ANCHORS, strict=True):
        first.setdefault(heading, anchor)
    mismatched = {
        heading: (links.slug(heading), anchor)
        for heading, anchor in first.items()
        if links.slug(heading) != anchor
    }
    assert mismatched == {}, (
        f"the rule and GitHub disagree, each heading to (rule, github): {mismatched}"
    )


def test_a_heading_the_rule_would_get_wrong_is_reported() -> None:
    """The comparison fails when the rule drops a class GitHub keeps.

    A rule written in terms of word characters drops the variation selector
    GitHub keeps, so the anchor it generates for a heading carrying one is
    not GitHub's. This holds the comparison itself to failing on that.
    """
    carried = [
        heading for heading in HEADINGS if any(character == "️" for character in heading)
    ]
    assert carried, "the capture holds no variation selector, so this proves nothing"
    word_characters = {
        heading: "".join(
            character
            for character in heading.lower()
            if character.isalnum() or character in links.SLUG_KEPT
        ).replace(" ", "-")
        for heading in carried
    }
    for heading, produced in word_characters.items():
        assert produced != links.slug(heading)
