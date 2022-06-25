from typing import Tuple, Union

from PIL import Image


class Canvas:
    """Canvas class

    Parameters
    ----------
    size : Tuple[float, float], optional
        Size of image, by default None
    width : float, optional
        Width of image, by default None
    height : float, optional
        Height of image, by default None
    color : Union[Tuple[int, int, int], str, int], optional
        Color of image, by default None

    Raises
    ------
    ValueError
        When either ``size`` or ``width and height`` is not a provided
    """

    def __init__(
        self,
        size: Tuple[float, float] = None,
        width: float = None,
        height: float = None,
        color: Union[Tuple[int, int, int], str, int] = None,
    ) -> None:
        if not size and not width and not height:
            raise ValueError("size, width, and height cannot all be None")

        if width and height:
            size = (width, height)

        self.size = size
        self.color = color

        self.image = Image.new("RGBA", size, color=color)
