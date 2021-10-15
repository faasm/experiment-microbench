FROM faasm/cpython:0.1.0

# Clone the code
RUN git clone https://github.com/faasm/experiment-microbench /code/experiment-microbench
WORKDIR /code/experiment-microbench

CMD "/bin/bash"

