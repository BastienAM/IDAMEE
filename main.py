from rdflib import Graph, Literal, RDF, URIRef
# rdflib knows about some namespaces, like FOAF
from rdflib.namespace import FOAF , XSD
import pprint
# create a Graph
g = Graph()

# Create an RDF URI node to use as the subject for multiple triples
bah = URIRef("http://example.org/bah")

# Add triples using store's add() method.
g.add((bah, RDF.type, FOAF.Person))
g.add((bah, FOAF.nick, Literal("bah", lang="fr")))
g.add((bah, FOAF.name, Literal("Rahmane BAH")))
g.add((bah, FOAF.mbox, URIRef("mailto:bah@univ-rennes1.fr")))

# Add another person
fatima = URIRef("http://example.org/fatima")

# Add triples using store's add() method.
g.add((fatima, RDF.type, FOAF.Person))
g.add((fatima, FOAF.nick, Literal("rihani", datatype=XSD.string)))
g.add((fatima, FOAF.name, Literal("Fatima RIHANI")))
g.add((fatima, FOAF.mbox, URIRef("mailto:rihani@univ-rennes1.fr")))

# Iterate over triples in store and print them out.
print("--- printing raw triples ---")
for s, p, o in g:
    print((s, p, o))

# For each foaf:Person in the store, print out their mbox property's value.
print("--- printing mboxes ---")
for person in g.subjects(RDF.type, FOAF.Person):
    for mbox in g.objects(person, FOAF.mbox):
        print(mbox)

# Bind the FOAF namespace to a prefix for more readable output
g.bind("foaf", FOAF)

# print all the data in the Notation3 format
print("--- printing mboxes ---")
print(g.serialize(format='turtle').decode("utf-8"))

##reading à remote graph
remoteGraph = Graph()
remoteGraph.parse("http://bigasterisk.com/foaf.rdf")
print(len(remoteGraph))

## Saving the created graph into the file with turtle format
g.serialize(destination='output.ttl', format='turtle')

