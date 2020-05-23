import os

import razorpay
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core import serializers
from django.contrib.auth.decorators import login_required
from rest_framework_encrypted_lookup.serializers import EncryptedLookupSerializerMixin

from .forms import MusicUploadForm, OrderForm
from .models import TrackUpload
from .tasks import split_tracks_wrapper
from ..users.models import Order

LAST_UPLOADED_TRACK_COOKIE = 'lastUploadedTrack'


def home(request):
    if request.method == 'POST':
        form = MusicUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.status = instance.STATUS.new
            if request.user.is_authenticated:
                instance.user = request.user
            instance.save()
            file_name = os.path.splitext(os.path.basename(instance.file.name))[0]
            serialized_instance = serializers.serialize('json', [instance])
            pro = False
            if request.user.is_authenticated and request.user.coins > 0:
                request.user.coins -= 1
                request.user.save()
                pro = True
            split_tracks_wrapper.delay(serialized_instance, file_name, pro=pro)
            return HttpResponseRedirect('/download/{}/'.format(instance.encrypted_id))

    else:
        form = MusicUploadForm()
    return render(request, 'home.html', {'form': form})


def download(request, encrypted_id):
    decrypted_id = EncryptedLookupSerializerMixin.get_cipher().decode(encrypted_id)
    track = TrackUpload.objects.get(id=decrypted_id)
    fname = os.path.splitext(os.path.basename(track.file.name))[0]
    url_base = os.path.join(settings.MEDIA_URL, 'processed', fname)

    response = render(request, 'download.html', {'url_base': url_base, 'track': track})
    response.set_cookie(LAST_UPLOADED_TRACK_COOKIE, encrypted_id)
    return response


@login_required()
def buy(request, pack_id=None):
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
    if request.method == 'POST':
        order = Order.objects.get(razorpay_order_id=request.POST.get('razorpay_order_id'))
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order_params = {
                'razorpay_order_id': order.razorpay_order_id,
                'razorpay_payment_id': order.razorpay_payment_id,
                'razorpay_signature': order.razorpay_signature
            }
            if client.utility.verify_payment_signature(order_params):  # TODO: else show error
                order.status = order.STATUS.paid
                request.user.coins += order.coins
                order.save()
                request.user.save()
                if request.COOKIES.get(LAST_UPLOADED_TRACK_COOKIE):
                    return HttpResponseRedirect('/regen')
                return HttpResponseRedirect('/')

    else:
        if pack_id == 1:
            amount = 1 * 100
            coins = 1
        elif pack_id == 2:
            amount = 160 * 100
            coins = 10
        elif pack_id == 3:
            amount = 750 * 100
            coins = 50

        order = Order(buyer=request.user, coins=coins)
        data = {
            'amount': amount,  # in paisa
            'currency': 'INR',
            'receipt': str(order.receipt),
            'payment_capture': 1
        }
        rz_order = client.order.create(data=data)
        order.razorpay_order_id = rz_order['id']
        order.status = order.STATUS.created
        order.amount = amount
        order.save()
        return render(request, 'buy.html', {'order_id': rz_order['id']})


@login_required()
def regen_full_track(request):
    if request.method == 'POST':
        if not request.COOKIES.get(LAST_UPLOADED_TRACK_COOKIE):
            return HttpResponseRedirect('/')
        encrypted_id = request.COOKIES.get(LAST_UPLOADED_TRACK_COOKIE)
        decrypted_id = EncryptedLookupSerializerMixin.get_cipher().decode(encrypted_id)
        track = TrackUpload.objects.get(id=decrypted_id)
        file_name = os.path.splitext(os.path.basename(track.file.name))[0]
        serialized_instance = serializers.serialize('json', [track])
        pro = False
        if request.user.coins > 0:
            request.user.coins -= 1
            request.user.save()
            pro = True
        # handle else redirect
        split_tracks_wrapper.delay(serialized_instance, file_name, pro=pro)
        return HttpResponseRedirect('/download/{}/'.format(encrypted_id))
    else:
        return render(request, 'regen.html', {})
