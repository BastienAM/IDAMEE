from datetime import date


class EventType:
    def __init__(self):
        self.label = ""


class Event:
    def __init__(self, executer, evenType):
        self.dateStart = date(1999, 1, 1)
        self.dateEnd = date(2100, 1, 1)
        self.executer = executer
        self.type = evenType


class ALD(EventType):
    def __init__(self):
        super().__init__()
        self.label = " "


class Hospitalisation(EventType):
    def __init__(self):
        super().__init__()
        self.acteLabel = ""
        self.diagnosis = ""


class Sequence:
    def __init__(self, event):
        self.composedOf = event


class Consultation(EventType):
    def __init__(self):
        super().__init__()
        self.label = ""


class Biology(EventType):
    def __init__(self):
        super().__init__()
        self.label = " "


class DrugDelevery(EventType):
    def __init__(self):
        super().__init__()
        self.label = ""
        self.quatity = 1

