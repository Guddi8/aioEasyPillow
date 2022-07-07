"""
AsyncIO Easy Pillow
~~~~~~~~~~~~~~~~~~~

Async working easy to use Pillow Library.

:copyright: (c) 2021-2022 shahriyardx & (c) 2022-present Guddi
:license: MIT, see LICENSE for more details.

"""

__title__ = 'aioEasyPillow'
__author__ = 'Guddi'
__license__ = 'MIT'
__copyright__ = 'Copyright 2021-2022 shahriyardx & 2022-present Guddi'
__version__ = '0.0.3'

from typing import NamedTuple, Literal

from .canvas import Canvas
from .editor import Editor
from .font import Font
from .text import Text
from .utils import load_image, run_in_executor


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    release: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(major=0, minor=0, micro=3, release='final', serial=0)

del NamedTuple, Literal, VersionInfo