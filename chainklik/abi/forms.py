from django import forms
import re

class EthAddressField(forms.CharField):
    def validate(self, value):
        super().validate(value)
        hex_pattern = re.compile(r'^0x[0-9a-fA-F]{40}$')
        if not hex_pattern.match(value):
            raise forms.ValidationError('Enter a valid ethereum address value.', code='invalid_eth_address')

class AbiForm(forms.Form):
    contract_address = EthAddressField(label='Contract Address', max_length=100)
    impl_address = EthAddressField(label='Implementaion Address', max_length=100)
    contract_name = forms.CharField(label='Contract Name', max_length=100)
    contract_description = forms.CharField(label='Contract Description', max_length=500)