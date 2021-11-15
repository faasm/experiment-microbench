#include <Python.h>
#include <wait.h>

#include <algorithm>
#include <chrono>
#include <fstream>
#include <vector>

#define OUTPUT_FILE "results/pyperf_native_out.csv"

long runPythonFile(const char* pyPath) {
    // To avoid contamination across runs, fork a new process
    int pid = fork();

    long startUs = std::chrono::duration_cast<std::chrono::microseconds>(
                      std::chrono::system_clock::now().time_since_epoch())
                      .count();

    if (pid == 0) {
        // Try to open it
        FILE* fp = fopen(pyPath, "r");
        if (fp == nullptr) {
            throw std::runtime_error("Failed to open python file");
        }

        printf("Running python function: %s\n", pyPath);

        Py_InitializeEx(0);

        PyRun_SimpleFile(fp, pyPath);

        Py_FinalizeEx();

        fclose(fp);

        exit(0);
    } else {
        int status = 0;
        while (-1 == waitpid(pid, &status, 0))
            ;

        if (!WIFEXITED(status) || WEXITSTATUS(status) != 0) {
            printf("Failed running native python benchmark %s\n", pyPath);
            exit(1);
        }
    }

    long endUs = std::chrono::duration_cast<std::chrono::microseconds>(
                      std::chrono::system_clock::now().time_since_epoch())
                      .count();

    long runTime = endUs - startUs;

    return runTime;
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        printf("Usage:\npy_runner <benchmark> <nRuns>");
        return 1;
    }

    std::string benchmark = argv[1];
    int iterations = std::stoi(argv[2]);

    std::vector<std::string> all_benchmarks = {
        "bench_chaos",      "bench_deltablue",       "bench_dulwich",
        "bench_fannkuch",   "bench_float",           "bench_genshi",
        "bench_go",         "bench_hexiom",          "bench_json_dumps",
        "bench_json_loads", "bench_logging",         "bench_mdp",
        "bench_nbody",      "bench_pickle",          "bench_pidigits",
        "bench_pyaes",      "bench_pyflate",         "bench_raytrace",
        "bench_richards",   "bench_scimark",         "bench_spectral_norm",
        "bench_telco",      "bench_unpack_sequence", "bench_version",
    };

    std::vector<std::string> benchmarks;
    if (benchmark == "all") {
        benchmarks = all_benchmarks;
    } else if (std::find(all_benchmarks.begin(), all_benchmarks.end(),
                         benchmark) != all_benchmarks.end()) {
        benchmarks = {benchmark};
    } else {
        printf("Unrecognised benchmark: %s\n", benchmark.c_str());
        return 1;
    }

    // Prepare output
    std::ofstream profOut;
    profOut.open(OUTPUT_FILE);
    profOut << "benchmark,type,microseconds" << std::endl;

    for (auto const& b : benchmarks) {
        // TODO - get file
        std::string filePath = "";
        for (int i = 0; i < iterations; i++) {
            long runTimeUs = runPythonFile(filePath.c_str());

            // TODO - write to file
        }
    }

    profOut.flush();
    profOut.close();

    return 0;
}
