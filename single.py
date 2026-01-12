import random as r
from collections import Counter
import matplotlib
#print(f"Current backend: {matplotlib.get_backend()}")
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time as t
import os

"""
viel ethen und ein paar radikale.
sie reagieren zu polypropen

radikale sind hier alles was offene ketten sind. ich weiss nicht ob die bennenung daher falsch ist, aber soweit ich weiss, macht es hier keinen unterschied ob es eine schon vorhandene kette ist oder ein einfaches einzelnes originales radikal
ausserdeme bennene ich radikale manchmal auch als atome, was nicht immer (meistens nicht) stimmt, aber sie agieren wie atome, also ist es mir egal
"""


"""
darstellungen:
"R" ein radikal
"RCCR" ein ethen was mit zwei radikalen reagiert hat, also die kleinstmögliche form von polypropen
"RCC[...]CCR" ein längeres polypropen
"""


class settings:
    def __init__(self, ethen_start_anzahl, radikale_start_anzahl, bins):
        self.seed = r.randint(0, 2**32)
        r.seed(self.seed)

        self.bins = bins

        self.ethen_start_anzahl = ethen_start_anzahl
        self.ethen_anzahl = self.ethen_start_anzahl
        self.radikale_start_anzahl = radikale_start_anzahl         #sollte gerade sein, damit am ende kein radikalübrig bleibt, das kein anderen radikal findet. dies sollte kein grösseres problem sein, aber es Könnte konsequenzen haben, wenn dadurche meherere ethen moleköle an diesen radikal in der liste "offene_radikale" kleben könnten, und so aus dem system kommen
        self.offene_radikale = ["R"] * self.radikale_start_anzahl
        self.polyporpen_molekuele = []

        #warschienlichkeit, dass ein radikal mit einem ethenmolekül reagiert
        self.ethen_reaktions_warscheinlichkeit = 1
        #warschienlichkeit, dass ein radikal mit einem anderen radikal reagiert
        self.radikal_reaktions_warscheinlichkeit = 1




def alle_radikale_gleichzeitig(sett):
    """ 
    in diesem versuch soll jede "generation" jedes offene radikal oder kette um 1 wachsen oder geschlossen werden
    """
    while len(sett.offene_radikale) > 0:
        #print(f"radikale: {len(offene_radikale)}")
        #print(f"ethen: {ethen_anzahl}")
        #print()
        
        #liste welche einträge nachher gelösht werden mussen, da ich während der schleife nicht die liste modifizieren will
        deleted_entrys = [0] * len(sett.offene_radikale)
        for i in range(len(sett.offene_radikale)):
            if deleted_entrys[i]:
                continue
            
            #entscheiden ob dises radikal mit einem anderen radikal reagiert oder mit einem ethen:
            if (
                r.randint(1, int(sett.ethen_anzahl*sett.ethen_reaktions_warscheinlichkeit + len(sett.offene_radikale)*sett.radikal_reaktions_warscheinlichkeit))
                <
                sett.ethen_anzahl*sett.ethen_reaktions_warscheinlichkeit
            ):
                #da alle ethenmoleküle  gleich sind, kann ich irgeneins nehemen
                sett.offene_radikale[i] += "CC"
                sett.ethen_anzahl -= 1
            else:
                #hier muss ich aber entscheidne welches radikal:
                #ich muss aber auch darauf achten, dass ich nicht ein radikln nehme, dass schon vorher "aufgebraucht wurde", also das schon zu einem ganzen polypropen reagiert it und kein fries elektron mehr hat, aber immerniohc in dieser liste ist, weil ich es noch nicht gelöscht habe
                deleted_entrys[i] = 1
                
                radikal_partner = r.randint(0, len(sett.offene_radikale)-1)
                while deleted_entrys[radikal_partner]:
                    radikal_partner = r.randint(0, len(sett.offene_radikale)-1)
                
                deleted_entrys[radikal_partner] = 1
                sett.polyporpen_molekuele.append(sett.offene_radikale[i] + sett.offene_radikale[radikal_partner][::-1])
        
        i = 0
        while i < len(deleted_entrys):
            if deleted_entrys[i]:
                sett.offene_radikale.pop(i)
                deleted_entrys.pop(i)
                continue
            
            i += 1

def einzeln_eins_nach_dem_anderen(sett):
    """
    hier wird immer ein einzelnes radikal ausgewähtl und es reagiert direkt mit etwa, und dan ein anderes, und so weiter
    es wird nicht jedes radikal jede iteration gezwungen, zu reagieren
    """
    
    while len(sett.offene_radikale) > 0:
        
        #ein zufälliges radikal auswählen
        i = r.randint(0, len(sett.offene_radikale)-1)
        
        #entscheiden ob dises radikal mit einem anderen radikal reagiert oder mit einem ethen:
        if (
            r.randint(1, int(sett.ethen_anzahl*sett.ethen_reaktions_warscheinlichkeit + len(sett.offene_radikale)*sett.radikal_reaktions_warscheinlichkeit))
            <
            sett.ethen_anzahl*sett.ethen_reaktions_warscheinlichkeit
        ):
            #da alle ethenmoleküle  gleich sind, kann ich irgeneins nehemen
            sett.offene_radikale[i] += "CC"
            sett.ethen_anzahl -= 1
        else:
            #hier muss ich aber entscheidne welches radikal:
            #ich muss aber auch darauf achten, dass ich nicht ein radikal nehme, dass das selbe ist was ich gerade habe
            radikal_partner = r.randint(0, len(sett.offene_radikale)-1)
            while radikal_partner == i:
                radikal_partner = r.randint(0, len(sett.offene_radikale)-1)
            
            sett.polyporpen_molekuele.append(sett.offene_radikale[i] + sett.offene_radikale[radikal_partner][::-1])
            if (i > radikal_partner):
                sett.offene_radikale.pop(i)
                sett.offene_radikale.pop(radikal_partner)
            elif(i < radikal_partner):
                sett.offene_radikale.pop(radikal_partner)
                sett.offene_radikale.pop(i)
            else:
                print("das sollte nicht passieren, die sollten nie gleich sein")
                break


def passen_alle_elemente(sett):
    """
    hier wird überprüft, dass keine elemente (c oder r) zu viel existieren oder zuwenige. einfach um zu überprüfen, dass es keine bugs gibt
    
    true = keine fehler
    false = feheler
    """
    
    #die jetziege anzahl an ethenmolekühlen, die noch da sind
    kohlenstoff_atome =  2 * sett.ethen_anzahl
    radikal_reste = 0
    
    for polypropen in sett.polyporpen_molekuele:
        for atom in polypropen:
            if atom == "C":
                kohlenstoff_atome += 1
            elif atom == "R":
                radikal_reste += 1
            else:
                print(f"ein atom wurde gefunden, dass nicht r oder c ist: {atom}")
    
    
    if(kohlenstoff_atome != 2 * sett.ethen_start_anzahl):
        print("a")
        return False
    if(radikal_reste != sett.radikale_start_anzahl):
        print("b")
        return False
    
    return True



def laengen_analisyeren(sett, print_results):
    """
    hier werden die längen gezählt und ananlisiert 
    """
    
    laengen = map(len, sett.polyporpen_molekuele)
    laengen_counts = dict(Counter(laengen))
    laengen_counts_keys = list(laengen_counts.keys())
    laengen_counts_values = [laengen_counts[key] for key in laengen_counts_keys]
    
    if print_results:
        print(laengen_counts_keys)
        print(laengen_counts_values)
    
    return (laengen_counts_keys, laengen_counts_values)

def durchschnitt_und_median_berechnen(keys, values):
    values_with_repetitions = []
    for i in range(len(keys)):
        for _ in range(keys[i]):
            values_with_repetitions.append(values[i])
    
    values_with_repetitions.sort()
    
    average = sum(values_with_repetitions) / len(values_with_repetitions)
    median = values_with_repetitions[int(len(values_with_repetitions) / 2)]

    return average, median

def render_results(sett, keys, values, display_results, save_results, return_results, subfolder, is_multi = False, alle_zusammen, einzeln):
    #set window size:
    fig = plt.figure(figsize=(20, 12))
    #set how many plots i want
    gs = gridspec.GridSpec(2, 1)
    
    ax_scatter = plt.subplot(gs[1:2, :2])
    ax_scatter.scatter(keys, values)
    ax_scatter.set(
        xlabel="länge der kette",
        ylabel="häufigkeit der länge",
    )

    durchsnchnitt, median = durchschnitt_und_median_berechnen(keys, values)

    if not is_multi:
        ax_scatter.set(
            title = f"""es it noch {sett.ethen_anzahl} ethen übrig, also {sett.ethen_anzahl/sett.ethen_start_anzahl * 100}%
            seed: {sett.seed}
            ethen start anzahl: {sett.ethen_start_anzahl}
            radikale start anzahl: {sett.radikale_start_anzahl}
            alle zusammen: {alle_zusammen}, einzeln: {einzeln}
            durchscnitt länge: {durchsnchnitt}, median länge: {median}"""
        )
    else:
        ax_scatter.set(
            title = f"""es it noch insgesammt {sett.ethen_anzahl} ethen übrig, also {sett.ethen_anzahl/(sett.ethen_start_anzahl * sett.instances_amount) * 100}%
            simulationen: {sett.instances_amount}
            ethen start anzahl pro simulation: {sett.ethen_start_anzahl}
            radikale start anzahl pro simularion: {sett.radikale_start_anzahl}
            alle zusammen: {alle_zusammen}, einzeln: {einzeln}
            durchscnitt länge: {durchsnchnitt}, median länge: {median}"""

        )
    

    ax_hist = plt.subplot(gs[0, :2],sharex=ax_scatter)
    ax_hist.hist(keys, bins = sett.bins)
    ax_hist.set(
        xlabel="länge der kette",
        ylabel="häufigkeit der länge"#,
        #title = f"es it noch {ethen_anzahl} übrig, also {ethen_anzahl/ethen_start_anzahl * 100}%\nseed: {seed}"
    )
    
    plt.tight_layout()
    
    if save_results:
        if not os.path.isdir(f"plot_saves/{subfolder}"):
            os.makedirs(f"plot_saves/{subfolder}")
        if not is_multi:
            plt.savefig(f"plot_saves/{subfolder}/image_{sett.seed}_{sett.ethen_start_anzahl}_{sett.radikale_start_anzahl}.svg", format="svg")
        else:
            plt.savefig(f"plot_saves/{subfolder}/image_{sett.ethen_start_anzahl}_{sett.radikale_start_anzahl}.svg", format="svg")
    if display_results:
        plt.show()
    if return_results:
        return (keys, values)
    else:
        return None


def main(alle_zusammen, einzeln, display_results, save_results, return_results, subfolder, ethen_start_anzahl, radikale_start_anzahl, bins):    
    sett = settings(ethen_start_anzahl, radikale_start_anzahl, bins)
    
    if alle_zusammen:
        alle_radikale_gleichzeitig(sett)
    if einzeln:
        einzeln_eins_nach_dem_anderen(sett)
    
    if not passen_alle_elemente(sett):
        print(f"error on seed: {sett.seed}")
        raise Exception
    
    laengen_counts_keys, laengen_counts_values = laengen_analisyeren(sett, False)
    
    res = render_results(sett, laengen_counts_keys, laengen_counts_values, display_results, save_results, return_results, subfolder, alle_zusammen, einzeln)
    
    if return_results:
        return res, sett.ethen_anzahl

if __name__ == "__main__":
    main(True, False, True, True, True, f"single_{int(t.time())}", 100000, 1000, 100)
#else:
    #main(True, False, False, True, True, f"multi_{int(t.time())}")