from benchmarks.run_benchmark import percentile, run


def test_benchmark_is_machine_readable_and_compares_implementations() -> None:
    result = run(samples=100, iterations=2, retention=25)
    assert result["schema_version"] == "1.0.0"
    assert result["optimized"]["throughput_messages_per_second"] > 0
    assert result["optimized"]["peak_memory_mib"] >= 0
    assert "throughput_change_percent" in result["comparison"]


def test_percentile_uses_observed_sample() -> None:
    assert percentile([4.0, 1.0, 3.0, 2.0], 0.95) == 4.0
