from owlready2 import *
from app.network import displayNetwork
import pandas as pd

path = "app/data/final.owl"
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
    """
    If the element is 6, return "a", if it's an integer, return the string version of the integer,
    otherwise return the element's name
    
    :param element: The element to be formatted
    :return: The name of the element.
    """
    if element == 6:
        return "a"
    elif isinstance(element, int):
        return str(element)
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


def find_select_position(query):
    """
    It finds the position of the word "SELECT" in the query and returns the position of the first
    character after the word "SELECT"
    
    :param query: The query you want to run
    :return: The position of the word "SELECT" in the query.
    """
    position = query.find("SELECT")
    if position == -1:
        position = query.find("select")
    return position+7


def find_where_position(query):
    """
    It finds the position of the select and where keywords in the query, and returns the substring
    between them.
    
    :param query: the query string
    :return: The variable that is being returned is the variable that is being selected.
    """
    position = query.find("WHERE")
    if position == -1:
        position = query.find("where")
    return position-1


def extractVariable(query):
    """
    It finds the position of the select and where keywords in the query, and returns the substring
    between them
    
    :param query: the query string
    :return: The variable that is being returned is the variable that is being selected.
    """
    # trouve la position du select
    select_position = find_select_position(query)
    # trouve la position du where
    where_position = find_where_position(query)
    return query[select_position:where_position]


# récupérer les colonnes depuis la requête
def getColumns(query):
    """
    It takes a query as input and returns a list of columns
    
    :param query: the query that you want to extract the columns from
    :return: The columns of the table
    """
    # extrait les variables
    variables = extractVariable(query)
    # converti les variables en colonnes
    colonnes = variables.split(" ")
    return colonnes


def getResults(query):
    """
    It takes a SPARQL query, runs it against the default world, formats the results, and returns a
    Pandas dataframe
    
    :param query: the query to be executed
    :return: A dataframe with the results of the query.
    """
    values = formatResults(list(default_world.sparql(prefix+query)))
    columns = getColumns(query)
    return pd.DataFrame(values, columns=columns).to_html(index=False)

