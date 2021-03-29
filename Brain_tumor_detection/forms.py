from django import forms
from .models import getImage

class ImageForm(forms.ModelForm):
    class Meta:
        model = getImage
        fields = ('caption','image')