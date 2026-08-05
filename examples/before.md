# queuectl

A powerful and comprehensive CLI for inspecting Redis-backed job queues — built for developers who need visibility into what their workers are actually doing.

## What It Does

queuectl serves as a single entry point for queue inspection, offering real-time visibility into pending, active, and failed jobs. It stands as the missing piece between your worker logs and your dashboards, providing insights that would otherwise require manual Redis inspection.

The tool boasts three inspection modes and features a live-tail view that streams state transitions as they happen, ensuring you never miss a failure.

## Key Features

- **Fast**: Reads directly from Redis with no intermediate service.
- **Portable**: A single static binary with no runtime dependencies.
- **Safe**: Read-only by default, requiring an explicit flag to mutate state.

## Installation

```bash
go install github.com/example/queuectl@latest
```

## Usage

The most common workflow is not just checking queue depth, but understanding why a queue is deep.

```bash
queuectl inspect --queue emails --state failed
```

### Flags

- **--queue**: queue name, required
- **--state**: one of `pending`, `active`, `failed`, `done`
- **--since**: only jobs newer than this duration, e.g. `15m`
- **--json**: emit machine-readable output
- **--mutate**: allow retry and delete operations

## Interpreting Failure Rates

A failure rate above 5% is crucial to investigate, highlighting a systemic problem rather than transient network issues.

In our benchmarks, throughput ranged 0.88–0.98 of the theoretical maximum, though this may potentially vary depending on your Redis configuration.

| Metric | p50 | p99 | Notes |
|---|---|---|---|
| Inspect latency | 4ms | 22ms | — |
| Tail startup | 11ms | 40ms | cold Redis connection |

## How Retries Work

```go
// backoff doubles each attempt — capped at the ceiling
delay := min(base<<attempt, ceiling)
```

If a job exhausts its retries it moves to the dead-letter queue, where it remains until manually cleared.

Despite its comprehensive feature set, queuectl faces several challenges around cluster mode, which the maintainers are actively working to address.

Observers have noted that queue introspection tooling is underserved in the Go ecosystem.
