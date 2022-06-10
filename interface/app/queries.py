from owlready2 import *
from app.network import displayNetwork

# path = "ontology_v2.owl"
path = "app/data/full_localisation.owl"

onto = get_ontology("file://"+path).load()

prefix = "PREFIX kos: <http://www.semanticweb.org/user/ontologies/2022/3/untitled-ontology-33#>"

query1 = """
        PREFIX kos: <http://www.semanticweb.org/user/ontologies/2022/3/untitled-ontology-33#>
           SELECT ?x ?y ?z WHERE
           { 
               ?x a kos:_Localisation.
               ?x ?y ?z.
           } LIMIT 10
    """
query2= """
           SELECT ?x ?y ?z where 
            { ?x kos:inDepartement ?y. 
            ?x ?y ?z. }
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
    print(f'query: {query}')

    L = list(default_world.sparql(prefix+query))
    print(f'L: {L}')
    triplets = formatResults(L)
    print(f'triplets: {triplets}')
    final_triplets = []
    for triplet in triplets:
        if triplet[2] != "NamedIndividual":
            final_triplets.append(triplet) 
    print(f'final_triplets: {final_triplets}')
    return displayNetwork(final_triplets)
