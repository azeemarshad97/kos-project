from owlready2 import *

path = "/home/fabrice/sessions/projet/knowledge/labs/pipeline/owl/example.owl"

onto = get_ontology("file://"+path).load()

# print(list(onto.classes()))
# print(list(onto.classes())[0])
# print(list(onto.classes())[0].instances())

# existing instance in example.AestheticsValue: 
#[example.ok, example.pretty, example.pretty_ugly, example.ugly]

# SPARQL Query
print(list(default_world.sparql("""
           SELECT ?x
           { ?x a owl:Class . }
    """)))
