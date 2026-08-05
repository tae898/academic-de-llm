# queuectl

A CLI for inspecting Redis-backed job queues, for developers who need to see what their workers are doing.

## What it does

queuectl is a single entry point for queue inspection. It shows pending, active, and failed jobs in real time, which otherwise requires reading Redis by hand alongside your worker logs.

It has three inspection modes and a live-tail view that streams state transitions as they happen.

## Key features

It reads directly from Redis with no intermediate service, ships as a single static binary with no runtime dependencies, and is read-only unless you pass `--mutate`.

## Installation

```bash
go install github.com/example/queuectl@latest
```

## Usage

The common workflow is not checking queue depth. It is finding out why a queue is deep.

```bash
queuectl inspect --queue emails --state failed
```

### Flags

- **--queue**: queue name, required
- **--state**: one of `pending`, `active`, `failed`, `done`
- **--since**: only jobs newer than this duration, e.g. `15m`
- **--json**: emit machine-readable output
- **--mutate**: allow retry and delete operations

## Interpreting failure rates

A failure rate above 5% is crucial to investigate. Below that, retries usually absorb transient network errors.

In our benchmarks, throughput ranged 0.88–0.98 of the theoretical maximum, though this may vary depending on your Redis configuration.

| Metric | p50 | p99 | Notes |
|---|---|---|---|
| Inspect latency | 4ms | 22ms | — |
| Tail startup | 11ms | 40ms | cold Redis connection |

## How retries work

```go
// backoff doubles each attempt — capped at the ceiling
delay := min(base<<attempt, ceiling)
```

If a job exhausts its retries it moves to the dead-letter queue, where it remains until manually cleared.

queuectl does not support Redis cluster mode.
