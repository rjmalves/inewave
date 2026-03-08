"""
benchmarks/bench_read.py
========================

Benchmark functions for inewave read operations.

Each benchmark reads a file using a mock-open pattern (identical to the test
suite) and measures wall-clock time and peak Python-level memory usage.

All inewave modules and test mocks are imported lazily via importlib so that
this module can be imported without side-effects and without contaminating
import-time measurements.
"""

from __future__ import annotations

import dataclasses
import importlib
import statistics
import time
import tracemalloc
from typing import Any
from unittest.mock import patch

# Path used for all mock reads — same dummy path the test suite uses.
_ARQ_TESTE = "./tests/mocks/arquivos/__init__.py"


@dataclasses.dataclass
class BenchmarkResult:
    """Statistics for a single benchmark run."""

    name: str
    times: list[float]
    peak_memory_mb: float

    def mean(self) -> float:
        return statistics.mean(self.times)

    def median(self) -> float:
        return statistics.median(self.times)

    def min(self) -> float:
        return min(self.times)

    def max(self) -> float:
        return max(self.times)

    def stdev(self) -> float:
        if len(self.times) < 2:
            return 0.0
        return statistics.stdev(self.times)


def run_read_benchmark(
    handler_cls: Any,
    mock_data: list[str],
    name: str,
    iterations: int,
    read_kwargs: dict[str, Any] | None = None,
) -> BenchmarkResult:
    """
    Benchmark one file handler over *iterations* reads.

    Parameters
    ----------
    handler_cls:
        The file handler class that exposes a `.read(path, **kwargs)` class
        method and a `.valores` property.
    mock_data:
        A list of strings that form the file content.
    name:
        Human-readable benchmark label.
    iterations:
        Number of read iterations to time.
    read_kwargs:
        Extra keyword arguments forwarded to `handler_cls.read()`.

    Returns
    -------
    BenchmarkResult with per-iteration times and peak memory.
    """
    if read_kwargs is None:
        read_kwargs = {}

    mock_open_mod = importlib.import_module("tests.mocks.mock_open")
    mock_open_fn = getattr(mock_open_mod, "mock_open")

    read_data = "".join(mock_data)
    times: list[float] = []
    peak_kb_overall = 0.0

    for _ in range(iterations):
        m = mock_open_fn(read_data=read_data)

        tracemalloc.start()
        t0 = time.perf_counter()
        try:
            with patch("builtins.open", m):
                obj = handler_cls.read(_ARQ_TESTE, **read_kwargs)
                # Force lazy property access so aggregation is measured.
                if hasattr(obj, "valores"):
                    _ = obj.valores
        finally:
            t1 = time.perf_counter()
            _, peak_kb = tracemalloc.get_traced_memory()
            tracemalloc.stop()

        times.append(t1 - t0)
        if peak_kb > peak_kb_overall:
            peak_kb_overall = peak_kb

    peak_mb = peak_kb_overall / (1024.0 * 1024.0)
    return BenchmarkResult(name=name, times=times, peak_memory_mb=peak_mb)


# Each entry: (benchmark_name, handler_module, handler_class_name,
#              mock_module, mock_attr_name, read_kwargs)
_READ_BENCHMARKS: list[tuple[str, str, str, str, str, dict[str, Any]]] = [
    (
        "Earmf (non-patamar REE)",
        "inewave.nwlistop.earmf",
        "Earmf",
        "tests.mocks.arquivos.earmf",
        "MockEarmf",
        {},
    ),
    (
        "Earmfsin (non-patamar SIN)",
        "inewave.nwlistop.earmfsin",
        "Earmfsin",
        "tests.mocks.arquivos.earmfsin",
        "MockEarmfSIN",
        {},
    ),
    (
        "Cmarg (patamar Submercado)",
        "inewave.nwlistop.cmarg",
        "Cmarg",
        "tests.mocks.arquivos.cmarg",
        "MockCmarg",
        {},
    ),
    (
        "Earmfp (patamar REE)",
        "inewave.nwlistop.earmfp",
        "Earmfp",
        "tests.mocks.arquivos.earmfp",
        "MockEarmfp",
        {},
    ),
    (
        "Pmo (newave SectionFile)",
        "inewave.newave.pmo",
        "Pmo",
        "tests.mocks.arquivos.pmo",
        "MockPMO",
        {},
    ),
]


def run_all_read_benchmarks(iterations: int) -> list[BenchmarkResult | str]:
    """
    Run every configured read benchmark.

    Returns a list of either `BenchmarkResult` (success) or the benchmark
    name string suffixed with " SKIPPED: <reason>" (failure/skip).
    """
    results: list[BenchmarkResult | str] = []

    for (
        bench_name,
        handler_mod,
        handler_cls_name,
        mock_mod,
        mock_attr,
        rk,
    ) in _READ_BENCHMARKS:
        try:
            handler_cls = getattr(
                importlib.import_module(handler_mod), handler_cls_name
            )
        except Exception as exc:
            results.append(
                f"{bench_name} SKIPPED: cannot import handler — {exc}"
            )
            continue

        try:
            mock_module = importlib.import_module(mock_mod)
            mock_data = list(getattr(mock_module, mock_attr))
        except Exception as exc:
            results.append(
                f"{bench_name} SKIPPED: cannot import mock data — {exc}"
            )
            continue

        try:
            result = run_read_benchmark(
                handler_cls=handler_cls,
                mock_data=mock_data,
                name=bench_name,
                iterations=iterations,
                read_kwargs=rk,
            )
            results.append(result)
        except Exception as exc:
            results.append(f"{bench_name} SKIPPED: benchmark failed — {exc}")

    return results


_HIDR_PATH = "./tests/mocks/arquivos/hidr.dat"


def run_hidr_benchmark(iterations: int) -> BenchmarkResult | str:
    """
    Benchmark Hidr.read() which reads a real binary file from disk.

    Returns a BenchmarkResult or a SKIPPED string on failure.
    """
    name = "Hidr (newave binary)"
    try:
        hidr_mod = importlib.import_module("inewave.newave.hidr")
        Hidr = getattr(hidr_mod, "Hidr")
    except Exception as exc:
        return f"{name} SKIPPED: cannot import handler — {exc}"

    repo_root = _find_repo_root()
    hidr_path = repo_root / "tests" / "mocks" / "arquivos" / "hidr.dat"
    if not hidr_path.exists():
        return f"{name} SKIPPED: fixture file not found at {hidr_path}"

    times: list[float] = []
    peak_kb_overall = 0.0

    for _ in range(iterations):
        tracemalloc.start()
        t0 = time.perf_counter()
        try:
            _ = Hidr.read(str(hidr_path))
        finally:
            t1 = time.perf_counter()
            _, peak_kb = tracemalloc.get_traced_memory()
            tracemalloc.stop()
        times.append(t1 - t0)
        if peak_kb > peak_kb_overall:
            peak_kb_overall = peak_kb

    peak_mb = peak_kb_overall / (1024.0 * 1024.0)
    return BenchmarkResult(name=name, times=times, peak_memory_mb=peak_mb)


def _find_repo_root():
    from pathlib import Path

    return Path(__file__).parent.parent


def run_aggregation_benchmark(
    handler_cls: Any,
    mock_data: list[str],
    name: str,
    iterations: int,
    read_kwargs: dict[str, Any] | None = None,
) -> BenchmarkResult:
    """
    Benchmark the ``handler.valores`` property access in isolation.

    For each iteration the handler is read outside the timed region so that
    only the ``__monta_tabela()`` call (triggered by the first access to
    ``valores``) is measured.  A fresh handler object is obtained per
    iteration so the lazy cache is never pre-warmed.

    Parameters
    ----------
    handler_cls:
        The file handler class with a `.read(path, **kwargs)` classmethod
        and a `.valores` property.
    mock_data:
        A list of strings that form the file content.
    name:
        Human-readable benchmark label.
    iterations:
        Number of iterations to time.
    read_kwargs:
        Extra keyword arguments forwarded to `handler_cls.read()`.

    Returns
    -------
    BenchmarkResult with per-iteration times and peak memory.
    """
    if read_kwargs is None:
        read_kwargs = {}

    mock_open_mod = importlib.import_module("tests.mocks.mock_open")
    mock_open_fn = getattr(mock_open_mod, "mock_open")

    read_data = "".join(mock_data)
    times: list[float] = []
    peak_kb_overall = 0.0

    for _ in range(iterations):
        # Read outside the timed region — gives a fresh object with an
        # un-warmed cache each iteration.
        m = mock_open_fn(read_data=read_data)
        with patch("builtins.open", m):
            obj = handler_cls.read(_ARQ_TESTE, **read_kwargs)

        # Time only the valores property access.
        tracemalloc.start()
        t0 = time.perf_counter()
        try:
            _ = obj.valores
        finally:
            t1 = time.perf_counter()
            _, peak_kb = tracemalloc.get_traced_memory()
            tracemalloc.stop()

        times.append(t1 - t0)
        if peak_kb > peak_kb_overall:
            peak_kb_overall = peak_kb

    peak_mb = peak_kb_overall / (1024.0 * 1024.0)
    return BenchmarkResult(name=name, times=times, peak_memory_mb=peak_mb)


_AGGREGATION_BENCHMARKS: list[
    tuple[str, str, str, str, str, dict[str, Any]]
] = [
    (
        "Earmf.valores (non-patamar REE)",
        "inewave.nwlistop.earmf",
        "Earmf",
        "tests.mocks.arquivos.earmf",
        "MockEarmf",
        {},
    ),
    (
        "Earmfsin.valores (non-patamar SIN)",
        "inewave.nwlistop.earmfsin",
        "Earmfsin",
        "tests.mocks.arquivos.earmfsin",
        "MockEarmfSIN",
        {},
    ),
    (
        "Cmarg.valores (patamar Submercado)",
        "inewave.nwlistop.cmarg",
        "Cmarg",
        "tests.mocks.arquivos.cmarg",
        "MockCmarg",
        {},
    ),
    (
        "Earmfp.valores (patamar REE)",
        "inewave.nwlistop.earmfp",
        "Earmfp",
        "tests.mocks.arquivos.earmfp",
        "MockEarmfp",
        {},
    ),
]


def run_all_aggregation_benchmarks(
    iterations: int,
) -> list[BenchmarkResult | str]:
    """
    Run every configured aggregation (valores-only) benchmark.

    Returns a list of either `BenchmarkResult` (success) or the benchmark
    name string suffixed with " SKIPPED: <reason>" (failure/skip).
    """
    results: list[BenchmarkResult | str] = []

    for (
        bench_name,
        handler_mod,
        handler_cls_name,
        mock_mod,
        mock_attr,
        rk,
    ) in _AGGREGATION_BENCHMARKS:
        try:
            handler_cls = getattr(
                importlib.import_module(handler_mod), handler_cls_name
            )
        except Exception as exc:
            results.append(
                f"{bench_name} SKIPPED: cannot import handler — {exc}"
            )
            continue

        try:
            mock_module = importlib.import_module(mock_mod)
            mock_data = list(getattr(mock_module, mock_attr))
        except Exception as exc:
            results.append(
                f"{bench_name} SKIPPED: cannot import mock data — {exc}"
            )
            continue

        try:
            result = run_aggregation_benchmark(
                handler_cls=handler_cls,
                mock_data=mock_data,
                name=bench_name,
                iterations=iterations,
                read_kwargs=rk,
            )
            results.append(result)
        except Exception as exc:
            results.append(f"{bench_name} SKIPPED: benchmark failed — {exc}")

    return results
