from django.urls import path
from app import views

app_name='app'

urlpatterns = [
    path('',views.Menu,name='Menu'),
    path('pulp/',views.Pulp,name='Pulp')
]