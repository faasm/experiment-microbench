#include "runner.h"

#include <Python.h>

#include <wait.h>
#include <fstream>

int main(int argc, char* argv[]) {
    if (argc < 3) {
        printf("Usage:\npy_runner <benchmark> <nRuns>\n");
        return 1;
    }

    std::string benchmark = argv[1];
    int iterations = std::stoi(argv[2]);

    const char* baseDir = getBaseDir();

    std::vector<std::string> allBenchmarks = {
        "bench_chaos",      "bench_deltablue",       "bench_dulwich",
        "bench_fannkuch",   "bench_float",           "bench_genshi",
        "bench_go",         "bench_hexiom",          "bench_json_dumps",
        "bench_json_loads", "bench_logging",         "bench_mdp",
        "bench_nbody",      "bench_pickle",          "bench_pidigits",
        "bench_pyaes",      "bench_pyflate",         "bench_raytrace",
        "bench_richards",   "bench_scimark",         "bench_spectral_norm",
        "bench_telco",      "bench_unpack_sequence", "bench_version",
    };

    std::vector<std::string> benchmarks =
        filterBenchmarks(allBenchmarks, benchmark);

    std::string outFile =
        std::string(baseDir) + "/results/pyperf_native_out.csv";
    printf("Project root: %s\n", baseDir);
    printf("Output file: %s\n", outFile.c_str());

    // Prepare output
    {
        std::ofstream profOut;
        profOut.open(outFile);

        // Use same format as microbench runner
        profOut << "User,Function,Return value,Execution (us),Reset (us)"
                << std::endl;
        profOut.flush();
        profOut.close();
    }

    for (auto const& b : benchmarks) {
        std::string filePath =
            std::string(baseDir) + "/func/python/" + b + ".py";

        for (int i = 0; i < iterations; i++) {
            // To avoid contamination across runs, fork a new process
            long forkStart = microsNow();
            int pid = fork();

            if (pid == 0) {
                long forkTimeUs = microsNow() - forkStart;

                // Open the python file
                FILE* fp = fopen(filePath.c_str(), "r");
                if (fp == nullptr) {
                    throw std::runtime_error("Failed to open python file");
                }

                printf("Running python function: %s\n", filePath.c_str());

                // ---- Running ----
                long runtimeStart = microsNow();
                Py_InitializeEx(0);

                PyRun_SimpleFile(fp, filePath.c_str());
                long runTimeUs = microsNow() - runtimeStart;

                // ---- Reset ----
                long resetStart = microsNow();
                Py_FinalizeEx();
                fclose(fp);
                long resetUs = (microsNow() - resetStart) + forkTimeUs;

                // Prepare output
                std::ofstream outStream;
                outStream.open(outFile, std::ios_base::app);

                // Write result
                outStream << "python," << b << ",0," << runTimeUs << ","
                          << resetUs << "\n";
                outStream.flush();
                outStream.close();

                exit(0);
            } else {
                int status = 0;
                while (-1 == waitpid(pid, &status, 0))
                    ;

                if (!WIFEXITED(status) || WEXITSTATUS(status) != 0) {
                    printf("Failed running native python benchmark %s\n",
                           filePath.c_str());
                    exit(1);
                }
            }
        }
    }

    return 0;
}
