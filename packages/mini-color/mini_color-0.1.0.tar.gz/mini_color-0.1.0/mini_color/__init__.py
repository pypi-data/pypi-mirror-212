import random


class Style(object):
    """
    The class of styles and effects for printing text

    样式和效果类类
    """
    """终端默认"""
    Default: None = 0

    """高亮显示"""
    HighLight: None = 1

    """下划线"""
    UnderLine: None = 4

    """闪烁"""
    Flash: None = 5

    """反白显示"""
    AntiWhite: None = 7

    """不可见"""
    Invisible: None = 8


class Color(object):
    """
    The class of colors for printing text

    颜色类
    """
    """黑色"""
    BLACK: None = 30

    """红色"""
    RED: None = 31

    """绿色"""
    GREEN: None = 32

    """黄色"""
    YELLOW: None = 33

    """蓝色"""
    BLUE: None = 34

    """紫色"""
    PURPLE: None = 35

    """青色"""
    CYAN: None = 36

    """白色"""
    WHITE: None = 37

    @classmethod
    def random(cls):
        """
        Return a random color

        随机色
        """
        color = [
            Color.BLACK,
            Color.RED,
            Color.GREEN,
            Color.YELLOW,
            Color.BLACK,
            Color.PURPLE,
            Color.CYAN,
            Color.WHITE
        ]
        return random.choice(color)


def _get_color_value(color: Color):
    """
    The get-method of color value which is in color class

    颜色值的get方法
    """
    return int(color.__str__())
