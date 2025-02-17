from django.urls import path
from .views import OrderAddView, OrderGetListView

app_name = "order"

urlpatterns = [
    path('create/', OrderAddView.as_view()),
    path('get-requests/<user_id>', OrderGetListView.as_view())
]