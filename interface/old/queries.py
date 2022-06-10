from owlready2 import *
from network import displayNetwork
import pandas as pd

path = "ontology_v2.owl"
# path = "ontology_and_index.owl"

onto = get_ontology("file://"+path).load()

query = """
           SELECT ?x ?y ?z WHERE
           {
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
    elif isinstance(element, int):
        return str(element)
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


def find_select_position(query):
    position = query.find("SELECT")
    if position == -1:
        position = query.find("select")
    return position+7


def find_where_position(query):
    position = query.find("WHERE")
    if position == -1:
        position = query.find("where")
    return position-1


def extractVariable(query):
    # trouve la position du select
    select_position = find_select_position(query)
    # trouve la position du where
    where_position = find_where_position(query)
    return query[select_position:where_position]


# récupérer les colonnes depuis la requête
def getColumns(query):
    # extrait les variables
    variables = extractVariable(query)
    # converti les variables en colonnes
    colonnes = variables.split(" ")
    return colonnes


def query_with_result_in_DataFrame():
    values = formatResults(list(default_world.sparql(query)))
    columns = getColumns(query)
    return pd.DataFrame(values, columns=columns)

query_with_result_in_DataFrame()
