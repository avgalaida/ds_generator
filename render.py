from typing import Literal
from PIL import ImageFont, ImageDraw, Image


class Font:
    align: Literal['center', 'left', 'right']
    anchor: str
    color: tuple[int, int, int, int]
    file: str
    size: int
    spacing: float

    @property
    def pil_font(self) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(self.file, self.size)

    def __init__(
            self,
            color: tuple[int, int, int, int],
            file: str,
            size: int,
            anchor: str = 'lt',
            spacing: float = 4.0,
            align: Literal['center', 'left', 'right'] = 'left',
    ) -> None:
        self.anchor = anchor
        self.color = color
        self.file = file
        self.size = size
        self.align = align
        self.spacing = spacing

    def __repr__(self) -> str:
        font_name = self.pil_font.getname()
        return f'{font_name} {self.size}. {self.color}'

    def draw(
            self,
            overlay: ImageDraw.ImageDraw,
            position: tuple[float, float],
            text: str,
    ) -> None:
        """Draw the text on the image overlay"""
        overlay.text(
            position,
            text,
            self.color,
            self.pil_font,
            self.anchor,
            self.spacing,
            self.align,
        )


class Renderer:
    font: Font

    def __init__(self, font: Font) -> None:
        self.font = font

    def render(self, image: Image.Image, fields: list['Field']) -> Image.Image:
        copy = image.copy()
        overlay = ImageDraw.Draw(copy)
        self._draw_fields(overlay, fields)
        return copy

    def _draw_fields(self, overlay: ImageDraw.ImageDraw, fields: list['Field']) -> None:
        for field in fields:
            position = field.point.x, field.point.y
            self.font.draw(overlay, position, field.value)


class OpacityRenderer(Renderer):
    def render(self, image: Image.Image, fields: list['Field']) -> Image.Image:
        copy = image.convert('RGBA')
        text = Image.new('RGBA', image.size, (0, 0, 0, 0))
        overlay = ImageDraw.Draw(text)
        self._draw_fields(overlay, fields)
        return Image.alpha_composite(copy, text)


class RotationRenderer(Renderer):
    angle: float
    resampling: int

    def __init__(self, font: Font, angle: float, resampling: int) -> None:
        super().__init__(font)
        self.angle = angle
        self.resampling = resampling

    def render(self, image: Image.Image, fields: list['Field']) -> Image.Image:
        copy = image.rotate(self.angle, self.resampling, True)
        overlay = ImageDraw.Draw(copy)
        self._draw_fields(overlay, fields)
        return copy.rotate(-self.angle, self.resampling, True)
