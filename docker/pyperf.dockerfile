FROM faasm/cpython:0.1.0

RUN apt update
RUN apt install -y python3-dev

# Clone the code
RUN git clone https://github.com/faasm/experiment-microbench /code/experiment-microbench

# TEMP - checkout dev branch
RUN git checkout native-py

WORKDIR /code/experiment-microbench

# Install Python deps
RUN pip3 install -r requirements.txt

# Build the native runner
RUN inv pyperf.native-build

CMD "/bin/bash"

