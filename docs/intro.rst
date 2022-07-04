Introduction
============
This is the documentation for aioEasyPillow.

Prerequisites
-------------

aioEasyPillow requires python 3.8 or higher. Support for previous version is not guaranteed.

Installing
-----------

You can get the library directly from PyPI: ::

    python3 -m pip install -U easy-pil

If you are using Windows, then the following should be used instead: ::

    py -3 -m pip install -U easy-pil

Basic Concepts
--------------

.. code-block:: python

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

