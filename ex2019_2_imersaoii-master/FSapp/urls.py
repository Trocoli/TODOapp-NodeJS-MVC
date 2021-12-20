from django.urls import path
from .views import *


urlpatterns = [
    path('cadastro/', cadastro, name='cadastro'),
    path('confirma_cadastro/<int:matricula>', confirma_cadastro, name='confirma_cadastro'),
    path('login',login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('', login_view, name='inicio'),
    path('rankingpalestra/', rankingpalestra, name='rankingpalestra'),
    path('rankingworkshop/', rankingworkshop, name='rankingworkshop'),
    path('rankinggeral/', rankinggeral, name='rankinggeral'),
    path('leitorqr/' , leitorqr, name='leitorqr'),
    path('baterponto/<int:matricula>', baterponto, name='baterponto'),
    path('evento/', criar_evento, name='criar_evento'),
    path('area', area_interesse, name='area_interesse'),
    path('enviarlink/', enviarlink, name='enviarlink'),

]
