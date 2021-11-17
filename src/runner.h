#include <stdio.h>
#include <stdlib.h>

#include <algorithm>
#include <chrono>
#include <stdexcept>
#include <vector>

long microsNow() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
               std::chrono::system_clock::now().time_since_epoch())
        .count();
}

const char* getBaseDir() {
    const char* baseDir = getenv("MICROBENCH_ROOT");
    if (baseDir == nullptr) {
        throw std::runtime_error(
            "Must set MICROBENCH_ROOT env var to the root of the project\n");
    }

    return baseDir;
}

std::vector<std::string> filterBenchmarks(
    std::vector<std::string> allBenchmarks, const std::string& benchmark) {
    std::vector<std::string> benchmarks;
    if (benchmark == "all") {
        benchmarks = allBenchmarks;
    } else if (std::find(allBenchmarks.begin(), allBenchmarks.end(),
                         benchmark) != allBenchmarks.end()) {
        benchmarks = {benchmark};
    } else {
        throw std::runtime_error("Unrecognised benchmark: " + benchmark);
    }

    return benchmarks;
}
