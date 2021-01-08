import sqlite3
import model

from rdflib import Graph, ConjunctiveGraph, Literal, RDF, URIRef, OWL, Namespace

# rdflib knows about some namespaces, like FOAF
from rdflib.namespace import FOAF , XSD
import pprint, model


conn = sqlite3.connect("../database/snds_2235.db")

qry = open('./SQL/query_hospital.sql', 'r').read()
#print(qry)

cursor = conn.cursor()
cursor.execute(qry)

snds_array = []

currentPatient = None
row = cursor.fetchone()
while row != None:
    #print(row)

    event = model.Event(model.Hospital(row[10]), model.Hospitalisation(None, row[6]), row[4], row[5])

    if currentPatient != None and currentPatient.refSequence == row[0]:
            currentPatient.events.append(event)
    else:
        if currentPatient != None:
            snds_array.append(currentPatient)
        currentPatient = model.Sequence(row[0], row[2], None, row[1], row[3], [event])


    row = cursor.fetchone()
cursor.close()

if currentPatient != None:
    snds_array.append(currentPatient)

# On ferme la connection à la base de donnée
conn.close()
#print(snds_array)


print("Création Fichier RDF")

#creating/prefix a namespace
SNDS = Namespace("http://www.localhost.org/")
CCAM = Namespace('http://www.CCAM.fr/CCAM#')
ALDCODE = Namespace('http://www.ALDCODE.fr/ALDCode#')
ATC = Namespace('http://www.atc.fr/ATC#')
UNCAM = Namespace('http://www.UNCAM.fr/UNCAM#')
CIM10 = Namespace('http://www.CIM10.fr/CIM10#')
IRNAT = Namespace('http://www.IRNAT.fr/IrNat#')
HOSPITAL =Namespace('http://www.localhost.org/hospital#')
DOCTOR = Namespace('http://www.localhost.fr/doctor#')
PHARMACY = Namespace('http://www.localhost.fr/pharmacy#')

## Definition of the object properties for Patient
patient = SNDS['Sequence']
is_composed_of = SNDS['isComposedOf']
date_of_birth = SNDS['hasDateOfBirth']
date_of_death = SNDS['hasDateOfDeath']
gender = SNDS['hasGender']
location_code = SNDS['hasLocationCode']
hasLabel = SNDS['hasLabel']

## Definition of the object properties for Event
event = SNDS['Event']
has_type = SNDS['hasType']
date_start = SNDS['hasDateStart']
date_end = SNDS['hasDateEnd']
executor = SNDS['hasExecutor']

#class of type of event
event_ald = SNDS['ALD']
event_drug_delivery = SNDS['DrugDelivery']
event_biology = SNDS['Biology']
event_hospitalisation = SNDS['Hospitalization']
event_acte = SNDS['Acte']
event_consultation= SNDS['Consultation']

## CREATING THE RDF FILE
graph1 = Graph()
for seq in snds_array:
    patient = SNDS[seq.refSequence]
    graph1.add((patient, RDF.type, patient))
    graph1.add((patient, gender, Literal(seq.gender)))
    graph1.add((patient, location_code, Literal(seq.localisation, datatype = XSD['string'])))
    graph1.add((patient, date_of_birth, Literal(seq.dateofBirth, datatype = XSD['date'])))
    graph1.add((patient, date_of_death, Literal(seq.dateofDeath, datatype = XSD['date'])))
    i = 0
    for evt in seq.events:
        i = i + 1
        event_i = patient + "evt" + str(i)
        graph1.add((patient, is_composed_of, event_i))
        graph1.add((event_i, RDF.type, event))
        graph1.add((event_i, date_start, Literal(evt.dateStart, datatype = XSD['date'])))
        graph1.add((event_i, date_end, Literal(evt.dateEnd, datatype = XSD['date'])))
        if(isinstance(evt.evenType,model.ALD)):
            graph1.add((event_i, has_type, event_drug_delivery))
            graph1.add((event_i, hasLabel, ALDCODE[evt.evenType.label]))
        elif(isinstance(evt.evenType,model.DrugDelevery)):
            graph1.add((event_i, has_type, event_drug_delivery))
            graph1.add((event_i, hasLabel, ATC[evt.evenType.label]))
            graph1.add((ATC[evt.evenType.label], SNDS['quantity'],Literal(evt.evenType.quantity)))
        elif(isinstance(evt.evenType,model.Acte)):
            graph1.add((event_i, has_type, event_acte))
            graph1.add((event_i, hasLabel, CCAM[evt.evenType.label]))
        elif(isinstance(evt.evenType,model.Biology)):
            graph1.add((event_i, has_type, event_biology))
            graph1.add((event_i, hasLabel, UNCAM[evt.evenType.label]))
        elif(isinstance(evt.evenType,model.Consultation)):
            graph1.add((event_i, has_type, event_consultation))
            graph1.add((event_i, hasLabel, IRNAT[evt.evenType.label]))
        elif(isinstance(evt.evenType,model.Hospitalisation)):
            graph1.add((event_i, has_type, event_hospitalisation))
            graph1.add((event_i, hasLabel, CIM10[evt.evenType.label]))
            graph1.add((CIM10[evt.evenType.label], SNDS['diagnosis'],Literal(evt.evenType.diagnosis)))

        if isinstance(evt.executer,model.Hospital):
            graph1.add((event_i, executor, HOSPITAL[evt.executer.label]))
        elif isinstance(evt.executer,model.Doctor):
            graph1.add((event_i, executor, DOCTOR[evt.executer.label]))
            graph1.add((DOCTOR[evt.executer.label], SNDS['hasSpeciality'], Literal(evt.executer.speciality, datatype = XSD['string'])))
        elif isinstance(evt.executer,model.Pharmacy):
            graph1.add((event_i, executor,PHARMACY[evt.executer.label]))

############################################################################################################################################
## fix the prefix on the head of the file
graph1.bind("foaf", FOAF)
graph1.bind("snds", SNDS)
graph1.bind("atc", ATC)
graph1.bind("ccam",CCAM)
graph1.bind("cim10", CIM10)
graph1.bind("ald",ALDCODE)
graph1.bind("uncam",UNCAM)
graph1.bind("irnat",IRNAT)
graph1.bind("hosp", HOSPITAL)
graph1.bind("pharm", PHARMACY)
graph1.bind("doctor", DOCTOR)


## Saving the created graph into the file with turtle format
graph1.serialize(destination='output.ttl', format='turtle')