from owlready2 import *
import subprocess
from modules.module import *


def corrector(line):
    """correct incosistencies from the html file"""
    line = line.replace(" ", " ")
    line = line.replace(",</span>", "</span>,")
    line = line.replace(", P</span>ierre","</span>, Pierre")
    line = line.replace('A<span class="smallcaps">','<span class="smallcaps">A')
    line = line.replace("0 0", "00")
    line = line.replace('<span class="smallcaps">, 271</span>', '')
    line = line.replace('<span class="smallcaps">, 197-198</span>', '')
    line = line.replace('<span class="smallcaps">, 412</span>', '')
    line = line.replace('Arlod (d’), Arlod(z) (d’), Arlo(z) (d’), Darlodz</span>', 'Arlod (d’)</span>, Arlod(z) (d’), Arlo(z) (d’), Darlodz')
    return line


def get_subject(triplet):
    return triplet[0]


def get_link(triplet):
    return triplet[1]


def get_goal(triplet):
    return triplet[2]


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


def unfold_substructures(structure):
    final = []
    for element in structure:
        if get_type(element) == "voir":
            for subelement in element[0][0]:
                final.append([subelement, "voir"])
        elif get_type(element) == "persons":
            for subelement in element[0]:
                final.append(subelement)
        elif get_type(element) == "place" and "(" in get_value(element):
            table_place = place([[get_value(element)]])
            if len(table_place) > 0:
                # enlever la liste vide à la fin de la liste
                table_place.pop()
                for place_element in table_place:
                    if place_element != []:
                        final.append([place_element[0], place_element[1]])
        else:
            final.append(element)
    return final


def is_valide_line(line):
    res = True
    if "blockquote>" in line or "<p>-" in line or "<p>—" in line or 'caps">—' in line:
        res = False
    return res


def html_to_triple(file_name):
    """After the html index is generated, we can access his datas"""
    text = open(file_name, "r").readlines()
    failed_lines = open("failed.html", "w")

    ignor = True
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
        elif ignor is False and not containsH5(line):
            res = parser.parse(corrector(line))
            if res is not None:
                res = unfold_substructures(res)
                tab.append(createTriplet(res))
            else:
                if is_valide_line(line):
                    failed_lines.write(line)
    failed_lines.close()
    return tab


def getType(onto, element, tab_type):
    for triplet in tab_type:
        if element == get_subject(triplet):
            if get_goal(triplet) == "Nom":
                return get_class(onto, "Nom")(get_subject(triplet).replace(" ( d ’ )", ""))
            elif get_goal(triplet) == "Localisation":
                return get_class(onto, "Localisation")(get_subject(triplet))
            elif get_goal(triplet) == "Page":
                return get_class(onto, "Page")(get_subject(triplet).replace(" ", ""))
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


def property_creator(onto, name, domain_name, range_name):
    """
    This is a exotic custom function that create
    a class from the given parameters
    it was made to create simply and dynamicaly
    new properties
    """
    Property = type(name, (ObjectProperty, ), {
       "namespace": onto,
       "domain": [get_class(onto, domain_name)],
       "range": [get_class(onto, range_name)]
        })


def define_properties(onto):
    # Creation of properties 
    property_creator(onto, "inPage", "Nom", "Localisation")
    property_creator(onto, "inCanton", "Localisation", "Canton")
    property_creator(onto, "inCommune", "Localisation", "Commune")
    property_creator(onto, "inCountry", "Localisation", "Pays")
    property_creator(onto, "inDepartement", "Localisation", "Departement")


def create_table_of_type(tab):
    # création de la table des types
    tab_type = []
    for ligne in tab:
        for triplet in ligne:
            if triplet[1] == "type":
                tab_type.append(triplet)
    return tab


def create_class_type(onto, triplet):
    """link classes to corresponding names"""
    if get_goal(triplet) == "person":
        get_class(onto, "Nom")(get_subject(triplet).replace(" ( d ’ )", ""))
    elif get_goal(triplet) == "place":
        get_class(onto, "Localisation")(get_subject(triplet))
    elif get_goal(triplet) == "page":
        get_class(onto, "Page")(get_subject(triplet).replace(" ", ""))


def get_class_from_instance(onto, instance):
    res = None
    if hasattr(onto, instance):
        if getattr(onto, instance) is not None:
            res = getattr(onto, instance)
    return res


def create_page_relation(onto, triplet):
    Any = get_class_from_instance(onto, get_subject(triplet))
    # Any = getType(onto, get_subject(triplet), tab_type)
    page = get_class(onto, "Page")(get_goal(triplet))
    if Any is not None:
        Any.inPage = [page]


def create_relation(onto, triplet):
    # relation creator
    link = get_link(triplet)
    python_class_of_the_link = getattr(onto, link)
    class1 = python_class_of_the_link.domain[0].name
    class2 = python_class_of_the_link.range[0].name
    element1 = get_class(onto, class1)(get_subject(triplet))
    element2 = get_class(onto, class2)(get_goal(triplet))
    setattr(element1, link, [element2])


def exist_in_ontology(onto, element):
    res = False
    if hasattr(onto, element):
        if getattr(onto, element) is not None:
            res = True
    return res


def create_instance_and_relation(onto, tab):
    # création des instances et des relations
    for ligne in tab:
        for triplet in ligne:
            if get_link(triplet) == "type":
                if exist_in_ontology(onto, get_goal(triplet)):
                    get_class(onto, get_goal(triplet))(get_subject(triplet).replace(" ( d ’ )", ""))
            elif get_link(triplet) == "Page":
                create_page_relation(onto, triplet)
            elif exist_in_ontology(onto, get_link(triplet)):
                create_relation(onto, triplet)


def triple_to_owl(tab):
    """
    une fonction qui va transformer le contenu html_to_triple
    en structure dans un premier temps puis crée des triplets
    """
    onto = get_ontology_from_file("ontology_v3.owl")
    define_properties(onto)
    create_instance_and_relation(onto, tab)
    onto.save(file="final.owl", format="rdfxml")

