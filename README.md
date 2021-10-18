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

docker-compose run faasm-cli /bin/bash

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

Results are found at `polybench_out.csv` in the root of this directory.

### Python performance benchmarks

Faasm's [Python support](https://github.com/faasm/python) includes the Python
performance benchmarks library and the transitive dependencies for the
benchmarks, hence we just need to upload the functions.

To set up the functions:

```bash
# Run container
docker-compose run pyperf

# Upload Python benchmark functions
inv pyperf

# Leave container
exit
```

Then run with:

```bash
./bin/run.sh pyperf
```

Results are found at `pyperf_out.csv` in the root of this directory.

## Docker images

To rebuild the Docker images, set up the virtualenv, then:

```bash
inv container.polybench --push

inv container.pyperf --push
```

