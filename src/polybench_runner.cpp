#include <wait.h>

#include <algorithm>
#include <chrono>
#include <fstream>
#include <vector>

#include "runner.h"

int main(int argc, char* argv[]) {
    if (argc < 3) {
        printf("Usage:\npolybench_runner <benchmark> <nRuns>\n");
        return 1;
    }

    std::string benchmark = argv[1];
    int iterations = std::stoi(argv[2]);

    printf("Running polybench benchmark [%s] %i times\n", benchmark.c_str(),
           iterations);

    const char* baseDir = getBaseDir();

    std::vector<std::string> allBenchmarks = {
        "poly_covariance",  "poly_correlation",
        "poly_2mm",         "poly_3mm",
        "poly_atax",        "poly_bicg",
        "poly_doitgen",     "poly_mvt",
        "poly_cholesky",    "poly_durbin",
        "poly_gramschmidt", "poly_lu",
        "poly_ludcmp",      "poly_trisolv",
        "poly_deriche",     "poly_floyd-warshall",
        "poly_nussinov",    "poly_adi",
        "poly_fdtd-2d",     "poly_heat-3d",
        "poly_jacobi-1d",   "poly_jacobi-2d",
        "poly_seidel-2d",
    };

    std::vector<std::string> benchmarks =
        filterBenchmarks(allBenchmarks, benchmark);

    std::string outFile =
        std::string(baseDir) + "/results/polybench_native_out.csv";
    printf("Project root: %s\n", baseDir);
    printf("Output file: %s\n", outFile.c_str());

    // Prepare output
    std::ofstream profOut;
    profOut.open(outFile);

    // Use same format as microbench runner
    profOut << "User,Function,Return value,Execution (us),Reset (us)"
            << std::endl;

    for (auto const& b : benchmarks) {
        std::string binPath = std::string(baseDir) + "/build/native/bin/" + b;

        for (int i = 0; i < iterations; i++) {
            printf("Running %s\n", b.c_str());
            long runtimeStart = microsNow();

            // TODO - is it possible to avoid system here?
            int error = system(binPath.c_str());
            if (error != 0) {
                printf("Failed to execute %s", binPath.c_str());
            }
            long runTimeUs = microsNow() - runtimeStart;

            // Write result
            profOut << "polybench," << b << ",0," << runTimeUs << ",0\n";
            printf("Ran %s in %luus\n", b.c_str(), runTimeUs);
        }
    }

    profOut.flush();
    profOut.close();
    return 0;
}
