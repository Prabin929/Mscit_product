from django.contrib import admin
from django.urls import path
from stress_detection import views
from django.conf.urls.static import static
from .views import add_stress_data

urlpatterns = [
    path('', views.index,name='home'),
    path('about', views.about,name='about'),
    path('stress_detect', views.stress_detect,name='stress_detect'),
    path('stress_mgnt', views.stress_mgnt, name='stress_mgnt'),
    path('add/', views.add_stress_data, name='add_stress_data'),
    path('detect_stress/', views.detect_stress, name='detect_stress'),
    path('stress_detection/', views.stress_detection, name='stress_detection')

]