from typing import Sequence
from PIL import Image
from ds_generator.factory import FieldFactory
from ds_generator.field import Field
from ds_generator.render import Renderer, RotationRenderer
from ds_generator.utils import get_field_text_position, get_field_multiline_text_position, calculate_bbox, \
    calculate_rotated_bbox


class FieldGroup:
    """Multiple fields designed to the same display way"""

    data: Sequence[Field]
    fields: Sequence[Field]
    renderer: Renderer
    fonts: dict[str, Renderer]

    def __init__(self, renderer: Renderer, data: Sequence[Field], fonts: dict[str, Renderer]) -> None:
        self.data = data
        self.renderer = renderer
        self.fields = []  # Initialize fields
        self.fonts = fonts  # Initialize fonts

    def __len__(self) -> int:
        return len(self.fields)

    def render(self, image: Image.Image) -> Image.Image:
        return self.renderer.render(image, self.fields)

    def seed(self) -> None:
        """Regenerate fields by factories if any"""
        self.fields = [
            item.create() if isinstance(item, FieldFactory) else item
            for item in self.data
        ]


class DocumentGenerator:
    """Create an image and render all fields on it"""

    groups: Sequence[FieldGroup]
    template: Image.Image

    @property
    def fields(self) -> list[Field]:
        return [field for group in self.groups for field in group.fields]

    def __init__(self, template: Image.Image, groups: Sequence[FieldGroup]) -> None:
        self.groups = groups
        self.template = template

    def generate(self, annotation_path: str) -> Image.Image:
        image = self.template
        annotations = []
        img_width, img_height = image.size

        for group in self.groups:
            group.seed()
            image = group.render(image)
            for field in group.fields:
                if field.name in ['series', 'number']:
                    if field.name == 'series':
                        x_center, y_center, w, h = 0.956526, 0.325223, 0.038960, 0.213232
                    elif field.name == 'number':
                        x_center, y_center, w, h = 0.957025, 0.620910, 0.037961, 0.197724
                else:
                    font_key = f"{field.font.pil_font.getname()} {field.font.size} {field.font.color}"
                    font = group.fonts[font_key]
                    if '\n' in field.value:
                        pos = get_field_multiline_text_position(font, field)
                    else:
                        pos = get_field_text_position(font, field)

                    if isinstance(group.renderer, RotationRenderer):
                        pos = calculate_rotated_bbox(pos, group.renderer.angle)

                    x_center, y_center, w, h = calculate_bbox(pos)
                    x_center /= img_width
                    y_center /= img_height
                    w /= img_width
                    h /= img_height

                annotations.append((field.class_id, x_center, y_center, w, h))

        # Запись аннотаций в файл
        with open(annotation_path, 'w') as file:
            for annotation in annotations:
                file.write(
                    f"{annotation[0]} {annotation[1]:.6f} {annotation[2]:.6f} {annotation[3]:.6f} {annotation[4]:.6f}\n")

        return image