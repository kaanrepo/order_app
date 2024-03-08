from pathlib import Path
from django.core.exceptions import ValidationError
from PIL import Image

def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.jpeg' , '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

    
def validate_image(image):
    # Check the file size
    if image.size > 2 * 1024 * 1024:  # 5MB
        raise ValidationError("The maximum file size that can be uploaded is 2MB")

    # Check if it's a valid image
    try:
        img = Image.open(image)
        img.verify()  # verify that it is, in fact an image
    except (IOError, SyntaxError) as e:
        raise ValidationError('Invalid image')