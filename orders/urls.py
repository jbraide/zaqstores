from django.urls import path
from .import views
from django.utils.translation import gettext_lazy as _

app_name = 'orders'

urlpatterns = [
    path(_('create/'), views.order_create, name='order_create'),
    path('created/', views.order_created, name='order_created')
]
