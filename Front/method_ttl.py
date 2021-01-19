import warnings
import numpy as np
import os, sys, getopt, glob
import scipy.sparse.csgraph
from rdflib import Graph,URIRef, ConjunctiveGraph
from rdflib.namespace import RDF
from SPARQLWrapper import SPARQLWrapper, JSON, XML
import time
from reco import *
import datetime


intro_prefix="""prefix atc: <http://chu-rouen.fr/cismef/ATC#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix ccam: <http://chu-rouen.fr/cismef/CCAM#> 
prefix cim10: <http://chu-rouen.fr/cismef/CIM-10> 
prefix doctor: <http://www.localhost.fr/doctor#> 
prefix hospital: <http://www.localhost.org/hospital#> 
prefix irnat: <http://www.localhost.org/IrNat#> 
prefix pharmacy: <http://www.localhost.fr/pharmacy#> 
prefix snds: <http://www.localhost.org/> 
prefix xsd: <http://www.w3.org/2001/XMLSchema#>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n\n """ 

def FindPatientsEvents(graph, c): #tous les patients + tous les evts
    evt_list=[] #enlever doublons
    """Construction Query"""
    query=''
    intro=intro_prefix+"SELECT DISTINCT ?patient "

    #Query building
    num=0
    for item, neg in c.items.values() :
        if (item not in evt_list) and (neg == 0):
            evt_list.append(item)
            intro += "?date"+str(num)+" "
            query += "\n?event"+str(num)+" a snds:Event .\n"
            query += "?event"+str(num)+" a snds:DrugDelivery.\n"
            query += "?patient snds:isComposedOf ?event"+str(num)+".\n"
            query += "?event"+str(num)+" snds:hasLabel/rdfs:subClassOf* "+"atc:"+item+".\n"
            query += "?event"+str(num)+" snds:hasDateStart ?date"+str(num)+".\n"
            
            num += 1
    query=intro + "\nWHERE { \n ?patient a snds:Sequence .\n" + query + "\n}"
    #print(query)

    #Extract patient and for each patient date from each occurence of event 
    #no double
    all_patients = {}
    graph.setQuery(query)
    graph.setReturnFormat(JSON)
    results = graph.query().convert()
    for result in results["results"]["bindings"]:
        patient = result["patient"]["value"].split('/')[-1]
        for num in range(0,len(evt_list)):
            str_to_datetime = datetime.datetime.strptime(result["date"+str(num)]["value"], '%Y-%m-%d')
            date = str_to_datetime.date()
            event = evt_list[num]
            if patient not in all_patients :
                all_patients[patient] = {}
            all_patients[patient].setdefault(event,[]).append(date)
    return all_patients


def MethodTtl(graph,chronicle):
    """Find all patients containing at least one of each events in the chronicle and then extract occurence of each event(only same events from the chronicle) from each patients.
    Extraction with values"""
    # ### Results files ###
    # file_reco="reco4.csv"
    # with open(file_reco,"w") as csv:
    #     csv.write("m p c t r ") # method, patient, chronicle, time, reco (VF)

    ##########################################
    ### Find Patients and events ###
    ##########################################
    #s=time.time()
    patients_events={}
    patients_events=FindPatientsEvents(graph, chronicle)

    ##########################################
    ### Recognition of the chronicle ###
    ##########################################
    occs = []
    patients_and_chronicle_occurrences = {}
    for patient in patients_events:
        events_to_analyse = patients_events[patient]
        occs = chronicle.recognize(events_to_analyse)
        if occs:
            patients_and_chronicle_occurrences[patient] = occs

    return patients_and_chronicle_occurrences