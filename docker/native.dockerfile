FROM faasm/faabric-base:0.2.0

WORKDIR /code/experiment

COPY . .

WORKDIR /code/experiment/build
RUN cmake -DCMAKE_BUILD_TYPE=Release \
    -GNinja \
    -DCMAKE_CXX_COMPILER=/usr/bin/clang++-10 \
    -DCMAKE_C_COMPILER=/usr/bin/clang-10 \
    ..

RUN cmake --build py_runner


