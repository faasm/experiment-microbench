from invoke import task
from shutil import rmtree
from os.path import exists, join
from os import makedirs, listdir
from subprocess import run
import requests

from tasks.env import PROJ_ROOT, FAASM_UPLOAD_HOST, FAASM_UPLOAD_PORT

CMAKE_TOOLCHAIN_FILE = "/usr/local/faasm/toolchain/tools/WasiToolchain.cmake"

POLYBENCH_BUILD_DIR = join(PROJ_ROOT, "build", "polybench")
POLYBENCH_SRC_DIR = join(PROJ_ROOT, "func", "polybench")

POLYBENCH_USER = "polybench"


@task(default=True)
def build(ctx, clean=False):
    """
    Builds the polybench functions
    """
    if clean and exists(POLYBENCH_BUILD_DIR):
        rmtree(POLYBENCH_BUILD_DIR)

    makedirs(POLYBENCH_BUILD_DIR, exist_ok=True)

    cmake_cmd = [
        "cmake",
        "-GNinja",
        "-DCMAKE_BUILD_TYPE=Release",
        "-DCMAKE_TOOLCHAIN_FILE={}".format(CMAKE_TOOLCHAIN_FILE),
        POLYBENCH_SRC_DIR,
    ]
    cmake_cmd_str = " ".join(cmake_cmd)

    run(cmake_cmd_str, shell=True, check=True, cwd=POLYBENCH_BUILD_DIR)

    run(
        "cmake --build . --target polybench_all",
        shell=True,
        check=True,
        cwd=POLYBENCH_BUILD_DIR,
    )

    all_files = listdir(POLYBENCH_BUILD_DIR)
    wasm_files = [f for f in all_files if f.endswith(".wasm")]

    for wasm_file in wasm_files:
        func_name = wasm_file.replace(".wasm", "")
        full_file = join(POLYBENCH_BUILD_DIR, wasm_file)

        print(
            "Uploading {} to {}:{}".format(
                full_file, POLYBENCH_USER, func_name
            )
        )
        url = "http://{}:{}/f/{}/{}".format(
            FAASM_UPLOAD_HOST, FAASM_UPLOAD_PORT, POLYBENCH_USER, func_name
        )
        requests.put(url, data=open(full_file, "rb"))
