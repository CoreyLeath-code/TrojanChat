# Benchmark report

## Research question

Can bounded, synchronized in-process retention prevent unbounded memory growth without exceeding a
15% write-throughput regression budget relative to the legacy list store?

## Protocol

Seven independent iterations insert 50,000 messages. Both variants perform identical UUID4 and UTC
timestamp generation. The optimized store retains the latest 10,000 messages. `perf_counter`
measures elapsed time and `tracemalloc` measures Python peak allocations. Results below are from
Windows 11 and Python 3.12.13 on 2026-07-18; CI regenerates JSON on Ubuntu/Python 3.11.

| Metric | Legacy baseline | Bounded store | Change |
|---|---:|---:|---:|
| Median latency | 1,155.519 ms | 1,239.880 ms | +7.3% |
| P95 / P99 latency | 1,221.577 ms | 1,303.501 ms | +6.7% |
| Throughput | 43,270.60 msg/s | 40,326.50 msg/s | -6.8% |
| Peak Python memory | 21.205 MiB | 4.228 MiB | **-80.06%** |

The 6.8% throughput tradeoff is within the 15% budget. This microbenchmark excludes network I/O,
JSON encoding, Redis, persistence, multi-process contention, CPU utilization, and allocator RSS.
It is systems evidence, not a production SLO. Raw evidence is in `benchmarks/latest.json`.

```bash
python -m benchmarks.run_benchmark --samples 50000 --iterations 7 --retention 10000
```
