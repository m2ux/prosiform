# Change List

## Applied

None. The unit delivered its rows as planned, through pull request #522, merged into i08/e03/main.

## Held

None.

## Scope decisions within the rows

- The extraction fixture the referrer carried is withdrawn rather than rewritten, since extraction/section-to-the-next-sibling already holds a section entry and its derived name.
- No separate derived-name fixture is added for W02; the surviving section-entry fixtures and src/tests/test_derived_output.py observe AC2.
- No fixture refuses -f as an unknown option: a retired option is removed, not refused, and make invocation shows the build declares none.

## Deferred debt and arising issues

None. Stale -r, -g and -f entries in the diagnostic-format scan, and the authoring check's value-taking set, were fixed in this unit.
