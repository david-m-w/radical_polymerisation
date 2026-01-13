from multiprocessing import Pool
import time as t

import single


class settings_setup:
    def __init__(self, ethen_start_anzahl, radikale_start_anzahl, bins, instances_amount):
        self.ethen_anzahl = None
        self.ethen_start_anzahl = ethen_start_anzahl
        self.radikale_start_anzahl = radikale_start_anzahl
        self.bins = bins
        self.instances_amount = instances_amount
    
    def ethen_anzahl_eintragen(self, ethen_anzahl):
        self.ethen_anzahl = ethen_anzahl

def main(number_of_simulations):
    with Pool(number_of_simulations) as p:
        sett = settings_setup(10000000, 1000, 100, number_of_simulations)
        subfolder = f"multi_{int(t.time())}"
        alle_zusammen = True
        einzeln = False
        data_for_the_processes = [(alle_zusammen, einzeln, False, True, True, subfolder, sett.ethen_start_anzahl, sett.radikale_start_anzahl, sett.bins)] * number_of_simulations
        
        results_mit_ethen = p.starmap(single.main, data_for_the_processes)
        
        #separate the results_mit_ethen list into smaller lists that all just contain one thing each
        results = [result_mit_ethen[0] for result_mit_ethen in results_mit_ethen]
        ethen_uebrig_anzahlen = [result_mit_ethen[1] for result_mit_ethen in results_mit_ethen]
        ethen_uebrig_gesamt = sum(ethen_uebrig_anzahlen)
        results_keys = [result[0] for result in results]
        results_values = [result[1] for result in results]
        results_keys_concatenated = [key for keys in results_keys for key in keys]
        results_values_concatenated = [value for values in results_values for value in values]
        
        sett.ethen_anzahl_eintragen(ethen_uebrig_gesamt)
        
        single.render_results(sett, results_keys_concatenated, results_values_concatenated, True, True, False, f"{subfolder}/all_added", True, alle_zusammen, einzeln)



if __name__ == "__main__":
    main(30)