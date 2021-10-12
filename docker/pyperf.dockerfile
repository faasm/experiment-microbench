FROM faasm/cpython:0.0.12

# Clone the code
RUN git clone https://github.com/faasm/experiment-microbench /code/experiment-microbench
WORKDIR /code/experiment-microbench

# TODO - remove once done devving
RUN git checkout first-cut

# Wasm build
# RUN inv pyperf

CMD "/bin/bash"

