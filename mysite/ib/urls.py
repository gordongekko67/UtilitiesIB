from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index2', views.importa),
    path('index3', views.show),
    
    path('index5', views.importa_portfolio_con_rischio_di_assegnazione),
    path('index6', views.importa_portfolio_da_rollare_profitto),
    path('index8', views.importa_portfolio_ITM),
    path('index19', views.importa_portfolio_ITM_valore_temporale),

    
    path('index7', views.importa_trades),
    path('index9', views.analisi_trade_scadenza),
    path('index10', views.analisi_trade_titolo),
    path('index11', views.analisi_bilanciamento_delta),
    path('index24', views.analisi_bilanciamento_delta_titolo_scadenza),
    path('index21', views.opzioni_PUT_da_rollare),
    path('index22', views.opzioni_CALL_da_vedere_se_andare_invertito),
    path('index12', views.analisi_trade_dettaglio),
    path('index13', views.calcolo_theta_portafoglio),
    path('index14', views.calcolo_totale_valore_temporale),
    path('index15', views.analisi_opzioni_potenzialmente_da_rollare),
    path('index16', views.analisi_trade_scadenza_simbolo),
    path('index18', views.analisi_trade_scadenza_simbolo_ancora_aperte),
    path('index20', views.analisi_trade_scadenza_simbolo_completamente_chiuse),
    path('index17', views.analisi_trade_dettaglio_simbolo_ancora_aperte),
    path('index99', views.analisi_di_portafoglio),
    path('index98', views.nuova_analisi_di_portafoglio),
    path('index100',views.ultimate_analisi_di_portafoglio),


    path('index4', views.analisi_opzioni_vendute_comprate),
    path('index23', views.analisi_operazioni), 
    path('index25', views.analisi_operazioni_di_un_determinato_mese),
    
   
    
]