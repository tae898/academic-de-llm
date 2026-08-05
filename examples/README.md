# Examples

Two fixtures. They are also the test corpus for `tests/check.sh`, so they cannot
drift from what the patterns actually do.

## `slopped.md`

One planted instance of every pattern in `SKILL.md`. Every finder must fire here.
Useful for checking that a change to `references/patterns.md` did not silently
break a pattern, which is exactly what happened in v2.

## `false-positive-trap.md`

The more important one.

Legitimate technical prose that trips the finders anyway: an em dash inside a
code comment, an em dash inside a Python string literal, a dash used as a table
"not applicable" placeholder, an en dash in a numeric range, a quoted error
message, CLI flags, and YAML frontmatter.

The correct output on this file is **no changes at all**.

The raw em dash search returns 4 hits and 0 of them are real:

```
11:| Chroma | 12ms | — |
14:# strip the prefix — the parser needs it bare
15:value = line.split("—")[0]
20:Error: `connection reset by peer — retrying`
```

Every other pattern stays silent. A tool that edited all 4 would corrupt a
table, two lines of working Python, and a quoted error string.

This is what step zero of `SKILL.md` exists to prevent, and it is the reason the
skill says greps find candidates rather than violations. Cleaning up bad prose
is easy. Correctly changing nothing is the harder test, and it is the one most
tools in this space fail.
