"""Reproducible before/after benchmark for the canonical message store."""

import argparse
import json
import platform
import statistics
import time
import tracemalloc
import uuid
from datetime import datetime, timezone
from pathlib import Path

from backend.services.chat_service import ChatService


class LegacyStore:
    """Pre-optimization unbounded list retained only as a benchmark control."""

    def __init__(self) -> None:
        self.messages: list[dict[str, str]] = []

    def send_message(self, username: str, content: str) -> None:
        self.messages.append(
            {
                "id": str(uuid.uuid4()),
                "username": username,
                "content": content,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )


def percentile(values: list[float], fraction: float) -> float:
    return sorted(values)[min(len(values) - 1, int(len(values) * fraction))]


def measure(factory, samples: int, iterations: int) -> dict[str, float]:
    latencies: list[float] = []
    peaks: list[int] = []
    for _ in range(iterations):
        store = factory()
        tracemalloc.start()
        started = time.perf_counter()
        for index in range(samples):
            store.send_message(f"user-{index % 100}", f"message-{index}")
        elapsed = time.perf_counter() - started
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        latencies.append(elapsed * 1_000)
        peaks.append(peak)
    median = statistics.median(latencies)
    return {
        "latency_mean_ms": round(statistics.mean(latencies), 3),
        "latency_median_ms": round(median, 3),
        "latency_p95_ms": round(percentile(latencies, 0.95), 3),
        "latency_p99_ms": round(percentile(latencies, 0.99), 3),
        "latency_min_ms": round(min(latencies), 3),
        "latency_max_ms": round(max(latencies), 3),
        "throughput_messages_per_second": round(samples / (median / 1_000), 2),
        "peak_memory_mib": round(max(peaks) / 1024 / 1024, 3),
    }


def run(samples: int = 50_000, iterations: int = 7, retention: int = 10_000) -> dict:
    baseline = measure(LegacyStore, samples, iterations)
    optimized = measure(lambda: ChatService(retention), samples, iterations)
    return {
        "schema_version": "1.0.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "parameters": {"samples": samples, "iterations": iterations, "retention": retention},
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "baseline": baseline,
        "optimized": optimized,
        "comparison": {
            "throughput_change_percent": round(
                (optimized["throughput_messages_per_second"] / baseline["throughput_messages_per_second"] - 1) * 100, 2
            ),
            "peak_memory_change_percent": round(
                (optimized["peak_memory_mib"] / baseline["peak_memory_mib"] - 1) * 100, 2
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=50_000)
    parser.add_argument("--iterations", type=int, default=7)
    parser.add_argument("--retention", type=int, default=10_000)
    parser.add_argument("--output", type=Path, default=Path("benchmarks/latest.json"))
    args = parser.parse_args()
    if min(args.samples, args.iterations, args.retention) < 1:
        parser.error("benchmark values must be positive")
    result = run(args.samples, args.iterations, args.retention)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
