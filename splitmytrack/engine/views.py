import os

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core import serializers
from rest_framework_encrypted_lookup.serializers import EncryptedLookupSerializerMixin

from .forms import MusicUploadForm
from .models import TrackUpload
from .tasks import split_tracks_wrapper


def home(request):
    if request.method == 'POST':
        form = MusicUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.status = instance.STATUS.new
            instance.save()
            file_name = os.path.splitext(os.path.basename(instance.file.name))[0]
            serialized_instance = serializers.serialize('json', [instance])
            split_tracks_wrapper.delay(serialized_instance, file_name)
            return HttpResponseRedirect('/download/{}/'.format(instance.encrypted_id))

    else:
        form = MusicUploadForm()
    return render(request, 'home.html', {'form': form})


def download(request, encrypted_id):
    decrypted_id = EncryptedLookupSerializerMixin.get_cipher().decode(encrypted_id)
    track = TrackUpload.objects.get(id=decrypted_id)
    fname = os.path.splitext(os.path.basename(track.file.name))[0]
    url_base = os.path.join(settings.MEDIA_URL, 'processed', fname)

    return render(request, 'download.html', {'url_base': url_base, 'status': track.status})
