from pyperformance.benchmarks.bm_raytrace import (
    bench_raytrace,
    DEFAULT_WIDTH,
    DEFAULT_HEIGHT,
)


def faasm_main():
    filename = "raytrace.ppm"
    bench_raytrace(2, DEFAULT_WIDTH, DEFAULT_HEIGHT, filename)
    return 0
