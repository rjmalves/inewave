"""
benchmarks/bench_import.py
==========================

Benchmark functions for inewave import operations.

For each target module, all `inewave` sub-modules are cleared from
`sys.modules` before every iteration so that `importlib.import_module`
performs a fresh bytecode-cache load.

Only keys starting with "inewave" are cleared; cfinterface, pandas, numpy
and other heavy dependencies are NOT cleared so that iteration-to-iteration
variance reflects only inewave's own import path cost.
"""

from __future__ import annotations

import importlib
import sys
import time
import tracemalloc

from benchmarks.bench_read import BenchmarkResult

_IMPORT_BENCHMARKS: list[str] = [
    "inewave",
    "inewave.nwlistop",
    "inewave.newave",
    "inewave.nwlistop.earmf",
]


def run_import_benchmark(module_path: str, iterations: int) -> BenchmarkResult:
    """
    Benchmark importing *module_path* from a cold (inewave-only) cache.

    Parameters
    ----------
    module_path:
        Fully qualified module name, e.g. ``"inewave.nwlistop.earmf"``.
    iterations:
        Number of import iterations to time.

    Returns
    -------
    BenchmarkResult with per-iteration times and peak memory.
    """
    times: list[float] = []
    peak_kb_overall = 0.0

    for _ in range(iterations):
        # Clear only inewave sub-modules to avoid invalidating shared heavy
        # dependencies (pandas, numpy, cfinterface, …).
        to_remove = [
            k for k in sys.modules if k == "inewave" or k.startswith("inewave.")
        ]
        for k in to_remove:
            del sys.modules[k]

        tracemalloc.start()
        t0 = time.perf_counter()
        try:
            importlib.import_module(module_path)
        finally:
            t1 = time.perf_counter()
            _, peak_kb = tracemalloc.get_traced_memory()
            tracemalloc.stop()

        times.append(t1 - t0)
        if peak_kb > peak_kb_overall:
            peak_kb_overall = peak_kb

    peak_mb = peak_kb_overall / (1024.0 * 1024.0)
    return BenchmarkResult(
        name=f"import {module_path}",
        times=times,
        peak_memory_mb=peak_mb,
    )


def run_all_import_benchmarks(iterations: int) -> list[BenchmarkResult | str]:
    """
    Run every configured import benchmark.

    Returns a list of either `BenchmarkResult` (success) or a SKIPPED
    string (failure).
    """
    results: list[BenchmarkResult | str] = []

    for module_path in _IMPORT_BENCHMARKS:
        try:
            result = run_import_benchmark(module_path, iterations)
            results.append(result)
        except Exception as exc:
            results.append(f"import {module_path} SKIPPED: {exc}")

    return results
