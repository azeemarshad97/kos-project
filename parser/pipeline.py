import sys
import subprocess
from modules.module import *
from owlready2 import *

# # prend le nom du fichier
# if len(sys.argv) == 1:
    # name = "Index_1543.docx"
# else:
    # name = sys.argv[1]
# newname = name[:-4]+"html"
# 
# # conversion en html
# subprocess.run(["pandoc", name, "-o", newname])
# 
# # conversion en triplets
# text = open(newname, "r").readlines()

text = open("Index_1543.html", "r").readlines()

# text = ["<p><strong>abattoir</strong>, eschorcherie, 417, 420 ; voir aussi boucherie</p>"]

# text = ["<p><span class='smallcaps'>Alardet, Allardet</span>, (†), mons<sup>r</sup>, 598, 604</p>"]

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
            if res != None:
                tab.append(createTriplet(res))


# On va mettre les triplets dans l'ontologie
path="owl/ontology_v2.owl"

onto = get_ontology("file://"+path).load()

classes = list(onto.classes())
ClasseNom = classes[24]
Classe_Localisation = classes[29]
Classe_Page = classes[30]

# définition des propriétés
with onto:
    class inPage(ObjectProperty):
        domain = [ClasseNom]
        range = [Classe_Page]

def getType(element, tab_type):
    for triplet in tab_type:
        if element == triplet[0]:
            if triplet[2] == "person":
                return ClasseNom(triplet[0].replace(" ( d ’ )",""))
            elif triplet[2] == "place":
                return Classe_Localisation(triplet[0])
            elif triplet[2] == "page":
                return Classe_Page(triplet[0].replace(" ", ""))
    return None

tab_type = [] 
for ligne in tab:
    for triplet in ligne:
        if triplet[1] == "type":
            tab_type.append(triplet)

for ligne in tab:
    for triplet in ligne:
        if triplet[1] == "type":
            if triplet[2] == "person":
                ClasseNom(triplet[0].replace(" ( d ’ )",""))
            elif triplet[2] == "place":
                Classe_Localisation(triplet[0])
            elif triplet[2] == "page":
                Classe_Page(triplet[0].replace(" ", ""))
        elif triplet[1] == "page":
            Any = getType(triplet[0], tab_type)
            page = Classe_Page(triplet[2])
            if Any != None:
                Any.inPage = [page]

print(Classe_Page.instances())
 
onto.save(file = "final.owl", format = "rdfxml")

