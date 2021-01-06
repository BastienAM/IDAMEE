class EventType:
    def __init__(self ,label):
        self.label = label

class Event:
    def __init__(self, refPatient, executer, evenType, dateStart, dateEnd):
        self.refPatient = refPatient
        self.dateStart = dateStart
        self.dateEnd = dateEnd
        self.executer = executer
        self.evenType = evenType


class ALD(EventType):
    def __init__(self, label):
        super().__init__('ALD')
        self.label = label


class Hospitalisation(EventType):
    def __init__(self, label,diagnosis):
        super().__init__('Hospitalisation')
        self.label = label
        self.diagnosis = diagnosis

class Consultation(EventType):
    def __init__(self,label):
        super().__init__('Consultation')
        self.label = label


class Biology(EventType):
    def __init__(self,label):
        super().__init__('Biology')
        self.label = label

class DrugDelevery(EventType):
    def __init__(self,label,quantity):
        super().__init__('DrugDelevery')
        self.label = label
        self.quantity = quantity

class Acte(EventType):
    def __init__(self,label):
        super().__init__('Acte')
        self.label = label
            
class Executer:
    def __init__(self,name):
        self.name = name
 
class Pharmacy(Executer):
    def __init__(self, label):
        super().__init__('Pharmacy')
        self.label = label
   
class Hospital(Executer):
    def __init__(self, label):
        super().__init__('Hospital')
        self.label = label
        
class Doctor(Executer):
    def __init__(self, label, speciality):
        super().__init__('Doctor')
        self.label = label
        self.speciality = speciality

class Sequence:
    def __init__(self, refSequence, gender, dateofBirth, dateofDeath, localisation):
        self.refSequence = refSequence
        self.gender = gender
        self.dateofBirth = dateofBirth
        self.dateofDeath = dateofDeath
        self.localisation = localisation
