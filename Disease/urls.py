from django.urls import path
from .views import predict_crop_disease,index
from .import views

urlpatterns = [
    path('', index, name='index'),
    path('', predict_crop_disease, name='predict_crop_disease'),
]
