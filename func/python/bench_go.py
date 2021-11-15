from pyperformance.benchmarks.bm_go import versus_cpu


def faasm_main():
    versus_cpu()
    return 0


if __name__ == "__main__":
    faasm_main()
