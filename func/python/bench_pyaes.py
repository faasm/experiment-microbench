from pyperformance.benchmarks.bm_crypto_pyaes import bench_pyaes


def faasm_main():
    bench_pyaes(20)
    return 0
