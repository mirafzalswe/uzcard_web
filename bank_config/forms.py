from django import forms
# from .models import BankProfile
#
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = BankProfile
#         fields = '__all__'

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                                widget=forms.Textarea)