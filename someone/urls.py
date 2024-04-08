from django.urls import path, register_converter
from . import views
# from . import converters

# register_converter(converters.FourDigitYearConverter, "year4")


urlpatterns = [
    path('', views.index, name = 'home'),          #  http://127.0.0.8000
    # path('cats/<int:cat_id>/', views.categories, name = 'cats_id'), # http://127.0.0.8000/cats/2/ , 'int' - конвертер
    path("about/", views.about, name = 'about'),
    path('addpage/', views.addpage, name = 'add_page'),
    path("contact/", views.contact, name = 'contact'),
    path("login/", views.login, name = 'login'),
    path("post/<slug:post_slug>/", views.show_post, name = 'post'), #'int' - конвертер
    path("category/<slug:cat_slug>/", views.show_category, name = 'category'), #'int' - конвертер
    path("tag/<slug:tag_slug>/", views.show_tag_postlist, name = 'tags'),
]
