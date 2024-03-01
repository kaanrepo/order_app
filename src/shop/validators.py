from pathlib import Path
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.jpeg' , '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def validate_file_size(value):
    filesize = value.size
    
    if filesize > 2097152:
        raise ValidationError("The maximum file size that can be uploaded is 2MB")