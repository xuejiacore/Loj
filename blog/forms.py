from django import forms


class BlogPublishForm(forms.Form):
    blogTitle = forms.CharField(label='blogTitle', min_length=1, max_length=30)
    blogContent = forms.CharField(min_length=1)
