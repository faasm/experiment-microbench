#!/bin/bash

set -e

if [[ -z "${FAASM_ROOT}" ]]; then
    echo "Must set FAASM_ROOT to Faasm checkout"
    exit 1
fi

EXPERIMENT=$1

echo "Copying ${EXPERIMENT} spec into place"
cp ${EXPERIMENT}.csv ${FAASM_ROOT}/bench

pushd ${FAASM_ROOT} >> /dev/null

echo "Running ${EXPERIMENT} benchmark"
docker-compose exec faasm-cli \
  /build/faasm/bin/microbench_runner \
  /usr/local/code/faasm/bench/${EXPERIMENT}.csv \
  /usr/local/code/faasm/bench/${EXPERIMENT}_out.csv

popd

mkdir -p results
cp ${FAASM_ROOT}/bench/${EXPERIMENT}_out.csv results
echo "Results at $(pwd)/results/${EXPERIMENT}_out.csv"
