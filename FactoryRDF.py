import model
import os

from rdflib import Graph, Literal, RDF, Namespace
from rdflib.namespace import FOAF , XSD

class FactoryRDF:

    #creating/prefix a namespace
    SNDS = Namespace("http://www.localhost.org/")
    CCAM = Namespace('http://chu-rouen.fr/cismef/CCAM#')
    ALDCODE = Namespace('http://chu-rouen.fr/cismef/ALD#')
    ATC = Namespace('http://chu-rouen.fr/cismef/ATC#')
    UNCAM = Namespace('http://chu-rouen.fr/cismef/NABM#')
    CIM10 = Namespace('http://chu-rouen.fr/cismef/CIM-10#')
    IRNAT = Namespace('http://www.localhost.org/IrNat#')
    HOSPITAL =Namespace('http://www.localhost.org/hospital#')
    DOCTOR = Namespace('http://www.localhost.org/doctor#')
    PHARMACY = Namespace('http://www.localhost.org/pharmacy#')

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

    def __init__(self):
        self.name = "FactoryRDF"
        self.indexEvent = 1
    
    def open(self, create):
        self.graph = Graph('Sleepycat')
        self.graph.open('./'+ self.name, create = create)

    def close(self):
        self.graph.close()

    def bind(self):
        self.graph.bind("foaf", FOAF)
        self.graph.bind("snds", self.SNDS)
        self.graph.bind("atc", self.ATC)
        self.graph.bind("ccam", self.CCAM)
        self.graph.bind("cim10", self.CIM10)
        self.graph.bind("ald", self.ALDCODE)
        self.graph.bind("uncam", self.UNCAM)
        self.graph.bind("irnat", self.IRNAT)
        self.graph.bind("hosp", self.HOSPITAL)
        self.graph.bind("pharm", self.PHARMACY)
        self.graph.bind("doctor", self.DOCTOR)

    def export(self):
        self.graph.serialize(destination='output.ttl', format='turtle')

    def __addEvent(self, evt, patient, event_i):
        self.graph.add((patient, self.is_composed_of, event_i))
        self.graph.add((event_i, RDF.type, self.event))
        self.graph.add((event_i, self.date_start, Literal(evt.dateStart, datatype=XSD['date'])))
        self.graph.add((event_i, self.date_end, Literal(evt.dateEnd, datatype=XSD['date'])))

    def addEventALD(self, evt):
        if not isinstance(evt.evenType,model.ALD):
            raise Exception('Wrong event type !')
        
        patient = self.SNDS[evt.refPatient]
        event_i = patient + "EVT" + str(self.indexEvent)
        self.__addEvent(evt, patient, event_i)
        
        self.graph.add((event_i, self.has_type, self.event_ald))
        self.graph.add((event_i, self.hasLabel, self.ALDCODE[evt.evenType.label]))

        self.indexEvent = self.indexEvent + 1

    def addEventDrugDelivery(self, evt):
        if not isinstance(evt.evenType,model.DrugDelevery):
            raise Exception('Wrong event type !')

        patient = self.SNDS[evt.refPatient]
        event_i = patient + "EVT" + str(self.indexEvent)
        self.__addEvent(evt, patient, event_i)
        
        self.graph.add((event_i, self.has_type, self.event_drug_delivery))
        self.graph.add((event_i, self.hasLabel, self.ATC[evt.evenType.label]))
        self.graph.add((self.ATC[evt.evenType.label], self.SNDS['quantity'], Literal(evt.evenType.quantity)))

        self.graph.add((event_i, self.executor, self.PHARMACY[evt.executer.label]))

        self.indexEvent = self.indexEvent + 1

    def addEventConsultation(self, evt):
        if not isinstance(evt.evenType,model.Consultation):
            raise Exception('Wrong event type !')

        patient = self.SNDS[evt.refPatient]
        event_i = patient + "EVT" + str(self.indexEvent)
        self.__addEvent(evt, patient, event_i)
        
        self.graph.add((event_i, self.has_type, self.event_consultation))
        self.graph.add((event_i, self.hasLabel, self.IRNAT[evt.evenType.label]))

        self.graph.add((event_i, self.executor, self.DOCTOR[evt.executer.label]))
        self.graph.add((self.DOCTOR[evt.executer.label], self.SNDS['hasSpeciality'], Literal(evt.executer.speciality, datatype=XSD['string'])))

        self.indexEvent = self.indexEvent + 1

    def addEventMedicalAct(self, evt):
        if not isinstance(evt.evenType,model.Acte):
            raise Exception('Wrong event type !')

        patient = self.SNDS[evt.refPatient]
        event_i = patient + "EVT" + str(self.indexEvent)
        self.__addEvent(evt, patient, event_i)
        
        self.graph.add((event_i, self.has_type, self.event_acte))
        self.graph.add((event_i, self.hasLabel, self.CCAM[evt.evenType.label]))

        self.graph.add((event_i, self.executor, self.DOCTOR[evt.executer.label]))
        self.graph.add((self.DOCTOR[evt.executer.label], self.SNDS['hasSpeciality'], Literal(evt.executer.speciality, datatype=XSD['string'])))

        self.indexEvent = self.indexEvent + 1

    def addEventHospitalisation(self, evt):
        if not isinstance(evt.evenType,model.Hospitalisation):
            raise Exception('Wrong event type !')

        patient = self.SNDS[evt.refPatient]
        event_i = patient + "EVT" + str(self.indexEvent)
        self.__addEvent(evt, patient, event_i)
        
        self.graph.add((event_i, self.has_type, self.event_hospitalisation))
        self.graph.add((event_i, self.hasLabel, self.CCAM[evt.evenType.label]))
        self.graph.add((self.CIM10[evt.evenType.label], self.SNDS['diagnosis'], Literal(evt.evenType.diagnosis)))

        self.graph.add((event_i, self.executor, self.HOSPITAL[evt.executer.label]))

        self.indexEvent = self.indexEvent + 1

    def addEventBiology(self, evt):
        if not isinstance(evt.evenType,model.Biology):
            raise Exception('Wrong event type !')

        patient = self.SNDS[evt.refPatient]
        event_i = patient + "EVT" + str(self.indexEvent)
        self.__addEvent(evt, patient, event_i)
        
        self.graph.add((event_i, self.has_type, self.event_biology))
        self.graph.add((event_i, self.hasLabel, self.UNCAM[evt.evenType.label]))

        self.graph.add((event_i, self.executor, self.DOCTOR[evt.executer.label]))
        self.graph.add((self.DOCTOR[evt.executer.label], self.SNDS['hasSpeciality'], Literal(evt.executer.speciality, datatype=XSD['string'])))

        self.indexEvent = self.indexEvent + 1


    def addSequence(self, sequence):
        patient = self.SNDS[sequence.refSequence]
        self.graph.add((patient, RDF.type, patient))
        self.graph.add((patient, self.gender, Literal(sequence.gender)))
        self.graph.add((patient, self.location_code, Literal(sequence.localisation, datatype = XSD['string'])))
        self.graph.add((patient, self.date_of_birth, Literal(sequence.dateofBirth, datatype = XSD['date'])))
        self.graph.add((patient, self.date_of_death, Literal(sequence.dateofDeath, datatype = XSD['date'])))

    def deleteTempFiles(self):
        for f in os.listdir(self.name):
            os.unlink(self.name + "/" + f)
        os.rmdir(self.name)