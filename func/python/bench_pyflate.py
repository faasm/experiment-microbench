import os

from pyperformance.benchmarks.bm_pyflate import bench_pyflake


def faasm_main():
    if os.environ.get("PYTHONWASM") == "1":
        file_path = "/lib/python3.8/site-packages/pyperformance/benchmarks/data/interpreter.tar.bz2"
    else:
        file_path = "/code/cpp/venv/lib/python3.8/site-packages/pyperformance/benchmarks/data/interpreter.tar.bz2"

    bench_pyflake(1, file_path)

    return 0


if __name__ == "__main__":
    faasm_main()
