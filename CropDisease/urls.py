from django.contrib import admin
from django.urls import path
from django.urls import re_path


from Disease import views


#devolpomnet only 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    
    re_path('^$',views.index,name='index'),  
    re_path('index',views.index, name='index'),

    re_path('^$',views.upload,name='homepage'),  
    re_path('upload',views.upload, name='upload'),

    re_path('predict_crop_disease',views.predict_crop_disease, name='predict_crop_disease'),

]

#devolpomnet only 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
