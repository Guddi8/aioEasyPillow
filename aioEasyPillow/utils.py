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

import asyncio
import functools
from io import BytesIO

import aiohttp
import requests
from PIL import Image


async def run_in_executor(func, **kwargs):
    """Run function in executor

    Parameters
    ----------
    func : func
        Function to run
    """
    func = functools.partial(func, **kwargs)
    data = await asyncio.get_event_loop().run_in_executor(None, func)
    return data


def load_image(link: str) -> Image.Image:
    """Load image from link

    Parameters
    ----------
    link : str
        Image link

    Returns
    -------
    PIL.Image.Image
        Image from the provided link (if any)
    """
    _bytes = BytesIO(requests.get(link).content)
    image = Image.open(_bytes).convert("RGBA")

    return image


async def load_image_async(link: str) -> Image.Image:
    """Load image from link (async)

    Parameters
    ----------
    link : str
        Image from the provided link (if any)

    Returns
    -------
    PIL.Image.Image
        Image link
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            data = await response.read()

    _bytes = BytesIO(data)
    image = Image.open(_bytes).convert("RGBA")
    return image
