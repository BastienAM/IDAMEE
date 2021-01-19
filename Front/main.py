import os, sys, getopt, glob
import scipy.sparse.csgraph
import subprocess
import time
import json
from rdflib import Graph, URIRef, ConjunctiveGraph
from rdflib.namespace import RDF
from SPARQLWrapper import SPARQLWrapper, JSON
from reco import *
from method_ttl import MethodTtl

if __name__ == "__main__":
            # Param fuseki-server, open sh and change JVM_ARGS=${JVM_ARGS:--Xmx1200M} to JVM_ARGS=${JVM_ARGS:--Xmx2048M}
            port = SPARQLWrapper("http://localhost:3030/data")
            port.setQuery("ASK{}")
            port.setReturnFormat(JSON)
            res = port.query().convert()

            #Json file given by the visu
            with open(os.getcwd()+'/c0.json') as json_file:
                cfile = json.load(json_file)
                c = as_ChronicleNegfromVisu(cfile)
                #print("CHRONICLE: ", c)

            #the algo of recognition
            s = time.time()
            patients_and_chronicle_occurrences = MethodTtl(port,c)
            e = time.time()

            #patients_and_chronicle_occurrences output fo the algo : list of patients verifying the chronicle (in the dropdown menu) + their corressponding chronicle occurrences (to print in the visu)
            for patient in patients_and_chronicle_occurrences :
                print("PATIENT TROUVE",patient ,":\n\tOCCURRENCES: ",patients_and_chronicle_occurrences[patient])
                print("\ttemps passé: ",e-s)
            print("\ttemps passé: ",e-s)