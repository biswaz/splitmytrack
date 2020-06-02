import os

from django.contrib import admin
from django.core import serializers
from .models import TrackUpload
from .tasks import split_tracks_wrapper


# Register your models here.

def regen_tracks(modeladmin, request, queryset):
    for instance in queryset:
        file_name = os.path.splitext(os.path.basename(instance.file.name))[0]
        serialized_instance = serializers.serialize('json', [instance])
        split_tracks_wrapper.delay(serialized_instance, file_name, pro=True)


class TrackUploadAdmin(admin.ModelAdmin):
    actions = [regen_tracks]


admin.site.register(TrackUpload, TrackUploadAdmin)
