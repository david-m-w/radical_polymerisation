import random as r
from collections import Counter
import matplotlib
print(f"Current backend: {matplotlib.get_backend()}")
matplotlib.use('TgAgg')
import matplotlib.pyplot as plt

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


ethen_start_anzahl = 10000
ethen_anzahl = ethen_start_anzahl
radikale_start_anzahl = 100         #sollte gerade sein, damit am ende kein radikalübrig bleibt, das kein anderen radikal findet. dies sollte kein grösseres problem sein, aber es Könnte konsequenzen haben, wenn dadurche meherere ethen moleköle an diesen radikal in der liste "offene_radikale" kleben könnten, und so aus dem system kommen
offene_radikale = ["R"] * radikale_start_anzahl
polyporpen_molekuele = []

#warschienlichkeit, dass ein radikal mit einem ethenmolekül reagiert
ethen_reaktions_warscheinlichkeit = 1
#warschienlichkeit, dass ein radikal mit einem anderen radikal reagiert
radikal_reaktions_warscheinlichkeit = 1





def alle_radikale_gleichzeitig():
    global ethen_anzahl, polyporpen_molekuele, offene_radikale, ethen_reaktions_warscheinlichkeit, radikal_reaktions_warscheinlichkeit
    """ 
    in diesem versuch soll jede "generation" jedes offene radikal oder kette um 1 wachsen oder geschlossen werden
    """
    while len(offene_radikale) > 0:
        #print(f"radikale: {len(offene_radikale)}")
        #print(f"ethen: {ethen_anzahl}")
        #print()
        
        #liste welche einträge nachher gelösht werden mussen, da ich während der schleife nicht die liste modifizieren will
        deleted_entrys = [0] * len(offene_radikale)
        for i in range(len(offene_radikale)):
            if deleted_entrys[i]:
                continue
            
            #entscheiden ob dises radikal mit einem anderen radikal reagiert oder mit einem ethen:
            if (
                r.randint(1, int(ethen_anzahl*ethen_reaktions_warscheinlichkeit + len(offene_radikale)*radikal_reaktions_warscheinlichkeit))
                <
                ethen_anzahl*ethen_reaktions_warscheinlichkeit
            ):
                #da alle ethenmoleküle  gleich sind, kann ich irgeneins nehemen
                offene_radikale[i] += "CC"
                ethen_anzahl -= 1
            else:
                #hier muss ich aber entscheidne welches radikal:
                #ich muss aber auch darauf achten, dass ich nicht ein radikln nehme, dass schon vorher "aufgebraucht wurde", also das schon zu einem ganzen polypropen reagiert it und kein fries elektron mehr hat, aber immerniohc in dieser liste ist, weil ich es noch nicht gelöscht habe
                deleted_entrys[i] = 1
                
                radikal_partner = r.randint(0, len(offene_radikale)-1)
                while deleted_entrys[radikal_partner]:
                    radikal_partner = r.randint(0, len(offene_radikale)-1)
                
                deleted_entrys[radikal_partner] = 1
                polyporpen_molekuele.append(offene_radikale[i] + offene_radikale[radikal_partner][::-1])
        
        i = 0
        while i < len(deleted_entrys):
            if deleted_entrys[i]:
                offene_radikale.pop(i)
                deleted_entrys.pop(i)
                continue
            
            i += 1

def einzeln_eins_nach_dem_anderen():
    global ethen_anzahl, polyporpen_molekuele, offene_radikale, ethen_reaktions_warscheinlichkeit, radikal_reaktions_warscheinlichkeit
    """
    hier wird immer ein einzelnes radikal ausgewähtl und es reagiert direkt mit etwa, und dan ein anderes, und so weiter
    es wird nicht jedes radikal jede iteration gezwungen, zu reagieren
    """
    
    while len(offene_radikale) > 0:
        
        #ein zufälliges radikal auswählen
        i = r.randint(0, len(offene_radikale)-1)
        
        #entscheiden ob dises radikal mit einem anderen radikal reagiert oder mit einem ethen:
        if (
            r.randint(1, int(ethen_anzahl*ethen_reaktions_warscheinlichkeit + len(offene_radikale)*radikal_reaktions_warscheinlichkeit))
            <
            ethen_anzahl*ethen_reaktions_warscheinlichkeit
        ):
            #da alle ethenmoleküle  gleich sind, kann ich irgeneins nehemen
            offene_radikale[i] += "CC"
            ethen_anzahl -= 1
        else:
            #hier muss ich aber entscheidne welches radikal:
            #ich muss aber auch darauf achten, dass ich nicht ein radikal nehme, dass das selbe ist was ich gerade habe
            radikal_partner = r.randint(0, len(offene_radikale)-1)
            while radikal_partner == i:
                radikal_partner = r.randint(0, len(offene_radikale)-1)
            
            polyporpen_molekuele.append(offene_radikale[i] + offene_radikale[radikal_partner][::-1])
            if (i > radikal_partner):
                offene_radikale.pop(i)
                offene_radikale.pop(radikal_partner)
            elif(i < radikal_partner):
                offene_radikale.pop(radikal_partner)
                offene_radikale.pop(i)
            else:
                print("das sollte nicht passieren, die sollten nie gleich sein")
                break


def passen_alle_elemente():
    global polyporpen_molekuele, ethen_start_anzahl, radikale_start_anzahl, ethen_anzahl
    """
    hier wird überprüft, dass keine elemente (c oder r) zu viel existieren oder zuwenige. einfach um zu überprüfen, dass es keine bugs gibt
    
    true = keine fehler
    false = feheler
    """
    
    #die jetziege anzahl an ethenmolekühlen, die noch da sind
    kohlenstoff_atome =  2 * ethen_anzahl
    radikal_reste = 0
    
    for polypropen in polyporpen_molekuele:
        for atom in polypropen:
            if atom == "C":
                kohlenstoff_atome += 1
            elif atom == "R":
                radikal_reste += 1
            else:
                print(f"ein atom wurde gefunden, dass nicht r oder c ist: {atom}")
    
    
    if(kohlenstoff_atome != 2 * ethen_start_anzahl):
        print("a")
        return False
    if(radikal_reste != radikale_start_anzahl):
        print("b")
        return False
    
    return True


def laengen_analisyeren():
    global polyporpen_molekuele, ethen_start_anzahl, radikale_start_anzahl
    """
    hier werden die längen gezählt und ananlisiert, uns visuell dargestellt
    """
    
    laengen = map(len, polyporpen_molekuele)
    laengen_counts = dict(Counter(laengen))
    laengen_counts_keys = list(laengen_counts.keys())
    laengen_counts_values = [laengen_counts[key] for key in laengen_counts_keys]
    
    print(laengen_counts_keys)
    print(laengen_counts_values)
    
    plt.plot(laengen_counts_keys, laengen_counts_values)
    plt.show()


einzeln_eins_nach_dem_anderen()

if not passen_alle_elemente():
    raise Exception

laengen_analisyeren()

raise "wenn die diagramme nicht klar genug sind, könnte man die simualation ofters machen und den durschschnitt nehmen"