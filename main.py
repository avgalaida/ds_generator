import sys
from pathlib import Path
from PIL import Image
import albumentations as A
from sklearn.model_selection import train_test_split
from ds_generator.document_generator import DocumentGenerator
import numpy as np

def load_template(template_name, fonts_dir, images_dir):
    if template_name == 'snils':
        from ds_generator.templates.snils_template import get_snils_template, get_field_names
        return get_snils_template(fonts_dir, images_dir), get_field_names()
    elif template_name == 'passport':
        from ds_generator.templates.passport_template import get_passport_template, get_field_names
        return get_passport_template(fonts_dir, images_dir), get_field_names()
    else:
        raise ValueError(f"Unknown template: {template_name}")

def augment_image(image: Image.Image) -> Image.Image:
    # Преобразуем изображение в RGB, если оно имеет альфа-канал
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    transform = A.Compose([
        A.Blur(blur_limit=3, p=0.1),
        A.RandomBrightnessContrast(p=0.2),
        A.RandomGamma(p=0.2),
        A.HueSaturationValue(p=0.2),
        A.RGBShift(p=0.1),
        A.ToGray(p=0.1)
    ])
    image_np = np.array(image)
    augmented = transform(image=image_np)['image']
    return Image.fromarray(augmented)

def generate_documents(template_name: str, output_dir: str, num_documents: int):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    root_dir = Path(__file__).resolve().parent
    fonts_dir = root_dir / 'fonts'
    images_dir = root_dir / 'images'

    document_dir = output_dir / template_name
    document_dir.mkdir(parents=True, exist_ok=True)

    train_dir = document_dir / 'train'
    valid_dir = document_dir / 'valid'

    train_images_dir = train_dir / 'images'
    train_labels_dir = train_dir / 'labels'
    valid_images_dir = valid_dir / 'images'
    valid_labels_dir = valid_dir / 'labels'

    train_images_dir.mkdir(parents=True, exist_ok=True)
    train_labels_dir.mkdir(parents=True, exist_ok=True)
    valid_images_dir.mkdir(parents=True, exist_ok=True)
    valid_labels_dir.mkdir(parents=True, exist_ok=True)

    try:
        (image_source, field_groups), field_names = load_template(template_name, fonts_dir, images_dir)

        all_files = []
        for i in range(1, num_documents + 1):
            image = Image.open(image_source)
            generator = DocumentGenerator(image, field_groups)

            image_name = f"{template_name}_{i}.png"
            label_name = f"{template_name}_{i}.txt"
            all_files.append((image_name, label_name))

            output_image_path = document_dir / image_name
            annotation_path = document_dir / label_name

            # Генерируем изображение с текстовыми полями
            output_image = generator.generate(annotation_path)

            # Применяем аугментации к сгенерированному изображению
            augmented_image = augment_image(output_image)
            augmented_image.save(output_image_path)

        # Split the data into training and validation sets
        train_files, valid_files = train_test_split(all_files, test_size=0.2, random_state=42)

        # Move files to the respective directories
        for image_name, label_name in train_files:
            (document_dir / image_name).rename(train_images_dir / image_name)
            (document_dir / label_name).rename(train_labels_dir / label_name)

        for image_name, label_name in valid_files:
            (document_dir / image_name).rename(valid_images_dir / image_name)
            (document_dir / label_name).rename(valid_labels_dir / label_name)

        # Create the conf.yaml file
        conf_yaml_path = document_dir / 'conf.yaml'
        with conf_yaml_path.open('w') as f:
            f.write(f"path: {output_dir}\n")
            f.write("train: 'train/images'\n")
            f.write("val: 'valid/images'\n\n")
            f.write("names:\n")
            for idx, name in field_names.items():
                f.write(f"  {idx}: '{name}'\n")

        print(f"Documents generated successfully in {document_dir}")
    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    template_name = "passport"
    output_dir = "./output/"
    num_documents = 10

    generate_documents(template_name, output_dir, num_documents)