from rdflib import Graph, Literal, RDF, URIRef, OWL, Namespace
# rdflib knows about some namespaces, like FOAF
from rdflib.namespace import FOAF , XSD
import pprint
# create a Graph
g = Graph()
#creating a namespace
SNDS = Namespace("http://www.semanticweb.org/user/ontologies/2020/9/my_ontology#")
isa = Namespace("http://www.isa.fr")
## subclass definition for label of event
ccam = Namespace('http://www.CCAM.fr/CCAM#')
ald_code =Namespace('http://www.ALDCODE.fr/ALDCode#')
atc = Namespace('http://www.atc.fr/')
uncam = Namespace('http://www.UNCAM.fr/UNCAM#')
cim10 = Namespace('http://www.CIM10.fr/CIM10#')
irnat = Namespace('http://www.IRNAT.fr/IrNat#')


## Definition of the object properties for Patient
patient = SNDS['Sequence']
is_composed_of = SNDS['isComposedOf']
date_of_birth = SNDS['hasDateOfBirth']
date_of_death = SNDS['hasDateOfDeath']
gender = SNDS['hasGender']
location_code = SNDS['hasLocationCode']


## Definition of the object properties for Event
event = SNDS['Event']
has_type = SNDS['hasType']
date_start = SNDS['hasDateStart']
date_end = SNDS['hasDateEnd']
executor = SNDS['hasExecutor']
event_label = SNDS['hasLabel']

#class of type of event
event_type_ald = SNDS['ALD']
event_type_drug_delivery = SNDS['DrugDelivery']
event_type_biology = SNDS['Biology']
event_type_hospitalisation = SNDS['Hospitalization']
event_type_acte = SNDS['Acte']
event_type_consultation= SNDS['Consultation']

## subclass definition for type of executor
pharmacy = SNDS['Pharmacy']
hospital = SNDS['Hospital']
doctor = SNDS['Doctor']
doctor_speciality = SNDS['hasSpeciality']


Event2 = SNDS['Patient1Evt3']
Event3 = SNDS['Patient1Evt4']
# Definition of the data properties for patient1
patient1 = SNDS['Patient1']
birth_date1 = Literal('1943-02-28', datatype = XSD['date'])
death_date1 = Literal('2090-02-28', datatype = XSD['date'])
gender1 = Literal('1', datatype = XSD['integer'])
location_code1 =Literal('35700', datatype = XSD['string'])

# Definition of data properties for event 1
Event0 = SNDS['Patient0Evt1']
start_date1 = Literal('2020-02-28', datatype = XSD['date'])
end_date1 = Literal('2020-07-28', datatype = XSD['date'])

# Definition of data properties for event 2
Event1 = SNDS['Patient0Evt2']


# Add triples using store's add() method for sequence patient1
g.add((patient1, RDF.type, patient))
g.add((patient1, gender, gender1))
g.add((patient1, location_code, location_code1))
g.add((patient1, date_of_birth, birth_date1))
g.add((patient1, date_of_death, death_date1))
g.add((patient1, is_composed_of, Event0))
g.add((patient1, is_composed_of, Event1))

g.add((Event0, RDF.type, event))
g.add((Event0, date_start, start_date1))
g.add((Event0, date_end, end_date1))
g.add((Event0, executor, pharmacy))
atclabel = atc['N02BE0']
g.add((Event0, event_label, atclabel))


# Add triples using store's add() method for Event0


# Definition of the data properties for patient2
patient2 = SNDS['Patient2']
birth_date2 =Literal('1943-02-28', datatype =XSD['date'])
death_date2 = Literal('2090-02-28', datatype = XSD['date'])
gender2 = Literal('2', datatype = XSD['integer'])
location_code2 =Literal('35700', datatype = XSD['string'])

# Add triples using store's add() method for patient2
g.add((patient2, RDF.type, patient))
g.add((patient2, gender, gender2))
g.add((patient2, location_code, location_code2))
g.add((patient2, date_of_birth, birth_date2))
g.add((patient2, date_of_death, death_date2))
g.add((patient2, is_composed_of, Event2))
g.add((patient2, is_composed_of, Event1))
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
g.bind("snds", SNDS)

# print all the data in the Notation3 format
print("--- printing mboxes ---")
print(g.serialize(format='xml').decode("utf-8"))


## Saving the created graph into the file with turtle format
g.serialize(destination='output.ttl', format='turtle')

