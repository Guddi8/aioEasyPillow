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

from typing import Tuple, Union

from PIL import ImageFont

from .font import Font


class Text:
    """Text class

    Parameters
    ----------
    text: :class:`str`
        Text to write
    font: Union[:class:`Font`, :class:`ImageFont.FreeTypeFont`]
        Font for the text
    color: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
        Font color, by default ``'black'``
    stroke_width: :class:`int`, optional
        The optional width of the text stroke, by default ``None``. Set this to ``0`` to disable the stroke.
    stroke_color: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
        Color to use for the text stroke, by default ``None``
    """

    def __init__(
        self,
        text: str,
        font: Union[Font, ImageFont.FreeTypeFont],
        color: Union[Tuple[int, int, int], str, int] = 'black',
        stroke_width: int = None,
        stroke_color: Union[Tuple[int, int, int], str, int] = None,
    ) -> None:
        self.text = text
        self.font = font.font if isinstance(font, Font) else font
        self.color = color
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color