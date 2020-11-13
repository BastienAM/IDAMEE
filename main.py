from rdflib import Graph, ConjunctiveGraph, Literal, RDF, URIRef, OWL, Namespace

# rdflib knows about some namespaces, like FOAF
from rdflib.namespace import FOAF , XSD
import pprint, model

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
## lOADING THE DATA IN THE STRUCTURE
events1 = []
events1.append(model.Event(model.Doctor('DO12050','SP0102'),model.Consultation('CONS100254'),'2020-02-15','2020-05-12'))
events1.append(model.Event(model.Doctor('DO12050','SP0102'),model.Acte('AC150254'),'2020-02-15','2020-05-12'))
events1.append(model.Event(model.Pharmacy('PH14250'),model.DrugDelevery('DD50254',10),'2020-02-15','2020-05-12'))
events1.append(model.Event(model.Hospital('HO12050'),model.Hospitalisation('AC150254','DIAG15200'),'2020-02-15','2020-05-12'))
sequence1 = model.Sequence('PAT125012','1943-01-12','2090-01-12',2,'35700',events1)
events2 = []
events2.append(model.Event(model.Doctor('DO12015','SP0111'),model.ALD('CONS100254'),'2020-02-15','2020-05-12'))
events2.append(model.Event(model.Hospital('HOS12015'),model.Biology('BIO150254'),'2021-02-15','2020-05-12'))
events2.append(model.Event(model.Doctor('DO12015','SP0111'),model.Consultation('CONS254'),'2020-02-15','2020-05-12'))
events2.append(model.Event(model.Hospital('HOS12015'),model.Acte('AC15515'),'2021-12-12','2021-05-12'))
sequence2 = model.Sequence('PAT125000','1950-01-02','2090-01-15',1,'9200',events2)
sdns_array = []
sdns_array.append(sequence1)
sdns_array.append(sequence2)
############################################################################################################################

## CREATING THE RDF FILE
graph1 = Graph()
for seq in sdns_array:
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


# print all the data in the xml format
print("--- print all the data in the xml format ---")
print(graph1.serialize(format='ttl').decode("utf-8"))


## Saving the created graph into the file with turtle format
graph1.serialize(destination='output3.ttl', format='turtle')