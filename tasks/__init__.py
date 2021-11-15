from invoke import Collection

from . import container
from . import plot
from . import polybench
from . import pyperf

ns = Collection(
    container,
    plot,
    polybench,
    pyperf,
)
