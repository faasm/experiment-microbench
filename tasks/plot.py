from invoke import task
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from os.path import join
from tasks.env import PROJ_ROOT

PYPERF_NATIVE_RESULTS = join(PROJ_ROOT, "results", "pyperf_native_out.csv")
PYPERF_FAASM_RESULTS = join(PROJ_ROOT, "results", "pyperf_out.csv")
PYPERF_PLOT_FILE = join(PROJ_ROOT, "results", "pyperf_plot.png")

POLY_NATIVE_RESULTS = join(PROJ_ROOT, "results", "polybench_native_out.csv")
POLY_FAASM_RESULTS = join(PROJ_ROOT, "results", "polybench_out.csv")
POLY_PLOT_FILE = join(PROJ_ROOT, "results", "polybench_plot.png")


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

            data[bench_name].append((exec_time, reset_time))

    return data


@task
def pyperf(ctx, headless=False):
    """
    Plot the results of the python performance functions
    """
    native_data = read_results(PYPERF_NATIVE_RESULTS)
    faasm_data = read_results(PYPERF_FAASM_RESULTS)
    _do_plot(native_data, faasm_data, PYPERF_PLOT_FILE, headless)


@task
def polybench(ctx, headless=False):
    """
    Plot the results of the polybench functions
    """
    native_data = read_results(POLY_NATIVE_RESULTS)
    faasm_data = read_results(POLY_FAASM_RESULTS)
    _do_plot(native_data, faasm_data, POLY_PLOT_FILE, headless)


def _do_plot(native_data, faasm_data, plot_file, headless):
    exec_times = list()
    exec_errs = list()

    # Load data for all benchmarks
    bench_names = sorted(faasm_data.keys())
    print("Plotting benchmarks: {}".format(bench_names))
    for bench_name in bench_names:
        native_bench = native_data[bench_name]
        faasm_bench = faasm_data[bench_name]

        if len(native_bench) != len(faasm_bench):
            print(
                "Mismatched results: {} for native and {} for faasm".format(
                    len(native_bench), len(faasm_bench)
                )
            )

        # Calculate averages and stddevs
        native_execs = [n[0] for n in native_bench]
        faasm_execs = [n[0] for n in faasm_bench]

        # Get ratios of Faasm runtime to native
        faasm_ratios = list()
        for f, n in zip(faasm_execs, native_execs):
            faasm_ratios.append(f / n)

        exec_times.append(np.mean(faasm_ratios))
        exec_errs.append(np.std(faasm_ratios))

    # Plot the bar chart
    labels = [b.replace("bench_", "").replace("poly_", "") for b in bench_names]
    plt.bar(
        labels,
        exec_times,
        yerr=exec_errs,
        alpha=0.9,
        color="steelblue",
        ecolor="dimgrey",
        capsize=2,
    )

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

    plt.savefig(plot_file, format="png")

    if not headless:
        plt.show()
