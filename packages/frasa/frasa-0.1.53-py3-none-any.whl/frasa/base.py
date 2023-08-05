import re

def slugify(string):
    """
    Mengubah string menjadi slug yang dapat digunakan dalam URL.

    Args:
        string (str): String yang akan diubah menjadi slug.

    Returns:
        str: Slug string hasil konversi.
    """
    slug = re.sub(r'\s+', '-', string)
    slug = re.sub(r'[^a-zA-Z0-9-]', '', slug)
    slug = slug.lower()

    return slug