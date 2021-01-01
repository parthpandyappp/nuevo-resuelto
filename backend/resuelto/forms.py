from django.forms import ModelForm
from .models import resolute


class ResolutionForm(ModelForm):
    class Meta:
        model = resolute
        fields = '__all__'
