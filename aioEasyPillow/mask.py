"""
MIT License

Copyright (c) 2021-2022 shahriyardx
Copyright (c) 2022-present Guddi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

from io import BytesIO
from typing import List, Tuple, Union

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from typing_extensions import Literal

from .canvas import Canvas
from .editor import Editor
from .font import Font
from .text import Text
from .utils import run_in_executor


class Mask:
    """Mask class. Works like :class:`Editor` but with some extra mask features.

    Parameters
    ----------
    size_or_image: Union[Tuple[:class:`float`, :class:`float`], :class:`Editor`, :class:`Canvas`, :class:`Image.Image`]
        Size of mask, by default ``None``
        width: :class:`float`, optional
        Width of image, by default ``None``
    height: :class:`float`, optional
        Height of image, by default ``None``
    antialias: :class:`int`
        The factor used for anti-aliasing.
    """

    def __init__(
            self,
            size: Tuple[float, float],
            width: float = None,
            height: float = None,
            antialias: int = 4
    ) -> None:
        if width and height:
            size = (width, height)

        if not size:
            raise ValueError('size, width, and height cannot all be None')


        self.size: Tuple[float, float] = size
        # self.size: Tuple[float, float] = (size[0] * antialias, size[1] * antialias)  # for later
        self.image: Image.Image = Canvas(size, (255,255,255,0)).image


    async def ellipse(
            self,
            position: Tuple[float, float],
            width: float,
            height: float,
            outline: Union[str, int, Tuple[int, int, int]] = None,
            stroke_width: float = 1,
    ):
        editor = Editor(self.image)
        await editor.ellipse(position, width, height, color='white', outline=outline, stroke_width=stroke_width)
        self.image = editor.image

    async def use_on_image(self, image: Union[Image.Image, Editor, Canvas]) -> Editor:
        """Use the mask on an Image.

        Parameters
        ----------
        image: Union[:class:`Image.Image`, :class:`Editor`, :class:`Canvas`]
            The to use the mask on

        Returns
        -------
            :class:`Editor`
            Creates a new Editor object, the mask stays the same.
        """
        if isinstance(image, (Editor, Canvas)):
            image = image.image

        background = Canvas(image.size, (255, 255, 255, 0)).image
        image = Image.composite(image, background, self.image)
        return Editor(image)


    async def show(self):
        self.image.show()