# Agent Instructions

How an agent writes in this repository.

## Docstrings and comments

A rule the build implements is stated once, in the docstring of the narrowest unit that implements it: the function or class whose code applies it, and the module only where no narrower unit does. Where several units apply one rule, one of them owns it and the others name it. Every other docstring states what its own unit does and names the rules it relies on by their owner.

- **Module docstring.** The module's responsibility and the contract it offers its callers.
- **Class or function docstring.** What that unit does, what it takes and what it returns, and any invariant a caller must keep. A class that only holds values states what each holds; a rule about a value is owned by the code that applies it.
- **A rule another unit owns.** Named by its owner and the rule, as the frontmatter delimiters `source.frontmatter` states, and never restated or paraphrased.
- **Comment.** Why the code is as it is, where the code cannot say it. A comment never states what the code does or how it came to be.

A change to a rule edits its owner's docstring and the code that implements it, and no other docstring or comment.
