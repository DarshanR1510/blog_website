from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from blog_app.models import Post, Comment


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('author', 'title', 'text',)

        #here, widgets are for giving css to the form fields.
        widgets = {
        'title': forms.TextInput(attrs={'class':'textinputclass'}),
        'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'})
        }                                           #editable and medium-editor-textarea are the css classes


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

        widgets = {
        'author': forms.TextInput(attrs={'class':'textinputclass'}),
        'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }
