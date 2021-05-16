from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>",views.entry, name="entry"),
    path("newpage",views.newpage, name="newpage"),
    path("wiki/<str:entry>/editpage", views.edit,name="edit" ),
    path("random",views.random,name = "random")
]
