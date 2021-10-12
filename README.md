# Faasm Microbenchmarks

These benchmarks aim to test the performance of Faasm's internals, rather than
the full end-to-end request cycle.

They include:

- Polybench/C
- Python performance benchmarks

## Set up and usage

First you need to set up a local Faasm cluster, as per the [Faasm
docs](https://github.com/faasm/faasm).

Check this is running with:

```bash
curl http://localhost:8002/ping
```

### Polybench/C

The Polybench functions are checked into this repo, and can be built with the
[Faasm C++ toolchain](https://github.com/faasm/cpp).

To do this, from the root of this repo:

```bash
docker-compose run polybench

inv polybench
```

### Python performance benchmarks

The Python performance benchmarks also contain some C/C++ code, which must also
be built and uploaded using the [Faasm Python
toolchain](https://github.com/faasm/python).

To do this, from the root of this repo:

```bash
docker-compose run pyperf

inv pyperf
```

## Docker images

To rebuild the Docker images, set up the virtualenv, then:

```bash
inv container.polybench --push

inv container.pyperf --push
```
