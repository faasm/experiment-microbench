import requests
from os.path import join
from invoke import task
from os import listdir
from tasks.env import PROJ_ROOT, FAASM_UPLOAD_HOST, FAASM_UPLOAD_PORT

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
        url = "http://{}:{}/p/{}/{}".format(
            FAASM_UPLOAD_HOST, FAASM_UPLOAD_PORT, USER, func
        )

        print(
            "Uploading {} to {}:{}".format(
                func_file, FAASM_UPLOAD_HOST, FAASM_UPLOAD_PORT
            )
        )
        response = requests.put(url, data=open(func_file, "rb"))

        print("Response ({}): {}".format(response.status_code, response.text))
