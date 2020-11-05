from rdflib import Graph, Literal, RDF, URIRef, OWL, Namespace
# rdflib knows about some namespaces, like FOAF
from rdflib.namespace import FOAF , XSD
import pprint
# create a graphraph
graph = Graph()
#creating/prefix a namespace
SNDS = Namespace("http://www.semanticweb.orgraph/user/ontolographies/2020/9/my_ontology#")
CCAM = Namespace('http://www.CCAM.fr/CCAM#')
ALDCODE =Namespace('http://www.ALDCODE.fr/ALDCode#')
ATC = Namespace('http://www.atc.fr/ATC#')
UNCAM = Namespace('http://www.UNCAM.fr/UNCAM#')
CIM10 = Namespace('http://www.CIM10.fr/CIM10#')
IRNAT = Namespace('http://www.IRNAT.fr/IrNat#')
HOSPITAL = Namespace('http://www.hospital.fr/hospital#')
DOCTOR = Namespace('http://www.doctor.fr/doctor#')
PHARMACY = Namespace('http://www.pharmacy.fr/pharmacy#')

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



# Definition of the data properties for patient1
patient1 = SNDS['Patient1']
patient2 = SNDS['Patient2']
# Definition of event
Event0 = SNDS['Patient0Evt1']
Event1 = SNDS['Patient0Evt2']
Event2 = SNDS['Patient1Evt3']
Event3 = SNDS['Patient1Evt4']
Event4 = SNDS['Patient1Evt5']
Event5 = SNDS['Patient1Evt6']


# Add triples usingraph store's add() method for sequence patient1
graph.add((patient1, RDF.type, patient))
graph.add((patient1, gender, Literal(1)))
graph.add((patient1, location_code, Literal('35700', datatype = XSD['string'])))
graph.add((patient1, date_of_birth, Literal('1943-02-28', datatype = XSD['date'])))
graph.add((patient1, date_of_death, Literal('2090-02-28', datatype = XSD['date'])))

graph.add((patient1, is_composed_of, Event0))
graph.add((Event0, RDF.type, event))
graph.add((Event0, hasLabel, ATC['N02BE0']))
graph.add((Event0, date_start, Literal('2020-02-28', datatype = XSD['date'])))
graph.add((Event0, date_end, Literal('2020-07-28', datatype = XSD['date'])))
graph.add((Event0, executor, HOSPITAL['22100450']))
graph.add((Event0, has_type, event_drug_delivery))
#graph.add((event_drug_delivery, hasLabel,ATC['N02BE0']))
#graph.add((event_drug_delivery, SNDS['quantity'],Literal(20)))

graph.add((patient1, is_composed_of, Event1))
graph.add((Event1, RDF.type, event))
graph.add((Event1, hasLabel, CCAM['YYYY600']))
graph.add((Event1, date_start, Literal('2020-01-28', datatype = XSD['date'])))
graph.add((Event1, date_end, Literal('2020-05-28', datatype = XSD['date'])))
graph.add((Event1, has_type, event_hospitalisation))
graph.add((Event1, executor, HOSPITAL['22100450']))

#hospital attributes
#Hospitalisation attribute
#graph.add((event_hospitalisation, SNDS['diagnosis'], CIM10['IH1152000']))
#graph.add((event_hospitalisation, hasLabel, CCAM['YYYY600']))


# Add triples usingraph store's add() method for patient2
graph.add((patient2, RDF.type, patient))
graph.add((patient2, gender, Literal(2)))
graph.add((patient2, location_code, Literal('35700', datatype = XSD['string'])))
graph.add((patient2, date_of_birth, Literal('1943-02-28', datatype = XSD['date'])))
graph.add((patient2, date_of_death, Literal('2090-02-28', datatype = XSD['date'])))

graph.add((patient2, is_composed_of, Event2))
graph.add((Event2, hasLabel, UNCAM['UNCAM00600']))
graph.add((Event2, date_start, Literal('2010-01-28', datatype = XSD['date'])))
graph.add((Event2, date_end, Literal('2010-05-28', datatype = XSD['date'])))
graph.add((Event2, has_type, event_consultation))
graph.add((Event2, executor, DOCTOR['501100450']))
graph.add((DOCTOR['501100450'],SNDS['hasSpeciality'], Literal('Ophtalmologie', datatype = XSD['string'])))

graph.add((patient2, is_composed_of, Event3))
graph.add((Event3, hasLabel, ALDCODE['ALD0152600']))
graph.add((Event3, date_start, Literal('2020-01-28', datatype = XSD['date'])))
graph.add((Event3, date_end, Literal('2020-05-28', datatype = XSD['date'])))
graph.add((Event3, has_type, event_ald))
graph.add((Event3, executor, DOCTOR['22100450']))
graph.add((DOCTOR['22100450'],SNDS['hasSpeciality'], Literal('Cancerologie', datatype = XSD['string'])))

graph.add((patient2, is_composed_of, Event4))
graph.add((Event4, hasLabel, IRNAT['IRNAT52600']))
graph.add((Event4, date_start, Literal('2020-11-28', datatype = XSD['date'])))
graph.add((Event4, date_end, Literal('2020-12-28', datatype = XSD['date'])))
graph.add((Event4, has_type, event_hospitalisation))
graph.add((Event4, executor, HOSPITAL['501100450']))

graph.add((patient2, is_composed_of, Event5))
graph.add((Event5, hasLabel, CIM10['CIM102600']))
graph.add((Event5, date_start, Literal('2018-01-28', datatype = XSD['date'])))
graph.add((Event5, date_end, Literal('2019-05-28', datatype = XSD['date'])))
graph.add((Event5, has_type, event_acte))
graph.add((Event5, executor, DOCTOR['22100450']))
graph.add((DOCTOR['22100450'],SNDS['hasSpeciality'], Literal('Cancerologie', datatype = XSD['string'])))

# Bind all namespaces to a prefix for more readable output
graph.bind("foaf", FOAF)
graph.bind("snds", SNDS)
graph.bind("atc", ATC)
graph.bind("ccam",CCAM)
graph.bind("cim10", CIM10)
graph.bind("ald",ALDCODE)
graph.bind("uncam",UNCAM)
graph.bind("irnat",IRNAT)
graph.bind("hosp", HOSPITAL)
graph.bind("pharm", PHARMACY)
graph.bind("doctor", DOCTOR)

# print all the data in the xml format
print("--- print all the data in the xml format ---")
print(graph.serialize(format='ttl').decode("utf-8"))


## Saving the created graph into the file with turtle format
graph.serialize(destination='output.ttl', format='xml')

