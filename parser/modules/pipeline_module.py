from owlready2 import *
import subprocess
from modules.module import *


def get_class(onto, name):
    """
    is a function that get the class object
    of the ontology given an name in string
    """
    results = onto.search(iri="*"+name)
    if len(results) == 0:
        return None
    else:
        return results[0]


def docx_to_html(name):
    """
    prend le fichier entré en docx
    puis le transforme en html
    """
    new_name = change_extension(name, "html")

    # conversion en html
    # TODO uncomment when everything is okay ()
    # because this conversion is taking a bit of time:
    # subprocess.run(["pandoc", name, "-o", new_name])

    return new_name


def html_to_triple(file_name):
    text = open(file_name, "r").readlines()
    # text = ["<p><em>Passeiry (CH, ct. Genève, com. Chancy)</em>, <em>Passeyrier</em>, 167</p>"]

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
            if ignor is False and not containsH5(line):
                res = parser.parse(line)
                if res is not None:
                    tab.append(createTriplet(res))
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


def get_ontology_from_file(path):
    # on ouvre l'ontologie
    onto = get_ontology("file://"+path).load()
    return onto


def get_classes(onto):
    # on y extrait les classes
    classes = list(onto.classes())
    # on crée les classes
    Classes = {
            "Nom": classes[24],
            "Localisation": classes[29],
            "Page": classes[30],
            "Canton": classes[4],
            "Commune": classes[4],
            "Pays": classes[31],
            "Departement": classes[11]
            }
    return Classes


def define_properties(onto, Classes):
    # Définition des propriétés
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


def create_table_of_type(tab):
    # création de la table des types
    tab_type = []
    for ligne in tab:
        for triplet in ligne:
            if triplet[1] == "type":
                tab_type.append(triplet)
    return tab

def create_instance_and_relation(tab,Classes,tab_type):
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
                if Any is not None:
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


def triple_to_owl(tab):
    """
    une fonction qui va transformer le contenu html_to_triple
    en structure dans un premier temps puis crée des triplets
    """
    onto = get_ontology("ontology_v2.owl")
    Classes = get_classes(onto)
    define_properties(onto, Classes)
    tab_type = create_table_of_type(tab)
    create_instance_and_relation(tab, Classes, tab_type)
    onto.save(file="final.owl", format="rdfxml")


