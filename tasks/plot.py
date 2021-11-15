from invoke import task
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import os
from os import listdir, makedirs
from os.path import join, exists
from tasks.env import (
    PROJ_ROOT,
    FAASM_UPLOAD_HOST,
    FAASM_UPLOAD_PORT,
    NATIVE_BUILD_DIR,
)

NATIVE_RESULTS = join(PROJ_ROOT, "results", "pyperf_native_out.csv")
FAASM_RESULTS = join(PROJ_ROOT, "results", "pyperf_out.csv")
PLOT_FILE = join(PROJ_ROOT, "results", "pyperf_plot.png")


def read_results(csv_path):
    data = defaultdict(list)
    with open(csv_path, "r") as fh:
        for line in fh:
            if line.startswith("User"):
                continue

            line_parts = line.split(",")
            line_parts = [lp.strip() for lp in line_parts if lp.strip()]

            bench_name = line_parts[1]
            exec_time = float(line_parts[3])
            reset_time = float(line_parts[4])

            print(
                "Found {}: {}us {}us".format(bench_name, exec_time, reset_time)
            )

            data[bench_name].append((exec_time, reset_time))

    return data


@task
def pyperf(ctx, headless=False):
    """
    Plot the results of the python performance functions
    """
    native_data = read_results(NATIVE_RESULTS)
    faasm_data = read_results(FAASM_RESULTS)

    bench_names = list()
    exec_times = list()

    for bench_name in native_data.keys():
        print("Found native bench {}".format(bench_name))
        if bench_name not in faasm_data:
            print("No Faasm data for bench {}".format(bench_name))
            continue

        native_bench = native_data[bench_name]
        faasm_bench = faasm_data[bench_name]

        native_exec = np.mean([n[0] for n in native_bench])
        faasm_exec = np.mean([n[0] for n in faasm_bench])

        faasm_ratio = faasm_exec / native_exec

        exec_times.append(faasm_ratio)
        bench_names.append(bench_name)

    plt.bar(bench_names, exec_times)

    ax = plt.gca()
    ax.axhline(1.0, linestyle="--", color="red")
    plt.setp(
        ax.xaxis.get_majorticklabels(),
        rotation=45,
        ha="right",
        rotation_mode="anchor",
    )

    ax.set_ylabel("vs. native")

    plt.tight_layout()

    if headless:
        plt.savefig(PLOT_FILE, format="png")
    else:
        plt.show()
