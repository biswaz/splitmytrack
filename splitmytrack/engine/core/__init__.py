import logging
import os
import random

from django.conf import settings
from django.core import serializers
from spleeter.separator import Separator
from pydub import AudioSegment

from .utils import mkdir_p

_LOG = logging.getLogger(__name__)
separator = Separator('spleeter:2stems')


def split_tracks(serialized_instance, file_name, pro=False):
    instance = next(serializers.deserialize('json', serialized_instance)).object
    input_file_path = instance.file.path
    instance.status = instance.STATUS.processing
    instance.save(force_update=True)

    input_audio = AudioSegment.from_mp3(input_file_path)
    output_base_path = os.path.join(settings.MEDIA_ROOT, 'processed')
    output_track_dir = os.path.join(output_base_path, file_name)
    mkdir_p(output_track_dir)

    if not pro and len(input_audio) > 30 * 1000:
        start = random.randrange(0, len(input_audio) - 30 * 1000, 1000)
        end = start + 30 * 1000
        _LOG.info("\nStart: {}\t End: {}".format(start, end))
        trimmed_file_name = os.path.basename(input_file_path)
        trimmed_file_path = os.path.join(output_track_dir, trimmed_file_name)
        input_audio[start:end].export(trimmed_file_path)
        input_file_path = trimmed_file_path

    separator.separate_to_file(input_file_path, output_base_path, synchronous=True)
    _LOG.info("separated file %s to path: %s", file_name, output_track_dir)

    AudioSegment.from_wav(os.path.join(output_track_dir, 'vocals.wav')) \
        .export(os.path.join(output_track_dir, 'vocals.mp3'))
    AudioSegment.from_wav(os.path.join(output_track_dir, 'accompaniment.wav')) \
        .export(os.path.join(output_track_dir, 'accompaniment.mp3'))

    instance.status = instance.STATUS.processed
    if pro:
        instance.conversion_type = instance.CONVERSION_CHOICES.full
    instance.save(force_update=True)
