from invoke import Collection

from . import container
from . import polybench
from . import pyperf

ns = Collection(
    container,
    polybench,
    pyperf,
)
