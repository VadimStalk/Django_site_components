from django import forms
from .models import Category, OneAnalog


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255,
                            min_length=5,
                            label='Заголовок',
                            widget=forms.TextInput(attrs={'class':'form-input'}),       # через widget меняем стиль отображения в поле ввода
                            error_messages={                                            # Собственный валидатор, обработчик ошибок
                                'min_length':'Слишком короткий заголовок',
                                'required':'Без заголовка никак',
                                })
    slug = forms.SlugField(max_length=255, label='URL')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols':50, 'rows': 5}), required=False, label='Контент')
    is_published = forms.BooleanField(required=False, initial=True, label='Публикация')
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Не выбрано', label='Категория')
    analog = forms.ModelChoiceField(queryset=OneAnalog.objects.all(), required=False, empty_label='Отсутствует',label='Аналог')
