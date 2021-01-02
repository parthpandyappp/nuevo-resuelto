from django.forms import ModelForm
from .models import Resolution


class ResolutionForm(ModelForm):
    class Meta:
        model = Resolution
        fields = '__all__'
