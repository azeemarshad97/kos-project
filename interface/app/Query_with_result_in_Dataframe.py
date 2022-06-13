from owlready2 import *
from app.network import displayNetwork
import pandas as pd

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


def getResults(query):
    values = formatResults(list(default_world.sparql(prefix+query)))
    columns = getColumns(query)
    return pd.DataFrame(values, columns=columns).to_html(index=False)

