from owlready2 import *
from app.network import displayNetwork

# path = "ontology_v2.owl"
path = "app/data/final.owl"

onto = get_ontology("file://"+path).load()

prefix = "PREFIX kos: <http://www.semanticweb.org/user/ontologies/2022/3/untitled-ontology-33#>"

# LINK CODE
"""
is : 6
"""
# Fonction de formatage d'element
def formatElement(element):
    """
    If the element is 6, return "a", otherwise return the element's name
    
    :param element: The element to format
    :return: The name of the element
    """
    if element == 6:
        return "a"
    else:
        return element.name

# Fonction de conversion
def formatResults(table):
    """
    It takes a table as input and returns a new table where each element is formatted
    
    :param table: the table to format
    :return: A list of lists.
    """
    nouvelle_table = []
    for ligne in table:
        nouvelle_ligne = []
        for element in ligne:
            nouvelle_ligne.append(formatElement(element))
        nouvelle_table.append(nouvelle_ligne)
    return nouvelle_table


def getResults(query):
    """
    It takes a query, runs it against the default_world, formats the results, and returns a network
    
    :param query: SELECT ?s ?p ?o WHERE { ?s ?p ?o }
    :return: A list of triplets
    """
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
