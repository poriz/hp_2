from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path("",views.index, name = 'index'),
    path("comment",views.comment_write, name = 'comment'),
    # path("data_to_db/", views.data_to_db, name = 'data_to_db'),
]