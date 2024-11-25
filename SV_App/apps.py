from django.apps import AppConfig
import os

class SvAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'SV_App'
    def ready(self):
        from . import DBMS
        from . import hdfc
        from . import MRF
        from . import Rel
        from . import tata
        from . import jindal
        DBMS.store_data("TATAMOTORS.NS","TATAMOTORS")
        DBMS.store_data("MRF.NS","MRF")
        DBMS.store_data("RELIANCE.BO","RELIANCE")
        DBMS.store_data("HDFCBANK.NS","HDFCBANK")
        DBMS.store_data("JINDALSTEL.NS","JINDALSTEL")
        print("Done Updating Database")
        hdfc.pred_hdfc()
        MRF.pred_MRF()
        Rel.pred_Rel()
        tata.pred_tata()
        jindal.pred_jindal()
        print("Predictions Stored")