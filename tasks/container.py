from invoke import task
from tasks.env import PROJ_ROOT, get_version
from os import environ
from os.path import join
from copy import copy
from subprocess import run


@task
def polybench(ctx, nocache=False, push=False):
    """
    Build the polybench experiment image
    """
    _do_build("polybench", nocache, push)


@task
def pyperf(ctx, nocache=False, push=False):
    """
    Build the pyperf experiment image
    """
    _do_build("pyperf", nocache, push)


def _do_build(experiment_name, nocache=False, push=False):
    shell_env = copy(environ)
    shell_env["DOCKER_BUILDKIT"] = "1"

    img_tag = "faasm/experiment-{}:{}".format(experiment_name, get_version())

    dockerfile = join(
        PROJ_ROOT, "docker", "{}.dockerfile".format(experiment_name)
    )

    cmd = [
        "docker",
        "build",
        "-f {}".format(dockerfile),
        "--no-cache" if nocache else "",
        "-t {}".format(img_tag),
        ".",
    ]

    cmd_str = " ".join(cmd)
    print(cmd_str)
    run(cmd_str, shell=True, check=True, cwd=PROJ_ROOT)

    if push:
        run("docker push {}".format(img_tag), check=True, shell=True)
