import validators
from urllib.parse import urlparse


def validate(url):
    errors = []
    if len(url) > 255:
        errors.append('URL превышает длину в 255 символов')
    if not validators.url(url):
        errors.append('Некорректный URL')
    return errors