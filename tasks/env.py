from os import environ
from os.path import dirname, realpath, expanduser, join, exists

HOME_DIR = expanduser("~")
PROJ_ROOT = dirname(dirname(realpath(__file__)))

NATIVE_BUILD_DIR = join(PROJ_ROOT, "build", "native")

FAASM_UPLOAD_HOST = "localhost"
FAASM_UPLOAD_PORT = "8002"


def get_faasm_root():
    faasm_root = environ.get("FAASM_ROOT", "")

    if not faasm_root:
        print("Must set FAASM_ROOT to Faasm project root")
        exit(1)

    if not exists(faasm_root):
        print("FAASM_ROOT {} does not exist".format(faasm_root))

    print("Taking FAASM_ROOT={}".format(faasm_root))
    return faasm_root


def get_version():
    ver_file = join(PROJ_ROOT, "VERSION")

    with open(ver_file, "r") as fh:
        version = fh.read()
        version = version.strip()

    return version
