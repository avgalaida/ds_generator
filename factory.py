from typing import Callable
from ds_generator.field import Field
from ds_generator.positioning import Point, Offset
from ds_generator.render import Font

class FieldFactory:
    name: str
    offset_limit: tuple[int, int]
    point: Point
    value_function: Callable[[], str]
    font: Font
    class_id: int

    def __init__(
        self,
        name: str,
        point: Point,
        value_function: Callable[[], str],
        font: Font,
        class_id: int,
        offset_limit: tuple[int, int] = (0, 0)
    ) -> None:
        self.name = name
        self.offset_limit = offset_limit
        self.point = point
        self.value_function = value_function
        self.font = font
        self.class_id = class_id

    def create(self) -> Field:
        position = self._shift_position()
        value = self.value_function()
        return Field(self.name, position, value, self.font, self.class_id)

    def _shift_position(self) -> Point:
        x, y = self.offset_limit
        if not x or not y:
            return self.point

        offset = Offset.random(x, y)
        vertical, horizontal = map(int, offset)

        return self.point.shift(vertical, horizontal)