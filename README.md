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

./bin/cli.sh faasm

# Set up the release build
inv dev.cmake --build=Release

# Build the benchmarker
inv dev.cc microbench_runner
```

## Polybench/C

The Polybench functions are checked into this repo, and can be built with the
[Faasm C++ toolchain](https://github.com/faasm/cpp).

To do this and upload to Faasm, from the root of this repo:

```bash
docker-compose run polybench

inv polybench
inv polybench.upload
```

Set up the spec for the Faasm benchmark:

```bash
cp polybench.csv ${FAASM_ROOT}/bench
```

Run the benchmark:

```bash
cd ${FAASM_ROOT}
docker-compose exec faasm-cli \
  /build/faasm/bin/microbench_runner \
  /usr/local/code/faasm/bench/polybench.csv \
  /usr/local/code/faasm/bench/polybench_out.csv
```

You can then parse the data at `${FAASM_ROOT}/bench/polybench_out.csv`.

### Python performance benchmarks

Faasm's [Python support](https://github.com/faasm/python) includes the Python
performance benchmarks library and the transitive dependencies for the
benchmarks, hence we just need to upload the functions.

To do this, from the root of this repo:

```bash
docker-compose run pyperf

inv pyperf
```

Set up the spec for the Faasm benchmark:

```bash
cp pyperf.csv ${FAASM_ROOT}/bench
```

Run the benchmark:

```bash
cd ${FAASM_ROOT}
docker-compose exec faasm-cli \
  /build/faasm/bin/microbench_runner \
  /usr/local/code/faasm/bench/pyperf.csv \
  /usr/local/code/faasm/bench/pyperf_out.csv
```

You can then parse the data at `${FAASM_ROOT}/bench/polybench_out.csv`.

## Docker images

To rebuild the Docker images, set up the virtualenv, then:

```bash
inv container.polybench --push

inv container.pyperf --push
```

