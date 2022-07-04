Discord Bot
===========

A basic Discord Bot example using `discord.py <https://discordpy.readthedocs.io>`_ or `Py-cord <https://docs.pycord.dev/>`_ version 2.
This will make the command author's avatar circular and send it.

.. code-block:: python

    import discord
    from discord.ext import commands

    from aioEasyPillow import Editor, Canvas, Font, load_image

    intents = discord.Intents.default()
    intents.members = True  # don't forget to activate this in the dev portal
    # You can also use the discord.Bot() or discord.Client() class
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