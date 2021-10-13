from pyperformance.benchmarks.bm_nbody import (
    bench_nbody,
    DEFAULT_REFERENCE,
    DEFAULT_ITERATIONS,
)


def faasm_main():
    bench_nbody(10, DEFAULT_REFERENCE, DEFAULT_ITERATIONS)
    return 0
