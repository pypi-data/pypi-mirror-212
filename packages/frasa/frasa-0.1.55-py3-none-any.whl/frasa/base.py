import re

"""A simple word representation."""
class text():

    def __init__(self, string):
        self.string = string
        
    def __str__(self):
        return self.string
    
    def lower(self):
        return self.string.lower()
    
    def upper(self):
        return self.string.upper()
    
    def slug(self):
        return slug(self.string)
    

"""A list-like collection of words."""
def list(string):
    return string

def slug(string):
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