from django import forms
from django_summernote.widgets import SummernoteWidget
from taggit.forms import TagWidget

from .models import Post, Category, FriendlyLink


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title_en', 'title_es', 'title_ar', 'content_en', 'content_es', 'content_ar', 'img', 'in_trend',
        'is_active', 'is_active', 'tags', 'category',)

        widgets = {
            'title_en': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'title English'}),
            'title_es': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'title Spain'}),
            'title_ar': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'title Arabic'}),
            'content_en': SummernoteWidget(),
            'content_es': SummernoteWidget(),
            'content_ar': SummernoteWidget(),
            'img': forms.FileInput(attrs={'class': 'form-file-input'}),
            'in_trend': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'tags': TagWidget(attrs={'placeholder': 'Enter the tags separated by a space'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title_en', 'title_es', 'title_ar',)

        widgets = {
            'title_en': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'title English'}),
            'title_es': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'title English'}),
            'title_ar': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'title English'}),
        }


class FriendlyLinkForm(forms.ModelForm):
    class Meta:
        model = FriendlyLink
        fields = ('friend', 'name_en', 'name_es', 'name_ar', 'link')

        widgets = {
            'friend': forms.TextInput(attrs={'class': 'form-input'}),
            'name_en': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'title English'}),
            'name_es': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'title English'}),
            'name_ar': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'title English'}),
            'link': forms.TextInput(attrs={'class': 'form-input'}),
        }