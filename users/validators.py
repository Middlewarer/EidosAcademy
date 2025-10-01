from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.files.uploadedfile import UploadedFile
from PIL import Image

ALLOWED_EXTENSIONS = ('jpg', 'jpeg', 'png', 'webp')
ALLOWED_CONTENT_TYPES = {
    'image/jpeg', 'image/jpg', 'image/pjpeg',
    'image/png',  'image/x-png',
    'image/webp',
}

MAX_SIZE = 2 * 1024 * 1024  # 2 MB
MIN_W, MIN_H = 96, 96

def validate_image(file):
    # 0) Поле может быть пустым
    if not file:
        return

    # 1) Размер файла (если доступен)
    size = getattr(file, 'size', None)
    if size and size > MAX_SIZE:
        raise ValidationError(f'Файл слишком большой (>{MAX_SIZE // (1024*1024)}MB)')

    # 2) Проверка контент-типа ТОЛЬКО для новой загрузки
    if isinstance(file, UploadedFile):
        ctype = (getattr(file, 'content_type', '') or '').lower()
        if ctype not in ALLOWED_CONTENT_TYPES:
            raise ValidationError('Файл должен быть в формате: JPG, PNG или WEBP')

    # 3) Проверка, что это действительно изображение, и его размеров
    #    Работает и для UploadedFile, и для FieldFile (существующий файл)
    try:
        # достаём «читаемый» объект файла
        fobj = getattr(file, 'file', file)  # у FieldFile есть .file, у UploadedFile сам file читаемый
        # Pillow должен уметь его открыть
        pos = None
        if hasattr(fobj, 'tell') and hasattr(fobj, 'seek'):
            pos = fobj.tell()
        with Image.open(fobj) as img:
            w, h = img.size
            if w < MIN_W or h < MIN_H:
                raise ValidationError(f'Изображение должно быть минимум {MIN_W}x{MIN_H}px')
    finally:
        # вернём указатель, если двигали
        if pos is not None and hasattr(fobj, 'seek'):
            fobj.seek(pos)