from django.urls import path
from .views import ProductAddView

app_name = "product"

urlpatterns = [
    path("create/", ProductAddView.as_view())

]