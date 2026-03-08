# inewave Benchmark Results

Generated: 2026-02-23 20:28:46 UTC  
Python: 3.14.2 (main, Dec  5 2025, 00:00:00) [GCC 15.2.1 20251111 (Red Hat 15.2.1-4)]  
Platform: Linux-6.18.12-200.fc43.x86_64-x86_64-with-glibc2.42  
CPU: x86_64  
Iterations: 2

Note: Memory measurements use tracemalloc (Python-level allocations only).

## Import Benchmarks

| Benchmark | Mean (s) | Delta | Median (s) | Min (s) | Max (s) | Std Dev (s) | Peak Memory (MB) |
|-----------|----------|-------|------------|---------|---------|-------------|------------------|
| import inewave | 0.3559 | +48.8% | 0.3559 | 0.0050 | 0.7068 | 0.4963 | 33.36 |
| import inewave.nwlistop | 0.0046 | +1.1% | 0.0046 | 0.0046 | 0.0047 | 0.0001 | 0.31 |
| import inewave.newave | 0.0046 | -0.4% | 0.0046 | 0.0046 | 0.0046 | 0.0000 | 0.31 |
| import inewave.nwlistop.earmf | 0.0072 | +0.6% | 0.0072 | 0.0070 | 0.0074 | 0.0003 | 0.43 |

## Read Benchmarks

| Benchmark | Mean (s) | Delta | Median (s) | Min (s) | Max (s) | Std Dev (s) | Peak Memory (MB) |
|-----------|----------|-------|------------|---------|---------|-------------|------------------|
| Earmf (non-patamar REE) | 0.0735 | -4.4% | 0.0735 | 0.0686 | 0.0784 | 0.0069 | 8.55 |
| Earmfsin (non-patamar SIN) | 0.0714 | +5.5% | 0.0714 | 0.0658 | 0.0770 | 0.0079 | 8.51 |
| Cmarg (patamar Submercado) | 0.2102 | -2.7% | 0.2102 | 0.2089 | 0.2115 | 0.0018 | 28.04 |
| Earmfp (patamar REE) | 0.0675 | +1.5% | 0.0675 | 0.0662 | 0.0688 | 0.0019 | 8.63 |
| Pmo (newave SectionFile) | 0.6437 | -2.2% | 0.6437 | 0.6343 | 0.6531 | 0.0134 | 21.02 |

## Aggregation Benchmarks

| Benchmark | Mean (s) | Delta | Median (s) | Min (s) | Max (s) | Std Dev (s) | Peak Memory (MB) |
|-----------|----------|-------|------------|---------|---------|-------------|------------------|
| Hidr (newave binary) | 0.0840 | +0.8% | 0.0840 | 0.0836 | 0.0843 | 0.0005 | 1.13 |
| Earmf.valores (non-patamar REE) | 0.0001 | +23.8% | 0.0001 | 0.0001 | 0.0001 | 0.0000 | 0.00 |
| Earmfsin.valores (non-patamar SIN) | 0.0001 | +16.9% | 0.0001 | 0.0001 | 0.0001 | 0.0000 | 0.00 |
| Cmarg.valores (patamar Submercado) | 0.0001 | +27.5% | 0.0001 | 0.0001 | 0.0001 | 0.0000 | 0.00 |
| Earmfp.valores (patamar REE) | 0.0001 | +22.3% | 0.0001 | 0.0001 | 0.0001 | 0.0000 | 0.00 |
