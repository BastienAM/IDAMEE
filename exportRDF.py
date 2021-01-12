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
    factory.addSequence(model.Event(str(row[0]), model.Pharmacy(str(row[5])), model.DrugDelevery(str(row[3]), row[4]), row[1], row[2]))

cursor.close()
#endregion

# On ferme la connexion à la base de donnée
conn.close()

# Export du fichier
factory.export()

# Fermeture connexion
factory.close()
# Suppression des fichiers temporaires
factory.deleteTempFiles()