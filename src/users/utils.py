from core.utils import get_filename

def upload_user_photo_to(instance, filename):
    new_filename = get_filename(filename)
    return f'users/{new_filename}'