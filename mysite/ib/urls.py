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
    path('index28', views.importa_portfolio_ITM_valore_temporale_percentuale),
    

    
    path('index7', views.importa_trades),
    path('index9', views.analisi_trade_scadenza),
    path('index10', views.analisi_trade_titolo),
    path('index11', views.analisi_bilanciamento_delta),
    path('index24', views.analisi_bilanciamento_delta_titolo_scadenza),
    path('index21', views.opzioni_da_vedere_se_andare_invertito),
   
    path('index12', views.analisi_trade_dettaglio),
    path('index13', views.calcolo_theta_portafoglio),
    path('index14', views.calcolo_totale_valore_temporale),
    path('index34', views.calcolo_totale_valore_temporale_residuo_per_scadenza),
    path('index15', views.analisi_opzioni_potenzialmente_da_rollare),
    path('index16', views.analisi_trade_scadenza_simbolo),
    path('index27', views.analisi_trade_scadenza_simbolo_2),
    path('index29', views.analisi_trade_scadenza_simbolo_3),
    path('index40', views.analisi_prendere_profitto),
     

    path('index18', views.analisi_trade_scadenza_simbolo_ancora_aperte),
    path('index37', views.analisi_trade_scadenza_simbolo_ancora_aperte_ordinate_per_mese),
    path('index38', views.analisi_trade_scadenza_simbolo_specifica),
    path('index20', views.analisi_trade_scadenza_simbolo_completamente_chiuse),
    path('index17', views.analisi_trade_dettaglio_simbolo_ancora_aperte),
    path('index99', views.analisi_di_portafoglio),
    path('index97', views.elevatissimo_rischio_di_assegnazione),
    path('index98', views.nuova_analisi_di_portafoglio),
    path('index100',views.ultimate_analisi_di_portafoglio),
    path('index8',views.ultimate_analisi_di_portafoglio_2),


    path('index4', views.analisi_opzioni_vendute_comprate),
    path('index23', views.analisi_operazioni), 
    path('index25', views.analisi_operazioni_di_un_determinato_mese),
    path('index26', views.analisi_opzioni_con_il_minore_Theta),

    path('index22', views.analisi_dei_movimenti_anno),
    path('index39', views.analisi_dei_movimenti_anno_2),
    path('index41', views.analisi_dei_movimenti_anno_3),
    path('index30', views.analisi_delle_perdite),
    path('index31', views.visualizza_tutte_le_opzioni_long),
    path('index32', views.analisi_opzioni_con_il_maggiore_gamma),
    path('index33', views.analisi_opzioni_con_il_maggiore_vega),
    path('index35', views.test_importazione),
    path('index36', views.analisi_di_una_determinata_posizione),
    path('index42', views.analisi_operazioni_vendute_comprate),
    path('index43', views.analisi_posizioni_da_rollare_prossima_scadenza),
    
    
]