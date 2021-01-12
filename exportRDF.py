import sqlite3
import model
import pprint
import FactoryRDF


conn = sqlite3.connect("../database/snds_2235.db")

# Création de la fabrique
factory = FactoryRDF.FactoryRDF()
factory.open(True)


#region Sequence
query = open('./SQL/sequence.sql', 'r').read()
cursor = conn.cursor()
cursor.execute(query)

records = cursor.fetchall()

for row in records:
    factory.addSequence(model.Sequence(row[0], row[2], None, row[1], row[3]))

cursor.close()
#endregion

#region Drug Delivery
query = open('./SQL/drug_delivery.sql', 'r').read()
cursor = conn.cursor()
cursor.execute(query)

records = cursor.fetchall()

for row in records:
    factory.addEventDrugDelivery(model.Event(str(row[0]), model.Pharmacy(str(row[5])), model.DrugDelevery(str(row[3]), row[4]), row[1], row[2]))

cursor.close()
#endregion

#region Medical Act
query = open('./SQL/medical_act.sql', 'r').read()
cursor = conn.cursor()
cursor.execute(query)

records = cursor.fetchall()

for row in records:
    factory.addEventMedicalAct(model.Event(str(row[0]), model.Doctor(str(row[4]), str(row[5])), model.Acte(row[3]), row[1], row[2]))

cursor.close()
#endregion

#region Hospitalization
#query = open('./SQL/hospitalization.sql', 'r').read()
#cursor = conn.cursor()
#cursor.execute(query)

#records = cursor.fetchall()

#for row in records:
#    factory.addEventHospitalisation(model.Event(str(row[0]), model.Hospital(str(row[5])), model.Hospitalisation(row[4], row[3]), row[1], row[2]))
#
#cursor.close()
#endregion

# On ferme la connexion à la base de donnée
conn.close()

# Ajout des namespaces
factory.bind()

# Export du fichier
factory.export()

# Fermeture connexion
factory.close()
# Suppression des fichiers temporaires
factory.deleteTempFiles()