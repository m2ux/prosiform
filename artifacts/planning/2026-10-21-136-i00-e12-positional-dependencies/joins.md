# Rows That Could Share a Pull Request

W02, W03, W04, W05 and W06 each depend on W01 and on nothing else, so any pair of them could land together. W04 and W05 do: both retire a refusal the old mark justified, in the same classifier, and one change removes both codes.

The others keep their own pull requests.

- **Each row is one criterion with its own fixtures.**
  A deferral carried with its mark, a reference that resolves nowhere, a resource under the root, and an entry reference that leaves the root are four outcomes a reader checks separately, and a pull request per outcome keeps each criterion's evidence its own.

- **The rows are delivered in parallel.**
  They are free as soon as W01 lands, and separate branches let one session take each. A shared pull request would serialise work that has no order between its parts.

- **W07 waits on W02 and is nobody's pair.**
  Rebasing a deferred destination needs the deferral it rebases, so it is a level below the rest.
