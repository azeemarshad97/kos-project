import sys
import subprocess
from modules.module import *
from owlready2 import *

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

for ligne in tab:
    for triplet in ligne:
        if triplet[1] == "type":
            if triplet[2] == "person":
                ClasseNom(triplet[0].replace(" ( d ’ )",""))
            elif triplet[2] == "place":
                Classe_Localisation(triplet[0])
            elif triplet[2] == "page":
                Classe_Page(triplet[0].replace(" ", ""))

print(Classe_Page.instances())

onto.save(file = "final.owl", format = "rdfxml")

