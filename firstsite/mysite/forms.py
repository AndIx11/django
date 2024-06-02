from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .models import Category, ISBN, MySite
from django.core.validators import MinLengthValidator, MaxLengthValidator


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                                 empty_label="Категория не выбрана",
                                 label="Категории")
    isbn = forms.ModelChoiceField(queryset=ISBN.objects.all(),
                                     required=False,
                                     empty_label="Не заполнено",
                                     label="Номер ISBN")

    class Meta:
        model = MySite
        fields = ['title', 'slug', 'content', 'photo',
                  'is_published', 'cat', 'isbn', 'tags']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-input'}),
                   'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
                   }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50: raise ValidationError('Длина превышает 50 символов')
        return title


class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Изображение")
