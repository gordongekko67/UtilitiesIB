from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index2', views.importa),
    path('index3', views.show),
    
    path('index5', views.importa_portfolio_con_rischio_di_assegnazione),
    path('index6', views.importa_portfolio_da_rollare_profitto),
    path('index8', views.importa_portfolio_ITM),
    
    path('index7', views.importa_trades),
    path('index9', views.analisi_trade),
    
]