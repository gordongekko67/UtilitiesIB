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
    path('index9', views.analisi_trade_scadenza),
    path('index10', views.analisi_trade_titolo),
    path('index11', views.analisi_bilanciamento_delta),
    path('index21', views.opzioni_PUT_da_rollare),
    path('index22', views.opzioni_CALL_da_vedere_se_andare_invertito),
    path('index12', views.analisi_trade_dettaglio),
    path('index13', views.calcolo_theta_portafoglio),
    path('index99', views.analisi_di_portafoglio),
    
   
    
]