from pyperformance.benchmarks.bm_fannkuch import fannkuch


def faasm_main():
    fannkuch(6)
    return 0


if __name__ == "__main__":
    faasm_main()
