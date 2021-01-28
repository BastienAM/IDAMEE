import time
from SPARQLWrapper import SPARQLWrapper, JSON
from reco import *
from method_ttl import MethodTtl
def chronicle_recognition():
  port = SPARQLWrapper("http://localhost:3030/data")
  port.setQuery("ASK{}")
  port.setReturnFormat(JSON)


  res = port.query().convert()

  # Json file given by the visu
  with open(os.getcwd() + '/c0.json') as json_file:
      cfile = json.load(json_file)
      c = as_ChronicleNegfromVisu(cfile)

  # the algo of recognition
  patients_and_chronicle_occurrences = MethodTtl(port, c)

  return patients_and_chronicle_occurrences,c