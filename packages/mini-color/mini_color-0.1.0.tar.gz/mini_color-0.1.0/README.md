# 一个易于使用的终端输出彩色文本库

## 环境及安装

对于python版本没有太多的要求，只要不低于python 3.6应该都可以正常使用

使用pip安装：`pip install mini-color`

## 快速上手

在终端打印一串某个颜色的文本，你只需要像这样：

```python
from mini_color.color import red

print(red('我只是一个输出'))
```
color中包含了所有可以使用print函数输出彩色字符的颜色方法

这将在终端输出红色的字符串

color中的内容：

    black(),white(),red(),yellow(),blue(),green(),cyan(),purple(),

    random_color()

其中random_color()是一个能够将输入的字符串转为随机颜色的方法

## 进阶：使用背景色

你只需要导入一个Color类，并在颜色方法中将Color中的属性传入back参数：

```python

from mini_color.color import Color,green

text = green(
    '我只是一个输出',
    back=Color.BLUE
)
print(text)
```
这将在终端输出绿色字体、蓝色背景的字符串

Color的属性内容同上面的color类似，因为在所有的颜色方法中都调用了Color中的颜色属性

Color类：

    BLACK,WHITE,RED,YELLOW,BLUE,GREEN,CYAN,PURPLE,

    random()

random()是一个方法，他能返回随机一个Color的颜色属性，这在color方法中也是可以作为参数传入的
    

## 进阶：使用样式

你只需要导入一个Style类，并在颜色方法中将Style中的属性传入style参数

```python

from mini_color.color import Color,Style,red

text = red(
    '我只是一个输出',
    back=Color.BLUE,
    style=Style.HighLight
)
print(text)
```
这将在终端输出红色字体、蓝色背景、带有高亮效果的字符串

Style中包含的样式：

    Default：默认样式，没有任何显示效果
    
    HighLight：高亮显示

    UnderLine：下划线效果

    Flash：闪烁效果

    AntiWhite：反白的显示效果

    Invisible：不可见

## 联系我

QQ:1435608435

