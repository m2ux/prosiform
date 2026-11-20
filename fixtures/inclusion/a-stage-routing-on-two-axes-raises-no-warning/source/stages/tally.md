---
prosiform:
  default:
    brief: "#contract"
    level: retrieval
  prose:
    choice: The source is prose.
    subst:
      - ../rules/kind.md: prose.md
  code:
    choice: The source is code.
    subst:
      - ../rules/kind.md: code.md
  strict:
    subst:
      - ../rules/counting.md: strict.md
  lenient:
    subst:
      - ../rules/counting.md: lenient.md
---
# Tally

Count one source's lines, by its kind and under one counting rule.

Follow the [Steps](#steps) under the [Contract](#contract).

## Contract

### Given

- The source.

### Answers

- `tallied`, with the count

## Steps

1. Read [the source's material](../rules/source.md).
2. Count its lines as [its kind](../rules/kind.md) and [the counting rule](../rules/counting.md) state.
3. Answer `tallied`, with the count.
