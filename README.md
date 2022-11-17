# aioEasyPillow
**⚠ This is a Private branch with some not documented changes**

[![PyPI](https://img.shields.io/pypi/v/aioEasyPillow?style=flat-square)](https://pypi.org/project/aioEasyPillow/)
[![Documentation Status](https://readthedocs.org/projects/aioeasypillow/badge/?version=latest&style=flat-square)](https://aioeasypillow.readthedocs.io/en/latest/)

[Pillow]: https://github.com/python-pillow/Pillow
[easy-pil]: https://github.com/shahriyardx/easy-pil
[documentation]: https://aioeasypillow.readthedocs.io/en/latest/

A python library based on [easy-pil] and [Pillow] to easily edit/modify images.

Read more details about this libary in the official [documentation].


## Installation

**Python 3.8 or above is required**\
To install the library directly from PyPI you can just run the following command:
```shell
# Linux/macOS
python3 -m pip install -U aioEasyPillow

# Windows
py -3 -m pip install -U aioEasyPillow
```


## Quick Example

```python
import asyncio

from aioEasyPillow import Editor, Canvas, Font

async def main():
    blank = Canvas((200, 100), 'black')
    editor = Editor(blank)
    font = Font.poppins('bold', 200)

    await editor.text((20,20), 'Quick Example', font)
    await editor.save('example.png', 'PNG')
    await editor.show()

asyncio.run(main())
```

## Discord Bot Example

```python
import discord
from discord.ext import commands

from aioEasyPillow import Editor, Canvas, Font, load_image

intents = discord.Intents.default()
intents.members = True  # don't forget to activate this in the dev portal

# You can of course also use the discord.Bot() or commands.Bot() class
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def circle(ctx):
    # Load the image using `load_image`
    image = await load_image(ctx.author.display_avatar.url)

    # Initialize the editor and pass image as a parameter
    editor = Editor(image)
    
    # Simply circle the image 
    await editor.circle_image()

    # Creating a discord.File object from the editors image_bytes, the image must not be saved
    file = discord.File(fp=editor.image_bytes, filename='circle.png')
    await ctx.send('Your circled imagavatare', file=file)


bot.run("TOKEN")
```
