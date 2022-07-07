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
from .font import Font
from .text import Text
from .utils import run_in_executor


class Editor:
    """Editor class. It does all the editing operations.

    Parameters
    ----------
    image: Union[:class:`Image.Image`, :class:`str`, :class:`Editor`, :class:`Canvas`]
        Image or Canvas to edit.
    """

    def __init__(self, image: Union[Image.Image, str, BytesIO, Editor, Canvas]) -> None:
        if isinstance(image, str) or isinstance(image, BytesIO):
            self.image: Image.Image = Image.open(image)
        elif isinstance(image, Canvas) or isinstance(image, Editor):
            self.image: Image.Image = image.image
        else:
            self.image: Image.Image = image
        self.image: Image.Image = self.image.convert("RGBA")


    @property
    def image_bytes(self) -> BytesIO:
        """Return image bytes

        Returns
        -------
        :class:`BytesIO`
            Bytes from the image of Editor
        """
        _bytes = BytesIO()
        self.image.save(_bytes, "png")
        _bytes.seek(0)

        return _bytes


    async def resize(self, size: Tuple[float, float], crop: bool = False) -> Editor:
        """Resize image

        Parameters
        ----------
        size: Tuple[:class:`float`, :class:`float`]
            New Size of image
        crop: :class:`bool`, optional
            Crop the image to bypass distortion, by default ``False``
        """
        return await run_in_executor(self.__resize, size, crop=crop)

    def __resize(self, size: Tuple[float, float], crop=False) -> Editor:
        if not crop:
            self.image = self.image.resize(size, Image.ANTIALIAS)

        else:
            width, height = self.image.size
            ideal_width, ideal_height = size

            aspect = width / float(height)
            ideal_aspect = ideal_width / float(ideal_height)

            if aspect > ideal_aspect:
                new_width = int(ideal_aspect * height)
                offset = (width - new_width) / 2
                resize = (offset, 0, width - offset, height)
            else:
                new_height = int(width / ideal_aspect)
                offset = (height - new_height) / 2
                resize = (0, offset, width, height - offset)

            self.image = self.image.crop(resize).resize(
                (ideal_width, ideal_height), Image.ANTIALIAS
            )

        return self


    async def rounded_corners(self, radius: int = 10, offset: int = 2) -> Editor:
        """Make image rounded corners

        Parameters
        ----------
        radius: :class:`int`, optional
            Radius of roundness, by default ``10``
        offset: :class:`int`, optional
            Offset pixel while making rounded, by default ``2``
        """
        return await run_in_executor(self.__rounded_corners, radius, offset)

    def __rounded_corners(self, radius: int = 10, offset: int = 2) -> Editor:
        background = Image.new("RGBA", size=self.image.size, color=(255, 255, 255, 0))
        holder = Image.new("RGBA", size=self.image.size, color=(255, 255, 255, 0))
        mask = Image.new("RGBA", size=self.image.size, color=(255, 255, 255, 0))
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle(
            (offset, offset) + (self.image.size[0] - offset, self.image.size[1] - offset),
            radius=radius,
            fill="black",
        )
        holder.paste(self.image, (0, 0))
        self.image = Image.composite(holder, background, mask)

        return self


    async def circle_image(self) -> Editor:
        """Make image circle"""
        return await run_in_executor(self.__circle_image)

    def __circle_image(self) -> Editor:
        background = Image.new("RGBA", size=self.image.size, color=(255, 255, 255, 0))
        holder = Image.new("RGBA", size=self.image.size, color=(255, 255, 255, 0))
        mask = Image.new("RGBA", size=self.image.size, color=(255, 255, 255, 0))
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0) + self.image.size, fill="black")
        holder.paste(self.image, (0, 0))
        self.image = Image.composite(holder, background, mask)

        return self


    async def rotate(self, deg: float = 0, expand: bool = False) -> Editor:
        """Rotate image

        Parameters
        ----------
        deg: :class:`float`, optional
            Degrees to rotate, by default ``0``
        expand: :class:`bool`, optional
            Expand while rotating, by default ``False``
        """
        return await run_in_executor(self.__rotate, deg, expand)

    def __rotate(self, deg: float = 0, expand: bool = False) -> Editor:
        self.image = self.image.rotate(angle=deg, expand=expand)
        return self


    async def blur(self, mode: Literal['box', 'gaussian'] = 'gaussian', amount: float = 1) -> Editor:
        """Blur image

        Parameters
        ----------
        mode: Literal['box', 'gaussian'], optional
            Blur mode, by default ``gaussian``
        amount: :class:`float`, optional
            Amount of blur, by default ``1``
        """
        return await run_in_executor(self.__blur, mode, amount)

    def __blur(self, mode: Literal['box', 'gaussian'] = 'gaussian', amount: float = 1) -> Editor:
        if mode == 'box':
            self.image = self.image.filter(ImageFilter.BoxBlur(radius=amount))
        if mode == 'gaussian':
            self.image = self.image.filter(ImageFilter.GaussianBlur(radius=amount))

        return self


    async def blend(
            self, image: Union[Image.Image, Editor, Canvas], alpha: float = 0.0, on_top: bool = False
    ) -> Editor:
        """Blend image into editor image

        Parameters
        ----------
        image: Union[:class:`Image.Image`, :class:`Editor`, :class:`Canvas`]
            Image to blend
        alpha: :class:`float`, optional
            Alpha amount, by default ``0.0``
        on_top: :class:`bool`, optional
            Places image on top, by default ``False``
        """
        return await run_in_executor(self.__blend, image, alpha, on_top)

    def __blend(
            self, image: Union[Image.Image, Editor, Canvas], alpha: float = 0.0, on_top: bool = False
    ) -> Editor:
        if isinstance(image, Editor) or isinstance(image, Canvas):
            image = image.image

        if image.size != self.image.size:
            image = Editor(image).resize(self.image.size, crop=True).image

        if on_top:
            self.image = Image.blend(self.image, image, alpha=alpha)
        else:
            self.image = Image.blend(image, self.image, alpha=alpha)

        return self


    async def paste(
            self,
            image: Union[Image.Image, Editor, Canvas],
            position: Tuple[float, float] = (0,0),
            mask: Union[Image.Image, Editor] = None
    ) -> Editor:
        """Paste image into editor

        Parameters
        ----------
        image: Union[:class:`Image.Image`, :class:`Editor`, :class:`Canvas`]
            Image to paste
        position: Tuple[:class:`float`, :class:`float`]
            Position to paste, default is ``(0,0)``
        mask: Union[:class:`Image.Image`, :class:`Editor`]
            An optional mask image, by default ``None``
        """
        return await run_in_executor(self.__paste, image, position, mask)

    def __paste(
            self,
            image: Union[Image.Image, Editor, Canvas],
            position: Tuple[float, float] = (0,0),
            mask: Union[Image.Image, Editor] = None
    ) -> Editor:
        blank = Image.new('RGBA', size=self.image.size, color=(255, 255, 255, 0))

        if isinstance(image, Editor) or isinstance(image, Canvas):
            image = image.image

        if mask and isinstance(mask, Editor):
            mask = mask.image

        blank.paste(image, position, mask)
        self.image = Image.alpha_composite(self.image, blank)

        return self


    async def text(
        self,
        position: Tuple[float, float],
        text: str,
        font: Union[ImageFont.FreeTypeFont, Font] = None,
        color: Union[Tuple[int, int, int], str, int] = 'black',
        align: Literal["left", "center", "right"] = 'left',
        stroke_width: int = 0,
        stroke_color: Union[Tuple[int, int, int], str, int] = None,
    ) -> Editor:
        """Draw text into image

        Parameters
        ----------
        position: Tuple[:class:`float`, :class:`float`]
            Position to draw text
        text: str
            Text to draw
        font: Union[:class:`ImageFont.FreeTypeFont`, :class:`Font`], optional
            Font used for text, by default ``None``
        color: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
            Color of the font, by default ``'black'``
        align: Literal['left', 'center', 'right'], optional
            Align text, by default ``'left'``
        stroke_width: :class:`int`, optional
            The optional width of the text stroke, by default ``0``
        stroke_color: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
            Color to use for the text stroke. Default to the `color` parameter.
        """
        return await run_in_executor(self.__text, position, text, font, color, align, stroke_width, stroke_color)

    def __text(
        self,
        position: Tuple[float, float],
        text: str,
        font: Union[ImageFont.FreeTypeFont, Font] = None,
        color: Union[Tuple[int, int, int], str, int] = 'black',
        align: Literal["left", "center", "right"] = 'left',
        stroke_width: int = 0,
        stroke_color: Union[Tuple[int, int, int], str, int] = None,
    ) -> Editor:
        if isinstance(font, Font):
            font = font.font

        anchors = {'left': 'lt', 'center': 'mt', 'right': 'rt'}

        draw = ImageDraw.Draw(self.image)
        draw.text(
            position, text, color,
            font=font, anchor=anchors[align],
            stroke_width=stroke_width, stroke_fill=stroke_color
        )
        return self


    async def multicolor_text(
        self,
        position: Tuple[float, float],
        texts: List[Text],
        space_separated: bool = True,
        align: Literal["left", "center", "right"] = "left",
        stroke_width: int = 0,
        stroke_color: Union[Tuple[int, int, int], str, int] = None,
    ) -> Editor:
        """Draw multicolor text

        Parameters
        ----------
        position: Tuple[:class:`float`, :class:`float`]
            Position to draw text
        texts: List[:class:`Text`]
            List of texts
        space_separated: :class:`bool`, optional
            Separate texts with space, by default ``True``
        align: Literal['left', 'center', 'right'], optional
            Align texts, by default ``'left'``
        stroke_width: :class:`int`, optional
            The optional width of the text stroke, by default ``0``.
            Use this as a default if not all of your :class:`Text` classes have a `stroke_width` defined.
        stroke_color: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
            Color to use for the text stroke.
            Use this as a default if not all of your :class:`Text` classes have a `stroke_color` defined.
            If there is no `stroke_with` set in this function nor in the :class:`Text` class its default is the `color` from the :class:`Text`
        """
        return await run_in_executor(self.__multicolor_text, position, texts, space_separated, align, stroke_width, stroke_color)

    def __multicolor_text(
        self,
        position: Tuple[float, float],
        texts: List[Text],
        space_separated: bool = True,
        align: Literal["left", "center", "right"] = 'left',
        stroke_width: int = 0,
        stroke_color: Union[Tuple[int, int, int], str, int] = None,
    ) -> Editor:
        draw = ImageDraw.Draw(self.image)

        if align == 'left':
            position = position

        if align == 'right':
            total_width = 0

            for text in texts:
                total_width += text.font.getsize(text.text)[0]

            position = (position[0] - total_width, position[1])

        if align == 'center':
            total_width = 0

            for text in texts:
                total_width += text.font.getsize(text.text)[0]

            position = (position[0] - (total_width / 2), position[1])

        for text in texts:
            _sentence = text.text
            _font = text.font
            _color = text.color
            _stroke_width = text.stroke_width if text.stroke_width is not None else stroke_width
            _stroke_color = text.stroke_color or stroke_color or text.color

            if space_separated:
                width, _ = (
                    _font.getsize(_sentence)[0] + _font.getsize(' ')[0],
                    _font.getsize(_sentence)[1],
                )
            else:
                width, _ = _font.getsize(_sentence)

            draw.text(
                position, _sentence, _color, _font,
                stroke_width=_stroke_width, stroke_fill=_stroke_color
            )
            position = (position[0] + width, position[1])

        return self


    async def rectangle(
        self,
        position: Tuple[float, float],
        width: float,
        height: float,
        fill: Union[str, int, Tuple[int, int, int]] = None,
        color: Union[str, int, Tuple[int, int, int]] = None,
        outline: Union[str, int, Tuple[int, int, int]] = None,
        stroke_width: float = 1,
        radius: int = 0,
    ) -> Editor:
        """Draw rectangle into image

        Parameters
        ----------
        position: Tuple[:class:`float`, :class:`float`]
            Position to draw rectangle
        width: :class:`float`
            Width of rectangle
        height: :class:`float`
            Height of rectangle
        fill: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`,], optional
            Fill color, by default None
        color: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
            Alias of fill, by default ``None``
        outline: :class:`Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
            Outline color, by default ``None``
        stroke_width: :class:`float`, optional
            Stroke width, by default ``1``
        radius: :class:`int`, optional
            Radius of rectangle, by default ``0``
        """
        return await run_in_executor(self.__rectangle, position, width, height, fill, color, outline, stroke_width, radius)

    def __rectangle(
        self,
        position: Tuple[float, float],
        width: float,
        height: float,
        fill: Union[str, int, Tuple[int, int, int]] = None,
        color: Union[str, int, Tuple[int, int, int]] = None,
        outline: Union[str, int, Tuple[int, int, int]] = None,
        stroke_width: float = 1,
        radius: int = 0,
    ) -> Editor:
        draw = ImageDraw.Draw(self.image)

        to_width = width + position[0]
        to_height = height + position[1]

        if color:
            fill = color

        if radius <= 0:
            draw.rectangle(
                position + (to_width, to_height),
                fill=fill,
                outline=outline,
                width=stroke_width,
            )
        else:
            draw.rounded_rectangle(
                position + (to_width, to_height),
                radius=radius,
                fill=fill,
                outline=outline,
                width=stroke_width,
            )

        return self


    async def bar(
        self,
        position: Tuple[float, float],
        max_width: Union[int, float],
        height: Union[int, float],
        percentage: int = 1,
        fill: Union[str, int, Tuple[int, int, int]] = None,
        color: Union[str, int, Tuple[int, int, int]] = None,
        outline: Union[str, int, Tuple[int, int, int]] = None,
        stroke_width: float = 1,
        radius: int = 0,
    ) -> Editor:
        """Draw a progress bar

        Parameters
        ----------
        position: Tuple[:class:`float`, :class:`float`]
            Position to draw bar
        max_width: Union[:class:`int`, :class:`float`]
            Max width of the bar
        height: Union[:class:`int`, :class:`float`]
            Height of the bar
        percentage: :class:`int`, optional
            Percentage to fill of the bar, by default 1
        fill: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
            Fill color, by default ``None``
        color: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
            Alias of fill, by default ``None``
        outline: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
            Outline color, by default ``None``
        stroke_width: :class:`float`, optional
            Stroke width, by default ``1``
        radius: :class:`int`, optional
            Radius of the bar, by default ``0``
        """
        return await run_in_executor(self.__bar, position, max_width, height, percentage, fill, color, outline, stroke_width, radius)

    def __bar(
        self,
        position: Tuple[float, float],
        max_width: Union[int, float],
        height: Union[int, float],
        percentage: int = 1,
        fill: Union[str, int, Tuple[int, int, int]] = None,
        color: Union[str, int, Tuple[int, int, int]] = None,
        outline: Union[str, int, Tuple[int, int, int]] = None,
        stroke_width: float = 1,
        radius: int = 0,
    ) -> Editor:
        draw = ImageDraw.Draw(self.image)

        if color:
            fill = color

        ratio = max_width / 100
        to_width = ratio * percentage + position[0]

        height = height + position[1]

        if radius <= 0:
            draw.rectangle(
                position + (to_width, height),
                fill=fill,
                outline=outline,
                width=stroke_width,
            )
        else:
            draw.rounded_rectangle(
                position + (to_width, height),
                radius=radius,
                fill=fill,
                outline=outline,
                width=stroke_width,
            )

        return self


    async def rounded_bar(
        self,
        position: Tuple[float, float],
        width: Union[int, float],
        height: Union[int, float],
        percentage: float,
        fill: Union[str, int, Tuple[int, int, int]] = None,
        color: Union[str, int, Tuple[int, int, int]] = None,
        stroke_width: float = 1,
    ) -> Editor:
        """Draw a rounded bar

        Parameters
        ----------
        position: Tuple[:class:`float`, :class:`float`]
            Position to draw rounded bar
        width: Union[:class:`int`, :class:`float`]
            Width of the bar
        height: Union[:class:`int`, :class:`float`]
            Height of the bar
        percentage: :class:`float`
            Percentage to fill
        fill: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
            Fill color, by default ``None``
        color: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
            Alias of color, by default ``None``
        stroke_width: :class:`float`, optional
            Stroke width, by default ``1``
        """
        return await run_in_executor(self.__rounded_bar, position, width, height, percentage, fill, color, stroke_width)

    def __rounded_bar(
        self,
        position: Tuple[float, float],
        width: Union[int, float],
        height: Union[int, float],
        percentage: float,
        fill: Union[str, int, Tuple[int, int, int]] = None,
        color: Union[str, int, Tuple[int, int, int]] = None,
        stroke_width: float = 1,
    ) -> Editor:
        draw = ImageDraw.Draw(self.image)

        if color:
            fill = color

        start = -90
        end = (percentage * 3.6) - 90

        draw.arc(
            position + (position[0] + width, position[1] + height),
            start,
            end,
            fill,
            width=stroke_width,
        )

        return self


    async def ellipse(
        self,
        position: Tuple[float, float],
        width: float,
        height: float,
        fill: Union[str, int, Tuple[int, int, int]] = None,
        color: Union[str, int, Tuple[int, int, int]] = None,
        outline: Union[str, int, Tuple[int, int, int]] = None,
        stroke_width: float = 1,
    ) -> Editor:
        """Draw an ellipse

        Parameters
        ----------
        position: Tuple[:class:`float`, :class:`float`]
            Position to draw ellipse
        width: :class:`float`
            Width of ellipse
        height: :class:`float`
            Height of ellipse
        fill: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
            Fill color, by default ``None``
        color: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
            Alias of fill, by default ``None``
        outline: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
            Outline color, by default ``None``
        stroke_width: :class:`float`, optional
            Stroke width, by default ``1``
        """
        return await run_in_executor(self.__ellipse, position, width, height, fill, color, outline, stroke_width)

    def __ellipse(
        self,
        position: Tuple[float, float],
        width: float,
        height: float,
        fill: Union[str, int, Tuple[int, int, int]] = None,
        color: Union[str, int, Tuple[int, int, int]] = None,
        outline: Union[str, int, Tuple[int, int, int]] = None,
        stroke_width: float = 1,
    ) -> Editor:
        draw = ImageDraw.Draw(self.image)
        to_width = width + position[0]
        to_height = height + position[1]

        if color:
            fill = color

        draw.ellipse(
            position + (to_width, to_height),
            outline=outline,
            fill=fill,
            width=stroke_width,
        )

        return self


    async def polygon(
        self,
        coordinates: list,
        fill: Union[str, int, Tuple[int, int, int]] = None,
        color: Union[str, int, Tuple[int, int, int]] = None,
        outline: Union[str, int, Tuple[int, int, int]] = None,
    ) -> Editor:
        """Draw a polygon

        Parameters
        ----------
        coordinates: :class:`list`
            Coordinates to draw
        fill: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
            Fill color, by default ``None``
        color: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
            Alias of fill, by default ``None``
        outline: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
            Outline color, by default ``None``
        """
        return await run_in_executor(self.__polygon, coordinates, fill, color, outline)

    def __polygon(
        self,
        coordinates: list,
        fill: Union[str, int, Tuple[int, int, int]] = None,
        color: Union[str, int, Tuple[int, int, int]] = None,
        outline: Union[str, int, Tuple[int, int, int]] = None,
    ) -> Editor:
        if color:
            fill = color

        draw = ImageDraw.Draw(self.image)
        draw.polygon(coordinates, fill=fill, outline=outline)

        return self


    async def arc(
        self,
        position: Tuple[float, float],
        width: float,
        height: float,
        start: float,
        rotation: float,
        fill: Union[str, int, Tuple[int, int, int]] = None,
        color: Union[str, int, Tuple[int, int, int]] = None,
        stroke_width: float = 1,
    ) -> Editor:
        """Draw arc

        Parameters
        ----------
        position: Tuple[:class:`float`, :class:`float`]
            Position to draw arc
        width: :class:`float`
            Width or arc
        height: :class:`float`
            Height of arch
        start: :class:`float`
            Start position of arch
        rotation: :class:`float`
            Rotation in degree
        fill: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
            Fill color, by default ``None``
        color: Union[Tuple[:class:`int`, :class:`int`, :class:`int`], :class:`str`, :class:`int`], optional
            Alias of fill, by default ``None``
        stroke_width: :class:`float`, optional
            Stroke width, by default ``1``
        """
        return await run_in_executor(self.__arc, position, width, height, start, rotation, fill, color, stroke_width)

    def __arc(
        self,
        position: Tuple[float, float],
        width: float,
        height: float,
        start: float,
        rotation: float,
        fill: Union[str, int, Tuple[int, int, int]] = None,
        color: Union[str, int, Tuple[int, int, int]] = None,
        stroke_width: float = 1,
    ) -> Editor:
        draw = ImageDraw.Draw(self.image)

        start = start - 90
        end = rotation - 90

        if color:
            fill = color

        draw.arc(
            position + (position[0] + width, position[1] + height),
            start,
            end,
            fill,
            width=stroke_width,
        )

        return self


    async def show(self):
        """Show the image."""
        return await run_in_executor(self.__show)

    def __show(self):
        self.image.show()


    async def save(self, fp, format: str = None, **params):
        """Save the image

        Parameters
        ----------
        fp: :class:`str`
            File path
        format: :class:`str`, optional
            File format, by default ``None``
        """
        return await run_in_executor(self.__save, fp, format, **params)

    def __save(self, fp, format: str = None, **params):
        self.image.save(fp, format, **params)
