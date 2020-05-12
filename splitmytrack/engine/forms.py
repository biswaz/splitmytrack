from django import forms
from .models import TrackUpload


class MusicUploadForm(forms.ModelForm):
    file = forms.FileField(widget=forms.FileInput(attrs={'class': "hidden"}))

    class Meta:
        model = TrackUpload
        fields = ['file']

