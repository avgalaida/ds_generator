import random
from faker import Faker
from pathlib import Path

from ds_generator.document_generator import FieldGroup
from ds_generator.factory import FieldFactory
from ds_generator.positioning import Point
from ds_generator.render import Font, OpacityRenderer

faker = Faker('ru_RU')

# Словарь для преобразования номера месяца в строку
months = {
    1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
    5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
    9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
}

def format_date(date):
    return f"{date.day} {months[date.month]} {date.year} года"

field_names = {
    0: 'last_name',
    1: 'first_name',
    2: 'middle_name',
    3: 'birth_date',
    4: 'birth_place',
    5: 'gender',
    6: 'reg_date',
    7: 'snils_number'
}

def get_snils_template(fonts_dir: Path, images_dir: Path):
    number_font = Font((0, 0, 0, 255), fonts_dir / 'cambriab.ttf', 42, 'ms')
    field_font = Font((0, 0, 0, 230), fonts_dir / 'calibri.ttf', 42, 'ms', 12, 'left')

    field_renderer = OpacityRenderer(field_font)
    number_renderer = OpacityRenderer(number_font)

    fonts = {
        f"{number_font.pil_font.getname()} {number_font.size} {number_font.color}": number_font,
        f"{field_font.pil_font.getname()} {field_font.size} {field_font.color}": field_font
    }

    fields = FieldGroup(field_renderer, (
        FieldFactory(
            'last_name',
            Point(420, 320),
            lambda: faker.last_name().upper(),
            field_font,
            class_id=0,
            offset_limit=(6, 2),
        ),
        FieldFactory(
            'first_name',
            Point(420, 360),
            lambda: faker.first_name().upper(),
            field_font,
            class_id=1,
            offset_limit=(6, 2),
        ),
        FieldFactory(
            'middle_name',
            Point(420, 400),
            lambda: faker.middle_name().upper(),
            field_font,
            class_id=2,
            offset_limit=(6, 2),
        ),
        FieldFactory(
            'birth_date',
            Point(700, 480),
            lambda: format_date(faker.date_of_birth(
                minimum_age=18,
                maximum_age=60,
            )),
            field_font,
            class_id=3,
            offset_limit=(4, 4),
        ),
        FieldFactory(
            'birth_place',
            Point(420, 560),
            lambda: f"{faker.city().upper()}\n{faker.region().upper()}",
            field_font,
            class_id=4,
            offset_limit=(8, 8),
        ),
        FieldFactory(
            'gender',
            Point(420, 700),
            lambda: random.choice(['мужской', 'женский']),
            field_font,
            class_id=5,
            offset_limit=(8, 8),
        ),
        FieldFactory(
            'reg_date',
            Point(700, 750),
            lambda: format_date(faker.date_of_birth(
                minimum_age=18,
                maximum_age=60,
            )),
            field_font,
            class_id=6,
            offset_limit=(4, 4),
        ),
    ), fonts)

    number = FieldGroup(number_renderer, (
        FieldFactory(
            'snils_number',
            Point(590, 280),
            lambda: f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(100, 999)} {random.randint(10, 99)}",
            number_font,
            class_id=7,
            offset_limit=(8, 8),
        ),
    ), fonts)

    image_source = images_dir / 'snils.png'
    return image_source, (fields, number)

def get_field_names():
    return field_names