from django.urls import path
from .views import SearchContactView 

urlpatterns = [
    path('search/', SearchContactView.as_view(), name='search_contacts'),
]