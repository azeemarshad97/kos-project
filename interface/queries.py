from owlready2 import *

# path = "ontology_v2.owl"
path = "ontology_and_index.owl"

onto = get_ontology("file://"+path).load()

query = """
           SELECT ?x ?y ?z WHERE
           { 
               ?x a ontology_and_index:_Localisation.
               ?x ?y ?z.
           }
    """

# LINK CODE
"""
is : 6
"""

# Fonction de formatage d'element
def formatElement(element):
    if element == 6:
        return "a"
    else:
        return element.name

# Fonction de conversion
def formatResults(table):
    nouvelle_table = []
    for ligne in table:
        nouvelle_ligne = []
        for element in ligne:
            nouvelle_ligne.append(formatElement(element))
        nouvelle_table.append(nouvelle_ligne)
    return nouvelle_table

# SPARQL Query
print(formatResults(list(default_world.sparql(query))))
# print(len(list(default_world.sparql(query))[1]))
# print(list(default_world.sparql(query))[1][2].name)

