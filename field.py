from ds_generator.positioning import Point
from ds_generator.render import Font

class Field:
    name: str
    point: Point
    value: str
    font: Font
    class_id: int

    def __init__(self, name: str, point: Point, value: str, font: Font, class_id: int) -> None:
        self.name = name
        self.point = point
        self.value = value
        self.font = font
        self.class_id = class_id

    def __repr__(self) -> str:
        return f'{self.name}: \'{self.value}\' at {self.point}'