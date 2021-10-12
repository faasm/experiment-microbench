import requests
from os.path import join
from invoke import task
from os import listdir
from tasks.env import PROJ_ROOT

PY_FUNC_DIR = join(PROJ_ROOT, "func", "python")

USER = "python"


@task(default=True)
def upload(ctx, host="upload", port=8002):
    """
    Upload the python performance functions
    """
    funcs = listdir(PY_FUNC_DIR)
    funcs = [f for f in funcs if f.endswith(".py")]

    for func in funcs:
        func_file = join(PY_FUNC_DIR, func)
        url = "http://{}:{}/p/{}/{}".format(host, port, USER, func)

        print("Uploading {} to {}:{}".format(func_file, host, port))
        response = requests.put(url, data=open(func_file, "rb"))

        print("Response ({}): {}".format(response.status_code, response.text))
