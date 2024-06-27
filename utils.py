from math import radians, cos, sin
from ds_generator.render import Font
from ds_generator.field import Field


def get_field_text_position(font: Font, field: Field) -> tuple[int, ...]:
    center = (field.point.x, field.point.y)
    bbox = font.pil_font.getbbox(field.value, anchor=font.anchor)
    return tuple(a + b for a, b in zip(center * 2, bbox))


def get_field_multiline_text_position(font: Font, field: Field) -> tuple[int, ...]:
    x_min, y_min, x_max, y_max = float('inf'), float('inf'), float('-inf'), float('-inf')

    for index, line in enumerate(field.value.splitlines()):
        bbox = font.pil_font.getbbox(line, anchor=font.anchor)
        offset_y = index * (font.size + font.spacing)

        line_x_min = field.point.x + bbox[0]
        line_y_min = field.point.y + offset_y + bbox[1]
        line_x_max = field.point.x + bbox[2]
        line_y_max = field.point.y + offset_y + bbox[3]

        x_min = min(x_min, line_x_min)
        y_min = min(y_min, line_y_min)
        x_max = max(x_max, line_x_max)
        y_max = max(y_max, line_y_max)

    return x_min, y_min, x_max, y_max


def calculate_bbox(position: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    x_min, y_min, x_max, y_max = position
    x_center = (x_min + x_max) // 2
    y_center = (y_min + y_max) // 2
    w = x_max - x_min
    h = y_max - y_min
    return x_center, y_center, w, h


def rotate_point(x, y, angle, cx, cy):
    angle = radians(angle)
    cos_a = cos(angle)
    sin_a = sin(angle)
    x -= cx
    y -= cy
    x_new = x * cos_a - y * sin_a
    y_new = x * sin_a + y * cos_a
    return x_new + cx, y_new + cy


def calculate_rotated_bbox(position: tuple[int, int, int, int], angle: float) -> tuple[int, int, int, int]:
    x_min, y_min, x_max, y_max = position

    width = x_max - x_min
    height = y_max - y_min

    if angle == 90 or angle == -270:
        new_x_min = y_min
        new_y_min = x_min
        new_x_max = y_min + height
        new_y_max = x_min + width
    elif angle == -90 or angle == 270:
        new_x_min = y_max - height
        new_y_min = x_max - width
        new_x_max = y_max
        new_y_max = x_max
    else:
        cx = (x_min + x_max) / 2
        cy = (y_min + y_max) / 2

        corners = [
            (x_min, y_min),
            (x_max, y_min),
            (x_max, y_max),
            (x_min, y_max),
        ]

        rotated_corners = [rotate_point(x, y, angle, cx, cy) for x, y in corners]

        x_coords, y_coords = zip(*rotated_corners)
        new_x_min = min(x_coords)
        new_y_min = min(y_coords)
        new_x_max = max(x_coords)
        new_y_max = max(y_coords)

    return calculate_bbox((new_x_min, new_y_min, new_x_max, new_y_max))