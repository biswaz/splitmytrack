from config import celery_app
from .core import split_tracks


@celery_app.task()
def split_tracks_wrapper(*args, **kwargs):
    split_tracks(*args, **kwargs)
