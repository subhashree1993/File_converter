
from django.urls import path
from .views import home, registrationSuccess, upload, login, loginAfterRegistration, getLogs

urlpatterns = [
    path('', home , name='home'),
    path('registrationSuccess' , registrationSuccess , name='registrationSuccess'),
    path('login' , login, name='login'),
    path('loginAfterRegistration' , loginAfterRegistration, name='loginAfterRegistration'),
    path('upload' , upload , name='upload'),
    path('getLogs' , getLogs , name='getLogs'),
]