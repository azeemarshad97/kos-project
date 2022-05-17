from owlready2 import *

path = "ontology_v2.owl"

onto = get_ontology("file://"+path).load()

query = """
           SELECT ?x
           { ?x a owl:Class . }
    """

# SPARQL Query
print(list(default_world.sparql(query)))
