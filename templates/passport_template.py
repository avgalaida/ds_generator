import random
from faker import Faker
from pathlib import Path
from PIL import Image
from PIL.Image import BICUBIC
from ds_generator.document_generator import FieldGroup
from ds_generator.factory import FieldFactory
from ds_generator.positioning import Point
from ds_generator.render import Font, OpacityRenderer, RotationRenderer

faker = Faker('ru_RU')

def generate_birth_place():
    city = faker.city().upper()
    region = faker.region().upper()
    country = faker.country().upper()

    # Рандомный выбор добавления страны
    if random.choice([True, False]):
        return f"{city}\n{region}\n{country}"
    else:
        return f"{city}\n{region}"

field_names = {
    0: 'last_name',
    1: 'first_name',
    2: 'middle_name',
    3: 'gender',
    4: 'birth_date',
    5: 'birth_place',
    6: 'series',
    7: 'number'
}

def get_passport_template(fonts_dir: Path, images_dir: Path):
    field_font = Font((0, 0, 0, 165),fonts_dir / 'cambriab.ttf',48,'ms',32,'center',)
    series_font = Font('#660c0c', fonts_dir / 'upcel.ttf', 84, 'ms')
    field_renderer = OpacityRenderer(field_font)
    series_renderer = RotationRenderer(series_font, 90, BICUBIC)

    fonts = {
        f"{field_font.pil_font.getname()} {field_font.size} {field_font.color}": field_font,
        f"{series_font.pil_font.getname()} {series_font.size} {series_font.color}": series_font
    }

    fields = FieldGroup(field_renderer, (
        FieldFactory(
            'last_name',
            Point(937, 218),
            lambda: faker.last_name().upper(),
            field_font,
            class_id=0,
            offset_limit=(20, 10),
        ),
        FieldFactory(
            'first_name',
            Point(937, 370),
            lambda: faker.first_name().upper(),
            field_font,
            class_id=1,
            offset_limit=(20, 10),
        ),
        FieldFactory(
            'middle_name',
            Point(937, 440),
            lambda: faker.middle_name().upper(),
            field_font,
            class_id=2,
            offset_limit=(20, 10),
        ),
        FieldFactory(
            'gender',
            Point(630, 510),
            lambda: random.choice(['МУЖ.', 'ЖЕН.']),
            field_font,
            class_id=3,
            offset_limit=(20, 10),
        ),
        FieldFactory(
            'birth_date',
            Point(1055, 510),
            lambda: faker.date_of_birth(
                minimum_age=14,
                maximum_age=60,
            ).strftime(r'%d.%m.%Y'),
            field_font,
            class_id=4,
            offset_limit=(20, 10),
        ),
        FieldFactory(
            'birth_place',
            Point(937, 580),
            generate_birth_place,
            field_font,
            class_id=5,
            offset_limit=(20, 10),
        ),
    ), fonts)

    series = FieldGroup(series_renderer, (
        FieldFactory(
            'series',
            Point(336, 1488 - 1405),
            lambda: f"{random.randint(10, 99)}    {random.randint(10, 99)}",
            series_font,
            class_id=6,
        ),
        FieldFactory(
            'number',
            Point(650, 1488 - 1405),
            lambda: str(random.randint(100000, 999999)),
            series_font,
            class_id=7,
        ),
    ), fonts)

    image_source = images_dir / 'passport.png'
    return image_source, (fields, series)

def get_field_names():
    return field_names