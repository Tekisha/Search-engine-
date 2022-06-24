

from file_parser import Parser
import os
import os.path
from trie import Trie
from sorter import quick_sort
from graph import Graph
import re

from kmp import KMPSearch




def recnik_to_lista(recnik):
    lista = []
    for key in recnik.keys():
        lista.append((key,recnik[key]))
    
    return lista

def print_rezultat(lista,granica,tekst):
    brojac=1

    if granica==-1:
        granica=8
        
    for i in lista:
        if brojac>granica:
            break
        print(i[0]+" ------> "+str(i[1])+"\n")
        if brojac == 1:
            print("Dio teksta:" )
            print(" ".join(tekst))

        brojac+=1







def zajednicki_recnik_rezultata(main_words_info):
    glavni_recnik = {}

    for lista in main_words_info:
        for triple in lista:
            recnik = triple[1]
            for key in recnik.keys():
                if key in glavni_recnik.keys():
                    glavni_recnik[key]= glavni_recnik[key]+recnik[key]
                else:
                    glavni_recnik[key]=recnik[key]
            
    
    return glavni_recnik

def AND_zajednicki_recnik_rezultata(main_words_info):
    word1_d = main_words_info[0][0][1]
    word1_d_keys = word1_d.keys()

    word2_d = main_words_info[1][0][1]
    word2_d_keys = word2_d.keys()

    glavni_recnik={}

    for key in word1_d_keys:
        if key in word2_d_keys:
            glavni_recnik[key]=word1_d[key]+word2_d[key]
    
    return glavni_recnik

def NOT_zajednicki_recnik_rezultata(main_words_info):
    word1_d = main_words_info[0][0][1]
    word1_d_keys = word1_d.keys()

    word2_d = main_words_info[1][0][1]
    word2_d_keys = word2_d.keys()

    glavni_recnik={}

    for key in word1_d_keys:
        if key not in word2_d_keys:
            glavni_recnik[key]=word1_d[key]
    
    return glavni_recnik

def OR_zajednicki_recnik_rezultata(main_words_info):
    glavni_recnik = {}

    for lista in main_words_info:
        recnik = lista[0][1]
        for key in recnik.keys():
            if key in glavni_recnik.keys():
                glavni_recnik[key]= glavni_recnik[key]+recnik[key]
            else:
                glavni_recnik[key] = recnik[key]
    
    return glavni_recnik

def WORD_zajednicki_recnik_rezultata(main_words_info):
    return main_words_info[0][0][1]

def FRAZA_zajednicki_recnik_rezultata(main_words_info):
    common_keys = set(main_words_info[0][0][1])

    glavni_recnik = {}

    for lista in main_words_info:  #nalazimo presjek svih fajlova koji sadrze sve rijeci fraze
        recnik = set(lista[0][1])
        common_keys = common_keys & recnik
    
    common_keys = list(common_keys)
    for lista in main_words_info: #racunamo ukupan broj ponavljanja rijeci
        recnik = lista[0][1]
        for key in common_keys:
            if key in glavni_recnik.keys():
                glavni_recnik[key]+= recnik[key]
            else:
                glavni_recnik[key] = recnik[key]
    
    return glavni_recnik









def sadrzi_html(directory,postoji):
    for filename in os.listdir(directory):
        f=os.path.join(directory, filename)
        if os.path.isfile(f) and os.path.splitext(f)[1]==".html":
            postoji = True
        elif (os.path.isdir(f)):
            postoji = sadrzi_html(f,postoji)
    return postoji

def prolazak_kroz_direktorijum(directory,parser,trie,graf): #kreira trie i graph

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f) and os.path.splitext(f)[1]==".html":


            lista_link, lista_reci = parser.parse(f)

            recnik_parsiranih_stranica[f]=[lista_reci,lista_link]
            for rec in lista_reci:
                trie.insert(rec.lower(),f)  #kreira trie
            
            for link in lista_link:
                graf.insert_edge(f,link)


        elif (os.path.isdir(f)):
            prolazak_kroz_direktorijum(f,parser,trie,graf)


def rank_pages(recnik,graf,main_word_info):
    ranked_recnik = {}


    for filename in recnik:
        rank = 0
        broj_reci_stranica = recnik[filename]
        broj_ulaznih_grana = graf.degree_vertex(filename,False)
        lista_susjeda = graf.get_neighbours(filename,False)
        for susjed in lista_susjeda:
            broj_reci_sused=0
            for lista in main_word_info:
                for triple in lista:
                    if susjed in triple[1].keys():
                        broj_reci_sused += triple[1][susjed]
            rank+=0.5*broj_reci_sused
        ranked_recnik[filename] = broj_reci_stranica + 8*broj_ulaznih_grana+rank
            


        
    
    return ranked_recnik

def izvuci_tekst(filename,reci,parser):
    
    lista_reci = recnik_parsiranih_stranica[filename][0]
    tekst = []

    for i in range(len(lista_reci)):
        lista_reci[i] = lista_reci[i].lower()

    for rec in reci:
        if rec.lower() in lista_reci:
            index = lista_reci.index(rec.lower())

            tekst.append("\"")
            
            for i in range(5,1,-1):
                try:
                    if((index-i)>=0):
                        tekst.append(lista_reci[index-i])
                except:
                    break

            tekst.append("\033[1m" +rec+"\033[0m")

            for i in range(1,5):
                try:
                    if((index+i)<len(lista_reci)):
                        tekst.append(lista_reci[index+i])
                except:
                    break
            
            tekst.append("\"\n")
        else:
            for tekst_rec in lista_reci:
                if tekst_rec.startswith(rec.lower()):
                    index = lista_reci.index(tekst_rec)

                    tekst.append("\"")
                    
                    for i in range(5,1,-1):
                        try:
                            if((index-i)>=0):
                                tekst.append(lista_reci[index-i])
                        except:
                            break

                    tekst.append("\033[1m" +tekst_rec+"\033[0m")

                    for i in range(1,5):
                        try:
                            if((index+i)<len(lista_reci)):
                                tekst.append(lista_reci[index+i])
                        except:
                            break
                    
                    tekst.append("\"\n")
                    break

        
    return tekst

def izvuci_tekst_fraza(lista_stranica,reci,parser,brojac):
    s=""

    lista_stranica_fraza=[]
    pronadjena_fraza = False

    for stranica in lista_stranica:
        if brojac>0:
            lista_reci = recnik_parsiranih_stranica[stranica[0]][0]

            for i in range(len(lista_reci)):
                lista_reci[i] = lista_reci[i].lower()
            
            tekst_reci = " ".join(lista_reci)
            tekst_fraza = " ".join(reci)

            index = KMPSearch(tekst_fraza,tekst_reci)

            if index != -1 and not pronadjena_fraza:
                pronadjena_fraza=True
                s="\""
                for i in range (40,0,-1):
                    if (index-i)>=0:
                        s=s+tekst_reci[index-i]
                    else:
                        break
                
                s= s + "\033[1m" +tekst_reci[index:index+len(tekst_fraza)]+"\033[0m"

                for i in range(len(tekst_fraza),40):
                    if (index+i)<len(tekst_reci):
                        s = s + tekst_reci[index+i]
                    else:
                        break

                s=s+"\"\n"

                lista_stranica_fraza.append(stranica)
            elif index!= -1:
                lista_stranica_fraza.append(stranica)
                brojac-=1
        else:
            break
    return [s],lista_stranica_fraza



    
    
           




def pretraga(trie,graf,parser):
    broj_prikaza=5
    while True :
        unos = input("Unesite trazeni pojam: ")
        if unos!="" and not unos.isspace():
            unos=unos.strip()
            break
        else:
            print("Uneli ste prazan string!")
    
    print("\n")
    
    while True:
        odgovor = input("Da li zelite da odredite max broj stranica u pretrazi?[da/ne]")
        if odgovor in ["DA","da"]:
            while True:
                try:
                    broj_prikaza = int(input("Unesite max broj prikaza stranica: "))
                    if broj_prikaza>0:
                        break
                    else:
                        print("Unos mora biti citav broj i veci od nule!")
                except:
                    print("Unos mora biti citav broj i veci od nule!")
            break
        elif odgovor in ["NE","ne"]:
            break
        else:
            print("Morate uneti DA ili NE!")
    
    logicki_operator_AND = False
    logicki_operator_OR = False
    logicki_operator_NOT = False
    logicki_operator_WORD = False
    osnovni_oblik = False
    fraza=False

    unos = re.sub(' +', ' ', unos)
    reci_pretrage = unos.split(" ")
    
    if unos[0] in ["\'","\""] and unos[-1] in ["\'","\""]:
        fraza = True
        osnovni_oblik = True
        reci_pretrage = unos[1:-1].split(" ")
        if unos[1:-1]=="" or unos[1:-1].isspace():
            print("Fraza mora da ima neke karaktere!")
            print("\n")
            return

    else:
        if len(reci_pretrage)==3: #provera da li se koristi logicki operator
            if "AND" == reci_pretrage[1]: 
                #TO-DO AND operator
                reci_pretrage.pop(1)
                logicki_operator_AND=True
                osnovni_oblik = True

            elif "OR" == reci_pretrage[1]:
                #TO-DO OR operator
                reci_pretrage.pop(1)
                logicki_operator_OR=True
                osnovni_oblik = True

            elif "NOT" == reci_pretrage[1]:
                #TO-DO NOT operator
                reci_pretrage.pop(1)
                logicki_operator_NOT=True
                osnovni_oblik = True

        elif len(reci_pretrage)==2: #provera da li se koristi operator WORD koji onda prikazuje samo rezultate u kojima se nalazi tacno ta rijec(inace moze da bude prefiks neke rijeci)
            if "WORD" == reci_pretrage[0]:
                reci_pretrage.pop(0)
                logicki_operator_WORD=True
                osnovni_oblik = True


    main_words_info=[] #lista sadrzi listu tuplse(rec,recnik[filename]=broj ponavljanja reci u fajlu, broj pominjanja rijeci ukupno)


    #vraca listu[glavna rijec,recnik [filename]=broj ponavljanja, broj pominjanja rijeci]
    # listu tuplsa (slicna rijec,recnik [filename]=broj ponavljanja,broj pominjanja rijeci)
    for rec in reci_pretrage:
        main_words_info.append(trie.query(rec,osnovni_oblik)) 


    print("\n")
    print("\n")

    if logicki_operator_AND:
        recnik_stranica = AND_zajednicki_recnik_rezultata(main_words_info)
    elif logicki_operator_NOT:
        recnik_stranica = NOT_zajednicki_recnik_rezultata(main_words_info)
        reci_pretrage.pop(1)
    elif logicki_operator_OR:
        recnik_stranica = OR_zajednicki_recnik_rezultata(main_words_info)
    elif logicki_operator_WORD:
        recnik_stranica = WORD_zajednicki_recnik_rezultata(main_words_info)
    elif fraza:
        recnik_stranica = FRAZA_zajednicki_recnik_rezultata(main_words_info)
    else:
        recnik_stranica = zajednicki_recnik_rezultata(main_words_info)



    

    recnik_stranica = rank_pages(recnik_stranica,graf,main_words_info)
    lista_stranica = recnik_to_lista(recnik_stranica)
    lista_stranica=quick_sort(lista_stranica)

    if len(lista_stranica)>0 and not fraza:
        tekst = izvuci_tekst(lista_stranica[0][0],reci_pretrage,parser)

    elif len(lista_stranica)>0 and fraza:
        tekst,lista_stranica = izvuci_tekst_fraza(lista_stranica,reci_pretrage,parser,broj_prikaza)
    else:
        tekst=[]
    
    print("Rezultati pretrage "+ unos +": " + str(len(lista_stranica))+" stranica")
    print_rezultat(lista_stranica,broj_prikaza,tekst)


   
        




    
def main():
    while True:

        while True:
            directory = input("Unesite putanju do direktorijuma: ")
            if os.path.isdir(directory):
                postoji_html = sadrzi_html(directory,False)
                if postoji_html:
                    break
                else:
                    print("U ovom direktorijumu ne postoji html dokument!")
                    print("\n")
            else:
                print("Niste uneli validnu putanju do direktorijuma.")
                print("\n")
            
        parser = Parser()
        trie = Trie()
        graf = Graph()

        print("Ucitavanje direktorijuma...")
        print("\n")
        prolazak_kroz_direktorijum(directory,parser,trie,graf)
        print("Ucitavanje uspjesno zavrseno!")
        print("\n")

        #print(graf.edge_count())
        #print(graf.vertex_count())

       

        pretraga(trie,graf,parser)
        

        while True:
            odgovor = input("Da li zelite promeniti direktorijum[da/ne]? ")
            if odgovor in ["DA","da"]:
                break
            elif odgovor in ["NE","ne"]:
                pretraga(trie,graf,parser)
            else:
                print("Morate uneti DA ili NE!")


recnik_parsiranih_stranica = {}   
            


if __name__=="__main__":
    main()