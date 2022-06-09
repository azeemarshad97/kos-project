import sys
import subprocess
from modules.module import *
from owlready2 import *

def docx_to_html():
    # prend le nom du fichier
    if len(sys.argv) == 1:
        name = "Index_1543.docx"
    else:
        name = sys.argv[1]
    newname = name[:-4]+"html"

    # conversion en html
    subprocess.run(["pandoc", name, "-o", newname])

    # conversion en triplets
    text = open(newname, "r").readlines()

def html_to_triple():
    # text = open("Index_1543.html", "r").readlines()
    text = ["<p><em>Passeiry (CH, ct. Genève, com. Chancy)</em>, <em>Passeyrier</em>, 167</p>"]

    # ignor = True
    ignor = False
    tab = []
    """
    Le fichier index contient du texte d'explication sur la structure de l'index
    Ce texte n'est pas intéressant vu qu'il ne peut pas être destructuré.
    On doit donc couper le texte du début.
    """
    for line in text:
        # premièrement, on ignore ce qu'il y a avant h5
        if containsH5(line):
            ignor = False
        else:
            if ignor == False and not containsH5(line):
                res = parser.parse(line)
                print(res)
                if res != None:
                    tab.append(createTriplet(res))
    print(tab)
    return tab

def getType(element, tab_type, Classes):
    for triplet in tab_type:
        if element == triplet[0]:
            if triplet[2] == "person":
                return Classes["Nom"](triplet[0].replace(" ( d ’ )",""))
            elif triplet[2] == "place":
                return Classes["Localisation"](triplet[0])
            elif triplet[2] == "page":
                return Classes["Page"](triplet[0].replace(" ", ""))
    return None

"""
0 ontology_v2.Armee
1 ontology_v2._Etatique
2 ontology_v2.Bourgeois
3 ontology_v2.GroupeSocial
4 ontology_v2.Canton
5 on tology_v2._Terre
6 ontology_v2.Clerge
7 ontology_v2._Occupation
8 ontology_v2.Commune
9 ontology_v2.Condamnation
10 onto logy_v2.Delit
11 ontology_v2.Departement
12 ontology_v2.District
13 ontology_v2.Ecrit
14 ontology_v2.Foritification
15 ontol ogy_v2._Edifice
16 ontology_v2.Honorable
17 ontology_v2.Hopital
18 ontology_v2.Imposition
19 ontology_v2._Finance
20 ontolog y_v2.Metier
21 ontology_v2.Monnaie
22 ontology_v2.Monsieur
23 ontology_v2.Noble
24 ontology_v2.Nom
25 ontology_v2._Personne
26 ontology_v2.Office
27 ontology_v2.Prenom
28 ontology_v2.Seigneur
29 ontology_v2._Localisation
30 ontology_v2._Page
31 ontol ogy_v2._Pays
32 ontology_v2._PointEau
"""

def triple_to_owl(tab):
    print(tab)
    # On va mettre les triplets dans l'ontologie
    path="owl/ontology_v2.owl"

    onto = get_ontology("file://"+path).load()

    classes = list(onto.classes())

    Classes = {"Nom" : classes[24], "Localisation" : classes[29], "Page" : classes[30], "Canton" : classes[4], "Commune" : classes[4], "Pays" : classes[31], "Departement" : classes[11]}

    # définition des propriétés
    with onto:
        class inPage(ObjectProperty):
            domain = [Classes["Nom"]]
            range = [Classes["Localisation"]]
        class inCanton(ObjectProperty):
            domain = [Classes["Localisation"]]
            range = [Classes["Canton"]]
        class inCommune(ObjectProperty):
            domain = [Classes["Localisation"]]
            range = [Classes["Commune"]]
        class inCountry(ObjectProperty):
            domain = [Classes["Localisation"]]
            range = [Classes["Pays"]]
        class inDepartement(ObjectProperty):
            domain = [Classes["Localisation"]]
            range = [Classes["Departement"]]
    # création de la table des types
    tab_type = [] 
    for ligne in tab:
        for triplet in ligne:
            if triplet[1] == "type":
                tab_type.append(triplet)
    # création des instances et des relations
    for ligne in tab:
        for triplet in ligne:
            if triplet[1] == "type":
                if triplet[2] == "person":
                    Classes["Nom"](triplet[0].replace(" ( d ’ )",""))
                elif triplet[2] == "place":
                    Classes["Localisation"](triplet[0])
                elif triplet[2] == "page":
                    Classes["Page"](triplet[0].replace(" ", ""))
            elif triplet[1] == "page":
                Any = getType(triplet[0], tab_type, Classes)
                page = Classes["Page"](triplet[2])
                if Any != None:
                    Any.inPage = [page]
            elif triplet[1] == "inCanton":
                loc = Classes["Localisation"](triplet[0])
                canton = Classes["Canton"](triplet[2])
                canton.inCanton = [loc]
            elif triplet[1] == "inCommune":
                loc = Classes["Localisation"](triplet[0])
                canton = Classes["Commune"](triplet[2])
                canton.inCommune = [loc]
            elif triplet[1] == "inCountry":
                loc = Classes["Localisation"](triplet[0])
                canton = Classes["Pays"](triplet[2])
                canton.inCountry = [loc]
            elif triplet[1] == "inDepartement":
                loc = Classes["Localisation"](triplet[0])
                canton = Classes["Departement"](triplet[2])
                canton.inDepartement = [loc]
    # enregistrement de l'ontologie
    onto.save(file = "final.owl", format = "rdfxml")

tab = html_to_triple()
triple_to_owl(tab)
