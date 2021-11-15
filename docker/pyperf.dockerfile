FROM faasm/cpython:0.1.0

RUN apt update
RUN apt install -y \
    python3-dev \
    python3-matplotlib \
    python3-pyaes

# Clone the code
RUN git clone https://github.com/faasm/experiment-microbench /code/experiment-microbench
WORKDIR /code/experiment-microbench

# TEMP - checkout dev branch
RUN git checkout native-py

# Install Python deps
RUN pip3 install -r requirements.txt

# Build the native runner
RUN inv pyperf.native-build

CMD "/bin/bash"

