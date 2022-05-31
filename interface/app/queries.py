from owlready2 import *
from app.network import displayNetwork

# path = "ontology_v2.owl"
path = "app/data/ontology_and_index.owl"

onto = get_ontology("file://"+path).load()

query1 = """
           SELECT ?x ?y ?z WHERE
           { 
               ?x a ontology_and_index:_Localisation.
               ?x ?y ?z.
           } LIMIT 10
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


def getResults(query):
    triplets = formatResults(list(default_world.sparql(query)))
    return displayNetwork(triplets)



# SPARQL Query
# triplets = formatResults(list(default_world.sparql(query)))
# # print(len(list(default_world.sparql(query))[1]))
# # print(list(default_world.sparql(query))[1][2].name)

# displayNetwork(triplets)
