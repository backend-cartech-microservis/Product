from django.urls import path
from .views import OrderAddView

app_name = "order"

urlpatterns = [
    path('create/', OrderAddView.as_view()),
]