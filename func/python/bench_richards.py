from pyperformance.benchmarks.bm_richards import Richards


def faasm_main():
    richard = Richards()
    richard.run(2)
    return 0
