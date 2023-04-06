from django import forms
from .models import EmergencyModePollResult
from .models import EmergencyModeIndicator

class AlertForm(forms.ModelForm):
    STATUS = [
    ('Safe', 'Safe'),
    ('Unsafe', 'Unsafe'),
    ('Not sure', 'Not sure'),
    ]
    status = forms.ChoiceField(choices=STATUS,widget=forms.RadioSelect)
    send_location = forms.BooleanField(required=False)

    class Meta:
        model = EmergencyModePollResult
        fields = ('status', 'lat', 'long')
        widgets = {
            'lat': forms.HiddenInput(attrs={'id': 'id_lat'}),
            'long': forms.HiddenInput(attrs={'id': 'id_long'}),
        }

class EmergencyForm(forms.ModelForm):
    enabled = forms.BooleanField(required=False)

    class Meta:
        model = EmergencyModeIndicator
        fields = ('enabled',)

class uploadFileForm(forms.Form):
    file = forms.FileField()

class uploadCSVForm(forms.Form):
    csvFile = forms.FileField()