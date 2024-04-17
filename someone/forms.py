from typing import Any
from django import forms
from django.utils.deconstruct import deconstructible
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from .models import Category, OneAnalog


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789- "
    code = 'russian'

    def __init__(self, message=None) -> None:
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел"

    def __call__(self, value, *args: Any, **kwds: Any) -> Any:
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=7, label='Заголовок', widget=forms.TextInput(attrs={'class':'form-input'}),
                            # validators=[
                            #     RussianValidator(),
                            #     ],
                            error_messages={'min_length':'Слишком короткий заголовок', 'required':'Без заголовка никак',}) # через widget меняем стиль отображения в поле ввода. Собственный валидатор, обработчик ошибок
    slug = forms.SlugField(max_length=255, label='URL',
                           validators=[
                               MinLengthValidator(5, message="Минимум 5 символов"),
                               MaxLengthValidator(100, message="Максимум 100 символов")])
    content = forms.CharField(widget=forms.Textarea(attrs={'cols':50, 'rows': 5}), required=False, label='Контент')
    is_published = forms.BooleanField(required=False, initial=True, label='Публикация')
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Не выбрано', label='Категория')
    analog = forms.ModelChoiceField(queryset=OneAnalog.objects.all(), required=False, empty_label='Отсутствует',label='Аналог')
    
    def clean_title(self):
        title = self.cleaned_data["title"]
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789- "

        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError("Должны присутствовать только русские символы, дефис и пробел")