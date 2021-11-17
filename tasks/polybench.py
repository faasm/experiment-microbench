from invoke import task
from shutil import rmtree
from copy import copy
import os
from os.path import exists, join
from os import makedirs, listdir
from subprocess import run
import requests

from tasks.env import (
    PROJ_ROOT,
    FAASM_UPLOAD_HOST,
    FAASM_UPLOAD_PORT,
    NATIVE_BUILD_DIR,
)

CMAKE_TOOLCHAIN_FILE = "/usr/local/faasm/toolchain/tools/WasiToolchain.cmake"

POLYBENCH_BUILD_DIR = join(PROJ_ROOT, "build", "polybench")
POLYBENCH_SRC_DIR = join(PROJ_ROOT, "func", "polybench")

POLYBENCH_USER = "polybench"


@task
def wasm(ctx, clean=False):
    """
    Builds the polybench functions to wasm
    """
    _do_build(POLYBENCH_BUILD_DIR, True, clean)


@task
def native_build(ctx, clean=False):
    """
    Builds the polybench functions natively
    """
    _do_build(NATIVE_BUILD_DIR, False, clean)


def _do_build(build_dir, is_wasm, clean):
    if clean and exists(build_dir):
        rmtree(build_dir)

    makedirs(build_dir, exist_ok=True)

    cmake_cmd = [
        "cmake",
        "-GNinja",
        "-DCMAKE_BUILD_TYPE=Release",
    ]

    if is_wasm:
        cmake_cmd.extend(
            [
                "-DFAASM_BUILD_TYPE=wasm",
                "-DCMAKE_TOOLCHAIN_FILE={}".format(CMAKE_TOOLCHAIN_FILE),
                POLYBENCH_SRC_DIR
            ]
        )
    else:
        cmake_cmd.append(PROJ_ROOT)

    cmake_cmd_str = " ".join(cmake_cmd)

    run(cmake_cmd_str, shell=True, check=True, cwd=build_dir)

    run(
        "cmake --build . --target polybench_all",
        shell=True,
        check=True,
        cwd=build_dir,
    )

    if not is_wasm:
        run(
            "cmake --build . --target polybench_runner",
            shell=True,
            check=True,
            cwd=build_dir,
        )


@task
def upload(ctx, clean=False):
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
        response = requests.put(url, data=open(full_file, "rb"))

        print("Response ({}): {}".format(response.status_code, response.text))


@task
def native_run(ctx, clean=False, bench="all", reps=3):
    """
    Runs the native polybench benchmarks
    """
    binary = join(NATIVE_BUILD_DIR, "bin", "polybench_runner")

    env = copy(os.environ)
    env["MICROBENCH_ROOT"] = PROJ_ROOT

    cmd = "{} {} {}".format(binary, bench, str(reps))
    run(cmd, check=True, shell=True, env=env)
