from django import forms
from .models import TrackUpload
from ..users.models import Order


class MusicUploadForm(forms.ModelForm):
    file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': "hidden "
        }))

    class Meta:
        model = TrackUpload
        fields = ['file']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature']
