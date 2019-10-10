from . import views
from django.urls import path
import subprocess

#subprocess.Popen(['C:\\Users\\lexsh\\Desktop\\stockProject\\stockpython\\dist\\realNowStock.exe'])

urlpatterns = [
 	path('', views.index),
    path('output/', views.output),
    path('test/', views.test),
    path('predict3/', views.predict3)
]
