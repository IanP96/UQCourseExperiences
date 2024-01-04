from django.urls import path, re_path
from .views import *
from django.views.static import serve
from mysite.settings import STATIC_ROOT

urlpatterns = [
    path("", index_view, name="home"),
    path("add-experience", add_experience_view, name="add_experience"),
    path("comment/<int:experience_id>", comment_view, name="comment"),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]
