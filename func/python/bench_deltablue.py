from pyperformance.benchmarks.bm_deltablue import delta_blue


def faasm_main():
    delta_blue(100)
    return 0


if __name__ == "__main__":
    faasm_main()
