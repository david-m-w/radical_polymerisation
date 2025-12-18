import random as r


"""
viel ethen und ein paar radikale.
sie reagieren zu polypropen

radikale sind hier alles was offene ketten sind. ich weiss nicht ob die bennenung daher falsch ist, aber soweit ich weiss, macht es hier keinen unterschied ob es eine schon vorhandene kette ist oder ein einfaches einzelnes originales radikal
"""


"""
darstellungen:
"R" ein radikal
"RCCR" ein ethen was mit zwei radikalen reagiert hat, also die kleinstmögliche form von polypropen
"RCC[...]CCR" ein längeres polypropen
"""


ethen_start_anzahl = 1000000
ethen_anzahl = ethen_start_anzahl
radikale_start_anzahl = 100
offene_radikale = ["R"] * radikale_start_anzahl
polyporpen_moleküle = []

#warschienlichkeit, dass ein radikal mit einem ethenmolekül reagiert
ethen_reaktions_warscheinlichkeit = 1
#warschienlichkeit, dass ein radikal mit einem anderen radikal reagiert
radikal_reaktions_warscheinlichkeit = 1





def alle_radikale_gleichzeitig():
    global ethen_anzahl, polyporpen_moleküle, offene_radikale, ethen_reaktions_warscheinlichkeit, radikal_reaktions_warscheinlichkeit
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
                polyporpen_moleküle.append(offene_radikale[i] + offene_radikale[radikal_partner][::-1])
        
        i = 0
        while i < len(deleted_entrys):
            if deleted_entrys[i]:
                offene_radikale.pop(i)
                deleted_entrys.pop(i)
                continue
            
            i += 1

def einzeln_eins_nach_dem_anderen():
    global ethen_anzahl, polyporpen_moleküle, offene_radikale, ethen_reaktions_warscheinlichkeit, radikal_reaktions_warscheinlichkeit
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
            
            polyporpen_moleküle.append(offene_radikale[i] + offene_radikale[radikal_partner][::-1])
            if (i > radikal_partner):
                offene_radikale.pop(i)
                offene_radikale.pop(radikal_partner)
            elif(i < radikal_partner):
                offene_radikale.pop(radikal_partner)
                offene_radikale.pop(i)
            else:
                print("das sollte nicht passieren, die sollten nie gleich sein")
                break


einzeln_eins_nach_dem_anderen()

raise("ich muss moch überprüfen, ob es bugs gibt, indem ich gucke, ob am ende von den originalen radikalen, also die \"R\" buchstaben, und de ethene, (die jeweils als \"CC\" representiert sein sollten) welche enstanden oder zerstort dorden sind, was ja eingentlich nicht passieren kann")


