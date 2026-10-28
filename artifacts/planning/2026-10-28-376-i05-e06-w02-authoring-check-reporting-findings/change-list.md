# Change List — I05:E06 W02

## Applied

- **Delivery record.** On #376, the W02 row links the pull request in place of this folder. It was written from a fresh read, and no other row or criterion changed.
- **Task merge.** The user merged #380 into `i05/e06/main` at `500aca85`, after CI passed on `256a032f`; the session's own merge had been refused by its permission classifier. #376 AC2 ticked and W02 Done, from a fresh read.

## Held

- **Epic review pull request.** Task Merge's review step for `i05/e06/main` is held. E06 has no review pull request, and the user has not confirmed one. Recommended: open the draft review `i05/e06/main` → `main` once the user confirms it.

## Notes for Later Rows

- **W06–W08.**
  - Start from the [findings scan](findings.md).
  - Re-run `make authoring` after each conversion. The count for the row's kind falls to zero for the files it converts.
- **W09.**
  - Reads the five files the size report names.
  - Owns the One home per rule findings, which the check does not read.
- **W10.**
  - `make authoring` and its row in `checks/README.md` already exist.
  - W10 adds `authoring` to `make check`.
  - It adds a `make authoring` row to the `checks.md` table and drops "`authoring.py` and" from the `checks/README.md` sentence on what `make check` runs.
  - The tests already include a failing file for each rule.
