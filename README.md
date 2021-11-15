# Faasm Microbenchmarks

These benchmarks aim to test the performance of Faasm's internals, rather than
the full end-to-end request cycle.

They include:

- Polybench/C
- Python performance benchmarks

## Local Faasm set-up

First you need to clone the [Faasm repo](https://github.com/faasm/faasm)
somewhere on your host.

Then set `FAASM_ROOT` to the location of this checkout.

From there, set up a local cluster that is able to execute Python functions,
according to the [Python
quick-start](https://github.com/faasm/faasm/blob/master/docs/python.md).

Then you need to build the benchmark runner:

```bash
cd ${FAASM_ROOT}
mkdir -p bench

# Start the faasm-cli container in the background
docker-compose up -d --no-recreate faasm-cli

# Get a terminal
docker-compose exec faasm-cli /bin/bash

# Set up the release build
inv dev.cmake --build=Release

# Build the benchmarker
inv dev.cc microbench_runner
```

## Polybench/C

The Polybench functions are checked into this repo, and can be built with the
[Faasm C++ toolchain](https://github.com/faasm/cpp).

To set up the functions:

```bash
# Enter the container
docker-compose run polybench

# Compile and upload
inv polybench
inv polybench.upload

# Exit
exit
```

Then run with:

```bash
./bin/run.sh polybench
```

Results are found at `results/polybench_out.csv`.

## Python performance benchmarks

Faasm's [Python support](https://github.com/faasm/python) includes the Python
performance benchmarks library and the transitive dependencies for the
benchmarks, hence we just need to upload the functions.

To set up the functions:

```bash
# Run container
docker-compose run pyperf

# Upload Python benchmark functions
inv pyperf.upload

# Leave container
exit
```

Then run with:

```bash
./bin/run.sh pyperf
```

Results are found at `results/pyperf_out.csv`.

### Native Python run

To run the benchmarks natively and ensure a like-for-like comparison, you can
set up and run the native Python benchmark runner with:

```bash
docker-compose run pyperf

inv pyperf.native

inv pyperf.native-run
```

Results are found at `results/pyperf_native_out.csv`.

### Plotting results

Once you've got both the Faasm and native runs, you can plot them with:

```bash
# If you have a display
int plot.pyperf

# Headless
int plot.pyperf --headless
```

## Docker images

To rebuild the Docker images, set up the virtualenv, then:

```bash
inv container.polybench --push

inv container.pyperf --push
```
