FROM faasm/cpp-sysroot:0.1.0

# Hack to override CPP container venv
WORKDIR /code/cpp
RUN python3 -m venv --system-site-packages venv

# Clone the code
RUN git clone https://github.com/faasm/experiment-microbench /code/experiment-microbench
WORKDIR /code/experiment-microbench

RUN pip3 install -r requirements.txt

# Wasm build
RUN inv polybench

CMD "/bin/bash"
