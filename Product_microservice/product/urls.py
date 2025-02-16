from django.urls import path
from .views import ProductAddView


urlpatterns = [
    path("create/", ProductAddView.as_view())

]