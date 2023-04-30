from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    """comments form"""
    comment = forms.CharField(widget=forms.Textarea(attrs={
                                                        "class": "form-control border",
                                                        "placeholder": "Comment here...",
                                                        "rows": "4",
                                                        }))
    class Meta:
        model = Comment
        fields = ['comment',]
        


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'slug','tags' , 'banner', ]
        prepopulated_fields = {"slug": ("title",)} #don't worked
        # <input type="text" data-role="tagsinput" class="form-control" name="tags">
        tags = forms.CharField(widget=forms.Textarea(
                                                    attrs={
                                                        "data-role": "tagsinput",
                                                        "class": "form-control",
                                                        "name": "tags"
                                                        }))