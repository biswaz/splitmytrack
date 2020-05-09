from django import forms
from .models import TrackUpload


class MusicUploadForm(forms.ModelForm):
    class Meta:
        model = TrackUpload
        fields = ['file']

