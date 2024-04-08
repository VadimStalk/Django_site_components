from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from .models import TechStr, Category, TagPost

menu = [
    {'title':"О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'}
    ]


# data_db = [
#     {'id':1, 'title':'Резистор', 'content': '''<p>Рези́стор</p> (англ. resistor, от лат. resisto — сопротивляюсь),
#      также сопротивление — пассивный элемент электрических цепей, 
#      обладающий определённым постоянным или переменным значением электрического сопротивления, 
#      предназначенный для линейного преобразования силы тока в напряжение и напряжения в силу тока, ограничения тока,
#      поглощения электрической энергии и других видов перераспределения электрической энергии. Весьма широко используемый
#      компонент практически всех электрических и электронных устройств.''',
#      'is_published': True},
#     {'id':2, 'title':'Конденсатор', 'content': '''<h1>Конденса́тор</h1> (от лат. condensare — «уплотнять», «сгущать»
#      или от лат. condensatio — «накопление») — электронный компонент, представляющий собой двухполюсник с постоянным
#      или переменным значением ёмкости и малой проводимостью; устройство для накопления заряда и энергии электрического поля.
#      Конденсатор является пассивным электронным компонентом. 
#      В СИ ёмкость конденсатора измеряется в фарадах.''',
#      'is_published': False},
#     {'id':3, 'title':'Дроссель', 'content': '''В широком смысле слова, дроссель — это ограничитель;
#      в электротехнике — катушка индуктивности, обладающая высоким сопротивлением переменному току и малым сопротивлением постоянному;
#      Гидравлический дроссель или пневматический дроссель — устройство на пути движения жидкости или газа, может быть нерегулируемое или регулируемое;
#      дроссельная заслонка в системах подачи топлива (например, в двигателе внутреннего сгорания), а также ручка, регулирующая эту заслонку;
#      дроссельная (редукционная) арматура — элемент трубопроводной арматуры, предназначенный для снижения (редуцирования) рабочего давления в системе
#      за счёт увеличения гидравлического сопротивления в проточной части;''', 'is_published': True}
#     ]


def index(request):   # HttpRequest
    # t = render_to_string("someone/index.html")
    # return HttpResponse(t)
    posts = TechStr.published.all().select_related('cat')
    data = {'title':'Главная станица',
            'title_inside': 'Полезная инфо',
            'menu': menu,
            'posts': posts,
            'cat_selected': 0,
            }
    return render(request, "someone/index.html", context=data)


def about(request):
    return render(request, "someone/about.html", { 'title':'О сайте', 'title_in': 'Инфо о сайте', 'menu': menu,})

def show_post(request, post_slug):
    post = get_object_or_404(TechStr, slug=post_slug)
    data ={
        'title': post.title,
        'menu' : menu,
        'post': post,
        'cat_selected': 1,
        }
    return render(request, 'someone/post.html', data)


def addpage(request):
    return HttpResponse(f"<h1>Добавить статью</h1>")

def contact(request):
    return HttpResponse(f"<h1>Обратная связь</h1>")

def login(request):
    return HttpResponse(f"<h1>Авторизация</h1>")

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = TechStr.objects.filter(cat_id=category.pk).select_related('cat')
    data = {'title': f'Рубрика {category.name}',
            'title_inside': 'Полезная инфо',
            'menu': menu,
            'posts': posts,
            'cat_selected': category.pk,
            }
    return render(request, "someone/index.html", context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=TechStr.Status.PUBLISHED).select_related('cat')
    data = {'title': f'Тег: {tag.tag}',
            'menu': menu,
            'posts': posts,
            'cat_selected': None,
            }
    return render(request, "someone/index.html", context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")