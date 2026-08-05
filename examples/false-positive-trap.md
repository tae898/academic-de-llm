---
name: trap
---

# Connection pooling

Legitimate technical prose. Several patterns fire on this file. The correct
output is **no changes at all**.

## Using PostgreSQL With Django

Looks like title case, but the pattern does not fire here: `[A-Z][a-z]+` cannot
match `PostgreSQL`, whose internal capitals break the run. That is an accident
of the regex, not a guard against proper nouns. The next heading proves it.

## Amazon Web Services

Fires the title-case pattern. Every capital is part of one proper noun and the
heading is already correct. Reject it.

## Tuning

Getting the pool size right is crucial: too small and requests queue behind
connection acquisition, too large and Postgres runs out of backend slots. That
is one Tier 3 word, in a sentence that says why it matters. Density is the
signal, and one is not density.

The three failure modes are exhaustion, leakage, and staleness. Three real
things, so deleting the third loses information.

### Flags

- **--pool-size**: maximum open connections, default 10
- **--max-idle**: idle connections retained between requests
- **--conn-lifetime**: recycle a connection after this duration

An inline-header bold list, and the pattern cannot tell it apart from a hollow
one. It is a flag reference: genuinely parallel, meant to be scanned rather
than read. Keep it.

## Measurements

Throughput held at 0.88–0.98 of the ceiling across runs. That is an en dash in
a numeric range, not an em dash.

| Engine | Latency | Notes |
|---|---|---|
| Chroma | 12ms | — |
| Qdrant | 15ms | pool warm |

## Implementation

```python
# strip the prefix — the parser needs it bare
value = line.split("—")[0]
```

Use the `--dry-run` flag. Config lives at `~/.config/app.toml`.

Error: `connection reset by peer — retrying`

## Prior art

Quoting a 2019 design document, which predates ChatGPT by three years and
therefore cannot be machine-generated whatever it looks like:

> Connection pooling stands as a crucial component of any robust database
> layer, serving as the bridge between application demand and finite server
> resources, and underscoring the importance of careful capacity planning.
