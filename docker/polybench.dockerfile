FROM faasm/cpp-sysroot:0.0.28

# Clone the code
RUN git clone https://github.com/faasm/experiment-microbench /code/experiment-microbench
WORKDIR /code/experiment-microbench

# Wasm build
RUN inv polybench

CMD "/bin/bash"
