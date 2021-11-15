import requests
from os.path import join
from invoke import task
from os import listdir
from tasks.env import PROJ_ROOT, FAASM_UPLOAD_HOST, FAASM_UPLOAD_PORT
from invoke import task
from shutil import rmtree
from os.path import exists
from os import makedirs
from subprocess import run

from tasks.env import PROJ_ROOT, NATIVE_BUILD_DIR


PY_FUNC_DIR = join(PROJ_ROOT, "func", "python")

USER = "python"


@task(default=True)
def upload(ctx):
    """
    Upload the python performance functions
    """
    funcs = listdir(PY_FUNC_DIR)
    funcs = [f for f in funcs if f.endswith(".py")]

    for func in funcs:
        func_file = join(PY_FUNC_DIR, func)
        func_name = func.replace(".py", "")
        url = "http://{}:{}/p/{}/{}".format(
            FAASM_UPLOAD_HOST, FAASM_UPLOAD_PORT, USER, func_name
        )

        print(
            "Uploading {} to {}:{}".format(
                func_file, FAASM_UPLOAD_HOST, FAASM_UPLOAD_PORT
            )
        )
        response = requests.put(url, data=open(func_file, "rb"))

        print("Response ({}): {}".format(response.status_code, response.text))


@task
def native_build(ctx, clean=False):
    """
    Builds the native python benchmark runner
    """
    if clean and exists(NATIVE_BUILD_DIR):
        rmtree(NATIVE_BUILD_DIR)

    makedirs(NATIVE_BUILD_DIR, exist_ok=True)

    cmake_cmd = [
        "cmake",
        "-GNinja",
        "-DCMAKE_BUILD_TYPE=Release",
        "-DCMAKE_CXX_COMPILER=/usr/bin/clang++-10",
        "-DCMAKE_C_COMPILER=/usr/bin/clang-10",
        PROJ_ROOT,
    ]
    cmake_cmd_str = " ".join(cmake_cmd)

    run(cmake_cmd_str, shell=True, check=True, cwd=NATIVE_BUILD_DIR)

    run(
        "cmake --build . --target py_runner",
        shell=True,
        check=True,
        cwd=NATIVE_BUILD_DIR,
    )


@task
def native_run(ctx, clean=False):
    """
    Runs the native python benchmarks
    """
    pass
