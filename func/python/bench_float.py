from pyperformance.benchmarks.bm_float import benchmark


def faasm_main():
    benchmark(10000)
    return 0


if __name__ == "__main__":
    faasm_main()
