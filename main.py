from datetime import date


class EventType:
    def __init__(self ,label):
        self.label = label


class Event:
    def __init__(self, executer, evenType):
        self.dateStart = date(1999, 1, 1)
        self.dateEnd = date(2100, 1, 1)
        self.executer = executer
        self.evenType = evenType


class ALD(EventType):
    def __init__(self,label):
        super().__init__()
        self.label = label


class Hospitalisation(EventType):
    def __init__(self,acteLabel,diagnosis):
        super().__init__()
        self.acteLabel = acteLabel
        self.diagnosis = diagnosis


class Sequence:
    def __init__(self, dateofBirth,dateofDeath,gender,localisation):
        self.dateofBirth = dateofBirth
        slef.dateofDeath=dateofDeath
        self.gender=gender
        slef.localisation=localisation


class Consultation(EventType):
    def __init__(self,label):
        super().__init__()
        self.label = label


class Biology(EventType):
    def __init__(self,label):
        super().__init__()
        self.label = label

class DrugDelevery(EventType):
    def __init__(self,label,quantity):
        super().__init__()
        self.label = label
        self.quantity = quantity
        
class Acte(EventType):
    def __init__(self,label):
        super().__init__()
        self.label = label
            
class Executer:
    def __init__(self,name):
        super().__init__()
        self.name = name
 
 class Pharmacy(Executer):
    def __init__(self):
        super().__init__()
   
class Hospital(Executer):
    def __init__(self):
        super().__init__()
        
        
class Docotor(Executer):
    def __init__(self):
        super().__init__()
