from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='socketio_web'),
    path('patient/', views.patient_page, name='patient'),
    path('visit/', views.visit_page, name='visit'),
]