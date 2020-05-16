import os

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.conf import settings

from .forms import MusicUploadForm
from .tasks import split_tracks_wrapper


def home(request):
    if request.method == 'POST':
        form = MusicUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            file_name = os.path.splitext(os.path.basename(instance.file.name))[0]
            split_tracks_wrapper.delay(instance.file.path, file_name)
            return HttpResponseRedirect('/download/{}/'.format(file_name))

    else:
        form = MusicUploadForm()
    return render(request, 'home.html', {'form': form})


def download(request, fname=None):
    if fname:
        url_base = os.path.join(settings.MEDIA_URL, 'processed', fname)
    return render(request, 'download.html', {'url_base': url_base})
