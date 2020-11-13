import sqlite3
import ClassModel

connection = sqlite3.connect("snds_2235.db")

#Récupération de la liste de tout les bénéficiaires (Sequence)
cursor = connection.cursor()
cursor.execute("select ben_nir_psa,ben_nai_moi,BEN_SEX_COD,BEN_RES_DPT from IR_BEN_R;")
results = cursor.fetchall()
se = []
for r in results:
    se.append(ClassModel.Sequence(r[0],r[1],'null',r[2],r[3]))


#Récupération des évènements pour chaque patient (Event)
for s in se:
    cursor.execute("select EXE_SOI_DTD,EXE_SOI_DTF,PFS_EXE_NUM from ER_PRS_F f join IR_BEN_R r on f.ben_nir_psa=r.ben_nir_psa where f.ben_nir_psa = "+s.refSequence)
    results = cursor.fetchall()
    for r in results:
        s.events.append(ClassModel.Event(r[0],r[1],r[2],'eventType'))


cursor.close()
connection.close()
