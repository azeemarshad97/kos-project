from owlready2 import *

path = "owl/ontology_v2.owl"
path = "final.owl"

onto = get_ontology("file://"+path).load()

# SPARQL Query
result = list(default_world.sparql("""
           PREFIX kos: <http://www.semanticweb.org/user/ontologies/2022/3/untitled-ontology-33#>
           SELECT ?x ?y where 
            { ?x kos:inDepartement ?y }
    """))
            # { ?x a kos:_Localisation. }
            # { ?x a owl:Class. }
            # { ?x ?y ?z}
            # { ?x a kos:Nom. }

for line in result:
    print(line)
