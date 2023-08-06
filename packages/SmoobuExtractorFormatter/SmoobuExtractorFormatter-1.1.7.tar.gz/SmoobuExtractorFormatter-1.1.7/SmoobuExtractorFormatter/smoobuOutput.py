import os
import pandas as pd
import numpy as np
import sys
import traceback

name_menage = "frais_menage"
name_taxe = "taxe_sejour"


SEJOUR_MOTS = ["Séjour", "Résidence", "Visite", "Escale", "Vacances", "Voyage","Tourisme"]
SEJOUR_WORDS = ["Stay", "Sojourn", "Visit", "Residence", "Stopover", "Vacation", "Trip",'Tourism']

SEJOUR = SEJOUR_MOTS + SEJOUR_WORDS


MENAGE_MOTS = ["ménage","nettoyage"]
MENAGE_WORDS = ["cleaning"]

MENAGE = MENAGE_MOTS + MENAGE_WORDS

TAB_INITIAL = {
	"type": "type",

	"created-at": "created-at",

	"modifiedAt": "modifiedAt",

	"channel": "channel",

	"guest-name": "guest-name",

	"firstname": "firstname",

	"lastname": "lastname",

	"email": "email",

	"phone": "phone",

	"adults": "adults",

	"children": "children",

	"check-in": "check-in",

	"check-out": "check-out",

	"price": "total-price",

	"guest-app-url": "guest-app-url",

	"is-blocked-booking": "is-blocked-booking",

	"guestId": "guest_id",

	"apartment_id": "apartment_id",

	"apartment_name": "apartment-name",

	"plateforme_id": "plateforme_id",

	"plateforme_name": "plateforme-name",

	"client": "client",

	"statut": "statut",

	"nuits": "nuits",

	"reservation-id": "reservation-id",

	"reservation-num": "reservation-num",

	"created_at": "created_at",

	"modified_at": "modified_at",
    
    'Taxe de séjour ( seulement si réservation via Booking.com ) <-> addon' : name_taxe,

	"basePrice": "basePrice",

	"Commission <-> commission": "commission",

	"frais de ménage <-> channelCustom": name_menage,

	"taxe de séjour <-> channelCustom": name_taxe,

	"Cleaning fee <-> cleaningFee": name_menage,

	"Airbnb Collected Tax <-> channelCustom": name_taxe,
    
    'Check Out 14H <-> addon' : 'addon',

	"TVA <-> channelCustom": "TVA",

	"frais de linge de lit <-> channelCustom": "frais_linge_lit",

	"Frais de nettoyage <-> cleaningFee": name_menage,

	"Taxe de séjour <-> addon": name_taxe,
 
	"[Sejournez à Troyes] Frais de gestion <-> addon": "frais_gestion", # à voir
    
    'Frais de gestion <-> addon' : "frais_gestion_2",

	"PASS_THROUGH_PET_FEE <-> channelCustom": "supp_animaux",

}





class SmoobuOutput:
    
    """
    Changes the format of the excel (or the json) given by the scrapping tool
    of the Smoobu application 
    
    :param file: the excel file or the json file to be changed
    :type file: str
    
    :param table: the table of the columns/keys to be changed
    :type table: dict

    """
    
    def __init__(self,file):
        self.file = file
        
        
    def format_allBookings(self,path_output = "./",table = TAB_INITIAL):
        
        def len_value(x):
            return len(x)

        def one_value(x):
            if len(x) == 1:
                return x[0]
            else:
                return x
        
        
        file_name,file_extension = os.path.splitext(self.file)
    

        if(file_extension == ".xlsx"):
            
            bookings = pd.read_excel(self.file)
            #bookings.rename(columns = table, inplace = True)
            
            columns = bookings.columns 
            dict = {}

            bookings.rename(columns = table, inplace = True)
            
            columns_exist = {}
            columns_notexist = []
            
            for name in table.keys():
                if name in columns :
                    columns_exist[name] = True
                else :
                    columns_exist[name] = False
                    columns_notexist.append(name)
            
            
            number_menage = bookings['frais_menage'].shape[0]
            number_sejour = bookings['taxe_sejour'].shape[0]
            
            
            
            
            # merging every columns into one : frais de menage
            
            bookings['frais_menage_'] = bookings['frais_menage'].apply(lambda x: [val for val in x if pd.notna(val)], axis=1)
            

            lens = bookings['frais_menage_'].apply(len_value)
            
            if lens[lens == 2].shape[0] == 0:
            
                del bookings['frais_menage']
                bookings['frais_menage_'] = bookings['frais_menage_'].apply(one_value)
                bookings['frais_menage_' ] = bookings['frais_menage_'].explode()
                
            else :
                del bookings['frais_menage_']
                
                
                
            # merging every columns into one : taxe de sejour

                bookings['taxe_sejour_'] = bookings['taxe_sejour'].apply(lambda x: [val for val in x if pd.notna(val)], axis=1)
                lens2 = bookings['taxe_sejour_'].apply(len_value)

                if lens2[lens2 == 2].shape[0] == 0:
                    del bookings['taxe_sejour']
                    bookings['taxe_sejour_'] = bookings['taxe_sejour_'].apply(one_value)
                    bookings['taxe_sejour_'] = bookings['taxe_sejour_'].explode()
                else:
                    del bookings['taxe_sejour_']

                # Sum of all the fees into the cleaning fee
                bookings['frais_menage_'] = bookings['frais_menage_'].fillna(0.0)

                frais_linge_serviettes = ['frais_linge_lit']
                bookings['frais_linge_serviettes'] = 0.0

                for frais in frais_linge_serviettes:
                    if frais in columns:
                        bookings['frais_linge_serviettes'] += bookings['frais'].fillna(0.0)

                try:
                    del bookings['frais_linge_lit']
                except:
                    pass
                try:
                    del bookings['supp_serviettes']
                    del bookings['supp_linen']
                except:
                    pass
                try:
                    del bookings['supp_animaux']  # not included in the price
                except:
                    pass
                try:
                    del bookings['addon']
                except:
                    pass

                # New column
                payé_voyageur_calculated = ['basePrice', 'frais_menage_', 'taxe_sejour_', 'frais_gestion', 'frais_linge_serviettes', 'frais_gestion_2']
                bookings['payé-voyageur_calculated'] = 0.0

                for frais in payé_voyageur_calculated:
                    if frais in columns:
                        bookings['payé-voyageur_calculated'] += bookings[frais].fillna(0.0)

                try:
                    bookings['delta'] = (abs(bookings['total-price'] - bookings['payé-voyageur_calculated']))
                    bookings = bookings.round(2)  # to avoid rounding errors
                    bookings['Added-Taxes'] = np.where(bookings['taxe_sejour_'] == bookings['delta'], True, False)
                    bookings['Equals-Prices'] = np.where(bookings['total-price'] == bookings['payé-voyageur_calculated'], True, False)

                    del bookings['delta']
                except KeyError as error:
                    _, _, tb = sys.exc_info()
                    line_number = traceback.extract_tb(tb)[-1][1]       
                    print(f"Error occurred on line {line_number}: {error}")
                    print("\nThere is a problem with the columns: total-price and payé-voyageur_calculated\n")

            # newly formated data to excel
            bookings = bookings.round(2)
            bookings.to_excel( path_output +"/Smoobu_"+file_name.split("/")[-1] + ".xlsx", index = False)
            
            print("\nSmoobu file created \n")
            for file in os.listdir():
                if file == "Smoobu_"+file_name.split("/")[-1] + ".xlsx":
                    file_path = os.path.join(os.getcwd(), file)
                    print("File path:", file_path)
                    break
            return bookings
    
    
        else:
            print("Le fichier n'est pas au format excel")
            return None
        







    
        
        