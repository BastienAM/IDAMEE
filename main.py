from rdflib import Graph, Literal, RDF, URIRef, OWL, Namespace
import sqlite3
# rdflib knows about some namespaces, like FOAF
from rdflib.namespace import FOAF , XSD
import pprint, model

###################################### creating/prefix a namespace ####################################################
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

############################# Definition of the object properties for Patient #########################################
patient = SNDS['Sequence']
is_composed_of = SNDS['isComposedOf']
date_of_birth = SNDS['hasDateOfBirth']
date_of_death = SNDS['hasDateOfDeath']
gender = SNDS['hasGender']
location_code = SNDS['hasLocationCode']
hasLabel = SNDS['hasLabel']

################################### Definition of the object properties for Event ######################################
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

####################################### DATA EXTRACTION ################################################################

conn = sqlite3.connect("../snds_2235.db")

###################################### SEQUENCE/PATIENTS ##############################################################
cursor = conn.cursor()
cursor.execute("select BEN_NIR_PSA, BEN_SEX_COD, BEN_NAI_MOI, BEN_DCD_DTE, BEN_RES_COM, BEN_RES_DPT from IR_BEN_R;")
results1 = cursor.fetchall()
sequence_list = []
for r in results1:
    sequence_list.append(model.Sequence(str(r[0]),r[1],r[2],r[3],r[4]))
###################################### DRUG DELIVERY ###################################################################

drug_delivery_list = []
cursor = conn.cursor()
cursor.execute('''SELECT BEN_NIR_PSA, ER_PRS_F.DCT_ORD_NUM, PHA_PRS_C13, PHA_ACT_QSN, EXE_SOI_DTD, EXE_SOI_DTF, PFS_EXE_NUM, PRS_MTT_NUM,PSP_ACT_NAT, PRS_NAT_REF FROM ER_PHA_F JOIN ER_PRS_F ON (
            ER_PRS_F.DCT_ORD_NUM	=	ER_PHA_F.DCT_ORD_NUM AND
            ER_PRS_F.FLX_DIS_DTD	=	ER_PHA_F.FLX_DIS_DTD AND
            ER_PRS_F.FLX_EMT_NUM	=	ER_PHA_F.FLX_EMT_NUM AND
            ER_PRS_F.FLX_EMT_ORD	=	ER_PHA_F.FLX_EMT_ORD AND
            ER_PRS_F.FLX_EMT_TYP	=	ER_PHA_F.FLX_EMT_TYP AND
            ER_PRS_F.FLX_TRT_DTD	=	ER_PHA_F.FLX_TRT_DTD AND
            ER_PRS_F.ORG_CLE_NUM	=	ER_PHA_F.ORG_CLE_NUM AND
            ER_PRS_F.PRS_ORD_NUM	=	ER_PHA_F.PRS_ORD_NUM AND
            ER_PRS_F.REM_TYP_AFF	=	ER_PHA_F.REM_TYP_AFF);''')
results2 = cursor.fetchall()
for r in results2:
    drug_delivery_list.append(model.Event(str(r[0]), model.Pharmacy(str(r[2])), model.DrugDelevery(str(r[1]), r[3]), r[4], r[5]))
print("Ok")
############################################### CONSULTATION ###########################################################
consultation_list = []
cursor = conn.cursor()
cursor.execute('''SELECT DISTINCT ER_PRS_F.PRS_ORD_NUM, BEN_NIR_PSA, EXE_SOI_DTD, PFS_EXE_NUM,PFS_PFS_NUM, PFS_PRA_SPE, PFS_COD_POS from DA_PRA_R JOIN ER_PRS_F WHERE 
                  PFS_PFS_NUM in (SELECT DISTINCT PFS_EXE_NUM from ER_PRS_F WHERE PRS_NAT_REF=1111) 
                  AND DA_PRA_R.PFS_PFS_NUM = ER_PRS_F.PFS_EXE_NUM
                  AND PFS_PRA_SPE != 50;''')
results3 = cursor.fetchall()
for r in results3:
    consultation_list.append(model.Event(r[1], model.Doctor(str(r[3]),r[5]),model.Consultation(str(r[0])),r[2],r[2]))
print("Ok")
############################################### ACTE MEDICAL ###########################################################
acte_medical_list = []
cursor = conn.cursor()
cursor.execute('''SELECT BEN_NIR_PSA, PFS_PFS_NUM,PFS_PRA_SPE, PFS_COD_POS,CAM_PRS_IDE, CAM_ACT_COD, EXE_SOI_DTD, EXE_SOI_DTF, PFS_EXE_NUM, PRS_MTT_NUM,PSP_ACT_NAT, PRS_NAT_REF
                    FROM ER_CAM_F , ER_PRS_F, DA_PRA_R
				    WHERE  ER_CAM_F.DCT_ORD_NUM = ER_PRS_F.DCT_ORD_NUM AND
				    ER_PRS_F.PFS_EXE_NUM = DA_PRA_R.PFS_PFS_NUM;''')
results4 = cursor.fetchall()
for r in results4:
    acte_medical_list.append(model.Event(str(r[0]),model.Hospital(str(r[1])),model.Acte(str(r[4])),r[6],r[7]))
print("Ok")

########################################## HOSPITALISATION #############################################################
hospitalisation_list = []
cursor = conn.cursor()
cursor.execute('''SELECT T_MCOaaB.ETA_NUM, T_MCOaaB.RSA_NUM, NIR_ANO_17, DGN_PAL, DGN_REL, ENT_DAT, SOR_DAT  FROM T_MCOaaB JOIN T_MCOaaC 
                    ON (T_MCOaaB.ETA_NUM=T_MCOaaC.ETA_NUM and T_MCOaaB.RSA_NUM=T_MCOaaC.RSA_NUM);''')
results5 = cursor.fetchall()
for r in results5:
    hospitalisation_list.append(model.Event(str(r[2]), model.Hospital(str(r[1])), model.Hospitalisation(r[0], r[3]), r[5], r[6]))
print("Ok")

conn.close()
################################################ END OF DATA EXTRACTION ################################################

########################################### CREATING THE RDF FILE ######################################################
graph1 = Graph(store='Sleepycat')
graph1.open('./TmpGraph', create = True)
#################################################### SEQUENCE ##########################################################
for seq in sequence_list:
    patient = SNDS[seq.refSequence]
    graph1.add((patient, RDF.type, patient))
    graph1.add((patient, gender, Literal(seq.gender)))
    graph1.add((patient, location_code, Literal(seq.localisation, datatype=XSD['string'])))
    graph1.add((patient, date_of_birth, Literal(seq.dateofBirth, datatype=XSD['date'])))
    graph1.add((patient, date_of_death, Literal(seq.dateofDeath, datatype=XSD['date'])))
i = 0
############################################## DRUG DELIVERY############################################################
for evt in drug_delivery_list:
    patient = SNDS[evt.refPatient]
    i = i + 1
    event_i = patient + "EVT" + str(i)
    graph1.add((patient, is_composed_of, event_i))
    graph1.add((event_i, RDF.type, event))
    graph1.add((event_i, date_start, Literal(evt.dateStart, datatype = XSD['date'])))
    graph1.add((event_i, date_end, Literal(evt.dateEnd, datatype = XSD['date'])))

    graph1.add((event_i, has_type, event_drug_delivery))
    graph1.add((event_i, hasLabel, ATC[evt.evenType.label]))
    graph1.add((ATC[evt.evenType.label], SNDS['quantity'], Literal(evt.evenType.quantity)))

    graph1.add((event_i, executor, PHARMACY[evt.executer.label]))
##################################################### CONSULTATION #####################################################
for evt in consultation_list:
    patient = SNDS[evt.refPatient]
    i = i + 1
    event_i = patient + "EVT" + str(i)
    graph1.add((patient, is_composed_of, event_i))
    graph1.add((event_i, RDF.type, event))
    graph1.add((event_i, date_start, Literal(evt.dateStart, datatype=XSD['date'])))
    graph1.add((event_i, date_end, Literal(evt.dateEnd, datatype=XSD['date'])))

    graph1.add((event_i, has_type, event_consultation))
    graph1.add((event_i, hasLabel, IRNAT[evt.evenType.label]))

    graph1.add((event_i, executor, DOCTOR[evt.executer.label]))
    graph1.add((DOCTOR[evt.executer.label], SNDS['hasSpeciality'],
                    Literal(evt.executer.speciality, datatype=XSD['string'])))
##################################################### ACTE MEDICAL #####################################################
for evt in acte_medical_list:
    patient = SNDS[evt.refPatient]
    i = i + 1
    event_i = patient + "EVT" + str(i)
    graph1.add((patient, is_composed_of, event_i))
    graph1.add((event_i, RDF.type, event))
    graph1.add((event_i, date_start, Literal(evt.dateStart, datatype=XSD['date'])))
    graph1.add((event_i, date_end, Literal(evt.dateEnd, datatype=XSD['date'])))

    graph1.add((event_i, has_type, event_acte))
    graph1.add((event_i, hasLabel, CCAM[evt.evenType.label]))

    graph1.add((event_i, executor, HOSPITAL[evt.executer.label]))

############################################### HOSPITALISATION ########################################################
for evt in hospitalisation_list:
    patient = SNDS[evt.refPatient]
    i = i + 1
    event_i = patient + "EVT" + str(i)
    graph1.add((patient, is_composed_of, event_i))
    graph1.add((event_i, RDF.type, event))
    graph1.add((event_i, date_start, Literal(evt.dateStart, datatype=XSD['date'])))
    graph1.add((event_i, date_end, Literal(evt.dateEnd, datatype=XSD['date'])))

    graph1.add((event_i, has_type, event_hospitalisation))
    graph1.add((event_i, hasLabel, CIM10[evt.evenType.label]))
    graph1.add((CIM10[evt.evenType.label], SNDS['diagnosis'], Literal(evt.evenType.diagnosis)))

    graph1.add((event_i, executor, HOSPITAL[evt.executer.label]))
################################## fix the prefix on the head of the file #############################################
graph1.bind("foaf", FOAF)
graph1.bind("snds", SNDS)
graph1.bind("atc", ATC)
graph1.bind("ccam",CCAM)
graph1.bind("cim10", CIM10)
graph1.bind("ald",ALDCODE)
graph1.bind("uncam",UNCAM)
graph1.bind("irnat",IRNAT)
graph1.bind("hospital", HOSPITAL)
graph1.bind("pharmacy", PHARMACY)
graph1.bind("doctor", DOCTOR)

###################################### Saving the created graph into the file with turtle format #######################
graph1.close()
graph1.open('./TmpGraph')
graph1.serialize(destination='output.ttl', format='turtle')