import os, sys, getopt, glob
import scipy.sparse.csgraph
import subprocess
import time
import json
from rdflib import Graph, URIRef, ConjunctiveGraph
from rdflib.namespace import RDF
from SPARQLWrapper import SPARQLWrapper, JSON
from reco import *
from method_ttl import MethodTtl
from flask import Flask, request, render_template, jsonify
from urllib.error import HTTPError
from flask import send_from_directory

app = Flask(__name__)

ENDPOINT_URL = "http://localhost:3030/data"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search',  methods=['post'])
def search():
    if request.method == 'POST' :
        search='[]'
        try:
           search = json.loads(request.form['search'])
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print('Decoding JSON has failed')
       
        port = SPARQLWrapper(ENDPOINT_URL)
        port.setQuery("ASK{}")
        port.setReturnFormat(JSON)
        res = port.query().convert()
        c = as_ChronicleNegfromVisu(search)
       
        #the algo of recognition
        s = time.time()
        patients_and_chronicle_occurrences = MethodTtl(port,c)
        e = time.time()

       #patients_and_chronicle_occurrences output fo the algo : list of patients verifying the chronicle (in the dropdown menu) + their corressponding chronicle occurrences (to print in the visu)
       # for patient in patients_and_chronicle_occurrences :
        #   print("PATIENT",patient ,": LISTE OCCURRENCES: ",patients_and_chronicle_occurrences[patient])
        #print("\ttemps passé: ",e-s)
        listResults = []
        try:
            for result in patients_and_chronicle_occurrences:
                listResults.append(result)
        except:
            print("Erreur déclenchée")
    return render_template('index.html', items = listResults, chronicle = request.form['search'] )

if __name__ == '__main__':
    app.run(debug=True)