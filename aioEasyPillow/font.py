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

import os

from PIL import ImageFont
from typing import Literal, Optional

fonts_directory = os.path.join(os.path.dirname(__file__), 'fonts')
fonts_path = {
    'caveat': {
        'regular': os.path.join(fonts_directory, 'caveat', 'caveat.ttf'),
        'bold': os.path.join(fonts_directory, 'caveat', 'caveat.ttf'),
        'italic': os.path.join(fonts_directory, 'caveat', 'caveat.ttf'),
        'light': os.path.join(fonts_directory, 'caveat', 'caveat.ttf'),
    },
    'montserrat': {
        'regular': os.path.join(
            fonts_directory, 'montserrat', 'montserrat_regular.ttf'
        ),
        'bold': os.path.join(fonts_directory, 'montserrat', 'montserrat_bold.ttf'),
        'italic': os.path.join(fonts_directory, 'montserrat', 'montserrat_italic.ttf'),
        'light': os.path.join(fonts_directory, 'montserrat', 'montserrat_light.ttf'),
    },
    'poppins': {
        'regular': os.path.join(fonts_directory, 'poppins', 'poppins_regular.ttf'),
        'bold': os.path.join(fonts_directory, 'poppins', 'poppins_bold.ttf'),
        'italic': os.path.join(fonts_directory, 'poppins', 'poppins_italic.ttf'),
        'light': os.path.join(fonts_directory, 'poppins', 'poppins_light.ttf'),
    },
}


class Font:
    """Font class

    Parameters
    ----------
    path: :class:`str`
        Path of font
    size: :class:`int`, optional
        Size of font, by default ``10``
    """

    def __init__(self, path: str, size: Optional[int] = 10, **kwargs) -> None:
        self.font = ImageFont.truetype(path, size=size, **kwargs)

    @classmethod
    def poppins(
        cls,
        variant: Literal['regular', 'bold', 'italic', 'light'] = 'regular',
        size: int = 10,
        **kwargs
    ):
        """Poppins font

        Parameters
        ----------
        variant: Literal['regular', 'bold', 'italic', 'light'], optional
            Font variant, by default ``'regular'``
        size: :class:`int`, optional
            Font size, by default ``10``
        """
        return cls(fonts_path["poppins"][variant], size, **kwargs)

    @classmethod
    def caveat(
        cls,
        variant: Literal['regular', 'bold', 'italic', 'light'] = 'regular',
        size: int = 10,
        **kwargs
    ):
        """Caveat font

        Parameters
        ----------
        variant: Literal['regular', 'bold', 'italic', 'light'], optional
            Font variant, by default ``'regular'``
        size: :class:`int`, optional
            Font size, by default ``10``
        """
        return cls(fonts_path["caveat"][variant], size, **kwargs)

    @classmethod
    def montserrat(
        cls,
        variant: Literal['regular', 'bold', 'italic', 'light'] = 'regular',
        size: int = 10,
        **kwargs
    ):
        """Montserrat font

        Parameters
        ----------
        variant: Literal['regular', 'bold', 'italic', 'light'], optional
            Font variant, by default ``'regular'``
        size: :class:`int`, optional
            Font size, by default ``10``
        """
        return cls(fonts_path["montserrat"][variant], size, **kwargs)
