from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify


menu = [
    {'title':"О сайте", 'url_name': 'about'}, 
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'}
    ]


data_db = [
    {'id':1, 'title':'Резистор', 'context': 'Инфо о резиторах', 'is_published': True},
    {'id':2, 'title':'Конденсатор', 'context': 'Инфо о конденсаторах', 'is_published': False},
    {'id':3, 'title':'Дроссель', 'context': 'Инфо о дросселях', 'is_published': True}
    ]
def index(request):   # HttpRequest
    # t = render_to_string("someone/index.html")
    # return HttpResponse(t)
    data = {'title':'Главная станица',
            'title_inside': 'Полезная инфо',
            'menu': menu,
            'posts': data_db,
            }
    return render(request, "someone/index.html", context=data)


def about(request):
    return render(request, "someone/about.html", { 'title':'О сайте', 'title_in': 'Инфо о сайте', 'menu': menu,})

def show_post(request, post_id):
    return HttpResponse(f"<h1>Отображение статьи</h1><p>id:{post_id}</p>")

def addpage(request):
    return HttpResponse(f"<h1>Добавить статью</h1>")

def contact(request):
    return HttpResponse(f"<h1>Обратная связь</h1>")

def login(request):
    return HttpResponse(f"<h1>Авторизация</h1>")

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")