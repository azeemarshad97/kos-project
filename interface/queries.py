from owlready2 import *

# path = "ontology_v2.owl"
path = "ontology_and_index.owl"

onto = get_ontology("file://"+path).load()

query = """
           SELECT ?x
           { ?x a ontology_and_index:_Localisation . }
    """

# SPARQL Query
print(list(default_world.sparql(query)))
# { ?x a ontology_and_index:_Localisation . }
