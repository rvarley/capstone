from django import forms


class ContactForm(forms.Form):
    contact_name = forms.CharField(max_length=100)
    contact_email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)
