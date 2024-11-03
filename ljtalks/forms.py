from django import forms
# from captcha.fields import ReCaptchaField


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'id': 'name'}),
        required=True)
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'id': 'email'}),
        required=True)
    message = forms.CharField(
        widget=forms.Textarea(attrs={'id': 'message'}),
        required=True)
    honeytrap = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ContactForm, self).__init__(*args, **kwargs)

    def is_user_authenticated(self):
        if self.request and self.request.user.is_authenticated:
            return True
        return False
