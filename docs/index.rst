.. aioEasyPillow documentation master file, created by
   sphinx-quickstart on Fri Jul  1 16:29:30 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to aioEasyPillow's documentation!
=========================================

.. toctree::
   :maxdepth: 2
   :caption: Table of Contents
   :hidden:

   intro.rst
   discord.rst
   api.rst

..
   Indices and tables
   ==================
..
   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`


Quickstart
==========

.. code-block:: python
   :caption: A quick example how to create a image an add some text

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


Scheint ja doch zu gehen