from owlready2 import *

# path = "ontology_v2.owl"
path = "ontology_and_index.owl"

onto = get_ontology("file://"+path).load()

query = """
           SELECT ?y WHERE
           { 
               ?x a ontology_and_index:_Localisation.
               ?x ?y ?z.
           }
    """

# LINK CODE
"""
is : 6
"""

# SPARQL Query
print(list(default_world.sparql(query)))
# print(len(list(default_world.sparql(query))[1]))
# print(list(default_world.sparql(query))[1][2].name)

