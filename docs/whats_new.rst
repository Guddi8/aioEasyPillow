.. currentmodule:: aioEasyPillow

Changelog
=========

This page keeps a detailed human friendly rendering of what’s new and changed in specific versions.

v0.0.3
------

New Features
~~~~~~~~~~~~

- Add support for masks in :class:`Editor.paste`
- Add support for strokes in :class:`Editor.text`
    - Added ``stroke_width`` keyword, by default ``0``
    - Added ``stroke_color`` keyword, default is same as the given ``color``
- Add support for strokes in :class:`Editor.multicolor_text`
    - Added ``stroke_width`` keyword, by default ``0``
    - Added ``stroke_color`` keyword, default to the given ``color`` of the :class:`Text`
    - Both are just a default if the stroke is not defined in :class:`Text`
- Added optional ``stroke_width`` and ``stroke_width`` keywords to :class:`Text`
    - If they are set in this class it will overwrite the stroke defined in :class:`Editor.multicolor_text`
- Added these (hopefully) beautiful docs!

Miscellaneous
~~~~~~~~~~~~~
- Parameter position on Editor.paste() is now optional, the default is (0, 0) (top left corner)
