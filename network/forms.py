from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_content']
        widgets = {
            'post_content': forms.Textarea(attrs={
                'placeholder': 'How are you feeling?...',
                'required': True,
                'rows': 4,
                'cols': 40
            })
        }


