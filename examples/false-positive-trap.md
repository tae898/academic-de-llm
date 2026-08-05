---
name: trap
---

## Legitimate technical prose

Accuracy ranged 0.88–0.98 across runs.

| Engine | Latency | Notes |
|---|---|---|
| Chroma | 12ms | — |

```python
# strip the prefix — the parser needs it bare
value = line.split("—")[0]
```

Use the `--dry-run` flag. The config file is `~/.config/app.toml`.

Error: `connection reset by peer — retrying`
