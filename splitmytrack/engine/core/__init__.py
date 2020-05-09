import os
from django.conf import settings
from spleeter.separator import Separator
separator = Separator('spleeter:2stems')


def split_tracks(file_path):
    separator.separate_to_file(file_path, os.path.join(settings.MEDIA_ROOT, 'processed'))

