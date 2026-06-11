from django import forms


class CommentForm(forms.Form):
    author_name = forms.CharField(label='Name', max_length=100)
    content = forms.CharField(label='Comment', widget=forms.Textarea)


class SearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=200, required=False)


class UploadForm(forms.Form):
    file = forms.FileField(label='File')
    description = forms.CharField(label='Description', max_length=255, required=False)


class FeedbackForm(forms.Form):
    message = forms.CharField(label='Message', widget=forms.Textarea)


class TransferForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    to_account = forms.CharField(label='To Account', max_length=50)
