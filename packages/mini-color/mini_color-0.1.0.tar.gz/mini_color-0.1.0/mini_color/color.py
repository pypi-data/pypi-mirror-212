from . import Color, Style, _get_color_value
from .exception import StyleValueError, ColorValueError


def _color(
        content: str,
        color: Color = 0,
        back: Color = 0,
        style: Style = Style.Default
) -> str:
    """
    The formatter of the colors and styles

    颜色与样式格式化器

    - content: 输入的内容
    - color：字体颜色
    - back：背景色
    - style：显示的样式
    """
    color_value = _get_color_value(color)
    back_value = _get_color_value(back)
    if style not in [0, 1, 4, 5, 7, 8]:
        raise StyleValueError('the value of param "style" is out of range')
    if (color_value < 30 and color_value != 0) or color_value > 37:
        raise ColorValueError('the value of param "color" is out of range')
    if 30 <= back_value <= 37 or back == 0:
        _back = back_value + 10
    else:
        raise ColorValueError('the value of param "back" is out of range')
    return f'\033[{style};{color};{_back}m{content}\033[0m'


def black(
        content: str,
        back: Color = 0,
        style: Style = Style.Default
) -> str:
    """
    Returns a black string

    返回黑色字符串

    - content: 输入的内容
    - back: 背景色，默认无背景色
    - style: 显示的样式，默认无样式
    """
    formatter = _color(
        content=content,
        color=Color.BLACK,
        back=back,
        style=style
    )
    return formatter


def red(
        content: str,
        back: Color = 0,
        style: Style = Style.Default
) -> str:
    """
    Returns a red string

    返回红色字符串

    - content: 输入的内容
    - back: 背景色，默认无背景色
    - style: 显示的样式，默认无样式
    """
    formatter = _color(
        content=content,
        color=Color.RED,
        back=back,
        style=style
    )
    return formatter


def green(
        content: str,
        back: Color = 0,
        style: Style = Style.Default
) -> str:
    """
    Returns a green string

    返回绿色字符串

    - content: 输入的内容
    - back: 背景色，默认无背景色
    - style: 显示的样式，默认无样式
    """
    formatter = _color(
        content=content,
        color=Color.GREEN,
        back=back,
        style=style
    )
    return formatter


def yellow(
        content: str,
        back: Color = 0,
        style: Style = Style.Default
) -> str:
    """
    Returns a yellow string

    返回黄色字符串

    - content: 输入的内容
    - back: 背景色，默认无背景色
    - style: 显示的样式，默认无样式
    """
    formatter = _color(
        content=content,
        color=Color.YELLOW,
        back=back,
        style=style
    )
    return formatter


def blue(
        content: str,
        back: Color = 0,
        style: Style = Style.Default
) -> str:
    """
    Returns a blue string

    返回蓝色字符串

    - content: 输入的内容
    - back: 背景色，默认无背景色
    - style: 显示的样式，默认无样式
    """
    formatter = _color(
        content=content,
        color=Color.BLUE,
        back=back,
        style=style
    )
    return formatter


def purple(
        content: str,
        back: Color = 0,
        style: Style = Style.Default
) -> str:
    """
    Returns a purple string

    返回紫色字符串

    - content: 输入的内容
    - back: 背景色，默认无背景色
    - style: 显示的样式，默认无样式
    """
    formatter = _color(
        content=content,
        color=Color.PURPLE,
        back=back,
        style=style
    )
    return formatter


def cyan(
        content: str,
        back: Color = 0,
        style: Style = Style.Default
) -> str:
    """
    Returns a cyan string

    返回青色字符串

    - content: 输入的内容
    - back: 背景色，默认无背景色
    - style: 显示的样式，默认无样式
    """
    formatter = _color(
        content=content,
        color=Color.CYAN,
        back=back,
        style=style
    )
    return formatter


def white(
        content: str,
        back: Color = 0,
        style: Style = Style.Default
) -> str:
    """
    Returns a white string

    返回白色字符串

    - content: 输入的内容
    - back: 背景色，默认无背景色
    - style: 显示的样式，默认无样式
    """
    formatter = _color(
        content=content,
        color=Color.WHITE,
        back=back,
        style=style
    )
    return formatter


def random_color(
        content: str,
        back: Color = 0,
        style: Style = Style.Default
) -> str:
    """
    Returns a random color string

    返回随机颜色的字符串

    - content: 输入的内容
    - back: 背景色，默认无背景色
    - style: 显示的样式，默认无样式
    """
    formatter = _color(
        content=content,
        color=Color.random(),
        back=back,
        style=style
    )
    return formatter


__all__ = (
    'black',
    'red',
    'green',
    'white',
    'yellow',
    'cyan',
    'purple',
    'blue',
    'random_color'
)
