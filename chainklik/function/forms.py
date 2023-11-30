from django import forms
from django.db.models import JSONField
from splitjson.widgets import SplitJSONWidget
import re

class EthAddressField(forms.CharField):
    def validate(self, value):
        super().validate(value)
        hex_pattern = re.compile(r'^0x[0-9a-fA-F]{40}$')
        if not hex_pattern.match(value):
            raise forms.ValidationError('Enter a valid ethereum address value.', code='invalid_eth_address')

class FunctionForm(forms.Form):
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(FunctionForm, self).__init__(*args, **kwargs)
        print(extra)
        for key in extra:
            self.fields['custom_%s' % key] = forms.CharField(label=extra[key])
