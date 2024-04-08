from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all() #filter(is_published=TechStr.Status.PUBLISHED)

   
class TechStr(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = (0, 'Черновик')
        PUBLISHED = (1, 'Опубликовано')
    title = models.CharField(max_length=225, verbose_name = 'Заголовок')
    slug = models.SlugField(max_length=225, unique=True, db_index=True, verbose_name = 'slug')
    content = models.TextField(blank=True, verbose_name = 'Текст статьи')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name = 'Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name = 'Время изменения')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), 
                                                        default=Status.DRAFT, verbose_name = 'Опубликовано') # пропишем кастыль, т.к.нет модели BoolianChoices
    cat = models.ForeignKey('Category', on_delete=models.PROTECT,related_name='posts', verbose_name = 'Категории')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name = 'Теги названий блоков')
    analog = models.OneToOneField('OneAnalog', on_delete=models.SET_NULL, null=True, blank=True, related_name='analogs', verbose_name = 'Аналог')

    published = PublishedManager()
    objects = models.Manager()

    def __str__(self):
        return self.title
   
    class Meta:
        verbose_name = "Радиоэлементы"
        verbose_name_plural = "Радиоэлементы"
        ordering = ['-time_create']
        indexes = [models.Index(fields =['-time_create'])]

    def get_absolute_url(self):
        return reverse("post", kwargs={'post_slug': self.slug}) # post имя маршрута
    


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name = 'Категории')
    slug = models.SlugField(max_length=225, unique=True, db_index=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категории"
        
    
    def get_absolute_url(self):
        return reverse("category", kwargs={'cat_slug': self.slug}) # category имя маршрута


class TagPost(models.Model):
    tag = models.CharField(max_length=100,db_index=True)
    slug = models.SlugField(max_length=255,unique=True, db_index=True) 

    def __str__(self):
        return self.tag
    
    def get_absolute_url(self):
        return reverse("tags", kwargs={'tag_slug': self.slug}) # tag имя маршрута
    

class OneAnalog(models.Model):
    name=models.CharField(max_length=100)
    сoincidence=models.IntegerField(null=True)
    a_count=models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name
    