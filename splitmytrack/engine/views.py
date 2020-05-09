import os

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.conf import settings

from .core import split_tracks
from .forms import MusicUploadForm


def home(request):
    if request.method == 'POST':
        form = MusicUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            split_tracks(instance.file.path)
            file_name = os.path.splitext(os.path.basename(instance.file.name))[0]
            return HttpResponseRedirect('/download/{}/'.format(file_name))

    else:
        form = MusicUploadForm()
    return render(request, 'pages/home.html', {'form': form})


def download(request, fname=None):
    if fname:
        url_base = os.path.join(settings.MEDIA_URL, 'processed', fname)
    return render(request, 'pages/download.html', {'url_base': url_base})
