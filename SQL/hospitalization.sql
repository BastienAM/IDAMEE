SELECT
    T_MCOaaC.NIR_ANO_17,
	T_MCOaaC.EXE_SOI_DTD,
	T_MCOaaC.EXE_SOI_DTF,

	T_MCOaaB.DGN_PAL,

    T_MCOaaA.CDC_ACT,

	T_MCOaaE.ETA_NUM
	
FROM T_MCOaaC

--Description sejours
INNER JOIN T_MCOaaB ON
	T_MCOaaC.ETA_NUM = T_MCOaaB.ETA_NUM AND
	T_MCOaaC.RSA_NUM = T_MCOaaB.RSA_NUM

--ACTE CCAM TABLE PAS DISPONIBLE
LEFT JOIN T_MCOaaA ON
	T_MCOaaB.ETA_NUM = T_MCOaaA.ETA_NUM AND
	T_MCOaaB.RSA_NUM = T_MCOaaA.RSA_NUM	

--Etablissement
LEFT JOIN T_MCOaaE ON
	T_MCOaaB.ETA_NUM = T_MCOaaE.ETA_NUM

LIMIT 100