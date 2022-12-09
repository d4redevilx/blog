from .models import Post
from django import forms


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=250)
    body = forms.Textarea()
    image = forms.FileField(required=False)

    class Meta:
        model = Post
        fields = ('title', 'body', 'image')
        widgets = {
            'title': forms.widgets.TextInput(attrs={'class': 'form-control'}),
            'body': forms.widgets.Textarea(attrs={'class': 'form-control'})
        }
