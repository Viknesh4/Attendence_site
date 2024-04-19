from django.urls import path
from .views import firebase_data_view,user_login,slogin
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('firebase_data/', firebase_data_view, name='firebase_data'),
    path('login/', user_login, name='login'),
    path('slogin/', slogin, name='slogin'),
    path('student_data/', views.student_data, name='student_data'),
]