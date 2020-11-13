from rdflib import Graph, ConjunctiveGraph, Literal, RDF, URIRef, OWL, Namespace,Store

# rdflib knows about some namespaces, like FOAF
from rdflib.namespace import FOAF , XSD
import pprint

store = plugin.get("IOMemory", Store)()
g = ConjunctiveGraph()
print(g)
g2 = Graph('IOMemory', URIRef("http://rdflib.net"))
print(g2)
print(g2.identifier)