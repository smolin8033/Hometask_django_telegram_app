from io import BytesIO, StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from PIL import Image


def generate_temp_image(counter: int = 1) -> list | SimpleUploadedFile:
    images = []
    for _ in list(range(counter)):
        file = BytesIO()
        image = Image.new("RGB", size=(100, 100))
        image.save(file, "jpeg")
        image.seek(0)
        images.append(SimpleUploadedFile(f"{id(file)}.jpg", file.getvalue()))
    return images[0] if counter == 1 else images


def generate_temp_file(counter: int = 1) -> list | InMemoryUploadedFile:
    files = []
    for _ in list(range(counter)):
        file = StringIO()
        file.write("hello world")
        text_file = InMemoryUploadedFile(file, None, f"{id(file)}.txt", "text", "charset", None)
        text_file.seek(0)
        files.append(text_file)
    return files[0] if counter == 1 else files
